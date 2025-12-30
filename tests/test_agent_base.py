"""
Tests for agent base classes.

Basic smoke tests to ensure core functionality works.
"""

import pytest
from agents.base import Agent, CriticalPathAgent, EnrichmentAgent
from shared.schemas.base import AgentInput, AgentOutput


class TestAgentImports:
    """Test agent imports work."""
    
    def test_agent_classes_importable(self):
        """Ensure agent base classes can be imported."""
        assert Agent is not None
        assert CriticalPathAgent is not None
        assert EnrichmentAgent is not None


class SimpleCriticalPathAgent(CriticalPathAgent):
    """Test implementation of critical path agent."""
    
    def execute(self, input_data: AgentInput) -> AgentOutput:
        """Return dummy result."""
        return AgentOutput(
            agent_name="test_critical",
            result={"score": 0.5},
            confidence=0.95
        )


class SimpleEnrichmentAgent(EnrichmentAgent):
    """Test implementation of enrichment agent."""
    
    def execute(self, input_data: AgentInput) -> AgentOutput:
        """Return dummy enrichment."""
        return AgentOutput(
            agent_name="test_enrichment",
            result={"enriched": True},
            confidence=0.8
        )


class TestCriticalPathAgent:
    """Test critical path agent."""
    
    def test_critical_path_agent_creation(self):
        """Test critical path agent can be created."""
        agent = SimpleCriticalPathAgent()
        assert agent is not None
    
    def test_critical_path_agent_execute(self):
        """Test critical path agent execution."""
        agent = SimpleCriticalPathAgent()
        
        # Create dummy request
        request = AgentInput(
            transaction_id="test_123",
            data={"amount": 100.0}
        )
        
        # Execute
        result = agent.execute(request)
        
        # Verify
        assert isinstance(result, AgentOutput)
        assert result.agent_name == "test_critical"
        assert result.result["score"] == 0.5


class TestEnrichmentAgent:
    """Test enrichment agent."""
    
    def test_enrichment_agent_creation(self):
        """Test enrichment agent can be created."""
        agent = SimpleEnrichmentAgent()
        assert agent is not None
    
    def test_enrichment_agent_execute(self):
        """Test enrichment agent execution."""
        agent = SimpleEnrichmentAgent()
        
        # Create dummy request
        request = AgentInput(
            transaction_id="test_123",
            data={"amount": 100.0}
        )
        
        # Execute
        result = agent.execute(request)
        
        # Verify
        assert isinstance(result, AgentOutput)
        assert result.agent_name == "test_enrichment"
        assert result.result["enriched"] is True

