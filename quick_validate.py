#!/usr/bin/env python3
"""
Quick Framework Validation
Tests that all major modules can be imported.
"""

print("🧪 SOTA Agent Framework - Quick Validation\n")
print("=" * 60)

tests_passed = 0
tests_failed = 0

def test_import(module_path, description):
    """Test if a module can be imported."""
    global tests_passed, tests_failed
    try:
        __import__(module_path)
        print(f"✅ {description}")
        tests_passed += 1
        return True
    except Exception as e:
        print(f"❌ {description}: {e}")
        tests_failed += 1
        return False

# Test all major modules
test_import("agents.base", "Core Agents")
test_import("agents.registry", "Agent Registry")
test_import("agents.yaml_to_registry", "YAML to Registry")

test_import("memory", "Memory System")
test_import("memory.manager", "Memory Manager")
test_import("memory.agents", "Memory Agents")

test_import("reasoning", "Reasoning Optimization")
test_import("reasoning.trajectory", "Trajectory Optimizer")
test_import("reasoning.distillation", "CoT Distiller")

test_import("optimization", "Prompt Optimization")
test_import("optimization.dspy_optimizer", "DSPy Optimizer")
test_import("optimization.textgrad_optimizer", "TextGrad Optimizer")

test_import("evaluation", "Benchmarking")
test_import("evaluation.metrics", "Evaluation Metrics")
test_import("evaluation.harness", "Evaluation Harness")

test_import("visualization", "Visualization")
test_import("visualization.databricks_viz", "Databricks Visualizer")

test_import("experiments", "Experiments")
test_import("experiments.tracker", "Experiment Tracker")
test_import("experiments.feature_flags", "Feature Flags")

test_import("monitoring", "Monitoring")
test_import("monitoring.health_check", "Health Checks")

test_import("telemetry", "Telemetry")
test_import("telemetry.tracer", "OpenTelemetry Tracer")

test_import("services", "Services")
test_import("services.api", "FastAPI Service")

test_import("uc_registry", "Unity Catalog")
test_import("uc_registry.prompt_registry", "Prompt Registry")

test_import("orchestration.langgraph", "LangGraph")

test_import("sota_agent.generator", "Project Generator")
test_import("sota_agent.cli", "CLI")

print("\n" + "=" * 60)
total = tests_passed + tests_failed
pass_rate = (tests_passed / total * 100) if total > 0 else 0

print(f"\n📊 Results: {tests_passed}/{total} modules working ({pass_rate:.1f}%)\n")

if tests_failed == 0:
    print("🎉 ALL MODULES WORKING! Framework is ready to use!\n")
    exit(0)
else:
    print(f"⚠️  {tests_failed} module(s) have import issues (see above).\n")
    exit(1)

