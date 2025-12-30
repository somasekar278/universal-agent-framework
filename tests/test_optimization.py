"""Test Suite for Prompt Optimization"""

import pytest
from optimization import PromptOptimizer


class TestPromptOptimizer:
    """Test prompt optimization."""
    
    @pytest.mark.asyncio
    async def test_system_prompt_optimization(self):
        """Test system prompt optimization."""
        optimizer = PromptOptimizer()
        
        result = await optimizer.optimize(
            prompt="You are helpful.",
            prompt_type="system",
            evaluation_data=[
                {"input": "test", "expected": "response"}
            ]
        )
        
        assert result is not None
        assert result.optimized_prompt != ""


class TestDSPyOptimizer:
    """Test DSPy optimizer."""
    
    def test_dspy_initialization(self):
        """Test DSPy optimizer initialization."""
        from optimization import DSPyOptimizer
        
        optimizer = DSPyOptimizer()
        assert optimizer is not None


class TestTextGradOptimizer:
    """Test TextGrad optimizer."""
    
    def test_textgrad_initialization(self):
        """Test TextGrad optimizer initialization."""
        from optimization import TextGradOptimizer
        
        optimizer = TextGradOptimizer()
        assert optimizer is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

