"""
LangGraph Workflow Nodes

Implements the cognitive orchestration nodes:
- Planner: Autonomous task decomposition
- Executor: Agent execution
- Critic: Result evaluation
- Replanner: Dynamic re-planning
"""

from typing import Dict, Any, List
import json

from agents import AgentRouter
from shared.schemas import AgentInput, AgentOutput
from .workflow import WorkflowState, WorkflowConfig, WorkflowStatus


class PlannerNode:
    """
    Planning node that decomposes objectives into executable steps.
    
    Uses LLM to analyze the objective and available agents,
    then creates a step-by-step execution plan.
    """
    
    def __init__(self, router: AgentRouter, config: WorkflowConfig):
        self.router = router
        self.config = config
    
    async def execute(self, state: WorkflowState) -> WorkflowState:
        """
        Generate execution plan.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with plan
        """
        try:
            # Get available agents
            available_agents = list(self.router.registry.agents.keys())
            
            # Create plan (in production, use LLM for intelligent planning)
            plan = self._generate_plan(
                objective=state["objective"],
                available_agents=available_agents,
                request_data=state["request_data"]
            )
            
            state["plan"] = plan
            state["status"] = WorkflowStatus.EXECUTING.value
            state["current_step"] = 0
            
            return state
            
        except Exception as e:
            state["error"] = f"Planning failed: {str(e)}"
            state["status"] = WorkflowStatus.FAILED.value
            return state
    
    def _generate_plan(
        self,
        objective: str,
        available_agents: List[str],
        request_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate execution plan.
        
        In production, this would use an LLM to intelligently plan.
        For now, we provide a template-based planner.
        
        Args:
            objective: User's objective
            available_agents: List of available agent names
            request_data: Request data
            
        Returns:
            List of execution steps
        """
        # TODO: Replace with LLM-based planning
        # For now, create a simple plan based on available agents
        
        plan = []
        
        # Example: If we have enrichment agents, use them first
        enrichment_agents = [a for a in available_agents if "enrichment" in a.lower()]
        for agent_name in enrichment_agents[:2]:  # Use first 2 enrichment agents
            plan.append({
                "step": len(plan) + 1,
                "agent": agent_name,
                "description": f"Run {agent_name} for data enrichment",
                "dependencies": [],
                "expected_output": "enriched_data"
            })
        
        # Add analysis agents
        analysis_agents = [a for a in available_agents if "analysis" in a.lower() or "detection" in a.lower()]
        for agent_name in analysis_agents[:1]:
            plan.append({
                "step": len(plan) + 1,
                "agent": agent_name,
                "description": f"Run {agent_name} for analysis",
                "dependencies": [i+1 for i in range(len(plan))],  # Depends on previous steps
                "expected_output": "analysis_result"
            })
        
        # If no specific agents found, use first available
        if not plan and available_agents:
            plan.append({
                "step": 1,
                "agent": available_agents[0],
                "description": f"Execute {available_agents[0]}",
                "dependencies": [],
                "expected_output": "result"
            })
        
        return plan[:self.config.max_plan_steps]


class ExecutorNode:
    """
    Execution node that runs planned agent steps.
    
    Executes one or more steps from the plan, collecting results
    and handling dependencies.
    """
    
    def __init__(self, router: AgentRouter, config: WorkflowConfig):
        self.router = router
        self.config = config
    
    async def execute(self, state: WorkflowState) -> WorkflowState:
        """
        Execute current plan step.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with execution results
        """
        try:
            plan = state["plan"]
            current_step = state["current_step"]
            
            if current_step >= len(plan):
                # All steps completed
                state["status"] = WorkflowStatus.CRITIQUING.value
                return state
            
            # Get current step
            step = plan[current_step]
            agent_name = step["agent"]
            
            # Create agent input
            agent_input = AgentInput(
                request_id=state["request_id"],
                request_data=state["request_data"],
                metadata={
                    "step": current_step + 1,
                    "plan_step": step,
                    "previous_results": state["execution_results"]
                }
            )
            
            # Execute agent
            result = await self.router.route(agent_name, agent_input)
            
            # Store result
            state["execution_results"].append({
                "step": current_step + 1,
                "agent": agent_name,
                "result": result.result if hasattr(result, 'result') else result,
                "confidence": result.confidence_score if hasattr(result, 'confidence_score') else None
            })
            
            state["agent_outputs"].append(result)
            state["current_step"] += 1
            
            # Check if more steps remain
            if state["current_step"] >= len(plan):
                state["status"] = WorkflowStatus.CRITIQUING.value
            
            return state
            
        except Exception as e:
            state["error"] = f"Execution failed at step {state['current_step'] + 1}: {str(e)}"
            state["status"] = WorkflowStatus.FAILED.value
            return state


class CriticNode:
    """
    Critique node that evaluates execution results.
    
    Analyzes the results against the objective and decides if:
    - Results are satisfactory (end workflow)
    - Need more execution steps (continue)
    - Need re-planning (trigger replanner)
    """
    
    def __init__(self, config: WorkflowConfig):
        self.config = config
    
    async def execute(self, state: WorkflowState) -> WorkflowState:
        """
        Critique execution results.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with critique
        """
        try:
            # Analyze results
            critique = self._analyze_results(
                objective=state["objective"],
                results=state["execution_results"],
                plan=state["plan"]
            )
            
            state["critique"] = critique
            state["status"] = WorkflowStatus.CRITIQUING.value
            state["iterations"] += 1
            
            # Determine if we should replan
            state["should_replan"] = critique["should_replan"]
            
            # If critique is good, mark as completed
            if critique["confidence"] >= self.config.critique_threshold:
                state["status"] = WorkflowStatus.COMPLETED.value
                state["final_result"] = self._extract_final_result(state)
            elif state["should_replan"] and self.config.enable_replanning:
                state["status"] = WorkflowStatus.REPLANNING.value
            
            return state
            
        except Exception as e:
            state["error"] = f"Critique failed: {str(e)}"
            state["status"] = WorkflowStatus.FAILED.value
            return state
    
    def _analyze_results(
        self,
        objective: str,
        results: List[Dict[str, Any]],
        plan: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze if results meet the objective.
        
        In production, use LLM to intelligently critique.
        
        Args:
            objective: Original objective
            results: Execution results
            plan: Execution plan
            
        Returns:
            Critique with confidence and recommendations
        """
        # TODO: Replace with LLM-based critique
        
        # Simple heuristic critique
        all_steps_completed = len(results) >= len(plan)
        all_successful = all(
            r.get("result") is not None 
            for r in results
        )
        
        confidence = 0.0
        if all_steps_completed and all_successful:
            # Calculate confidence based on agent confidences
            agent_confidences = [
                r.get("confidence", 0.5) 
                for r in results 
                if r.get("confidence") is not None
            ]
            confidence = sum(agent_confidences) / len(agent_confidences) if agent_confidences else 0.5
        
        should_replan = (
            not all_successful or 
            (confidence < self.config.critique_threshold and len(results) < self.config.max_plan_steps)
        )
        
        return {
            "confidence": confidence,
            "all_steps_completed": all_steps_completed,
            "all_successful": all_successful,
            "should_replan": should_replan,
            "feedback": self._generate_feedback(results, all_successful),
            "recommendations": self._generate_recommendations(results, plan)
        }
    
    def _generate_feedback(
        self,
        results: List[Dict[str, Any]],
        all_successful: bool
    ) -> str:
        """Generate feedback on execution."""
        if not results:
            return "No results generated. Plan execution may have failed."
        
        if all_successful:
            return f"Successfully executed {len(results)} steps."
        
        failed_steps = [r["step"] for r in results if r.get("result") is None]
        return f"Execution partially successful. Steps {failed_steps} failed."
    
    def _generate_recommendations(
        self,
        results: List[Dict[str, Any]],
        plan: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate recommendations for improvement."""
        recommendations = []
        
        if len(results) < len(plan):
            recommendations.append(f"Complete remaining {len(plan) - len(results)} steps")
        
        for result in results:
            if result.get("confidence", 1.0) < 0.5:
                recommendations.append(f"Re-execute step {result['step']} with different approach")
        
        return recommendations
    
    def _extract_final_result(self, state: WorkflowState) -> Any:
        """Extract final result from execution results."""
        if not state["execution_results"]:
            return None
        
        # Return last result as final output
        return state["execution_results"][-1]["result"]


class ReplannerNode:
    """
    Re-planning node that adjusts the plan based on critique.
    
    Takes feedback from the critic and generates an improved plan,
    potentially adding new steps or modifying existing ones.
    """
    
    def __init__(self, router: AgentRouter, config: WorkflowConfig):
        self.router = router
        self.config = config
    
    async def execute(self, state: WorkflowState) -> WorkflowState:
        """
        Re-plan based on critique.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with new plan
        """
        try:
            critique = state.get("critique", {})
            current_plan = state["plan"]
            executed_steps = state["current_step"]
            
            # Generate new plan
            new_plan = self._generate_revised_plan(
                objective=state["objective"],
                current_plan=current_plan,
                executed_steps=executed_steps,
                critique=critique,
                available_agents=list(self.router.registry.agents.keys())
            )
            
            state["plan"] = new_plan
            state["current_step"] = 0  # Reset to start of new plan
            state["execution_results"] = []  # Clear previous results
            state["status"] = WorkflowStatus.EXECUTING.value
            
            return state
            
        except Exception as e:
            state["error"] = f"Re-planning failed: {str(e)}"
            state["status"] = WorkflowStatus.FAILED.value
            return state
    
    def _generate_revised_plan(
        self,
        objective: str,
        current_plan: List[Dict[str, Any]],
        executed_steps: int,
        critique: Dict[str, Any],
        available_agents: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Generate revised plan based on critique.
        
        In production, use LLM to intelligently replan.
        
        Args:
            objective: Original objective
            current_plan: Current plan
            executed_steps: Number of steps executed
            critique: Critique feedback
            available_agents: Available agents
            
        Returns:
            Revised execution plan
        """
        # TODO: Replace with LLM-based replanning
        
        # Simple heuristic: add more agents if confidence is low
        new_plan = []
        
        # Keep successful executed steps
        for i, step in enumerate(current_plan[:executed_steps]):
            if i < len(critique.get("feedback", [])):
                new_plan.append(step)
        
        # Add new steps from unused agents
        used_agents = {step["agent"] for step in new_plan}
        unused_agents = [a for a in available_agents if a not in used_agents]
        
        for agent_name in unused_agents[:2]:  # Add up to 2 new agents
            new_plan.append({
                "step": len(new_plan) + 1,
                "agent": agent_name,
                "description": f"Try {agent_name} for alternative approach",
                "dependencies": [i+1 for i in range(len(new_plan))],
                "expected_output": "improved_result"
            })
        
        return new_plan[:self.config.max_plan_steps]

