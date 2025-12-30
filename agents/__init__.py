"""
Agent framework for ephemeral fraud detection agents.

Provides:
- Base agent interfaces (Agent, CriticalPathAgent, EnrichmentAgent)
- Pluggable execution backends (in-process, Ray, process pool)
- Agent registry and routing
- Uniform invocation interface
- Configuration-driven deployment (plug-and-play)

Quick start (plug-and-play):
    from agents import AgentRouter
    
    # Load agents from config
    router = AgentRouter.from_yaml("config/agents.yaml")
    
    # Use in your pipeline
    result = await router.route("narrative", agent_input)
"""

from .base import (
    Agent,
    CriticalPathAgent,
    EnrichmentAgent,
    AgentType,
    ExecutionPriority,
    AgentExecutionError,
)

from .registry import (
    AgentRegistry,
    AgentRouter,
    AgentMetadata,
)

from .execution import (
    AgentRunner,
    ExecutionMode,
)

from .config import (
    AgentConfig,
    AgentConfigError,
)

# Optional MCP client (requires mcp package)
try:
    from .mcp_client import AgentMCPClient
    _HAS_MCP = True
except ImportError:
    _HAS_MCP = False
    AgentMCPClient = None

# Dynamic tool registry
from .tool_registry import (
    DynamicToolRegistry,
    ToolMetadata,
    ToolStatus,
    get_global_registry
)

__all__ = [
    # Base classes
    "Agent",
    "CriticalPathAgent",
    "EnrichmentAgent",
    "AgentType",
    "ExecutionPriority",
    "AgentExecutionError",
    
    # Registry and routing
    "AgentRegistry",
    "AgentRouter",
    "AgentMetadata",
    
    # Execution
    "AgentRunner",
    "ExecutionMode",
    
    # Configuration
    "AgentConfig",
    "AgentConfigError",
    
    # Tool Registry
    "DynamicToolRegistry",
    "ToolMetadata",
    "ToolStatus",
    "get_global_registry",
]

# Add MCP client to __all__ only if available
if _HAS_MCP:
    __all__.append("AgentMCPClient")

