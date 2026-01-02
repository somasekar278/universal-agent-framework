# Advanced Features Guide

**All advanced features in one place**: Memory, Reasoning, Optimization, Benchmarking

---

## 📋 Table of Contents

- [Agent-Governed Memory](#agent-governed-memory)
- [Reasoning Optimization](#reasoning-optimization)
- [Prompt Optimization](#prompt-optimization)
- [Agent Benchmarking](#agent-benchmarking)

---

## 🧠 Agent-Governed Memory

**Purpose**: Intelligent memory where agents decide what to store, retrieve, and forget

### Quick Start

```python
from memory import MemoryManager, MemoryType, MemoryImportance

# Initialize
memory = MemoryManager()

# Store (agent decides importance)
await memory.store(
    content="Important transaction detected",
    memory_type=MemoryType.EPISODIC,
    importance=MemoryImportance.HIGH
)

# Retrieve
results = await memory.retrieve(query="recent fraud cases", top_k=5)

# Reflect
reflections = await memory.reflect(timeframe="last_week")
```

### Features

#### **5 Memory Types**
1. **Short-term** - Recent interactions (last 100 items)
2. **Long-term** - Persistent storage (Unity Catalog)
3. **Episodic** - Specific events
4. **Semantic** - Conceptual knowledge
5. **Procedural** - How-to knowledge

#### **Retrieval Strategies**
- **Semantic** - Find by meaning
- **Recency** - Most recent first
- **Importance** - Highest priority first
- **Hybrid** - Combined approach

#### **Agent-Governed**
- **Storage Agent** - Decides what to remember
- **Reflection Agent** - Summarizes memories
- **Forget Agent** - Decides what to forget

### Configuration

```yaml
memory:
  enabled: true
  short_term_capacity: 100
  agent_governed: true
  semantic_embeddings:
    provider: "sentence-transformers"  # or openai, databricks
```

### When to Use

- ✅ Context-aware assistants
- ✅ Conversation agents
- ✅ Agents that learn from history
- ❌ Stateless APIs
- ❌ Simple chatbots

**Full Documentation**: See `docs/MEMORY_SYSTEM.md` (archived)

---

## 🎯 Reasoning Optimization

**Purpose**: Optimize how agents think and make decisions

### Quick Start

```python
from reasoning import ReasoningOptimizer, TrajectoryOptimizer

# Initialize
optimizer = ReasoningOptimizer(agent)

# Optimize execution
result = await optimizer.optimize(input_data)

# Learn from execution
await optimizer.learn_from_execution(
    trajectory=execution_path,
    reasoning_chain=agent_reasoning,
    reward=0.85
)
```

### Features

#### **1. Trajectory Optimization**
Learn optimal action sequences from past executions

```python
from reasoning import TrajectoryOptimizer

optimizer = TrajectoryOptimizer()

# Record trajectory
trajectory = optimizer.record(agent_execution)

# Analyze inefficiencies
analysis = optimizer.analyze(trajectory)

# Get suggestions
suggestions = optimizer.suggest_improvements(trajectory)
```

#### **2. Chain-of-Thought Distillation**
Compress reasoning chains (50%+ token savings)

```python
from reasoning import CoTDistiller

distiller = CoTDistiller()

# Distill reasoning
compressed = await distiller.distill(
    reasoning_chain=long_reasoning,
    method="extractive"  # or abstractive, neural
)
```

#### **3. Feedback Loops**
Self-improvement through critique → revise → retry

```python
from reasoning import FeedbackLoop

feedback = FeedbackLoop(agent)

# Automatic improvement
result = await feedback.improve_with_feedback(
    input_data=task,
    max_iterations=3
)
```

#### **4. Policy Constraints**
Enforce safety, cost, and latency guardrails

```python
from reasoning import PolicyEngine

policy = PolicyEngine()
policy.add_constraint("max_cost", 0.50)  # $0.50 per execution
policy.add_constraint("max_latency", 2000)  # 2 seconds

# Enforced automatically
result = await agent.execute_with_policy(input_data, policy)
```

### Configuration

```yaml
reasoning:
  enabled: true
  trajectory_optimization: true
  cot_distillation:
    enabled: true
    method: "extractive"
  feedback_loops:
    enabled: true
    max_iterations: 3
  policies:
    max_cost_per_execution: 0.50
    max_latency_ms: 2000
```

### When to Use

- ✅ Autonomous agents
- ✅ Complex decision-making
- ✅ Agents that need to improve
- ❌ Simple Q&A
- ❌ Stateless APIs

**Full Documentation**: See `docs/REASONING_OPTIMIZATION.md` (archived)

---

## 🎓 Prompt Optimization

**Purpose**: Automatically improve prompts using DSPy and TextGrad

### Quick Start

```python
from optimization import PromptOptimizer

optimizer = PromptOptimizer()

# Optimize system prompt (TextGrad)
result = await optimizer.optimize(
    prompt="You are a fraud detection expert.",
    prompt_type="system",
    evaluation_data=eval_data
)

# Optimize task prompt (DSPy)
result = await optimizer.optimize(
    prompt="Classify the transaction",
    prompt_type="task",
    training_data=train_data
)
```

### Features

#### **1. DSPy (Task Prompts)**
Few-shot learning and chain-of-thought optimization

```python
from optimization import DSPyOptimizer

optimizer = DSPyOptimizer()

result = await optimizer.optimize(
    task="fraud_detection",
    training_data=examples,
    metric=custom_metric
)
```

#### **2. TextGrad (System Prompts)**
Gradient-based prompt refinement

```python
from optimization import TextGradOptimizer

optimizer = TextGradOptimizer()

result = await optimizer.optimize(
    system_prompt=current_prompt,
    evaluation_data=eval_data,
    objective="Maximize accuracy while being concise"
)
```

#### **3. A/B Testing**
Statistical comparison of prompt variants

```python
from optimization import ABTestFramework

framework = ABTestFramework()

result = await framework.run_test(
    variants=[baseline, optimized],
    test_data=test_cases
)
```

#### **4. Multi-Stage Pipelines**
System → Task → A/B Test

```python
from optimization import OptimizationPipeline

pipeline = OptimizationPipeline()

result = await pipeline.run(
    agent_config=agent_config,
    training_data=train_data,
    evaluation_data=eval_data
)
```

### Configuration

```yaml
optimization:
  dspy:
    enabled: true
    teacher_model: "gpt-4"
    max_iterations: 10
  textgrad:
    enabled: true
    max_iterations: 20
    learning_rate: 0.1
```

### When to Use

- ✅ Frequent prompt iterations
- ✅ Performance optimization
- ✅ A/B testing prompts
- ❌ One-off agents
- ❌ Stable prompts

**Full Documentation**: See `docs/OPTIMIZATION.md` (archived)

---

## 📊 Agent Benchmarking

**Purpose**: Track agent performance over time with comprehensive metrics

### Quick Start

```bash
# Install with benchmarking
pip install sota-agent-framework[dev]

# Run benchmarks
agent-benchmark run --suite fraud_detection --report md

# View leaderboard
cat benchmark_results/leaderboard.md
```

### Features

#### **6 Core Metrics**

1. **Tool Call Success Rate** - How often tools work
2. **Plan Correctness** - Quality of plans
3. **Hallucination Rate** - Factual accuracy
4. **Latency** - Response time
5. **Coherence** - Output quality
6. **Domain Accuracy** - Domain-specific correctness

#### **Evaluation Harness**

```python
from evaluation import EvaluationHarness, ToolCallMetric

# Create harness
harness = EvaluationHarness()
harness.add_metric(ToolCallMetric())

# Run evaluation
results = await harness.evaluate(
    agent=my_agent,
    test_suite=test_cases
)
```

#### **Benchmark Suites**

```yaml
# benchmarks/fraud_detection.yaml
name: "Fraud Detection Suite"
agents:
  - fraud_detector
  - risk_analyzer

test_cases:
  - input: "Large wire transfer"
    expected_action: "FLAG_HIGH_RISK"
    expected_tools: ["sanctions_check", "velocity_check"]

metrics:
  - tool_call_success
  - plan_correctness
  - latency
```

#### **Report Formats**

- **Markdown** - Human-readable
- **JSON** - Machine-readable
- **HTML** - Interactive
- **Leaderboard** - Agent rankings

### Configuration

```yaml
benchmarking:
  enabled: true
  output_dir: "benchmark_results"
  metrics:
    - tool_call_success
    - plan_correctness
    - hallucination_rate
    - latency
    - coherence
    - domain_accuracy
```

### When to Use

- ✅ Production agents
- ✅ Tracking performance
- ✅ Preventing regressions
- ✅ Comparing agents
- ❌ Early prototypes

**Full Documentation**: See `docs/BENCHMARKING.md` (archived)

---

## 📦 Installation Matrix

| Feature | Install Command | When Needed |
|---------|----------------|-------------|
| **Memory** | Included in base | Context-aware agents |
| **Reasoning** | Included in base | Autonomous decisions |
| **Optimization** | `[optimization]` | Prompt tuning |
| **Benchmarking** | `[dev]` | Performance tracking |
| **All** | `[all]` | Full framework |

---

## 🎯 Feature Selection by Use Case

| Use Case | Memory | Reasoning | Optimization | Benchmarking |
|----------|--------|-----------|--------------|--------------|
| **Simple Chatbot** | ⚪ Optional | ❌ No | ❌ No | ❌ No |
| **Context Agent** | ✅ Yes | ⚪ Optional | ⚪ Optional | ⚪ Optional |
| **Complex Workflows** | ✅ Yes | ✅ Yes | ⚪ Optional | ✅ Yes |
| **Autonomous Agent** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Production API** | ⚪ Optional | ❌ No | ⚪ Optional | ✅ Yes |

---

## 📚 Additional Resources

- **Memory**: `docs/MEMORY_SYSTEM.md` (archived)
- **Reasoning**: `docs/REASONING_OPTIMIZATION.md` (archived)
- **Optimization**: `docs/OPTIMIZATION.md` (archived)
- **Benchmarking**: `docs/BENCHMARKING.md` (archived)
- **Examples**: See `examples/` directory
- **Tests**: See `tests/` directory

---

**All features are optional - enable based on your needs!** 🎯

**See [FEATURE_SELECTION.md](FEATURE_SELECTION.md) for use-case specific guidance**

