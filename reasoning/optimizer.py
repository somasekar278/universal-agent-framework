"""
Reasoning Optimizer

Unified interface for all reasoning optimization techniques.

Combines:
- Trajectory optimization
- CoT distillation
- Feedback loops
- Policy enforcement
- RL tuning
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from .trajectory import TrajectoryOptimizer, Trajectory
from .distillation import CoTDistiller, ReasoningChain
from .feedback import FeedbackLoop, ImprovementTracker
from .policies import PolicyEngine
from .tuner import RLTuner, RewardSignal


@dataclass
class OptimizationConfig:
    """Configuration for reasoning optimization."""
    enable_trajectory_opt: bool = True
    enable_distillation: bool = True
    enable_feedback: bool = True
    enable_policies: bool = True
    enable_rl_tuning: bool = True
    
    # Component-specific configs
    target_compression: float = 0.5
    max_feedback_retries: int = 3
    rl_learning_rate: float = 0.01


@dataclass
class OptimizationResult:
    """Result of optimization."""
    original_cost: float
    optimized_cost: float
    cost_savings: float
    original_latency: float
    optimized_latency: float
    latency_savings: float
    quality_score: float
    suggestions: list
    metadata: Dict[str, Any]


class ReasoningOptimizer:
    """
    Unified reasoning optimizer.
    
    Applies all optimization techniques to improve agent reasoning.
    
    Usage:
        optimizer = ReasoningOptimizer(agent)
        
        # Optimize execution
        result = await optimizer.optimize(input_data)
        
        # Learn from execution
        await optimizer.learn_from_execution(
            trajectory=execution_trajectory,
            reasoning_chain=agent_reasoning,
            reward=0.85
        )
        
        # Get optimization report
        report = optimizer.get_optimization_report()
    """
    
    def __init__(
        self,
        agent: Any,
        config: Optional[OptimizationConfig] = None
    ):
        """
        Initialize optimizer.
        
        Args:
            agent: Agent to optimize
            config: Optimization configuration
        """
        self.agent = agent
        self.config = config or OptimizationConfig()
        
        # Initialize components
        self.trajectory_optimizer = (
            TrajectoryOptimizer() if self.config.enable_trajectory_opt else None
        )
        self.distiller = (
            CoTDistiller() if self.config.enable_distillation else None
        )
        self.feedback_loop = (
            FeedbackLoop(agent) if self.config.enable_feedback else None
        )
        self.policy_engine = (
            PolicyEngine() if self.config.enable_policies else None
        )
        self.rl_tuner = (
            RLTuner(agent.agent_id if hasattr(agent, 'agent_id') else "agent")
            if self.config.enable_rl_tuning else None
        )
    
    async def optimize(self, input_data: Any) -> Any:
        """
        Optimize agent execution.
        
        Applies all enabled optimization techniques.
        
        Args:
            input_data: Input to process
            
        Returns:
            Optimized output
        """
        # 1. Check policies before execution
        if self.policy_engine:
            violations = await self.policy_engine.check({"input": input_data})
            if any(v.severity == "critical" for v in violations):
                raise ValueError("Critical policy violations detected")
        
        # 2. Get optimal configuration from RL tuner
        if self.rl_tuner:
            optimal_config = await self.rl_tuner.tune()
            # Apply to agent (implementation specific)
        
        # 3. Execute with feedback loop
        if self.feedback_loop:
            output = await self.feedback_loop.process_with_feedback(input_data)
        else:
            output = await self.agent.process(input_data)
        
        return output
    
    async def learn_from_execution(
        self,
        trajectory: Optional[Trajectory] = None,
        reasoning_chain: Optional[ReasoningChain] = None,
        reward: Optional[float] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Learn from execution.
        
        Args:
            trajectory: Execution trajectory
            reasoning_chain: Reasoning chain
            reward: Reward signal
            config: Configuration used
        """
        # Learn from trajectory
        if trajectory and self.trajectory_optimizer:
            self.trajectory_optimizer.record(trajectory)
        
        # Learn from reasoning
        if reasoning_chain and self.distiller:
            # Apply importance assessment
            self.distiller.apply_to_chain(reasoning_chain)
            # Distill for future use
            await self.distiller.distill(reasoning_chain)
        
        # Learn from reward
        if reward is not None and self.rl_tuner and config:
            reward_signal = RewardSignal(
                task_id=trajectory.task_id if trajectory else "unknown",
                agent_id=self.agent.agent_id if hasattr(self.agent, 'agent_id') else "agent",
                reward=reward,
                metrics={},
                config=config
            )
            self.rl_tuner.record_reward(reward_signal)
    
    def get_optimization_report(self) -> Dict[str, Any]:
        """Get comprehensive optimization report."""
        report = {
            "enabled_components": {
                "trajectory_optimization": self.config.enable_trajectory_opt,
                "distillation": self.config.enable_distillation,
                "feedback_loops": self.config.enable_feedback,
                "policy_enforcement": self.config.enable_policies,
                "rl_tuning": self.config.enable_rl_tuning
            }
        }
        
        # Trajectory metrics
        if self.trajectory_optimizer:
            metrics = self.trajectory_optimizer.get_metrics()
            report["trajectory"] = {
                "avg_duration_ms": metrics.avg_duration_ms,
                "avg_cost": metrics.avg_cost,
                "efficiency_score": metrics.efficiency_score
            }
        
        # Distillation metrics
        if self.distiller:
            metrics = self.distiller.get_metrics()
            report["distillation"] = {
                "compression_ratio": metrics.compression_ratio,
                "tokens_saved": metrics.tokens_saved
            }
        
        # Feedback metrics
        if self.feedback_loop:
            stats = self.feedback_loop.get_improvement_stats()
            report["feedback"] = stats
        
        # Policy violations
        if self.policy_engine:
            violations = self.policy_engine.get_violations()
            report["policy_violations"] = len(violations)
        
        # RL tuning
        if self.rl_tuner:
            stats = self.rl_tuner.get_stats()
            report["rl_tuning"] = stats
        
        return report
    
    def export_optimizations(self) -> Dict[str, Any]:
        """Export all learned optimizations."""
        exports = {}
        
        if self.trajectory_optimizer:
            exports["trajectory_patterns"] = self.trajectory_optimizer.export_learned_patterns()
        
        if self.distiller:
            exports["distillation_rules"] = self.distiller.export_distillation_rules()
        
        if self.feedback_loop:
            exports["learnings"] = self.feedback_loop.export_learnings()
        
        if self.policy_engine:
            exports["policies"] = {
                name: {"type": p.policy_type.value, "priority": p.priority}
                for name, p in self.policy_engine.get_policies().items()
            }
        
        if self.rl_tuner:
            exports["best_config"] = self.rl_tuner.get_best_config()
        
        return exports

