"""
Adapters for integrating SOTA agents with LangGraph

Provides conversion utilities between Agent framework types and LangGraph types.
"""

from typing import Dict, Any, Callable
from agents import Agent
from shared.schemas import AgentInput, AgentOutput
from .workflow import WorkflowState


def agent_to_langgraph_tool(agent: Agent) -> Dict[str, Any]:
    """
    Convert a SOTA Agent to a LangGraph tool specification.
    
    Args:
        agent: SOTA Agent instance
        
    Returns:
        Tool specification dict compatible with LangGraph
        
    Example:
        ```python
        from agents import MyAgent
        agent = MyAgent()
        tool_spec = agent_to_langgraph_tool(agent)
        ```
    """
    return {
        "name": agent.name,
        "description": agent.__doc__ or f"Agent: {agent.name}",
        "parameters": {
            "type": "object",
            "properties": {
                "request_data": {
                    "type": "object",
                    "description": "Input data for the agent"
                },
                "metadata": {
                    "type": "object",
                    "description": "Optional metadata"
                }
            },
            "required": ["request_data"]
        },
        "function": _create_agent_wrapper(agent)
    }


def _create_agent_wrapper(agent: Agent) -> Callable:
    """Create async wrapper function for agent execution."""
    async def wrapper(request_data: Dict[str, Any], metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Wrapper that calls agent.execute()."""
        agent_input = AgentInput(
            request_id=metadata.get("request_id", "unknown") if metadata else "unknown",
            request_data=request_data,
            metadata=metadata or {}
        )
        
        result = await agent.execute(agent_input)
        
        return {
            "result": result.result if hasattr(result, 'result') else result,
            "confidence": result.confidence_score if hasattr(result, 'confidence_score') else None,
            "metadata": result.metadata if hasattr(result, 'metadata') else {}
        }
    
    return wrapper


def langgraph_state_to_agent_input(
    state: WorkflowState,
    agent_name: str
) -> AgentInput:
    """
    Convert LangGraph workflow state to AgentInput.
    
    Args:
        state: LangGraph workflow state
        agent_name: Name of the agent to execute
        
    Returns:
        AgentInput instance
        
    Example:
        ```python
        agent_input = langgraph_state_to_agent_input(state, "fraud_detection")
        result = await agent.execute(agent_input)
        ```
    """
    return AgentInput(
        request_id=state["request_id"],
        request_data=state["request_data"],
        metadata={
            "workflow_step": state.get("current_step"),
            "workflow_plan": state.get("plan"),
            "previous_results": state.get("execution_results", []),
            "agent_name": agent_name
        }
    )


def agent_output_to_langgraph_state(
    output: AgentOutput,
    state: WorkflowState
) -> WorkflowState:
    """
    Update LangGraph state with agent output.
    
    Args:
        output: Agent execution output
        state: Current workflow state
        
    Returns:
        Updated workflow state
        
    Example:
        ```python
        result = await agent.execute(input_data)
        state = agent_output_to_langgraph_state(result, state)
        ```
    """
    # Add result to execution results
    state["execution_results"].append({
        "step": state["current_step"] + 1,
        "agent": output.agent_name,
        "result": output.result,
        "confidence": output.confidence_score,
        "metadata": output.metadata
    })
    
    state["agent_outputs"].append(output)
    state["current_step"] += 1
    
    return state


def create_agent_chain(agents: list[Agent]) -> Dict[str, Any]:
    """
    Create a LangGraph chain from a list of agents.
    
    Args:
        agents: List of SOTA agents
        
    Returns:
        Chain specification for LangGraph
        
    Example:
        ```python
        from agents import AgentA, AgentB
        chain = create_agent_chain([AgentA(), AgentB()])
        ```
    """
    return {
        "agents": [agent_to_langgraph_tool(agent) for agent in agents],
        "execution_order": [agent.name for agent in agents]
    }

