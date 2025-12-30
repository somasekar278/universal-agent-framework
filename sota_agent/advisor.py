#!/usr/bin/env python3
"""
Framework Advisor

Analyzes your project and recommends features/improvements.
Helps both beginners and advanced users optimize their setup.
"""

import os
import yaml
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class Recommendation:
    """A framework recommendation."""
    category: str  # feature, configuration, best_practice
    priority: str  # critical, high, medium, low
    title: str
    description: str
    action: str
    benefit: str


class FrameworkAdvisor:
    """
    Analyzes agent projects and provides recommendations.
    
    Usage:
        advisor = FrameworkAdvisor()
        recommendations = advisor.analyze("./my_project")
        advisor.print_report(recommendations)
    """
    
    def __init__(self):
        """Initialize advisor."""
        self.recommendations = []
    
    def analyze(self, project_dir: str) -> List[Recommendation]:
        """
        Analyze a project and generate recommendations.
        
        Args:
            project_dir: Path to project directory
            
        Returns:
            List of recommendations
        """
        self.recommendations = []
        
        # Check if project exists
        if not os.path.exists(project_dir):
            print(f"❌ Project directory not found: {project_dir}")
            return []
        
        print(f"🔍 Analyzing project: {project_dir}\n")
        
        # Load configuration if exists
        config = self._load_config(project_dir)
        
        # Run analyses
        self._check_memory_system(project_dir, config)
        self._check_monitoring(project_dir, config)
        self._check_telemetry(project_dir, config)
        self._check_benchmarking(project_dir, config)
        self._check_optimization(project_dir, config)
        self._check_experiments(project_dir, config)
        self._check_documentation(project_dir)
        self._check_configuration(project_dir, config)
        
        return self.recommendations
    
    def _load_config(self, project_dir: str) -> Dict[str, Any]:
        """Load project configuration."""
        config_path = os.path.join(project_dir, "framework_config.yaml")
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f) or {}
        
        return {}
    
    def _check_memory_system(self, project_dir: str, config: Dict):
        """Check if memory system is configured."""
        memory_enabled = config.get("features", {}).get("memory", {}).get("enabled", False)
        
        if not memory_enabled:
            self.recommendations.append(Recommendation(
                category="feature",
                priority="high",
                title="Enable Agent Memory System",
                description="Your agents don't have memory enabled",
                action="Add 'memory' to enabled features in framework_config.yaml",
                benefit="Agents will remember context across interactions, improving coherence"
            ))
        else:
            # Check if agent-governed
            agent_governed = config.get("features", {}).get("memory", {}).get("agent_governed", False)
            
            if not agent_governed:
                self.recommendations.append(Recommendation(
                    category="configuration",
                    priority="medium",
                    title="Enable Agent-Governed Memory",
                    description="Memory is enabled but not agent-governed",
                    action="Set 'agent_governed: true' in memory configuration",
                    benefit="Let agents decide what to remember for smarter memory management"
                ))
    
    def _check_monitoring(self, project_dir: str, config: Dict):
        """Check monitoring setup."""
        monitoring_enabled = config.get("features", {}).get("monitoring", {}).get("enabled", False)
        
        if not monitoring_enabled:
            self.recommendations.append(Recommendation(
                category="feature",
                priority="critical",
                title="Enable Production Monitoring",
                description="No monitoring configured for production readiness",
                action="Enable 'monitoring' feature",
                benefit="Track agent health, performance, and catch issues early"
            ))
    
    def _check_telemetry(self, project_dir: str, config: Dict):
        """Check telemetry setup."""
        telemetry_enabled = config.get("features", {}).get("telemetry", {}).get("enabled", False)
        monitoring_enabled = config.get("features", {}).get("monitoring", {}).get("enabled", False)
        
        if monitoring_enabled and not telemetry_enabled:
            self.recommendations.append(Recommendation(
                category="feature",
                priority="high",
                title="Add Detailed Telemetry",
                description="Monitoring is enabled but telemetry is not",
                action="Enable 'telemetry' feature for OpenTelemetry → Delta Lake",
                benefit="Get detailed traces, metrics, and logs for deep observability"
            ))
    
    def _check_benchmarking(self, project_dir: str, config: Dict):
        """Check benchmarking setup."""
        benchmarking_enabled = config.get("features", {}).get("benchmarking", {}).get("enabled", False)
        
        if not benchmarking_enabled:
            self.recommendations.append(Recommendation(
                category="feature",
                priority="medium",
                title="Add Agent Benchmarking",
                description="No benchmarking suite configured",
                action="Enable 'benchmarking' and create test suites in benchmarks/",
                benefit="Track agent performance over time and prevent regressions"
            ))
    
    def _check_optimization(self, project_dir: str, config: Dict):
        """Check prompt optimization."""
        optimization_enabled = config.get("features", {}).get("optimization", {}).get("enabled", False)
        
        if not optimization_enabled:
            self.recommendations.append(Recommendation(
                category="feature",
                priority="low",
                title="Consider Prompt Optimization",
                description="Prompt optimization (DSPy/TextGrad) not enabled",
                action="Enable 'optimization' feature",
                benefit="Automatically improve prompts for better agent performance"
            ))
    
    def _check_experiments(self, project_dir: str, config: Dict):
        """Check experiment tracking."""
        experiments_enabled = config.get("features", {}).get("experiments", {}).get("enabled", False)
        
        if not experiments_enabled:
            self.recommendations.append(Recommendation(
                category="feature",
                priority="medium",
                title="Add Experiment Tracking",
                description="No experiment tracking configured",
                action="Enable 'experiments' for MLflow tracking and feature flags",
                benefit="Track experiments and safely roll out new features"
            ))
    
    def _check_documentation(self, project_dir: str):
        """Check documentation."""
        readme_path = os.path.join(project_dir, "README.md")
        
        if not os.path.exists(readme_path):
            self.recommendations.append(Recommendation(
                category="best_practice",
                priority="medium",
                title="Add Project Documentation",
                description="No README.md found",
                action="Create README.md with project overview and usage",
                benefit="Help team members understand and use your agent system"
            ))
    
    def _check_configuration(self, project_dir: str, config: Dict):
        """Check configuration quality."""
        if not config:
            self.recommendations.append(Recommendation(
                category="configuration",
                priority="high",
                title="Create Framework Configuration",
                description="No framework_config.yaml found",
                action="Run 'sota-setup' to create configuration",
                benefit="Centralize all framework settings in one place"
            ))
    
    def print_report(self, recommendations: List[Recommendation]):
        """
        Print analysis report.
        
        Args:
            recommendations: List of recommendations
        """
        if not recommendations:
            print("✅ Great! Your project follows all best practices.\n")
            return
        
        print("="*70)
        print("📊 Framework Analysis Report")
        print("="*70)
        
        # Group by priority
        critical = [r for r in recommendations if r.priority == "critical"]
        high = [r for r in recommendations if r.priority == "high"]
        medium = [r for r in recommendations if r.priority == "medium"]
        low = [r for r in recommendations if r.priority == "low"]
        
        if critical:
            print("\n🔴 CRITICAL Issues:")
            for rec in critical:
                self._print_recommendation(rec)
        
        if high:
            print("\n🟠 HIGH Priority:")
            for rec in high:
                self._print_recommendation(rec)
        
        if medium:
            print("\n🟡 MEDIUM Priority:")
            for rec in medium:
                self._print_recommendation(rec)
        
        if low:
            print("\n🟢 LOW Priority (Optional):")
            for rec in low:
                self._print_recommendation(rec)
        
        print("\n" + "="*70)
        print(f"Total Recommendations: {len(recommendations)}")
        print("="*70)
    
    def _print_recommendation(self, rec: Recommendation):
        """Print a single recommendation."""
        print(f"\n  📌 {rec.title}")
        print(f"     {rec.description}")
        print(f"     Action: {rec.action}")
        print(f"     Benefit: {rec.benefit}")


def main():
    """Main entry point."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: sota-advisor <project_directory>")
        sys.exit(1)
    
    project_dir = sys.argv[1]
    
    advisor = FrameworkAdvisor()
    recommendations = advisor.analyze(project_dir)
    advisor.print_report(recommendations)


if __name__ == "__main__":
    main()

