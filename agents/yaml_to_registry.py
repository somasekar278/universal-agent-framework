"""
YAML to Dynamic Registry Adapter

Converts static YAML agent configurations to dynamic tool registry entries
with rich metadata.
"""

from typing import Dict, Any, List
import yaml
from pathlib import Path

from .tool_registry import DynamicToolRegistry, ToolMetadata, ToolStatus
from .base import Agent


def convert_agent_to_tool_metadata(
    agent: Agent,
    yaml_config: Dict[str, Any]
) -> ToolMetadata:
    """
    Convert an Agent instance to ToolMetadata.
    
    Extracts metadata from agent class and YAML config to create
    rich tool metadata with schemas, cost, version, etc.
    
    Args:
        agent: Agent instance
        yaml_config: Original YAML configuration
        
    Returns:
        ToolMetadata with rich information
    """
    # Extract from agent
    name = agent.name
    description = agent.__doc__ or yaml_config.get("description", f"Agent: {name}")
    
    # Extract capabilities from agent type and metadata
    capabilities = []
    if hasattr(agent, 'agent_type'):
        capabilities.append(agent.agent_type.value)
    if hasattr(agent, 'capabilities'):
        capabilities.extend(agent.capabilities)
    
    # Build input schema from agent's expected inputs
    input_schema = yaml_config.get("input_schema", {
        "type": "object",
        "properties": {
            "request_data": {"type": "object"},
            "metadata": {"type": "object"}
        },
        "required": ["request_data"]
    })
    
    # Build output schema
    output_schema = yaml_config.get("output_schema", {
        "type": "object",
        "properties": {
            "result": {"type": "object"},
            "confidence_score": {"type": "number"},
            "metadata": {"type": "object"}
        }
    })
    
    # Extract cost and latency estimates
    estimated_latency_ms = yaml_config.get("estimated_latency_ms")
    if hasattr(agent, 'timeout_seconds'):
        estimated_latency_ms = estimated_latency_ms or (agent.timeout_seconds * 1000)
    
    estimated_cost = yaml_config.get("estimated_cost")
    
    # Extract version info
    version = yaml_config.get("version", "1.0.0")
    status_str = yaml_config.get("status", "active")
    status = ToolStatus(status_str) if status_str in [s.value for s in ToolStatus] else ToolStatus.ACTIVE
    
    # Create metadata
    return ToolMetadata(
        name=name,
        version=version,
        description=description,
        input_schema=input_schema,
        output_schema=output_schema,
        capabilities=capabilities,
        tags=yaml_config.get("tags", []),
        category=yaml_config.get("category"),
        estimated_latency_ms=estimated_latency_ms,
        estimated_cost=estimated_cost,
        rate_limit=yaml_config.get("rate_limit"),
        status=status,
        deprecated=yaml_config.get("deprecated", False),
        deprecated_in_favor_of=yaml_config.get("deprecated_in_favor_of"),
        examples=yaml_config.get("examples", []),
        documentation_url=yaml_config.get("documentation_url")
    )


def load_agents_to_registry(
    yaml_path: Path,
    registry: DynamicToolRegistry
) -> Dict[str, Agent]:
    """
    Load agents from YAML and register them in the dynamic registry.
    
    This provides backward compatibility with YAML configs while
    enabling modern dynamic discovery.
    
    Args:
        yaml_path: Path to YAML config file
        registry: Tool registry to populate
        
    Returns:
        Dict of agent name to agent instance
        
    Example:
        ```python
        registry = DynamicToolRegistry()
        agents = load_agents_to_registry(
            Path("config/agents.yaml"),
            registry
        )
        
        # Now use semantic search
        tools = registry.search_tools("find fraud")
        ```
    """
    with open(yaml_path) as f:
        config = yaml.safe_load(f)
    
    agents = {}
    
    for agent_config in config.get("agents", []):
        # Load agent class (existing logic)
        agent_class_path = agent_config["class"]
        # ... agent instantiation logic ...
        
        # For now, skip actual instantiation (would need AgentConfig logic)
        # This is a template showing how to integrate
        pass
    
    return agents


def enhance_yaml_config(yaml_path: Path, output_path: Path):
    """
    Enhance existing YAML config with rich metadata fields.
    
    Adds fields like:
    - input_schema, output_schema
    - estimated_cost, estimated_latency_ms
    - version, status
    - capabilities, tags, category
    - examples, documentation_url
    
    Args:
        yaml_path: Path to existing YAML config
        output_path: Path to write enhanced config
        
    Example:
        ```python
        enhance_yaml_config(
            Path("config/agents.yaml"),
            Path("config/agents_enhanced.yaml")
        )
        ```
    """
    with open(yaml_path) as f:
        config = yaml.safe_load(f)
    
    # Enhance each agent config
    for agent_config in config.get("agents", []):
        # Add missing fields with defaults
        agent_config.setdefault("version", "1.0.0")
        agent_config.setdefault("status", "active")
        agent_config.setdefault("deprecated", False)
        
        agent_config.setdefault("input_schema", {
            "type": "object",
            "properties": {
                "request_data": {"type": "object", "description": "Input data for the agent"}
            },
            "required": ["request_data"]
        })
        
        agent_config.setdefault("output_schema", {
            "type": "object",
            "properties": {
                "result": {"type": "object", "description": "Agent execution result"},
                "confidence_score": {"type": "number", "description": "Confidence in result (0-1)"}
            }
        })
        
        agent_config.setdefault("capabilities", [])
        agent_config.setdefault("tags", [])
        agent_config.setdefault("examples", [])
        
        # Add template example if none exist
        if not agent_config["examples"]:
            agent_config["examples"] = [{
                "input": {"request_data": {}},
                "output": {"result": {}, "confidence_score": 0.0},
                "description": "Example usage"
            }]
    
    # Write enhanced config
    with open(output_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)


# Example enhanced YAML format
ENHANCED_YAML_EXAMPLE = """
agents:
  - name: fraud_detector
    class: fraud_detection.FraudDetectionAgent
    version: "2.1.0"
    status: active  # active|deprecated|experimental|beta
    deprecated: false
    
    # Semantic description for discovery
    description: >
      Detects fraudulent patterns in financial transactions using
      machine learning models and rule-based checks. Analyzes transaction
      amount, merchant, location, and customer history.
    
    # Capabilities for search
    capabilities:
      - fraud_detection
      - risk_analysis
      - transaction_analysis
      - anomaly_detection
    
    # Tags for filtering
    tags:
      - financial
      - security
      - ml-powered
    
    category: security
    
    # Schemas for validation
    input_schema:
      type: object
      properties:
        request_data:
          type: object
          properties:
            transaction_id: {type: string}
            amount: {type: number}
            merchant_id: {type: string}
            customer_id: {type: string}
          required: [transaction_id, amount]
      required: [request_data]
    
    output_schema:
      type: object
      properties:
        result:
          type: object
          properties:
            fraud_score: {type: number, minimum: 0, maximum: 1}
            risk_level: {type: string, enum: [low, medium, high, critical]}
            indicators: {type: array, items: {type: string}}
        confidence_score: {type: number, minimum: 0, maximum: 1}
    
    # Cost & Performance
    estimated_latency_ms: 250
    estimated_cost: 0.002  # $ per invocation
    rate_limit: 1000  # per minute
    
    # Lifecycle
    min_version: "2.0.0"
    max_version: null
    deprecated_in_favor_of: null
    
    # Documentation
    documentation_url: https://docs.example.com/fraud-detector
    examples:
      - input:
          request_data:
            transaction_id: "txn-123"
            amount: 5000.00
            merchant_id: "merch-456"
        output:
          result:
            fraud_score: 0.85
            risk_level: "high"
            indicators: ["unusual_amount", "new_merchant"]
          confidence_score: 0.92
        description: "High-value transaction at new merchant"
"""

