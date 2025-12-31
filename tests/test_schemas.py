"""
Comprehensive tests for all schema classes.
"""
import pytest
from datetime import datetime
from shared.schemas.learning import (
    ChatInput, ChatOutput,
    ContextAwareInput, ContextAwareOutput,
    APIRequest, APIResponse,
    WorkflowInput, WorkflowOutput,
    CollaborationRequest, CollaborationResponse,
    UniversalInput, UniversalOutput
)


class TestLevel1Schemas:
    """Test Level 1 (Simple Chatbot) schemas."""
    
    def test_chat_input_basic(self):
        """Test basic ChatInput creation."""
        input_data = ChatInput(
            question="What is AI?",
            user_id="user123"
        )
        assert input_data.question == "What is AI?"
        assert input_data.user_id == "user123"
        assert input_data.context == {}  # default_factory=dict
    
    def test_chat_input_with_context(self):
        """Test ChatInput with optional context."""
        input_data = ChatInput(
            question="Tell me more",
            user_id="user123",
            context={"previous": "AI discussion"}
        )
        assert input_data.context == {"previous": "AI discussion"}
    
    def test_chat_output_basic(self):
        """Test basic ChatOutput creation."""
        output = ChatOutput(
            answer="AI is artificial intelligence",
            confidence=0.95
        )
        assert output.answer == "AI is artificial intelligence"
        assert output.confidence == 0.95
        assert output.sources == []  # default_factory=list
    
    def test_chat_output_with_sources(self):
        """Test ChatOutput with sources."""
        output = ChatOutput(
            answer="AI is...",
            confidence=0.95,
            sources=["wikipedia.org"]
        )
        assert len(output.sources) == 1
    
    def test_chat_input_validation(self):
        """Test ChatInput validation."""
        with pytest.raises(Exception):
            # Missing required field
            ChatInput(question="test")


class TestLevel2Schemas:
    """Test Level 2 (Context-Aware) schemas."""
    
    def test_context_aware_input(self):
        """Test ContextAwareInput creation."""
        input_data = ContextAwareInput(
            message="Remember this",
            user_id="user123",
            session_id="sess456"
        )
        assert input_data.message == "Remember this"
        assert input_data.session_id == "sess456"
    
    def test_context_aware_output(self):
        """Test ContextAwareOutput creation."""
        output = ContextAwareOutput(
            response="I remember",
            confidence=0.9,
            context_used=["previous_conversation", "user_preference"]
        )
        assert len(output.context_used) == 2


class TestLevel3Schemas:
    """Test Level 3 (Production API) schemas."""
    
    def test_api_request(self):
        """Test APIRequest creation."""
        request = APIRequest(
            endpoint="/api/predict",
            data={"input": "test"},
            request_id="req123"
        )
        assert request.endpoint == "/api/predict"
        assert request.data == {"input": "test"}
    
    def test_api_response(self):
        """Test APIResponse creation."""
        response = APIResponse(
            success=True,
            data={"result": "success"},
            request_id="req123",
            processing_time_ms=150.5
        )
        assert response.success is True
        assert response.processing_time_ms == 150.5


class TestLevel4Schemas:
    """Test Level 4 (Complex Workflow) schemas."""
    
    def test_workflow_input(self):
        """Test WorkflowInput creation."""
        workflow = WorkflowInput(
            objective="Analyze and report",
            context={"data": "sample"},
            max_iterations=3
        )
        assert workflow.objective == "Analyze and report"
        assert workflow.max_iterations == 3
    
    def test_workflow_output(self):
        """Test WorkflowOutput creation."""
        from shared.schemas.learning import TaskStep, TaskStatus
        
        output = WorkflowOutput(
            objective="Test objective",
            plan=[TaskStep(step_id="1", action="analyze")],
            execution_results={"status": "complete"},
            final_status=TaskStatus.COMPLETED,
            iterations=1,
            total_time_seconds=10.5
        )
        assert len(output.plan) == 1


class TestLevel5Schemas:
    """Test Level 5 (Multi-Agent) schemas."""
    
    def test_collaboration_request(self):
        """Test CollaborationRequest creation."""
        request = CollaborationRequest(
            task_id="collab123",
            initiating_agent="agent1",
            required_capabilities=["analyze", "summarize"],
            task_data={"problem": "Solve problem together"}
        )
        assert len(request.required_capabilities) == 2
        assert request.task_id == "collab123"
    
    def test_collaboration_response(self):
        """Test CollaborationResponse creation."""
        response = CollaborationResponse(
            task_id="collab123",
            participating_agents=["agent1", "agent2"],
            individual_results={"agent1": "result1", "agent2": "result2"},
            aggregated_result={"final": "complete"},
            consensus_reached=True,
            collaboration_time_seconds=5.5
        )
        assert len(response.participating_agents) == 2
        assert response.consensus_reached is True


class TestUniversalSchemas:
    """Test universal schemas that work across all levels."""
    
    def test_universal_input(self):
        """Test UniversalInput with different data types."""
        # UniversalInput.data must be Dict[str, Any]
        test_cases = [
            {"query": "simple question"},
            {"items": ["item1", "item2"]},
            {"text": "just a string"},
            {"nested": {"data": "structure"}},
        ]
        
        for data in test_cases:
            universal = UniversalInput(data=data)
            assert universal.data == data
            assert isinstance(universal.data, dict)
    
    def test_universal_output(self):
        """Test UniversalOutput with metadata."""
        output = UniversalOutput(
            result={"answer": "42"},
            metadata={"confidence": 0.99}
        )
        assert output.metadata["confidence"] == 0.99


class TestSchemaValidation:
    """Test schema validation and error handling."""
    
    def test_required_fields(self):
        """Test that required fields are enforced."""
        with pytest.raises(Exception):
            ChatInput()  # Missing required fields
    
    def test_type_validation(self):
        """Test that types are validated."""
        with pytest.raises(Exception):
            ChatOutput(
                answer="test",
                confidence="not a number"  # Should be float
            )
    
    def test_default_values(self):
        """Test that default values work."""
        request = APIRequest(
            endpoint="/test",
            data={},
            request_id="123"
        )
        assert request.metadata == {}  # Default value
        assert request.user_id is None  # Optional field

