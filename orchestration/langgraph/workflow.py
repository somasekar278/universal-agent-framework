"""
LangGraph Workflow Orchestration

Provides StateGraph-based workflows that orchestrate SOTA Agent Framework agents
with planning, execution, critique, and re-planning capabilities.
"""

from typing import Dict, Any, List, Optional, TypedDict, Annotated
from dataclasses import dataclass
from enum import Enum

try:
    from langgraph.graph import StateGraph, END
    from langgraph.prebuilt import ToolExecutor
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    StateGraph = None
    END = None

from agents import Agent, AgentRouter


class WorkflowStatus(str, Enum):
    """Workflow execution status."""
    PLANNING = "planning"
    EXECUTING = "executing"
    CRITIQUING = "critiquing"
    REPLANNING = "replanning"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkflowState(TypedDict):
    """
    State for the agent workflow graph.
    
    This state is passed through the LangGraph workflow and updated
    by each node (planner, executor, critic, etc.).
    """
    # Input
    request_id: str
    request_data: Dict[str, Any]
    objective: str
    
    # Planning
    plan: Optional[List[Dict[str, Any]]]  # List of planned steps
    current_step: int
    
    # Execution
    execution_results: List[Dict[str, Any]]
    agent_outputs: List[Any]
    
    # Critique
    critique: Optional[Dict[str, Any]]
    should_replan: bool
    iterations: int
    max_iterations: int
    
    # Status
    status: str
    error: Optional[str]
    final_result: Optional[Any]


@dataclass
class WorkflowConfig:
    """Configuration for agent workflows."""
    max_iterations: int = 3
    max_plan_steps: int = 10
    critique_threshold: float = 0.7  # Confidence threshold for accepting results
    enable_replanning: bool = True
    enable_self_correction: bool = True
    planning_model: str = "gpt-4"
    critique_model: str = "gpt-4"


class AgentWorkflowGraph:
    """
    LangGraph-powered workflow orchestrator for SOTA agents.
    
    Provides cognitive orchestration with:
    - Autonomous planning and task decomposition
    - Dynamic agent selection and execution
    - Result critique and quality assessment
    - Self-correcting re-planning loops
    
    Example:
        ```python
        from orchestration.langgraph import AgentWorkflowGraph
        from agents import AgentRouter
        
        # Create workflow
        router = AgentRouter.from_yaml("config/agents.yaml")
        workflow = AgentWorkflowGraph(router)
        
        # Execute with planning
        result = await workflow.execute({
            "request_id": "req-001",
            "objective": "Analyze transaction for fraud",
            "request_data": {...}
        })
        ```
    """
    
    def __init__(
        self,
        agent_router: AgentRouter,
        config: Optional[WorkflowConfig] = None
    ):
        """
        Initialize workflow graph.
        
        Args:
            agent_router: Router containing available agents
            config: Workflow configuration
        """
        if not LANGGRAPH_AVAILABLE:
            raise ImportError(
                "LangGraph not installed. Install with: "
                "pip install sota-agent-framework[agent-frameworks]"
            )
        
        self.router = agent_router
        self.config = config or WorkflowConfig()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph StateGraph.
        
        Creates a graph with planning, execution, critique, and re-planning nodes.
        """
        from .nodes import PlannerNode, ExecutorNode, CriticNode, ReplannerNode
        
        # Create workflow graph
        workflow = StateGraph(WorkflowState)
        
        # Initialize nodes
        planner = PlannerNode(self.router, self.config)
        executor = ExecutorNode(self.router, self.config)
        critic = CriticNode(self.config)
        replanner = ReplannerNode(self.router, self.config)
        
        # Add nodes to graph
        workflow.add_node("planner", planner.execute)
        workflow.add_node("executor", executor.execute)
        workflow.add_node("critic", critic.execute)
        workflow.add_node("replanner", replanner.execute)
        
        # Define entry point
        workflow.set_entry_point("planner")
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "planner",
            self._should_execute,
            {
                "execute": "executor",
                "end": END
            }
        )
        
        workflow.add_edge("executor", "critic")
        
        workflow.add_conditional_edges(
            "critic",
            self._should_replan,
            {
                "replan": "replanner",
                "continue": "executor",
                "end": END
            }
        )
        
        workflow.add_edge("replanner", "executor")
        
        return workflow.compile()
    
    def _should_execute(self, state: WorkflowState) -> str:
        """
        Decide if we should execute the plan.
        
        Args:
            state: Current workflow state
            
        Returns:
            "execute" if plan is valid, "end" if planning failed
        """
        if state.get("error"):
            return "end"
        
        if not state.get("plan") or len(state["plan"]) == 0:
            return "end"
        
        return "execute"
    
    def _should_replan(self, state: WorkflowState) -> str:
        """
        Decide if we should re-plan based on critique.
        
        Args:
            state: Current workflow state
            
        Returns:
            "replan" if should replan, "continue" if should continue execution,
            "end" if done
        """
        # Check if max iterations reached
        if state["iterations"] >= state["max_iterations"]:
            return "end"
        
        # Check if all steps completed
        if state["current_step"] >= len(state.get("plan", [])):
            # All steps done, check quality
            critique = state.get("critique", {})
            confidence = critique.get("confidence", 0.0)
            
            if confidence >= self.config.critique_threshold:
                return "end"  # Good enough!
            
            if state.get("should_replan") and self.config.enable_replanning:
                return "replan"
            
            return "end"
        
        # More steps to execute
        return "continue"
    
    async def execute(
        self,
        input_data: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute the workflow with autonomous planning.
        
        Args:
            input_data: Input data with request_id, objective, request_data
            config: Optional runtime configuration overrides
            
        Returns:
            Workflow execution result with plan, results, and final output
        """
        # Initialize state
        initial_state: WorkflowState = {
            "request_id": input_data["request_id"],
            "request_data": input_data.get("request_data", {}),
            "objective": input_data["objective"],
            "plan": None,
            "current_step": 0,
            "execution_results": [],
            "agent_outputs": [],
            "critique": None,
            "should_replan": False,
            "iterations": 0,
            "max_iterations": self.config.max_iterations,
            "status": WorkflowStatus.PLANNING.value,
            "error": None,
            "final_result": None
        }
        
        # Execute graph
        try:
            final_state = await self.graph.ainvoke(initial_state, config=config)
            
            return {
                "success": final_state.get("status") == WorkflowStatus.COMPLETED.value,
                "request_id": final_state["request_id"],
                "plan": final_state.get("plan"),
                "execution_results": final_state.get("execution_results"),
                "critique": final_state.get("critique"),
                "iterations": final_state.get("iterations"),
                "final_result": final_state.get("final_result"),
                "error": final_state.get("error")
            }
        except Exception as e:
            return {
                "success": False,
                "request_id": input_data["request_id"],
                "error": str(e),
                "plan": None,
                "execution_results": [],
                "final_result": None
            }
    
    async def stream_execute(
        self,
        input_data: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Stream workflow execution events.
        
        Yields state updates as the workflow progresses through
        planning, execution, critique, and re-planning.
        
        Args:
            input_data: Input data
            config: Optional configuration
            
        Yields:
            State updates at each workflow step
        """
        initial_state: WorkflowState = {
            "request_id": input_data["request_id"],
            "request_data": input_data.get("request_data", {}),
            "objective": input_data["objective"],
            "plan": None,
            "current_step": 0,
            "execution_results": [],
            "agent_outputs": [],
            "critique": None,
            "should_replan": False,
            "iterations": 0,
            "max_iterations": self.config.max_iterations,
            "status": WorkflowStatus.PLANNING.value,
            "error": None,
            "final_result": None
        }
        
        async for event in self.graph.astream(initial_state, config=config):
            yield event
    
    def visualize(self, output_path: str = "workflow_graph.png"):
        """
        Visualize the workflow graph.
        
        Args:
            output_path: Path to save the visualization
        """
        try:
            from IPython.display import Image, display
            display(Image(self.graph.get_graph().draw_mermaid_png()))
        except Exception as e:
            print(f"Visualization failed: {e}")
            print("Install graphviz for visualization: pip install graphviz")

