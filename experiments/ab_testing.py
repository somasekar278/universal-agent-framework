"""
A/B Testing for Experiments

Statistical A/B testing integrated with experiment tracking.
"""

# This is integrated with optimization/ab_testing.py
# Import from there for full A/B testing functionality

from typing import Dict, Any, List

__all__ = ["ABExperiment", "Variant", "ExperimentAnalysis"]


class ABExperiment:
    """Wrapper for optimization.ABTestFramework."""
    pass


class Variant:
    """Experiment variant (see optimization.PromptVariant)."""
    pass


class ExperimentAnalysis:
    """Statistical analysis (see optimization.ABTestFramework)."""
    pass

