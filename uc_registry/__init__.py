"""
Unity Catalog Registry

Databricks Unity Catalog integration for:
- Prompt versioning and management
- Model registry integration
- Configuration management
- Lineage tracking

Install:
    pip install sota-agent-framework[databricks]

Usage:
    from uc_registry import PromptRegistry, ModelRegistry
    
    # Register prompts in Unity Catalog
    registry = PromptRegistry()
    registry.register_prompt("fraud_detector_v1", prompt_text)
    
    # Get latest version
    prompt = registry.get_prompt("fraud_detector", version="latest")
"""

from .prompt_registry import (
    PromptRegistry,
    PromptVersion,
    PromptMetadata
)

from .model_registry import (
    ModelRegistry,
    ModelVersion,
    ModelMetadata
)

from .config_manager import (
    ConfigManager,
    AgentConfig
)

__all__ = [
    # Prompt Registry
    "PromptRegistry",
    "PromptVersion",
    "PromptMetadata",
    
    # Model Registry
    "ModelRegistry",
    "ModelVersion",
    "ModelMetadata",
    
    # Config Manager
    "ConfigManager",
    "AgentConfig",
]

