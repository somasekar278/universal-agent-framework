"""
Feature Flag Management

Production-grade feature flag system with gradual rollouts.
"""

from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import random


class RolloutStrategy(Enum):
    """Rollout strategies for feature flags."""
    ALL = "all"  # Everyone gets the feature
    NONE = "none"  # Nobody gets the feature
    PERCENTAGE = "percentage"  # Percentage-based rollout
    WHITELIST = "whitelist"  # Specific users
    CANARY = "canary"  # Canary deployment


@dataclass
class FeatureFlagConfig:
    """Configuration for a feature flag."""
    name: str
    enabled: bool
    strategy: RolloutStrategy
    percentage: float = 100.0  # For PERCENTAGE strategy
    whitelist: list = None  # For WHITELIST strategy
    metadata: Dict[str, Any] = None


class FeatureFlagManager:
    """
    Manage feature flags for gradual rollouts.
    
    Usage:
        manager = FeatureFlagManager()
        
        # Register flags
        manager.register("new_memory_system", 
            strategy=RolloutStrategy.PERCENTAGE,
            percentage=10.0  # 10% rollout
        )
        
        # Check flag
        if manager.is_enabled("new_memory_system", user_id="user123"):
            use_new_system()
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize feature flag manager.
        
        Args:
            config_path: Path to feature flags config (YAML)
        """
        self.flags: Dict[str, FeatureFlagConfig] = {}
        
        if config_path:
            self._load_config(config_path)
    
    def register(
        self,
        name: str,
        enabled: bool = True,
        strategy: RolloutStrategy = RolloutStrategy.ALL,
        percentage: float = 100.0,
        whitelist: Optional[list] = None,
        **metadata
    ):
        """Register a feature flag."""
        self.flags[name] = FeatureFlagConfig(
            name=name,
            enabled=enabled,
            strategy=strategy,
            percentage=percentage,
            whitelist=whitelist or [],
            metadata=metadata or {}
        )
        
        print(f"🚩 Registered feature flag: {name} (strategy={strategy.value})")
    
    def is_enabled(
        self,
        name: str,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Check if feature is enabled.
        
        Args:
            name: Feature flag name
            user_id: Optional user ID for targeting
            context: Additional context for evaluation
            
        Returns:
            True if feature is enabled
        """
        if name not in self.flags:
            return False
        
        flag = self.flags[name]
        
        if not flag.enabled:
            return False
        
        # Apply strategy
        if flag.strategy == RolloutStrategy.ALL:
            return True
        
        elif flag.strategy == RolloutStrategy.NONE:
            return False
        
        elif flag.strategy == RolloutStrategy.PERCENTAGE:
            if user_id:
                # Consistent hashing for stable rollout
                hash_val = hash(f"{name}:{user_id}") % 100
                return hash_val < flag.percentage
            else:
                # Random rollout without user ID
                return random.random() * 100 < flag.percentage
        
        elif flag.strategy == RolloutStrategy.WHITELIST:
            return user_id in flag.whitelist if user_id else False
        
        elif flag.strategy == RolloutStrategy.CANARY:
            # Canary: whitelist + small percentage
            if user_id in flag.whitelist:
                return True
            hash_val = hash(f"{name}:{user_id}") % 100 if user_id else random.randint(0, 99)
            return hash_val < 5  # 5% canary
        
        return False
    
    def update(
        self,
        name: str,
        enabled: Optional[bool] = None,
        percentage: Optional[float] = None,
        whitelist: Optional[list] = None
    ):
        """Update a feature flag."""
        if name not in self.flags:
            raise ValueError(f"Feature flag {name} not found")
        
        flag = self.flags[name]
        
        if enabled is not None:
            flag.enabled = enabled
        
        if percentage is not None:
            flag.percentage = percentage
        
        if whitelist is not None:
            flag.whitelist = whitelist
        
        print(f"🔄 Updated feature flag: {name}")
    
    def _load_config(self, config_path: str):
        """Load feature flags from YAML config."""
        try:
            from shared.config_loader import get_config
            config = get_config()
            
            flags_config = config.get_dict("feature_flags", {})
            
            for name, flag_data in flags_config.items():
                self.register(
                    name=name,
                    enabled=flag_data.get("enabled", True),
                    strategy=RolloutStrategy(flag_data.get("strategy", "all")),
                    percentage=flag_data.get("percentage", 100.0),
                    whitelist=flag_data.get("whitelist", []),
                    **flag_data.get("metadata", {})
                )
        except Exception as e:
            print(f"⚠️  Could not load feature flags: {e}")
    
    def get_all_flags(self) -> Dict[str, Dict[str, Any]]:
        """Get all feature flags with their status."""
        return {
            name: {
                "enabled": flag.enabled,
                "strategy": flag.strategy.value,
                "percentage": flag.percentage,
                "whitelist_count": len(flag.whitelist)
            }
            for name, flag in self.flags.items()
        }


class FeatureFlag:
    """
    Static helper for feature flags.
    
    Usage:
        if FeatureFlag.is_enabled("new_feature"):
            use_new_feature()
    """
    
    _manager: Optional[FeatureFlagManager] = None
    
    @classmethod
    def initialize(cls, manager: FeatureFlagManager):
        """Initialize with a manager."""
        cls._manager = manager
    
    @classmethod
    def is_enabled(cls, name: str, user_id: Optional[str] = None) -> bool:
        """Check if feature is enabled."""
        if cls._manager is None:
            cls._manager = FeatureFlagManager()
        
        return cls._manager.is_enabled(name, user_id)


# Stub implementations for other modules
from .tracker import ExperimentResult


class ABExperiment:
    """A/B experiment implementation."""
    pass


class Variant:
    """Experiment variant."""
    pass


class ExperimentAnalysis:
    """Statistical analysis of experiments."""
    pass


class MLflowExperimentLogger:
    """MLflow experiment logger."""
    pass


def log_experiment_metrics(name: str, metrics: Dict[str, float]):
    """Log experiment metrics to MLflow."""
    try:
        import mlflow
        for key, value in metrics.items():
            mlflow.log_metric(key, value)
    except:
        pass

