"""Test Suite for Experiments"""

import pytest
from experiments import ExperimentTracker, FeatureFlagManager, RolloutStrategy


class TestExperimentTracker:
    """Test experiment tracker."""
    
    def test_tracker_initialization(self):
        """Test tracker initialization."""
        tracker = ExperimentTracker(mlflow_tracking=False)
        assert tracker is not None
    
    def test_start_experiment(self):
        """Test starting an experiment."""
        tracker = ExperimentTracker(mlflow_tracking=False)
        
        exp = tracker.start_experiment(
            name="test_experiment",
            description="Test description",
            hypothesis="Test hypothesis"
        )
        
        assert exp.name == "test_experiment"
        assert exp.status == "running"


class TestFeatureFlags:
    """Test feature flag system."""
    
    def test_feature_flag_manager(self):
        """Test feature flag manager."""
        manager = FeatureFlagManager()
        assert manager is not None
    
    def test_register_flag(self):
        """Test registering a feature flag."""
        manager = FeatureFlagManager()
        
        manager.register(
            "test_feature",
            enabled=True,
            strategy=RolloutStrategy.ALL
        )
        
        assert manager.is_enabled("test_feature")
    
    def test_percentage_rollout(self):
        """Test percentage-based rollout."""
        manager = FeatureFlagManager()
        
        manager.register(
            "partial_feature",
            enabled=True,
            strategy=RolloutStrategy.PERCENTAGE,
            percentage=50.0
        )
        
        # Should return boolean
        result = manager.is_enabled("partial_feature", user_id="test_user")
        assert isinstance(result, bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

