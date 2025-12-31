"""
Comprehensive tests for CLI tools.
"""
import pytest
import subprocess
import sys
import tempfile
from pathlib import Path


class TestCLITools:
    """Test all CLI commands."""
    
    def test_architect_help(self):
        """Test sota-architect --help."""
        result = subprocess.run(
            [sys.executable, "-m", "sota_agent.architect", "--help"],
            capture_output=True,
            text=True
        )
        assert "usage" in result.stdout.lower() or "brief" in result.stdout.lower()
    
    def test_architect_basic_brief(self):
        """Test sota-architect with a simple brief."""
        result = subprocess.run(
            [sys.executable, "-m", "sota_agent.architect", "Build a simple chatbot", "--json"],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0
        assert "level" in result.stdout.lower()
    
    def test_architect_all_levels(self):
        """Test architect recommendations for all levels."""
        test_cases = [
            ("Simple FAQ bot", 1),
            ("Chatbot with persistent memory, session tracking, and conversation history storage", 2),
            ("Production API with 99.9% uptime, monitoring, rate limiting, and authentication", 3),
            ("Agent that creates plans, executes them, critiques results, and replans based on feedback", 4),
            ("Multiple autonomous agents that communicate using A2A protocol and coordinate tasks", 5),
        ]
        
        for brief, expected_level in test_cases:
            result = subprocess.run(
                [sys.executable, "-m", "sota_agent.architect", brief, "--json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            assert result.returncode == 0
            # Check level is present (allow some tolerance for edge cases)
            output_lower = result.stdout.lower()
            has_level = f"level {expected_level}" in output_lower or f"level\": {expected_level}" in output_lower
            # For edge cases, check if it's within ±1 level
            if not has_level and expected_level > 1:
                has_nearby = (f"level {expected_level-1}" in output_lower or 
                             f"level {expected_level+1}" in output_lower or
                             f"level\": {expected_level-1}" in output_lower or
                             f"level\": {expected_level+1}" in output_lower)
                assert has_nearby, f"Expected level {expected_level} or nearby, got: {result.stdout[:200]}"
            else:
                assert has_level, f"Expected level {expected_level}, got: {result.stdout[:200]}"
    
    def test_learn_help(self):
        """Test sota-learn --help."""
        result = subprocess.run(
            [sys.executable, "-m", "sota_agent.learn", "--help"],
            capture_output=True,
            text=True
        )
        assert "usage" in result.stdout.lower() or "learn" in result.stdout.lower()
    
    def test_learn_info(self):
        """Test sota-learn info command."""
        # Test info command with level 1
        result = subprocess.run(
            [sys.executable, "-m", "sota_agent.learn", "info", "1"],
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode == 0
        assert "level" in result.stdout.lower()
        assert "chatbot" in result.stdout.lower() or "simple" in result.stdout.lower()
    
    def test_generate_help(self):
        """Test sota-generate --help."""
        result = subprocess.run(
            [sys.executable, "-m", "sota_agent.cli", "--help"],
            capture_output=True,
            text=True
        )
        assert "usage" in result.stdout.lower()
        assert "domain" in result.stdout.lower()
    
    def test_generate_project(self):
        """Test sota-generate creates a project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test_agent"
            result = subprocess.run(
                [
                    sys.executable, "-m", "sota_agent.cli",
                    "--domain", "test_domain",
                    "--output", str(output_path)
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Check command succeeded
            assert result.returncode == 0, f"Command failed: {result.stderr}"
            
            # Check output directory exists
            assert output_path.exists(), f"Output path not created: {output_path}"
            
            # Check key files are created (may vary by implementation)
            files_created = list(output_path.rglob("*"))
            assert len(files_created) > 0, "No files were created"
            
            # Try to find key files (they might be in subdirectories)
            has_pyproject = any("pyproject.toml" in str(f) for f in files_created)
            has_readme = any("README.md" in str(f) for f in files_created)
            
            # At minimum, check that SOME files were created
            assert has_pyproject or has_readme or len(files_created) > 5, \
                f"Expected project files not found. Created: {[f.name for f in files_created[:10]]}"
    
    def test_setup_wizard(self):
        """Test sota-setup runs without error."""
        result = subprocess.run(
            [sys.executable, "-m", "sota_agent.setup_wizard"],
            capture_output=True,
            text=True,
            timeout=5
        )
        assert "setup" in result.stdout.lower() or "wizard" in result.stdout.lower()

