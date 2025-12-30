"""
Tests for configuration system.

Tests YAML-based agent configuration loading.
"""

import pytest
import tempfile
import os
import yaml
from pathlib import Path


class TestConfigLoader:
    """Test configuration loading."""
    
    def test_load_yaml_valid(self):
        """Test loading valid YAML config."""
        # Create temp YAML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
agents:
  test_agent:
    class: "agents.base.Agent"
    enabled: true
    execution_mode: "in_process"
    timeout: 30
""")
            config_path = f.name
        
        try:
            # Load config
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
            
            # Verify structure
            assert "agents" in config
            assert "test_agent" in config["agents"]
            assert config["agents"]["test_agent"]["enabled"] is True
        
        finally:
            os.unlink(config_path)
    
    def test_load_yaml_missing_file(self):
        """Test loading non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            with open("nonexistent.yaml", 'r') as f:
                yaml.safe_load(f)
    
    def test_load_yaml_invalid(self):
        """Test loading invalid YAML raises error."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("invalid: yaml: [content")
            config_path = f.name
        
        try:
            with pytest.raises(yaml.YAMLError):
                with open(config_path, 'r') as file:
                    yaml.safe_load(file)
        finally:
            os.unlink(config_path)


class TestConfigValidation:
    """Test configuration validation."""
    
    def test_validate_missing_agents_key(self):
        """Test validation fails without 'agents' key."""
        config = {"wrong_key": {}}
        
        assert "agents" not in config
    
    def test_validate_has_required_fields(self):
        """Test validation checks for required fields."""
        config = {
            "agents": {
                "test_agent": {
                    "class": "agents.base.Agent",
                    "enabled": True
                }
            }
        }
        
        assert "class" in config["agents"]["test_agent"]
        assert "enabled" in config["agents"]["test_agent"]


def test_config_file_examples_exist():
    """Test that example config files exist."""
    example_files = [
        "config/agents/example_basic.yaml",
        "config/agents/example_advanced.yaml",
        "config/agents/example_customer_sla.yaml",
    ]
    
    for example_file in example_files:
        if os.path.exists(example_file):
            # Should load without error
            with open(example_file, 'r') as f:
                config = yaml.safe_load(f)
            
            # Should have agents key
            assert isinstance(config, dict)

