"""
Test Fixtures and Configuration

Shared pytest fixtures for all tests.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
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
    from shared.schemas import AgentInput, AgentOutput
    
    class TestAgent(Agent):
        async def process(self, input_data: AgentInput) -> AgentOutput:
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


# Temporary directory fixtures
@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def temp_config_file(temp_dir):
    """Create a temporary config file."""
    config_path = temp_dir / "test_config.yaml"
    config_content = """
agents:
  test_agent:
    type: critical_path
    execution_mode: in_process
    timeout: 30
"""
    config_path.write_text(config_content)
    return config_path


# Schema fixtures
@pytest.fixture
def chat_input():
    """Sample ChatInput for testing."""
    from shared.schemas.learning import ChatInput
    return ChatInput(
        question="What is AI?",
        user_id="test_user"
    )


@pytest.fixture
def api_request():
    """Sample APIRequest for testing."""
    from shared.schemas.learning import APIRequest
    return APIRequest(
        endpoint="/api/test",
        data={"test": "data"},
        request_id="test_123"
    )


# Agent fixtures
@pytest.fixture
def mock_agent_router():
    """Mock AgentRouter for testing."""
    from agents.registry import AgentRouter
    return AgentRouter()


@pytest.fixture
def sample_architect_brief():
    """Sample architecture brief."""
    return """
    Build a production-ready chatbot that:
    - Remembers conversation history
    - Has 99.9% uptime
    - Scales to handle 10K concurrent users
    - Includes monitoring and alerting
    """


# pytest configuration
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "cli: marks tests as CLI tests"
    )
    config.addinivalue_line(
        "markers", "requires_api: marks tests that require API access"
    )
    config.addinivalue_line(
        "markers", "requires_databricks: marks tests that require Databricks"
    )

