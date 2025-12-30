"""
Test Suite for Agents

Tests for core agent functionality.
"""

import pytest
from agents.base import Agent, CriticalPathAgent, EnrichmentAgent
from shared.schemas.base import AgentInput, AgentOutput


class TestAgent(Agent):
    """Test agent implementation."""
    
    async def execute(self, input_data: AgentInput) -> AgentOutput:
        """Test execution."""
        return AgentOutput(
            agent_name="test_agent",
            result={"status": "success"},
            confidence=0.95
        )


class TestAgentBase:
    """Test base agent functionality."""
    
    @pytest.mark.asyncio
    async def test_agent_execute(self):
        """Test basic agent execution."""
        agent = TestAgent()
        
        input_data = AgentInput(
            transaction_id="test_123",
            data={"amount": 1000}
        )
        
        result = await agent.execute(input_data)
        
        assert result.agent_name == "test_agent"
        assert result.result["status"] == "success"
        assert result.confidence == 0.95
    
    def test_agent_initialization(self):
        """Test agent initialization."""
        agent = TestAgent()
        assert agent is not None


class TestCriticalPathAgent:
    """Test critical path agent."""
    
    @pytest.mark.asyncio
    async def test_critical_path_execution(self):
        """Test critical path execution."""
        
        class TestCriticalAgent(CriticalPathAgent):
            async def execute(self, input_data: AgentInput) -> AgentOutput:
                return AgentOutput(
                    agent_name="critical",
                    result={"critical": True},
                    confidence=1.0
                )
        
        agent = TestCriticalAgent()
        input_data = AgentInput(transaction_id="test")
        
        result = await agent.execute(input_data)
        assert result.result["critical"] is True


class TestEnrichmentAgent:
    """Test enrichment agent."""
    
    @pytest.mark.asyncio
    async def test_enrichment_execution(self):
        """Test enrichment execution."""
        
        class TestEnrichmentAgent(EnrichmentAgent):
            async def execute(self, input_data: AgentInput) -> AgentOutput:
                return AgentOutput(
                    agent_name="enrichment",
                    result={"enriched": True},
                    confidence=0.8
                )
        
        agent = TestEnrichmentAgent()
        input_data = AgentInput(transaction_id="test")
        
        result = await agent.execute(input_data)
        assert result.result["enriched"] is True


class TestAgentRegistry:
    """Test agent registry."""
    
    def test_registry_initialization(self):
        """Test registry initialization."""
        from agents.registry import AgentRegistry
        
        registry = AgentRegistry()
        assert registry is not None
    
    def test_register_agent(self):
        """Test agent registration."""
        from agents.registry import AgentRegistry
        
        registry = AgentRegistry()
        agent = TestAgent()
        
        registry.register("test_agent", agent)
        assert "test_agent" in registry.list_agents()


class TestAgentRouter:
    """Test agent router."""
    
    def test_router_initialization(self):
        """Test router initialization."""
        from agents.router import AgentRouter
        
        router = AgentRouter()
        assert router is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

