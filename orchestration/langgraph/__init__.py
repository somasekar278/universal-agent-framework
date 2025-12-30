"""
LangGraph Integration for SOTA Agent Framework

Provides cognitive orchestration with:
- Plan → Act → Critique → Re-plan loops
- Task decomposition
- Dynamic tool discovery
- Self-correcting execution graphs

Install with: pip install sota-agent-framework[agent-frameworks]
"""

from .workflow import AgentWorkflowGraph, WorkflowState, WorkflowConfig
from .nodes import PlannerNode, ExecutorNode, CriticNode, ReplannerNode
from .adapters import agent_to_langgraph_tool, langgraph_state_to_agent_input
from .examples import create_simple_workflow, create_planning_workflow

__all__ = [
    "AgentWorkflowGraph",
    "WorkflowState",
    "WorkflowConfig",
    "PlannerNode",
    "ExecutorNode",
    "CriticNode",
    "ReplannerNode",
    "agent_to_langgraph_tool",
    "langgraph_state_to_agent_input",
    "create_simple_workflow",
    "create_planning_workflow",
]

