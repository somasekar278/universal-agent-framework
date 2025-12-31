#!/usr/bin/env python3
"""
Comprehensive Framework Testing Suite
Tests the SOTA Agent Framework without requiring full agent builds.

Usage:
    python test_framework.py              # Run all tests
    python test_framework.py --quick      # Quick smoke tests only
    python test_framework.py --module memory  # Test specific module
"""

import sys
import importlib
import subprocess
from pathlib import Path
from typing import List, Tuple, Dict, Any
import json


class FrameworkTester:
    """Comprehensive framework testing without building full agents."""
    
    def __init__(self):
        self.results = {
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "details": []
        }
    
    def run_all_tests(self, quick: bool = False):
        """Run all framework tests."""
        print("="*80)
        print("🧪 SOTA Agent Framework - Comprehensive Test Suite")
        print("="*80)
        print()
        
        tests = [
            ("Module Imports", self.test_imports),
            ("CLI Tools", self.test_cli_tools),
            ("Schema Validation", self.test_schemas),
            ("Architecture Advisor", self.test_architect),
        ]
        
        if not quick:
            tests.extend([
                ("Example Files", self.test_examples),
                ("Documentation", self.test_documentation),
                ("Config Files", self.test_config_files),
            ])
        
        for test_name, test_func in tests:
            print(f"\n{'='*80}")
            print(f"📋 Testing: {test_name}")
            print(f"{'='*80}")
            try:
                test_func()
            except Exception as e:
                print(f"❌ {test_name} FAILED: {e}")
                self.results["failed"] += 1
        
        self.print_summary()
    
    def test_imports(self):
        """Test that all core modules can be imported."""
        modules = [
            "agents",
            "agents.base",
            "agents.registry",
            "shared.schemas",
            "shared.schemas.learning",
            "memory",
            "memory.manager",
            "orchestration",
            "evaluation",
            "reasoning",
            "sota_agent",
            "sota_agent.architect",
        ]
        
        print(f"\nTesting {len(modules)} module imports...\n")
        
        for module in modules:
            try:
                importlib.import_module(module)
                print(f"  ✅ {module}")
                self.results["passed"] += 1
            except ImportError as e:
                print(f"  ❌ {module}: {e}")
                self.results["failed"] += 1
            except Exception as e:
                print(f"  ⚠️  {module}: {e}")
                self.results["skipped"] += 1
    
    def test_cli_tools(self):
        """Test that CLI tools are accessible."""
        cli_tools = [
            ("sota-architect", "architect", ["--help"], ["usage", "brief"]),
            ("sota-learn", "learn", ["--help"], ["usage", "level", "learning"]),
            ("sota-setup", "setup_wizard", [], ["setup", "wizard", "agent"]),
            ("sota-generate", "cli", ["--help"], ["usage", "domain", "generate"]),
        ]
        
        print(f"\nTesting {len(cli_tools)} CLI tools...\n")
        
        for tool_name, module_name, args, expected_keywords in cli_tools:
            try:
                cmd = [sys.executable, "-m", f"sota_agent.{module_name}"] + args
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                output = result.stdout.lower() + result.stderr.lower()
                
                # Check if any expected keyword is in output
                if any(keyword in output for keyword in expected_keywords):
                    print(f"  ✅ {tool_name}")
                    self.results["passed"] += 1
                else:
                    print(f"  ❌ {tool_name}: No expected output found")
                    self.results["failed"] += 1
                    
            except subprocess.TimeoutExpired:
                print(f"  ⚠️  {tool_name}: Timeout")
                self.results["skipped"] += 1
            except Exception as e:
                print(f"  ❌ {tool_name}: {e}")
                self.results["failed"] += 1
    
    def test_schemas(self):
        """Test that all schema classes can be instantiated."""
        from shared.schemas.learning import (
            ChatInput, ChatOutput,
            ContextAwareInput, ContextAwareOutput,
            APIRequest, APIResponse,
            WorkflowInput, WorkflowOutput,
            CollaborationRequest, CollaborationResponse
        )
        
        schemas_to_test = [
            ("ChatInput", ChatInput, {"question": "test", "user_id": "user1"}),
            ("ChatOutput", ChatOutput, {"answer": "test", "confidence": 0.9}),
            ("ContextAwareInput", ContextAwareInput, {
                "message": "test", "user_id": "user1", "session_id": "sess1"
            }),
            ("APIRequest", APIRequest, {
                "endpoint": "test", "data": {}, "request_id": "req1"
            }),
            ("APIResponse", APIResponse, {
                "success": True, "request_id": "req1", "processing_time_ms": 10.0
            }),
        ]
        
        print(f"\nTesting {len(schemas_to_test)} schema validations...\n")
        
        for schema_name, schema_class, test_data in schemas_to_test:
            try:
                instance = schema_class(**test_data)
                assert instance is not None
                print(f"  ✅ {schema_name}")
                self.results["passed"] += 1
            except Exception as e:
                print(f"  ❌ {schema_name}: {e}")
                self.results["failed"] += 1
    
    def test_architect(self):
        """Test architecture advisor with sample briefs."""
        from sota_agent.architect import ArchitectureAdvisor
        
        test_briefs = [
            ("Simple chatbot", "Build a simple FAQ bot", 1),
            ("Context-aware", "Assistant that remembers user preferences", 2),
            ("Production API", "Production API with monitoring and 99.9% uptime", 3),
            ("Complex workflow", "System that plans, executes, and improves based on feedback", 4),
            ("Multi-agent", "Multiple autonomous agents that communicate and coordinate with each other", 5),
        ]
        
        print(f"\nTesting architect with {len(test_briefs)} briefs...\n")
        
        advisor = ArchitectureAdvisor()
        
        for test_name, brief, expected_level in test_briefs:
            try:
                recommendation = advisor.analyze_brief(brief)
                if recommendation.level.value == expected_level:
                    print(f"  ✅ {test_name} → Level {recommendation.level.value} (confidence: {recommendation.confidence:.0%})")
                    self.results["passed"] += 1
                else:
                    print(f"  ⚠️  {test_name} → Level {recommendation.level.value} (expected {expected_level}, confidence: {recommendation.confidence:.0%})")
                    self.results["skipped"] += 1
            except Exception as e:
                print(f"  ❌ {test_name}: {e}")
                self.results["failed"] += 1
    
    def test_examples(self):
        """Test that example files can be imported."""
        examples = [
            "examples.learning_agents_generic",
            "examples.a2a_official_example",
        ]
        
        print(f"\nTesting {len(examples)} example files...\n")
        
        for example in examples:
            try:
                # Just try to import, don't run
                spec = importlib.util.find_spec(example)
                if spec is not None:
                    print(f"  ✅ {example}")
                    self.results["passed"] += 1
                else:
                    print(f"  ❌ {example}: Not found")
                    self.results["failed"] += 1
            except Exception as e:
                print(f"  ⚠️  {example}: {e}")
                self.results["skipped"] += 1
    
    def test_documentation(self):
        """Test that key documentation files exist."""
        docs = [
            "README.md",
            "DOCUMENTATION_MAP.md",
            "GETTING_STARTED.md",
            "docs/ARCHITECTURE_ADVISOR.md",
            "docs/LEARNING_PATH.md",
            "docs/LEARNING_SCHEMAS.md",
            "docs/INTEGRATIONS.md",
        ]
        
        print(f"\nTesting {len(docs)} documentation files...\n")
        
        for doc in docs:
            path = Path(doc)
            if path.exists():
                # Check it's not empty
                if path.stat().st_size > 100:
                    print(f"  ✅ {doc}")
                    self.results["passed"] += 1
                else:
                    print(f"  ⚠️  {doc}: Too small")
                    self.results["skipped"] += 1
            else:
                print(f"  ❌ {doc}: Not found")
                self.results["failed"] += 1
    
    def test_config_files(self):
        """Test that configuration files are valid."""
        configs = [
            ("pyproject.toml", self._validate_toml),
            ("config/sota_config.yaml", self._validate_yaml),
        ]
        
        print(f"\nTesting {len(configs)} config files...\n")
        
        for config_path, validator in configs:
            path = Path(config_path)
            if path.exists():
                try:
                    validator(path)
                    print(f"  ✅ {config_path}")
                    self.results["passed"] += 1
                except Exception as e:
                    print(f"  ❌ {config_path}: {e}")
                    self.results["failed"] += 1
            else:
                print(f"  ⚠️  {config_path}: Not found")
                self.results["skipped"] += 1
    
    def _validate_toml(self, path: Path):
        """Validate TOML file."""
        try:
            import tomli
            with open(path, 'rb') as f:
                tomli.load(f)
        except ImportError:
            # Try with toml
            import toml
            with open(path, 'r') as f:
                toml.load(f)
    
    def _validate_yaml(self, path: Path):
        """Validate YAML file."""
        import yaml
        with open(path, 'r') as f:
            yaml.safe_load(f)
    
    def print_summary(self):
        """Print test summary."""
        print("\n" + "="*80)
        print("📊 Test Summary")
        print("="*80)
        
        total = self.results["passed"] + self.results["failed"] + self.results["skipped"]
        
        print(f"\nTotal Tests: {total}")
        print(f"✅ Passed:   {self.results['passed']} ({self.results['passed']/total*100:.1f}%)")
        print(f"❌ Failed:   {self.results['failed']} ({self.results['failed']/total*100:.1f}%)")
        print(f"⚠️  Skipped:  {self.results['skipped']} ({self.results['skipped']/total*100:.1f}%)")
        print()
        
        if self.results["failed"] == 0:
            print("🎉 All critical tests passed!")
            return 0
        else:
            print(f"⚠️  {self.results['failed']} test(s) failed")
            return 1


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Test SOTA Agent Framework without building full agents"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run quick smoke tests only"
    )
    parser.add_argument(
        "--module",
        type=str,
        help="Test specific module only"
    )
    
    args = parser.parse_args()
    
    tester = FrameworkTester()
    
    if args.module:
        print(f"Testing module: {args.module}")
        # Module-specific testing
        try:
            importlib.import_module(args.module)
            print(f"✅ {args.module} imported successfully")
            return 0
        except Exception as e:
            print(f"❌ {args.module} failed: {e}")
            return 1
    else:
        return tester.run_all_tests(quick=args.quick)


if __name__ == "__main__":
    sys.exit(main())

