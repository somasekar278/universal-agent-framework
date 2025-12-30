"""
Experiment Tracking Module

Production experiment infrastructure:
- A/B testing framework
- Feature flags
- Experiment logging
- MLflow integration
- Statistical analysis
- Rollout management

Usage:
    from experiments import ExperimentTracker, FeatureFlag
    
    # Track experiment
    tracker = ExperimentTracker()
    with tracker.experiment("prompt_v2"):
        result = agent.execute(input_data)
    
    # Feature flags
    if FeatureFlag.is_enabled("new_memory_system", user_id):
        use_new_system()
"""

from .tracker import (
    ExperimentTracker,
    Experiment,
    ExperimentResult
)

from .feature_flags import (
    FeatureFlag,
    FeatureFlagManager,
    RolloutStrategy
)

from .ab_testing import (
    ABExperiment,
    Variant,
    ExperimentAnalysis
)

from .mlflow_integration import (
    MLflowExperimentLogger,
    log_experiment_metrics
)

__all__ = [
    # Tracking
    "ExperimentTracker",
    "Experiment",
    "ExperimentResult",
    
    # Feature Flags
    "FeatureFlag",
    "FeatureFlagManager",
    "RolloutStrategy",
    
    # A/B Testing
    "ABExperiment",
    "Variant",
    "ExperimentAnalysis",
    
    # MLflow
    "MLflowExperimentLogger",
    "log_experiment_metrics",
]

