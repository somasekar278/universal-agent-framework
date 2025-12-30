"""
Reasoning Optimization Module

Advanced reasoning optimization techniques for agent improvement:
- Trajectory optimization: Learn optimal action sequences
- Chain-of-thought distillation: Compress reasoning chains
- Self-improvement: Learn from feedback and mistakes
- Policy constraints: Define reasoning guardrails
- RL-style tuning: Optimize via reward signals

Install:
    pip install sota-agent-framework[optimization]

Usage:
    from reasoning import TrajectoryOptimizer, FeedbackLoop, PolicyEngine
    
    # Optimize agent trajectories
    optimizer = TrajectoryOptimizer()
    optimized_path = await optimizer.optimize(agent, task)
    
    # Self-improvement loop
    feedback = FeedbackLoop(agent)
    await feedback.learn_from_critique(result, critique)
    
    # Enforce policies
    policy = PolicyEngine()
    policy.add_constraint("verify_sources", priority="high")
"""

from .trajectory import (
    TrajectoryOptimizer,
    Trajectory,
    Action,
    TrajectoryMetrics,
    TrajectoryLibrary
)

from .distillation import (
    CoTDistiller,
    ReasoningChain,
    DistillationConfig,
    DistillationMetrics
)

from .feedback import (
    FeedbackLoop,
    Critique,
    Revision,
    ImprovementTracker,
    FeedbackConfig
)

from .policies import (
    PolicyEngine,
    Policy,
    PolicyType,
    PolicyViolation,
    PolicyEnforcer
)

from .tuner import (
    RLTuner,
    RewardSignal,
    TuningConfig,
    AgentPolicy,
    ExperienceBuffer
)

from .optimizer import (
    ReasoningOptimizer,
    OptimizationConfig,
    OptimizationResult
)

__all__ = [
    # Trajectory
    "TrajectoryOptimizer",
    "Trajectory",
    "Action",
    "TrajectoryMetrics",
    "TrajectoryLibrary",
    
    # Distillation
    "CoTDistiller",
    "ReasoningChain",
    "DistillationConfig",
    "DistillationMetrics",
    
    # Feedback
    "FeedbackLoop",
    "Critique",
    "Revision",
    "ImprovementTracker",
    "FeedbackConfig",
    
    # Policies
    "PolicyEngine",
    "Policy",
    "PolicyType",
    "PolicyViolation",
    "PolicyEnforcer",
    
    # Tuner
    "RLTuner",
    "RewardSignal",
    "TuningConfig",
    "AgentPolicy",
    "ExperienceBuffer",
    
    # Optimizer
    "ReasoningOptimizer",
    "OptimizationConfig",
    "OptimizationResult",
]

