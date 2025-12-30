"""Config Manager - stub."""

from dataclasses import dataclass

@dataclass
class AgentConfig:
    """Agent configuration."""
    name: str
    config: dict

class ConfigManager:
    """Configuration management in Unity Catalog."""
    
    def __init__(self, catalog: str = "sota_agents"):
        self.catalog = catalog

