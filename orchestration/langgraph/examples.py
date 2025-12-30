"""
Example LangGraph Workflows

Pre-built workflows for common use cases.
"""

from typing import Dict, Any, Optional
from agents import AgentRouter
from .workflow import AgentWorkflowGraph, WorkflowConfig


def create_simple_workflow(
    agent_router: AgentRouter,
    max_iterations: int = 3
) -> AgentWorkflowGraph:
    """
    Create a simple workflow with basic planning and execution.
    
    Good for: Single-objective tasks with straightforward execution
    
    Args:
        agent_router: Router with available agents
        max_iterations: Maximum planning iterations
        
    Returns:
        Configured workflow graph
        
    Example:
        ```python
        from agents import AgentRouter
        from orchestration.langgraph import create_simple_workflow
        
        router = AgentRouter.from_yaml("config/agents.yaml")
        workflow = create_simple_workflow(router)
        
        result = await workflow.execute({
            "request_id": "req-001",
            "objective": "Analyze transaction",
            "request_data": {...}
        })
        ```
    """
    config = WorkflowConfig(
        max_iterations=max_iterations,
        max_plan_steps=5,
        critique_threshold=0.7,
        enable_replanning=False,  # Simple workflow doesn't replan
        enable_self_correction=False
    )
    
    return AgentWorkflowGraph(agent_router, config)


def create_planning_workflow(
    agent_router: AgentRouter,
    max_iterations: int = 5,
    critique_threshold: float = 0.8
) -> AgentWorkflowGraph:
    """
    Create a planning workflow with critique and re-planning.
    
    Good for: Complex tasks requiring adaptive planning
    
    Features:
    - Autonomous task decomposition
    - Result quality assessment
    - Self-correcting re-planning
    - Up to max_iterations attempts
    
    Args:
        agent_router: Router with available agents
        max_iterations: Maximum planning iterations
        critique_threshold: Minimum confidence to accept results
        
    Returns:
        Configured workflow graph
        
    Example:
        ```python
        workflow = create_planning_workflow(router, max_iterations=5)
        
        result = await workflow.execute({
            "request_id": "req-001",
            "objective": "Comprehensive fraud analysis with multiple checks",
            "request_data": {...}
        })
        ```
    """
    config = WorkflowConfig(
        max_iterations=max_iterations,
        max_plan_steps=10,
        critique_threshold=critique_threshold,
        enable_replanning=True,
        enable_self_correction=True
    )
    
    return AgentWorkflowGraph(agent_router, config)


def create_research_workflow(
    agent_router: AgentRouter,
    depth: int = 3
) -> AgentWorkflowGraph:
    """
    Create a research workflow with iterative refinement.
    
    Good for: Information gathering and synthesis tasks
    
    Features:
    - Multi-step research process
    - Iterative refinement based on findings
    - Synthesis of multiple sources
    
    Args:
        agent_router: Router with available agents
        depth: Number of research iterations
        
    Returns:
        Configured workflow graph
    """
    config = WorkflowConfig(
        max_iterations=depth,
        max_plan_steps=15,
        critique_threshold=0.75,
        enable_replanning=True,
        enable_self_correction=True
    )
    
    return AgentWorkflowGraph(agent_router, config)


def create_consensus_workflow(
    agent_router: AgentRouter,
    min_agents: int = 3
) -> AgentWorkflowGraph:
    """
    Create a consensus workflow that runs multiple agents.
    
    Good for: High-stakes decisions requiring multiple opinions
    
    Features:
    - Runs multiple agents in parallel/sequence
    - Aggregates results
    - Reaches consensus or identifies conflicts
    
    Args:
        agent_router: Router with available agents
        min_agents: Minimum number of agents to consult
        
    Returns:
        Configured workflow graph
    """
    config = WorkflowConfig(
        max_iterations=2,
        max_plan_steps=min_agents,
        critique_threshold=0.85,  # Higher threshold for consensus
        enable_replanning=False,
        enable_self_correction=True
    )
    
    return AgentWorkflowGraph(agent_router, config)


# Example: Pre-configured workflow for specific domains

def create_fraud_detection_workflow(
    agent_router: AgentRouter
) -> AgentWorkflowGraph:
    """
    Create workflow optimized for fraud detection.
    
    Includes:
    - Data enrichment phase
    - Risk analysis phase
    - Decision making phase
    """
    config = WorkflowConfig(
        max_iterations=3,
        max_plan_steps=8,
        critique_threshold=0.9,  # High threshold for fraud detection
        enable_replanning=True,
        enable_self_correction=True
    )
    
    return AgentWorkflowGraph(agent_router, config)


def create_customer_support_workflow(
    agent_router: AgentRouter
) -> AgentWorkflowGraph:
    """
    Create workflow optimized for customer support.
    
    Includes:
    - Intent classification
    - Context gathering
    - Response generation
    - Quality check
    """
    config = WorkflowConfig(
        max_iterations=2,
        max_plan_steps=5,
        critique_threshold=0.75,
        enable_replanning=False,  # Quick response for support
        enable_self_correction=True
    )
    
    return AgentWorkflowGraph(agent_router, config)

