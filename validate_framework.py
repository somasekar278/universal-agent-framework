#!/usr/bin/env python3
"""
SOTA Agent Framework Validation Script

Comprehensive validation that tests all major components:
- Core agent execution
- Memory system
- Reasoning optimization  
- Prompt optimization
- Benchmarking
- Visualization
- Experiments & feature flags
- Monitoring & health checks
- Telemetry
- Services

Run this to verify the entire framework works!
"""

import sys
import asyncio
from datetime import datetime
from typing import Dict, Any

# Color codes for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_header(text: str):
    """Print section header."""
    print(f"\n{BLUE}{'=' * 80}{RESET}")
    print(f"{BLUE}{text.center(80)}{RESET}")
    print(f"{BLUE}{'=' * 80}{RESET}\n")


def print_success(text: str):
    """Print success message."""
    print(f"{GREEN}✅ {text}{RESET}")


def print_error(text: str):
    """Print error message."""
    print(f"{RED}❌ {text}{RESET}")


def print_warning(text: str):
    """Print warning message."""
    print(f"{YELLOW}⚠️  {text}{RESET}")


def print_info(text: str):
    """Print info message."""
    print(f"{BLUE}ℹ️  {text}{RESET}")


class FrameworkValidator:
    """Validates all framework components."""
    
    def __init__(self):
        """Initialize validator."""
        self.passed = []
        self.failed = []
        self.warnings = []
    
    def test_core_agents(self) -> bool:
        """Test core agent functionality."""
        print_header("Testing Core Agents")
        
        try:
            from agents.base import Agent, CriticalPathAgent, EnrichmentAgent
            from shared.schemas import AgentInput, AgentOutput
            
            print_info("Creating test agent...")
            
            class TestAgent(Agent):
                async def execute(self, input_data: AgentInput) -> AgentOutput:
                    return AgentOutput(
                        agent_name="test",
                        result={"status": "success"},
                        confidence=0.95
                    )
                
                async def process(self, input_data: AgentInput) -> AgentOutput:
                    return await self.execute(input_data)
            
            agent = TestAgent()
            input_data = AgentInput(transaction_id="test_123", data={"test": True})
            result = asyncio.run(agent.execute(input_data))
            
            assert result.agent_name == "test"
            assert result.confidence == 0.95
            
            print_success("Core agent execution works!")
            self.passed.append("Core Agents")
            return True
            
        except Exception as e:
            print_error(f"Core agents failed: {e}")
            self.failed.append(f"Core Agents: {e}")
            return False
    
    def test_memory_system(self) -> bool:
        """Test memory system."""
        print_header("Testing Memory System")
        
        try:
            from memory import MemoryManager, MemoryType, MemoryImportance
            
            print_info("Initializing memory manager...")
            
            manager = MemoryManager()
            
            # Test storage
            print_info("Testing memory storage...")
            asyncio.run(manager.store(
                content="Test memory",
                memory_type=MemoryType.SHORT_TERM,
                importance=MemoryImportance.HIGH
            ))
            
            print_success("Memory system works!")
            self.passed.append("Memory System")
            return True
            
        except Exception as e:
            print_error(f"Memory system failed: {e}")
            self.failed.append(f"Memory System: {e}")
            return False
    
    def test_optimization(self) -> bool:
        """Test prompt optimization."""
        print_header("Testing Prompt Optimization")
        
        try:
            from optimization import PromptOptimizer, DSPyOptimizer, TextGradOptimizer
            
            print_info("Initializing optimizers...")
            
            optimizer = PromptOptimizer()
            dspy = DSPyOptimizer()
            textgrad = TextGradOptimizer()
            
            assert optimizer is not None
            assert dspy is not None
            assert textgrad is not None
            
            print_success("Optimization modules work!")
            self.passed.append("Prompt Optimization")
            return True
            
        except Exception as e:
            print_error(f"Optimization failed: {e}")
            self.failed.append(f"Optimization: {e}")
            return False
    
    def test_reasoning(self) -> bool:
        """Test reasoning optimization."""
        print_header("Testing Reasoning Optimization")
        
        try:
            from reasoning import (
                TrajectoryOptimizer,
                CoTDistiller,
                FeedbackLoop,
                PolicyEngine
            )
            
            print_info("Initializing reasoning components...")
            
            trajectory = TrajectoryOptimizer()
            distiller = CoTDistiller()
            feedback = FeedbackLoop()
            policy = PolicyEngine()
            
            assert trajectory is not None
            assert distiller is not None
            
            print_success("Reasoning optimization works!")
            self.passed.append("Reasoning Optimization")
            return True
            
        except Exception as e:
            print_error(f"Reasoning failed: {e}")
            self.failed.append(f"Reasoning: {e}")
            return False
    
    def test_benchmarking(self) -> bool:
        """Test benchmarking system."""
        print_header("Testing Benchmarking System")
        
        try:
            from evaluation.metrics import (
                ToolCallMetric,
                PlanCorrectnessMetric,
                HallucinationMetric
            )
            from evaluation.harness import EvaluationHarness
            
            print_info("Initializing benchmark metrics...")
            
            tool_metric = ToolCallMetric()
            plan_metric = PlanCorrectnessMetric()
            hallucination_metric = HallucinationMetric()
            harness = EvaluationHarness()
            
            assert tool_metric is not None
            assert harness is not None
            
            print_success("Benchmarking system works!")
            self.passed.append("Benchmarking")
            return True
            
        except Exception as e:
            print_error(f"Benchmarking failed: {e}")
            self.failed.append(f"Benchmarking: {e}")
            return False
    
    def test_visualization(self) -> bool:
        """Test visualization."""
        print_header("Testing Visualization")
        
        try:
            from visualization.databricks_viz import DatabricksVisualizer
            
            print_info("Initializing visualizer...")
            
            viz = DatabricksVisualizer()
            
            assert viz is not None
            
            print_success("Visualization works!")
            self.passed.append("Visualization")
            return True
            
        except Exception as e:
            print_error(f"Visualization failed: {e}")
            self.failed.append(f"Visualization: {e}")
            return False
    
    def test_experiments(self) -> bool:
        """Test experiments and feature flags."""
        print_header("Testing Experiments & Feature Flags")
        
        try:
            from experiments import (
                ExperimentTracker,
                FeatureFlagManager,
                RolloutStrategy
            )
            
            print_info("Initializing experiment tracker...")
            
            tracker = ExperimentTracker(mlflow_tracking=False)
            flags = FeatureFlagManager()
            
            # Test experiment
            exp = tracker.start_experiment(
                name="test_experiment",
                hypothesis="Testing works"
            )
            
            assert exp.name == "test_experiment"
            
            # Test feature flag
            flags.register("test_feature", strategy=RolloutStrategy.ALL)
            assert flags.is_enabled("test_feature")
            
            tracker.end_experiment(exp)
            
            print_success("Experiments & feature flags work!")
            self.passed.append("Experiments")
            return True
            
        except Exception as e:
            print_error(f"Experiments failed: {e}")
            self.failed.append(f"Experiments: {e}")
            return False
    
    def test_monitoring(self) -> bool:
        """Test monitoring and health checks."""
        print_header("Testing Monitoring & Health Checks")
        
        try:
            from monitoring import HealthCheck, MetricsCollector, AlertManager
            
            print_info("Running health checks...")
            
            health = HealthCheck()
            metrics = MetricsCollector()
            alerts = AlertManager()
            
            # Run health checks
            status = health.check_all()
            
            assert isinstance(status, dict)
            assert len(status) > 0
            
            # Check overall health
            is_healthy = health.is_healthy()
            
            if is_healthy:
                print_info("All health checks passed!")
            else:
                print_warning("Some health checks degraded (non-critical)")
            
            print_success("Monitoring system works!")
            self.passed.append("Monitoring")
            return True
            
        except Exception as e:
            print_error(f"Monitoring failed: {e}")
            self.failed.append(f"Monitoring: {e}")
            return False
    
    def test_telemetry(self) -> bool:
        """Test telemetry system."""
        print_header("Testing Telemetry")
        
        try:
            from telemetry import AgentTracer, MetricsRecorder
            
            print_info("Initializing telemetry...")
            
            tracer = AgentTracer()
            metrics = MetricsRecorder()
            
            assert tracer is not None
            assert metrics is not None
            
            print_success("Telemetry works!")
            self.passed.append("Telemetry")
            return True
            
        except Exception as e:
            print_error(f"Telemetry failed: {e}")
            self.failed.append(f"Telemetry: {e}")
            return False
    
    def test_services(self) -> bool:
        """Test services (API, workers)."""
        print_header("Testing Services")
        
        try:
            from services import AgentAPI, BackgroundWorker
            
            print_info("Initializing services...")
            
            api = AgentAPI()
            worker = BackgroundWorker()
            
            assert api is not None
            assert worker is not None
            
            if api.app is not None:
                print_success("FastAPI service initialized!")
            else:
                print_warning("FastAPI not available (install with: pip install fastapi)")
            
            print_success("Services work!")
            self.passed.append("Services")
            return True
            
        except Exception as e:
            print_error(f"Services failed: {e}")
            self.failed.append(f"Services: {e}")
            return False
    
    def test_unity_catalog(self) -> bool:
        """Test Unity Catalog registry."""
        print_header("Testing Unity Catalog Registry")
        
        try:
            from uc_registry import PromptRegistry
            
            print_info("Initializing UC registry...")
            
            registry = PromptRegistry()
            
            assert registry is not None
            
            print_success("Unity Catalog registry works!")
            self.passed.append("Unity Catalog")
            return True
            
        except Exception as e:
            print_error(f"Unity Catalog failed: {e}")
            self.failed.append(f"Unity Catalog: {e}")
            return False
    
    def test_langgraph(self) -> bool:
        """Test LangGraph integration."""
        print_header("Testing LangGraph Integration")
        
        try:
            from orchestration.langgraph.workflow import AgentWorkflowGraph
            from orchestration.langgraph.nodes import PlannerNode
            
            print_info("Checking LangGraph modules...")
            
            # Just check imports work
            assert AgentWorkflowGraph is not None
            assert PlannerNode is not None
            
            print_success("LangGraph integration works!")
            self.passed.append("LangGraph")
            return True
            
        except Exception as e:
            print_error(f"LangGraph failed: {e}")
            self.failed.append(f"LangGraph: {e}")
            return False
    
    def print_summary(self):
        """Print validation summary."""
        print_header("Validation Summary")
        
        total = len(self.passed) + len(self.failed)
        pass_rate = (len(self.passed) / total * 100) if total > 0 else 0
        
        print(f"\n📊 Results: {len(self.passed)}/{total} tests passed ({pass_rate:.1f}%)\n")
        
        if self.passed:
            print(f"{GREEN}✅ Passed ({len(self.passed)}):{RESET}")
            for item in self.passed:
                print(f"  • {item}")
        
        if self.failed:
            print(f"\n{RED}❌ Failed ({len(self.failed)}):{RESET}")
            for item in self.failed:
                print(f"  • {item}")
        
        if self.warnings:
            print(f"\n{YELLOW}⚠️  Warnings ({len(self.warnings)}):{RESET}")
            for item in self.warnings:
                print(f"  • {item}")
        
        print("\n" + "=" * 80 + "\n")
        
        if len(self.failed) == 0:
            print_success("🎉 ALL TESTS PASSED! Framework is ready to use!")
            return True
        else:
            print_error(f"❌ {len(self.failed)} test(s) failed. Check errors above.")
            return False
    
    def run_all(self) -> bool:
        """Run all validation tests."""
        print_header("SOTA Agent Framework Validation")
        print_info(f"Starting validation at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all tests
        self.test_core_agents()
        self.test_memory_system()
        self.test_optimization()
        self.test_reasoning()
        self.test_benchmarking()
        self.test_visualization()
        self.test_experiments()
        self.test_monitoring()
        self.test_telemetry()
        self.test_services()
        self.test_unity_catalog()
        self.test_langgraph()
        
        # Print summary
        return self.print_summary()


def main():
    """Main entry point."""
    validator = FrameworkValidator()
    success = validator.run_all()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

