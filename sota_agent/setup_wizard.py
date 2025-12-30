#!/usr/bin/env python3
"""
SOTA Agent Framework Setup Wizard

Interactive wizard that guides users through framework setup:
- Beginner mode: Opinionated defaults with all best practices
- Advanced mode: Full control and customization
- Validates configuration and suggests improvements
"""

import os
import sys
from typing import Dict, Any, List, Optional
from enum import Enum
import yaml


class ExperienceLevel(str, Enum):
    """User experience level."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class FrameworkPreset(str, Enum):
    """Framework configuration presets."""
    MINIMAL = "minimal"
    RECOMMENDED = "recommended"
    FULL_FEATURED = "full"
    CUSTOM = "custom"


class FrameworkSetupWizard:
    """
    Interactive setup wizard for SOTA Agent Framework.
    
    Guides users through:
    - Experience level selection
    - Feature selection
    - Configuration generation
    - Best practices recommendations
    
    Usage:
        wizard = FrameworkSetupWizard()
        config = wizard.run()
        wizard.generate_project(config, output_dir="./my_project")
    """
    
    def __init__(self):
        """Initialize setup wizard."""
        self.config = {}
        self.experience_level = None
        self.preset = None
        self.features = []
    
    def run(self, interactive: bool = True) -> Dict[str, Any]:
        """
        Run the setup wizard.
        
        Args:
            interactive: If True, prompts user for input. If False, uses defaults.
            
        Returns:
            Complete framework configuration
        """
        self._print_welcome()
        
        if interactive:
            self.experience_level = self._ask_experience_level()
            self.preset = self._ask_preset()
            
            if self.preset == FrameworkPreset.CUSTOM:
                self.features = self._ask_features()
            else:
                self.features = self._get_preset_features(self.preset)
        else:
            # Non-interactive defaults
            self.experience_level = ExperienceLevel.INTERMEDIATE
            self.preset = FrameworkPreset.RECOMMENDED
            self.features = self._get_preset_features(self.preset)
        
        # Generate configuration
        self.config = self._generate_config()
        
        # Show recommendations
        self._show_recommendations()
        
        return self.config
    
    def _print_welcome(self):
        """Print welcome message."""
        print("\n" + "="*70)
        print("🚀 SOTA Agent Framework - Setup Wizard")
        print("="*70)
        print("\nThis wizard will help you set up your agent project with")
        print("best practices and recommended features.\n")
    
    def _ask_experience_level(self) -> ExperienceLevel:
        """Ask user about their experience level."""
        print("What is your experience level with agentic solutions?")
        print("  1. Beginner - New to agents, want opinionated setup")
        print("  2. Intermediate - Some experience, want recommendations")
        print("  3. Advanced - Expert, want full control")
        
        choice = input("\nSelect (1-3) [default: 2]: ").strip() or "2"
        
        levels = {
            "1": ExperienceLevel.BEGINNER,
            "2": ExperienceLevel.INTERMEDIATE,
            "3": ExperienceLevel.ADVANCED
        }
        
        return levels.get(choice, ExperienceLevel.INTERMEDIATE)
    
    def _ask_preset(self) -> FrameworkPreset:
        """Ask user about configuration preset."""
        if self.experience_level == ExperienceLevel.BEGINNER:
            print("\n✨ Beginner Mode: Let's pick the right features for YOUR use case!")
            return self._ask_use_case_preset()
        
        print("\nChoose a configuration preset:")
        print("  1. Minimal - Core agents only")
        print("  2. Recommended - Core + memory + monitoring")
        print("  3. Full-Featured - All features enabled")
        print("  4. Use Case Based - Pick based on what you're building")
        print("  5. Custom - Pick and choose features")
        
        choice = input("\nSelect (1-5) [default: 4]: ").strip() or "4"
        
        if choice == "4":
            return self._ask_use_case_preset()
        
        presets = {
            "1": FrameworkPreset.MINIMAL,
            "2": FrameworkPreset.RECOMMENDED,
            "3": FrameworkPreset.FULL_FEATURED,
            "5": FrameworkPreset.CUSTOM
        }
        
        return presets.get(choice, FrameworkPreset.RECOMMENDED)
    
    def _ask_use_case_preset(self) -> FrameworkPreset:
        """Ask about use case and return appropriate preset."""
        print("\nWhat are you building?")
        print("  1. Simple chatbot")
        print("  2. Context-aware assistant")
        print("  3. Complex workflow orchestration")
        print("  4. Batch data processing")
        print("  5. Production API service")
        print("  6. Research/prototype")
        print("  7. Data analytics agent")
        print("  8. Autonomous agent system")
        
        choice = input("\nSelect (1-8) [default: 2]: ").strip() or "2"
        
        # Map use cases to feature sets
        use_case_features = {
            "1": ["core", "monitoring", "experiments", "services"],  # Simple chatbot
            "2": ["core", "memory", "monitoring", "experiments", "services"],  # Context-aware
            "3": ["core", "memory", "monitoring", "telemetry", "langgraph", "reasoning", "visualization", "benchmarking", "experiments"],  # Complex workflows
            "4": ["core", "monitoring", "telemetry", "benchmarking"],  # Batch processing
            "5": ["core", "monitoring", "telemetry", "experiments", "benchmarking", "visualization", "services"],  # Production API
            "6": ["core"],  # Research/prototype
            "7": ["core", "memory", "monitoring", "telemetry", "visualization", "benchmarking"],  # Data analytics
            "8": ["core", "memory", "monitoring", "telemetry", "langgraph", "reasoning", "optimization", "benchmarking", "visualization", "experiments"]  # Autonomous
        }
        
        self.features = use_case_features.get(choice, use_case_features["2"])
        
        use_case_names = {
            "1": "Simple Chatbot",
            "2": "Context-Aware Assistant",
            "3": "Complex Workflow Orchestration",
            "4": "Batch Data Processing",
            "5": "Production API Service",
            "6": "Research/Prototype",
            "7": "Data Analytics Agent",
            "8": "Autonomous Agent System"
        }
        
        use_case_name = use_case_names.get(choice, "Context-Aware Assistant")
        
        print(f"\n✅ Configuring for: {use_case_name}")
        print(f"   Enabling: {', '.join(self.features)}")
        
        return FrameworkPreset.CUSTOM  # Use custom with pre-selected features
    
    def _ask_features(self) -> List[str]:
        """Ask user to select specific features."""
        print("\nSelect features to enable (y/n):")
        
        features_to_ask = [
            ("memory", "Agent-governed memory system", True),
            ("reasoning", "Reasoning optimization (trajectories, CoT)", True),
            ("optimization", "Prompt optimization (DSPy/TextGrad)", True),
            ("benchmarking", "Comprehensive evaluation suite", True),
            ("visualization", "Databricks-native visualization", True),
            ("experiments", "Experiment tracking & feature flags", True),
            ("monitoring", "Health checks & metrics", True),
            ("telemetry", "OpenTelemetry → Delta Lake", True),
            ("langgraph", "LangGraph orchestration", False),
            ("mcp", "Model Context Protocol integration", False),
            ("services", "FastAPI REST API", False),
        ]
        
        selected = ["core"]  # Core is always included
        
        for feature_id, description, default in features_to_ask:
            default_str = "Y/n" if default else "y/N"
            response = input(f"  {description}? [{default_str}]: ").strip().lower()
            
            should_include = (response == "y") or (default and response != "n")
            
            if should_include:
                selected.append(feature_id)
        
        return selected
    
    def _get_preset_features(self, preset: FrameworkPreset) -> List[str]:
        """Get features for a preset."""
        presets = {
            FrameworkPreset.MINIMAL: [
                "core"
            ],
            FrameworkPreset.RECOMMENDED: [
                "core",
                "memory",
                "monitoring",
                "telemetry",
                "experiments"
            ],
            FrameworkPreset.FULL_FEATURED: [
                "core",
                "memory",
                "reasoning",
                "optimization",
                "benchmarking",
                "visualization",
                "experiments",
                "monitoring",
                "telemetry",
                "langgraph",
                "services"
            ]
        }
        
        return presets.get(preset, presets[FrameworkPreset.RECOMMENDED])
    
    def _generate_config(self) -> Dict[str, Any]:
        """Generate framework configuration."""
        config = {
            "framework": {
                "version": "0.2.1",
                "experience_level": self.experience_level.value,
                "preset": self.preset.value
            },
            "features": {
                feature: self._get_feature_config(feature)
                for feature in self.features
            },
            "agents": {
                "enabled": True,
                "registry": "config/agents.yaml"
            }
        }
        
        return config
    
    def _get_feature_config(self, feature: str) -> Dict[str, Any]:
        """Get configuration for a specific feature."""
        configs = {
            "core": {
                "enabled": True
            },
            "memory": {
                "enabled": True,
                "short_term_capacity": 100,
                "long_term_storage": "unity_catalog",
                "agent_governed": True
            },
            "reasoning": {
                "enabled": True,
                "trajectory_optimization": True,
                "cot_distillation": True,
                "feedback_loops": True
            },
            "optimization": {
                "enabled": True,
                "dspy": {
                    "enabled": True,
                    "teacher_model": "gpt-4"
                },
                "textgrad": {
                    "enabled": True,
                    "max_iterations": 20
                }
            },
            "benchmarking": {
                "enabled": True,
                "metrics": [
                    "tool_call_success",
                    "plan_correctness",
                    "hallucination_rate",
                    "latency",
                    "coherence"
                ]
            },
            "visualization": {
                "enabled": True,
                "databricks_native": True,
                "mlflow_integration": True
            },
            "experiments": {
                "enabled": True,
                "mlflow_tracking": True,
                "feature_flags": True
            },
            "monitoring": {
                "enabled": True,
                "health_checks": ["system", "memory", "disk"],
                "alerting": True
            },
            "telemetry": {
                "enabled": True,
                "otel_enabled": True,
                "delta_lake_export": True
            },
            "langgraph": {
                "enabled": True,
                "plan_act_critique": True
            },
            "mcp": {
                "enabled": True,
                "servers": []
            },
            "services": {
                "enabled": True,
                "api_port": 8000,
                "websockets": True
            }
        }
        
        return configs.get(feature, {"enabled": True})
    
    def _show_recommendations(self):
        """Show recommendations based on configuration."""
        print("\n" + "="*70)
        print("📋 Configuration Summary")
        print("="*70)
        
        print(f"\nExperience Level: {self.experience_level.value.title()}")
        print(f"Preset: {self.preset.value.title()}")
        print(f"Enabled Features: {', '.join(self.features)}")
        
        # Show guidance based on experience level
        if self.experience_level == ExperienceLevel.BEGINNER:
            self._show_beginner_guidance()
        elif self.experience_level == ExperienceLevel.INTERMEDIATE:
            self._show_intermediate_guidance()
        else:
            self._show_advanced_guidance()
        
        # Feature-specific recommendations
        self._show_feature_recommendations()
    
    def _show_beginner_guidance(self):
        """Show guidance for beginners."""
        print("\n🎓 Beginner's Guide:")
        print("  1. Start with simple agents (see examples/)")
        print("  2. Use YAML configuration (config/agents.yaml)")
        print("  3. Run: python examples/example_usage.py")
        print("  4. Check health: python -m monitoring.health_check")
        print("  5. View documentation: docs/GETTING_STARTED.md")
        
        print("\n💡 The framework will:")
        print("  ✅ Automatically track all agent executions")
        print("  ✅ Store memories intelligently")
        print("  ✅ Monitor health and performance")
        print("  ✅ Provide helpful error messages")
    
    def _show_intermediate_guidance(self):
        """Show guidance for intermediate users."""
        print("\n🚀 Next Steps:")
        print("  1. Customize agent behavior in config/agents.yaml")
        print("  2. Add custom agents by extending agents.base.Agent")
        print("  3. Run benchmarks: sota-benchmark run --suite your_suite")
        print("  4. View telemetry in Delta Lake")
        print("  5. Experiment with feature flags")
    
    def _show_advanced_guidance(self):
        """Show guidance for advanced users."""
        print("\n⚡ Advanced Features:")
        print("  • Override any component by subclassing")
        print("  • Custom execution backends in agents/execution/")
        print("  • Direct access to all internal APIs")
        print("  • Full YAML configuration control")
        print("  • Extend with custom metrics/visualizations")
        
        print("\n🔧 Override Examples:")
        print("  - Memory strategies: memory/strategies.py")
        print("  - Reasoning policies: reasoning/policies.py")
        print("  - Custom metrics: evaluation/metrics.py")
    
    def _show_feature_recommendations(self):
        """Show feature-specific recommendations."""
        recommendations = []
        
        if "memory" not in self.features:
            recommendations.append(
                "💡 Consider enabling memory for context-aware agents"
            )
        
        if "monitoring" not in self.features:
            recommendations.append(
                "⚠️  Recommendation: Enable monitoring for production deployments"
            )
        
        if "benchmarking" not in self.features:
            recommendations.append(
                "💡 Enable benchmarking to track agent performance over time"
            )
        
        if "telemetry" not in self.features and "monitoring" in self.features:
            recommendations.append(
                "💡 Add telemetry for detailed observability"
            )
        
        if recommendations:
            print("\n📌 Recommendations:")
            for rec in recommendations:
                print(f"  {rec}")
    
    def generate_project(
        self,
        config: Dict[str, Any],
        output_dir: str,
        domain: str = "my_agent"
    ):
        """
        Generate a new project with the configuration.
        
        Args:
            config: Framework configuration
            output_dir: Output directory
            domain: Domain name for the project
        """
        print(f"\n🔨 Generating project: {output_dir}")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Save configuration
        config_path = os.path.join(output_dir, "framework_config.yaml")
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        print(f"✅ Saved configuration to {config_path}")
        
        # Use existing generator with feature flags
        from .generator import generate_project
        
        generate_project(
            domain=domain,
            output_dir=output_dir,
            include_examples=True
        )
        
        # Create feature-specific files
        self._generate_feature_files(output_dir, config)
        
        print(f"\n✅ Project generated: {output_dir}")
        print(f"\nNext steps:")
        print(f"  cd {output_dir}")
        print(f"  pip install -r requirements.txt")
        print(f"  python examples/example_usage.py")
    
    def _generate_feature_files(
        self,
        output_dir: str,
        config: Dict[str, Any]
    ):
        """Generate feature-specific configuration files."""
        features = config.get("features", {})
        
        # Generate memory config
        if features.get("memory", {}).get("enabled"):
            self._generate_memory_config(output_dir, features["memory"])
        
        # Generate monitoring config
        if features.get("monitoring", {}).get("enabled"):
            self._generate_monitoring_config(output_dir, features["monitoring"])
        
        # Generate experiments config
        if features.get("experiments", {}).get("enabled"):
            self._generate_experiments_config(output_dir, features["experiments"])
    
    def _generate_memory_config(self, output_dir: str, memory_config: Dict):
        """Generate memory configuration."""
        config_dir = os.path.join(output_dir, "config")
        os.makedirs(config_dir, exist_ok=True)
        
        memory_yaml = {
            "memory": {
                "enabled": True,
                "short_term": {
                    "capacity": memory_config.get("short_term_capacity", 100)
                },
                "long_term": {
                    "storage": memory_config.get("long_term_storage", "unity_catalog")
                },
                "agent_governed": memory_config.get("agent_governed", True)
            }
        }
        
        path = os.path.join(config_dir, "memory.yaml")
        with open(path, 'w') as f:
            yaml.dump(memory_yaml, f, default_flow_style=False)
    
    def _generate_monitoring_config(self, output_dir: str, monitoring_config: Dict):
        """Generate monitoring configuration."""
        config_dir = os.path.join(output_dir, "config")
        os.makedirs(config_dir, exist_ok=True)
        
        monitoring_yaml = {
            "monitoring": {
                "health_checks": monitoring_config.get("health_checks", []),
                "alerting": monitoring_config.get("alerting", False),
                "metrics": {
                    "enabled": True,
                    "export_interval_seconds": 60
                }
            }
        }
        
        path = os.path.join(config_dir, "monitoring.yaml")
        with open(path, 'w') as f:
            yaml.dump(monitoring_yaml, f, default_flow_style=False)
    
    def _generate_experiments_config(self, output_dir: str, experiments_config: Dict):
        """Generate experiments configuration."""
        config_dir = os.path.join(output_dir, "config")
        os.makedirs(config_dir, exist_ok=True)
        
        experiments_yaml = {
            "experiments": {
                "mlflow_tracking": experiments_config.get("mlflow_tracking", True),
                "feature_flags": experiments_config.get("feature_flags", True)
            }
        }
        
        path = os.path.join(config_dir, "experiments.yaml")
        with open(path, 'w') as f:
            yaml.dump(experiments_yaml, f, default_flow_style=False)


def main():
    """Main entry point for setup wizard."""
    wizard = FrameworkSetupWizard()
    
    # Check if running interactively
    interactive = sys.stdin.isatty()
    
    config = wizard.run(interactive=interactive)
    
    if interactive:
        generate = input("\nGenerate project now? (y/N): ").strip().lower()
        
        if generate == "y":
            domain = input("Domain name [my_agent]: ").strip() or "my_agent"
            output_dir = input(f"Output directory [./{domain}]: ").strip() or f"./{domain}"
            
            wizard.generate_project(config, output_dir, domain)


if __name__ == "__main__":
    main()

