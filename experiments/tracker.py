"""
Experiment Tracker

Tracks experiments with automatic logging to MLflow and Unity Catalog.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from contextlib import contextmanager
import json


@dataclass
class Experiment:
    """Experiment definition."""
    name: str
    description: str
    hypothesis: str
    metrics: List[str]
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    status: str = "running"  # running, completed, failed
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExperimentResult:
    """Result from an experiment run."""
    experiment_name: str
    variant: str
    metrics: Dict[str, float]
    duration_ms: float
    success: bool
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)


class ExperimentTracker:
    """
    Track experiments with automatic logging.
    
    Usage:
        tracker = ExperimentTracker()
        
        # Context manager
        with tracker.experiment("prompt_optimization_v2"):
            result = optimize_prompt()
            tracker.log_metric("improvement", 0.15)
        
        # Manual tracking
        exp = tracker.start_experiment("new_feature")
        try:
            result = run_experiment()
            tracker.log_result(exp, result)
        finally:
            tracker.end_experiment(exp)
    """
    
    def __init__(self, mlflow_tracking: bool = True, uc_logging: bool = True):
        """
        Initialize experiment tracker.
        
        Args:
            mlflow_tracking: Enable MLflow logging
            uc_logging: Enable Unity Catalog logging
        """
        self.mlflow_tracking = mlflow_tracking
        self.uc_logging = uc_logging
        self.active_experiments: Dict[str, Experiment] = {}
        self.results: List[ExperimentResult] = []
        
        self._init_mlflow()
    
    def _init_mlflow(self):
        """Initialize MLflow if available."""
        if self.mlflow_tracking:
            try:
                import mlflow
                self.mlflow = mlflow
                
                # Set experiment
                self.mlflow.set_experiment("sota_agent_experiments")
            except ImportError:
                print("⚠️  MLflow not available. Install: pip install mlflow")
                self.mlflow_tracking = False
    
    @contextmanager
    def experiment(self, name: str, **metadata):
        """
        Context manager for experiments.
        
        Args:
            name: Experiment name
            **metadata: Additional metadata
        """
        exp = self.start_experiment(name, **metadata)
        
        try:
            if self.mlflow_tracking:
                with self.mlflow.start_run(run_name=name):
                    # Log metadata
                    for key, value in metadata.items():
                        self.mlflow.log_param(key, value)
                    
                    yield exp
            else:
                yield exp
            
            self.end_experiment(exp, status="completed")
            
        except Exception as e:
            self.end_experiment(exp, status="failed")
            print(f"❌ Experiment failed: {e}")
            raise
    
    def start_experiment(
        self,
        name: str,
        description: str = "",
        hypothesis: str = "",
        metrics: Optional[List[str]] = None,
        **metadata
    ) -> Experiment:
        """Start a new experiment."""
        if metrics is None:
            metrics = ["accuracy", "latency", "cost"]
        
        exp = Experiment(
            name=name,
            description=description,
            hypothesis=hypothesis,
            metrics=metrics,
            metadata=metadata
        )
        
        self.active_experiments[name] = exp
        
        print(f"🧪 Started experiment: {name}")
        if hypothesis:
            print(f"   Hypothesis: {hypothesis}")
        
        return exp
    
    def end_experiment(self, experiment: Experiment, status: str = "completed"):
        """End an experiment."""
        experiment.end_time = datetime.now()
        experiment.status = status
        
        duration = (experiment.end_time - experiment.start_time).total_seconds()
        
        print(f"✅ Experiment {experiment.name} {status} ({duration:.2f}s)")
        
        # Remove from active
        if experiment.name in self.active_experiments:
            del self.active_experiments[experiment.name]
        
        # Log to Unity Catalog
        if self.uc_logging:
            self._log_to_uc(experiment)
    
    def log_metric(self, name: str, value: float, step: Optional[int] = None):
        """Log a metric."""
        if self.mlflow_tracking:
            try:
                self.mlflow.log_metric(name, value, step=step)
            except:
                pass
        
        print(f"📊 {name}: {value}")
    
    def log_param(self, name: str, value: Any):
        """Log a parameter."""
        if self.mlflow_tracking:
            try:
                self.mlflow.log_param(name, value)
            except:
                pass
    
    def log_result(self, experiment: Experiment, result: ExperimentResult):
        """Log an experiment result."""
        self.results.append(result)
        
        # Log metrics
        for metric_name, metric_value in result.metrics.items():
            self.log_metric(f"{experiment.name}_{metric_name}", metric_value)
    
    def _log_to_uc(self, experiment: Experiment):
        """Log experiment to Unity Catalog."""
        try:
            # Save to UC Volume
            import os
            uc_path = os.getenv(
                "UNITY_CATALOG_VOLUME_PATH",
                "/Volumes/main/sota_agents/experiments"
            )
            
            filepath = f"{uc_path}/{experiment.name}_{experiment.start_time.strftime('%Y%m%d_%H%M%S')}.json"
            
            data = {
                "name": experiment.name,
                "description": experiment.description,
                "hypothesis": experiment.hypothesis,
                "metrics": experiment.metrics,
                "start_time": experiment.start_time.isoformat(),
                "end_time": experiment.end_time.isoformat() if experiment.end_time else None,
                "status": experiment.status,
                "metadata": experiment.metadata,
                "results": [
                    {
                        "variant": r.variant,
                        "metrics": r.metrics,
                        "duration_ms": r.duration_ms,
                        "success": r.success
                    }
                    for r in self.results
                    if r.experiment_name == experiment.name
                ]
            }
            
            os.makedirs(uc_path, exist_ok=True)
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)
            
            print(f"💾 Logged to Unity Catalog: {filepath}")
            
        except Exception as e:
            print(f"⚠️  Could not log to UC: {e}")
    
    def compare_experiments(
        self,
        experiment_names: List[str],
        metric: str = "accuracy"
    ) -> Dict[str, Any]:
        """Compare multiple experiments."""
        comparison = {}
        
        for exp_name in experiment_names:
            exp_results = [
                r for r in self.results
                if r.experiment_name == exp_name
            ]
            
            if exp_results:
                metric_values = [
                    r.metrics.get(metric, 0.0)
                    for r in exp_results
                ]
                
                comparison[exp_name] = {
                    "mean": sum(metric_values) / len(metric_values),
                    "max": max(metric_values),
                    "min": min(metric_values),
                    "count": len(metric_values)
                }
        
        return comparison
    
    def get_best_experiment(self, metric: str = "accuracy") -> Optional[str]:
        """Get best performing experiment."""
        comparison = self.compare_experiments(
            [r.experiment_name for r in self.results],
            metric=metric
        )
        
        if not comparison:
            return None
        
        best = max(comparison.items(), key=lambda x: x[1]["mean"])
        return best[0]

