# Reasoning Optimization Guide

**Advanced reasoning optimization for continuously improving AI agents.**

## Overview

The Agent Framework includes a **production-grade reasoning optimization system** that enables agents to learn, improve, and adapt over time.

### What Makes It Agent?

✅ **Trajectory Optimization** - Learn optimal action sequences  
✅ **CoT Distillation** - Compress reasoning chains (50%+ token savings)  
✅ **Self-Improvement** - Critique → Revise → Retry loops  
✅ **Policy Constraints** - Enforce safety, cost, and latency guardrails  
✅ **RL-Style Tuning** - Optimize hyperparameters via reward signals  

---

## Quick Start

### Installation

```bash
# With optimization features
pip install sota-agent-framework[optimization]

# Everything
pip install sota-agent-framework[all]
```

### Basic Usage

```python
from reasoning import ReasoningOptimizer

# Initialize optimizer
optimizer = ReasoningOptimizer(agent)

# Optimize execution
result = await optimizer.optimize(input_data)

# Learn from execution
await optimizer.learn_from_execution(
    trajectory=execution_trajectory,
    reasoning_chain=agent_reasoning,
    reward=0.85
)

# Get report
report = optimizer.get_optimization_report()
```

---

## Core Components

### 1. Trajectory Optimization

Learns optimal action sequences from past executions.

**Problem:** Agents waste time/cost on redundant or inefficient action sequences.

**Solution:** Record trajectories, identify patterns, suggest improvements.

```python
from reasoning import TrajectoryOptimizer, Trajectory, Action, ActionType

# Create optimizer
optimizer = TrajectoryOptimizer()

# Record trajectory
trajectory = Trajectory(task_id="fraud_001", agent_id="fraud_detector")
trajectory.add_action(Action(
    action_type=ActionType.TOOL_CALL,
    name="check_merchant",
    input={"merchant_id": "M123"},
    output={"reputation": "good"},
    duration_ms=150,
    cost=0.002
))
trajectory.add_action(Action(
    action_type=ActionType.REASONING,
    name="analyze_risk",
    input={"data": "..."},
    output={"risk_score": 0.2},
    duration_ms=300,
    cost=0.01
))

# Record
optimizer.record(trajectory)

# Get suggestions
suggestions = await optimizer.suggest_improvements(trajectory)
# Returns: [
#     {
#         "rule": "order_by_cost",
#         "suggestion": "Do cheap validation before expensive processing",
#         "potential_savings": {"cost": 0.005, "duration_ms": 100}
#     }
# ]

# Get optimal trajectory for task type
optimal = optimizer.get_optimal_trajectory("fraud_detection")
```

**Optimization Rules:**
- **Avoid redundant retrievals** - Cache and reuse
- **Order by cost** - Cheap operations first
- **Avoid unnecessary reasoning** - Early exits for simple cases
- **Parallelize independent** - Run concurrently when possible

### 2. Chain-of-Thought Distillation

Compresses verbose reasoning into efficient forms.

**Problem:** Verbose reasoning wastes tokens and costs money.

**Solution:** Distill reasoning chains while maintaining accuracy.

```python
from reasoning import CoTDistiller, ReasoningChain, ReasoningStep

# Create distiller
distiller = CoTDistiller()

# Record verbose reasoning
chain = ReasoningChain(task_id="task_001")
chain.add_step(ReasoningStep(
    step_number=1,
    content="First, let's analyze the transaction amount...",
    tokens=50
))
chain.add_step(ReasoningStep(
    step_number=2,
    content="The amount is $5000 which is significantly higher...",
    tokens=60
))
chain.add_step(ReasoningStep(
    step_number=3,
    content="This means we should flag it as suspicious.",
    tokens=30
))

# Distill (target 50% compression)
distilled = await distiller.distill(chain, target_compression=0.5)

print(f"Saved {distilled.tokens_saved} tokens!")
# Output: Saved 70 tokens!

# Use distilled version for future similar tasks
```

**Distillation Methods:**
- **Importance-based** - Keep most important steps
- **Summarization** - Merge consecutive steps
- **DSPy-powered** - ML-optimized distillation

**Importance Assessment:**
- Final steps: High importance
- Conclusions ("therefore", "thus"): High importance
- Numbers/facts: Medium importance
- Repetitive content: Low importance

### 3. Feedback Loops

Self-improvement through critique → revise → retry cycles.

**Problem:** Agents make mistakes but don't learn from them.

**Solution:** Automated critique generation and revision.

```python
from reasoning import FeedbackLoop

# Create feedback loop
loop = FeedbackLoop(agent)

# Process with automatic feedback
result = await loop.process_with_feedback(input_data)
# Automatically critiques and revises until satisfied

# Manual critique
critiques = await loop.critique(output)
# Returns: [
#     Critique(
#         critique_type=CritiqueType.COMPLETENESS,
#         severity="high",
#         message="Missing required field: risk_score",
#         suggested_fix="Add risk_score to output"
#     )
# ]

# Revise based on critiques
revision = await loop.revise(output, critiques)
print(f"Improvement: {revision.improvement_score:.2f}")

# Learn from external feedback
await loop.learn_from_critique(result, "Risk score seems too low")

# Get improvement stats
stats = loop.get_improvement_stats()
# {
#     "total_iterations": 47,
#     "avg_improvement": 0.23,
#     "common_issues": {"completeness": 15, "accuracy": 12}
# }
```

**Critique Dimensions:**
- **Accuracy** - Correctness of output
- **Completeness** - All required fields present
- **Efficiency** - Output size and performance
- **Safety** - No PII or sensitive data
- **Reasoning** - Quality of explanation

### 4. Policy Engine

Defines and enforces reasoning constraints.

**Problem:** Agents violate safety, cost, or latency requirements.

**Solution:** Define policies that constrain reasoning.

```python
from reasoning import PolicyEngine

# Create policy engine
engine = PolicyEngine()

# Add constraints
engine.add_cost_limit(max_tokens=5000, priority="high")
engine.add_latency_limit(max_ms=2000, priority="high")

# Custom safety check
engine.add_safety_check(
    "verify_sources",
    lambda ctx: "source" in ctx.get("output", {}),
    priority="critical"
)

# Check before execution
violations = await engine.check(context)
if violations:
    for v in violations:
        print(f"{v.severity}: {v.message}")
    # Output: critical: Policy violated: Safety: verify_sources
```

**Policy Types:**
- **Safety** - PII detection, content moderation
- **Cost** - Token/API limits
- **Latency** - Response time limits
- **Quality** - Output quality requirements
- **Compliance** - Regulatory constraints

### 5. RL-Style Tuning

Optimizes hyperparameters using reward signals.

**Problem:** Fixed hyperparameters don't adapt to task performance.

**Solution:** RL-style tuning with reward signals.

```python
from reasoning import RLTuner, RewardSignal

# Create tuner
tuner = RLTuner(agent_id="fraud_detector")

# Record reward after execution
reward = RewardSignal(
    task_id="task_001",
    agent_id="fraud_detector",
    reward=0.85,  # High reward for good performance
    metrics={"accuracy": 0.95, "latency": 230},
    config={"temperature": 0.7, "max_tokens": 1000}
)
tuner.record_reward(reward)

# Tune based on rewards
optimized_config = await tuner.tune()
# Returns: {"temperature": 0.72, "max_tokens": 950, ...}

# Apply optimized config
agent.update_config(optimized_config)

# Get stats
stats = tuner.get_stats()
# {
#     "total_episodes": 150,
#     "avg_reward": 0.78,
#     "best_reward": 0.95,
#     "current_policy": {...}
# }
```

**Reward Calculation:**
```python
# Example reward function
def calculate_reward(result):
    accuracy = result.get("accuracy", 0)
    latency = result.get("latency_ms", 1000)
    cost = result.get("cost", 0.01)
    
    # Weighted reward
    reward = (
        accuracy * 0.5 +  # 50% accuracy
        (1 - latency / 2000) * 0.3 +  # 30% speed
        (1 - cost / 0.05) * 0.2  # 20% cost
    )
    
    return max(0, min(1, reward))
```

---

## Unified Optimizer

Use all techniques together:

```python
from reasoning import ReasoningOptimizer, OptimizationConfig

# Configure
config = OptimizationConfig(
    enable_trajectory_opt=True,
    enable_distillation=True,
    enable_feedback=True,
    enable_policies=True,
    enable_rl_tuning=True,
    target_compression=0.5,
    max_feedback_retries=3
)

# Create optimizer
optimizer = ReasoningOptimizer(agent, config)

# Optimize execution (applies all techniques)
result = await optimizer.optimize(input_data)

# Learn from execution
await optimizer.learn_from_execution(
    trajectory=execution_trajectory,
    reasoning_chain=agent_reasoning,
    reward=0.85,
    config={"temperature": 0.7}
)

# Get comprehensive report
report = optimizer.get_optimization_report()
# {
#     "trajectory": {"avg_duration_ms": 450, "efficiency_score": 0.82},
#     "distillation": {"compression_ratio": 0.53, "tokens_saved": 2340},
#     "feedback": {"total_iterations": 47, "avg_improvement": 0.23},
#     "rl_tuning": {"avg_reward": 0.78, "best_reward": 0.95}
# }

# Export learned optimizations
exports = optimizer.export_optimizations()
```

---

## Integration Example

Complete example with agent:

```python
from agents.base import EnrichmentAgent
from reasoning import ReasoningOptimizer, Trajectory, Action, ActionType
from reasoning import ReasoningChain, ReasoningStep

class OptimizedAgent(EnrichmentAgent):
    """Agent with reasoning optimization."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.optimizer = ReasoningOptimizer(self)
    
    async def process_internal(self, input_data):
        # Start trajectory recording
        trajectory = Trajectory(
            task_id=input_data.request_id,
            agent_id=self.agent_id
        )
        
        # Record actions
        start_time = time.time()
        result = await self._execute_with_tracking(input_data, trajectory)
        
        # Record reasoning chain
        reasoning_chain = self._extract_reasoning(result)
        
        # Calculate reward
        reward = self._calculate_reward(result)
        
        # Learn from execution
        await self.optimizer.learn_from_execution(
            trajectory=trajectory,
            reasoning_chain=reasoning_chain,
            reward=reward,
            config=self.get_config()
        )
        
        return result
    
    async def _execute_with_tracking(self, input_data, trajectory):
        """Execute while tracking actions."""
        # Tool call
        start = time.time()
        merchant_data = await self.call_tool("check_merchant", input_data)
        trajectory.add_action(Action(
            action_type=ActionType.TOOL_CALL,
            name="check_merchant",
            input=input_data,
            output=merchant_data,
            duration_ms=(time.time() - start) * 1000,
            cost=0.002
        ))
        
        # Reasoning
        start = time.time()
        analysis = await self.analyze(merchant_data)
        trajectory.add_action(Action(
            action_type=ActionType.REASONING,
            name="analyze_risk",
            input=merchant_data,
            output=analysis,
            duration_ms=(time.time() - start) * 1000,
            cost=0.01
        ))
        
        trajectory.success = True
        return analysis
    
    def _calculate_reward(self, result):
        """Calculate reward signal."""
        accuracy = result.get("accuracy", 0.5)
        latency = result.get("latency_ms", 1000)
        
        reward = accuracy * 0.7 + (1 - latency / 2000) * 0.3
        return max(0, min(1, reward))
```

---

## Best Practices

### 1. Start with Trajectory Optimization

```python
# Begin by recording trajectories
optimizer = TrajectoryOptimizer()

# Record for 100+ executions
for input_data in test_cases:
    trajectory = execute_and_track(agent, input_data)
    optimizer.record(trajectory)

# Analyze patterns
metrics = optimizer.get_metrics()
print(f"Efficiency: {metrics.efficiency_score}")

# Get suggestions
suggestions = await optimizer.suggest_improvements(trajectory)
```

### 2. Distill After Stabilization

```python
# Once reasoning is stable, distill
distiller = CoTDistiller()

# Apply importance assessment
for chain in reasoning_chains:
    distiller.apply_to_chain(chain)
    distilled = await distiller.distill(chain)
    
    # Validate accuracy maintained
    if distilled.accuracy_retained > 0.95:
        use_distilled(distilled)
```

### 3. Enable Feedback Gradually

```python
# Start with low retry count
config = FeedbackConfig(max_retries=1)
loop = FeedbackLoop(agent, config)

# Increase as confidence grows
config.max_retries = 3
```

### 4. Define Critical Policies First

```python
engine = PolicyEngine()

# Start with safety
engine.add_safety_check("no_pii", detect_pii, priority="critical")

# Add operational constraints
engine.add_cost_limit(max_tokens=10000, priority="high")
engine.add_latency_limit(max_ms=5000, priority="high")
```

### 5. Tune on Real Data

```python
tuner = RLTuner(agent_id="myagent")

# Use real outcomes as rewards
for execution in production_logs:
    reward = calculate_reward_from_outcome(execution)
    tuner.record_reward(reward)

# Tune periodically
optimized = await tuner.tune()
```

---

## Monitoring & Metrics

```python
# Get comprehensive stats
report = optimizer.get_optimization_report()

# Log to MLflow
import mlflow

with mlflow.start_run():
    mlflow.log_metrics({
        "trajectory_efficiency": report["trajectory"]["efficiency_score"],
        "distillation_ratio": report["distillation"]["compression_ratio"],
        "tokens_saved": report["distillation"]["tokens_saved"],
        "avg_improvement": report["feedback"]["avg_improvement"],
        "avg_reward": report["rl_tuning"]["avg_reward"]
    })
```

---

## Advanced Topics

### Custom Optimization Rules

```python
class CustomTrajectoryOptimizer(TrajectoryOptimizer):
    def _initialize_rules(self):
        super()._initialize_rules()
        
        # Add custom rule
        self._optimization_rules.append({
            "name": "prefer_cached_data",
            "description": "Use cached data when available",
            "pattern": self._detect_cache_misses,
            "suggestion": "Check cache before API calls"
        })
    
    def _detect_cache_misses(self, actions):
        # Custom detection logic
        pass
```

### Integration with DSPy

```python
import dspy

class DistillWithDSPy(CoTDistiller):
    async def _distill_with_dspy(self, chain, target):
        # Use DSPy for learned distillation
        optimizer = dspy.BootstrapFewShot(metric=accuracy_metric)
        optimized_distiller = optimizer.compile(
            distiller_module,
            trainset=training_data
        )
        
        return await optimized_distiller(chain)
```

---

## Next Steps

- **[Main Documentation](../README.md)** - Framework overview
- **[Memory System](MEMORY_SYSTEM.md)** - Agent memory
- **[Benchmarking](BENCHMARKING.md)** - Agent evaluation
- **[LangGraph Integration](LANGGRAPH_INTEGRATION.md)** - Autonomous workflows

---

**Ready to optimize your agents?** Install now:

```bash
pip install sota-agent-framework[optimization]
```

