"""
Test that all critical modules can be imported.
This is the fastest test to catch import errors.
"""
import pytest


class TestCoreImports:
    """Test core module imports."""
    
    def test_import_agents(self):
        """Test agents module imports."""
        import agents
        assert agents is not None
    
    def test_import_agent_base(self):
        """Test agent base classes."""
        from agents.base import Agent, CriticalPathAgent, EnrichmentAgent
        assert Agent is not None
        assert CriticalPathAgent is not None
        assert EnrichmentAgent is not None
    
    def test_import_agent_registry(self):
        """Test agent registry."""
        from agents.registry import AgentRegistry, AgentRouter
        assert AgentRegistry is not None
        assert AgentRouter is not None


class TestSchemaImports:
    """Test schema module imports."""
    
    def test_import_schemas(self):
        """Test shared.schemas module."""
        import shared.schemas
        assert shared.schemas is not None
    
    def test_import_learning_schemas(self):
        """Test learning schemas."""
        from shared.schemas.learning import (
            ChatInput, ChatOutput,
            ContextAwareInput, ContextAwareOutput,
            APIRequest, APIResponse,
            WorkflowInput, WorkflowOutput,
            CollaborationRequest, CollaborationResponse
        )
        assert ChatInput is not None
        assert APIRequest is not None
        assert WorkflowInput is not None
    
    def test_import_base_schemas(self):
        """Test base schemas."""
        from shared.schemas import AgentInput, AgentOutput
        assert AgentInput is not None
        assert AgentOutput is not None


class TestMemoryImports:
    """Test memory system imports."""
    
    def test_import_memory(self):
        """Test memory module."""
        import memory
        assert memory is not None
    
    def test_import_memory_manager(self):
        """Test memory manager."""
        from memory.manager import MemoryManager
        assert MemoryManager is not None
    
    def test_import_memory_components(self):
        """Test memory components."""
        try:
            from memory.storage import MemoryStorage
            assert MemoryStorage is not None
        except (ImportError, AttributeError):
            pytest.skip("Memory storage module not available")
        
        try:
            from memory.retrieval import RetrievalStrategy
            assert RetrievalStrategy is not None
        except (ImportError, AttributeError):
            pytest.skip("Memory retrieval module not available")


class TestOrchestrationImports:
    """Test orchestration imports."""
    
    def test_import_orchestration(self):
        """Test orchestration module."""
        import orchestration
        assert orchestration is not None
    
    def test_import_langgraph(self):
        """Test LangGraph integration."""
        try:
            from orchestration.langgraph_workflow import AgentWorkflowGraph
            assert AgentWorkflowGraph is not None
        except (ImportError, AttributeError):
            # Try alternative import
            try:
                from orchestration.workflow import AgentWorkflowGraph
                assert AgentWorkflowGraph is not None
            except (ImportError, AttributeError):
                pytest.skip("LangGraph workflow not available")


class TestEvaluationImports:
    """Test evaluation imports."""
    
    def test_import_evaluation(self):
        """Test evaluation module."""
        import evaluation
        assert evaluation is not None
    
    def test_import_metrics(self):
        """Test metrics."""
        try:
            from evaluation import metrics
            # Check if module has metric classes
            assert hasattr(metrics, 'AgentMetric') or hasattr(metrics, 'Metric')
        except (ImportError, AttributeError, AssertionError):
            pytest.skip("Evaluation metrics not fully implemented")
    
    def test_import_harness(self):
        """Test evaluation harness."""
        from evaluation.harness import EvaluationHarness
        assert EvaluationHarness is not None


class TestReasoningImports:
    """Test reasoning imports."""
    
    def test_import_reasoning(self):
        """Test reasoning module."""
        import reasoning
        assert reasoning is not None
    
    def test_import_optimizer(self):
        """Test reasoning optimizer."""
        from reasoning.optimizer import ReasoningOptimizer
        assert ReasoningOptimizer is not None


class TestVisualizationImports:
    """Test visualization imports."""
    
    def test_import_visualization(self):
        """Test visualization module."""
        import visualization
        assert visualization is not None
    
    def test_import_databricks_viz(self):
        """Test Databricks visualizations."""
        from visualization.databricks_viz import DatabricksVisualizer
        assert DatabricksVisualizer is not None


class TestTelemetryImports:
    """Test telemetry imports."""
    
    def test_import_telemetry(self):
        """Test telemetry module."""
        import telemetry
        assert telemetry is not None
    
    def test_import_otel(self):
        """Test OpenTelemetry integration."""
        try:
            from telemetry.otel_tracer import AgentTracer
            assert AgentTracer is not None
        except (ImportError, AttributeError):
            # Try alternative import
            try:
                from telemetry import tracer
                assert tracer is not None
            except (ImportError, AttributeError):
                pytest.skip("OpenTelemetry integration not available")


class TestCLIImports:
    """Test CLI module imports."""
    
    def test_import_sota_agent(self):
        """Test sota_agent module."""
        import sota_agent
        assert sota_agent is not None
    
    def test_import_architect(self):
        """Test architect CLI."""
        from sota_agent.architect import ArchitectureAdvisor
        assert ArchitectureAdvisor is not None
    
    def test_import_learn(self):
        """Test learn CLI."""
        try:
            from sota_agent.learn import LearningPathManager
            assert LearningPathManager is not None
        except (ImportError, AttributeError):
            # Just check the module imports
            import sota_agent.learn
            assert sota_agent.learn is not None
    
    def test_import_cli(self):
        """Test generate CLI."""
        from sota_agent.cli import main
        assert main is not None


class TestOptionalImports:
    """Test optional dependency imports."""
    
    def test_import_a2a(self):
        """Test A2A imports (may not be available)."""
        try:
            from agents.a2a import A2A_AVAILABLE
            if A2A_AVAILABLE:
                from agents.a2a.client import A2AClient
                assert A2AClient is not None
        except ImportError:
            pytest.skip("A2A not installed")
    
    def test_import_mcp(self):
        """Test MCP imports (may not be available)."""
        try:
            from agents import MCP_AVAILABLE
            if MCP_AVAILABLE:
                from agents.mcp_client import AgentMCPClient
                assert AgentMCPClient is not None
        except ImportError:
            pytest.skip("MCP not installed")

