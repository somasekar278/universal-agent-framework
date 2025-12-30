"""
MLflow Integration for Experiments

Automatic logging to MLflow with Databricks integration.
"""

from typing import Dict, Any, Optional
import os


class MLflowExperimentLogger:
    """
    MLflow experiment logger with Databricks support.
    
    Usage:
        logger = MLflowExperimentLogger(experiment_name="my_experiment")
        
        with logger.run("run_1"):
            logger.log_params({"model": "gpt-4"})
            logger.log_metrics({"accuracy": 0.95})
    """
    
    def __init__(self, experiment_name: str = "sota_agents"):
        """Initialize MLflow logger."""
        self.experiment_name = experiment_name
        self.mlflow = None
        
        self._init_mlflow()
    
    def _init_mlflow(self):
        """Initialize MLflow."""
        try:
            import mlflow
            self.mlflow = mlflow
            
            # Detect Databricks
            if "DATABRICKS_RUNTIME_VERSION" in os.environ:
                print("📊 Databricks MLflow detected")
            
            # Set experiment
            self.mlflow.set_experiment(self.experiment_name)
            
        except ImportError:
            print("⚠️  MLflow not available")
    
    def run(self, run_name: str):
        """Start a run context."""
        if self.mlflow:
            return self.mlflow.start_run(run_name=run_name)
        else:
            from contextlib import nullcontext
            return nullcontext()
    
    def log_params(self, params: Dict[str, Any]):
        """Log parameters."""
        if self.mlflow:
            self.mlflow.log_params(params)
    
    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None):
        """Log metrics."""
        if self.mlflow:
            for key, value in metrics.items():
                self.mlflow.log_metric(key, value, step=step)
    
    def log_artifact(self, filepath: str):
        """Log an artifact."""
        if self.mlflow:
            self.mlflow.log_artifact(filepath)


def log_experiment_metrics(name: str, metrics: Dict[str, float]):
    """Quick helper to log metrics."""
    try:
        import mlflow
        for key, value in metrics.items():
            mlflow.log_metric(f"{name}_{key}", value)
    except:
        pass

