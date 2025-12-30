"""
Test Fixtures and Configuration

Shared pytest fixtures for all tests.
"""

import pytest
from typing import Dict, Any


@pytest.fixture
def sample_input_data() -> Dict[str, Any]:
    """Sample input data for testing."""
    return {
        "transaction_id": "test_123",
        "amount": 1000.00,
        "merchant": "Test Merchant",
        "timestamp": "2025-06-30T10:00:00Z"
    }


@pytest.fixture
def sample_agent_config() -> Dict[str, Any]:
    """Sample agent configuration."""
    return {
        "name": "test_agent",
        "type": "critical_path",
        "execution_mode": "in_process",
        "timeout_seconds": 30,
        "retry_policy": {
            "max_retries": 3,
            "backoff_multiplier": 2
        }
    }


@pytest.fixture
def sample_training_data():
    """Sample training data for optimization."""
    return [
        {"input": "Transaction $100", "output": "legitimate"},
        {"input": "Wire transfer $10000", "output": "review"},
        {"input": "Multiple rapid transactions", "output": "fraud"},
        {"input": "Regular grocery purchase", "output": "legitimate"},
    ]


@pytest.fixture
def sample_evaluation_data():
    """Sample evaluation data."""
    return [
        {"input": "Test case 1", "expected": "result 1"},
        {"input": "Test case 2", "expected": "result 2"},
    ]


@pytest.fixture
def mock_llm_response():
    """Mock LLM response."""
    return {
        "result": "Test response",
        "confidence": 0.95,
        "reasoning": "This is a test"
    }


# Async fixtures
@pytest.fixture
async def async_agent():
    """Async agent fixture."""
    from agents.base import Agent
    from shared.schemas.base import AgentInput, AgentOutput
    
    class TestAgent(Agent):
        async def execute(self, input_data: AgentInput) -> AgentOutput:
            return AgentOutput(
                agent_name="test",
                result={"status": "success"},
                confidence=1.0
            )
    
    return TestAgent()


# Setup and teardown
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment."""
    print("\n🧪 Setting up test environment...")
    yield
    print("\n✅ Test environment cleaned up")


# pytest configuration
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )

