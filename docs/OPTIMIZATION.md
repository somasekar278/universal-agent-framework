# Prompt Optimization Guide

**SOTA Agent Framework** includes advanced prompt optimization using **DSPy** and **TextGrad**. This guide shows you how to optimize your agent prompts for maximum performance.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [DSPy Optimizer (Task Prompts)](#dspy-optimizer-task-prompts)
- [TextGrad Optimizer (System Prompts)](#textgrad-optimizer-system-prompts)
- [Unified Optimizer](#unified-optimizer)
- [Optimization Pipelines](#optimization-pipelines)
- [A/B Testing Framework](#ab-testing-framework)
- [Unity Catalog Integration](#unity-catalog-integration)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Examples](#examples)

---

## Overview

The optimization module provides:

### 🎯 **DSPy Integration**
- **Task prompt optimization** through few-shot learning
- Chain-of-thought optimization
- Signature optimization
- Multi-metric evaluation

### 🎓 **TextGrad Integration**
- **System prompt optimization** through gradient descent
- Automatic differentiation of text
- Multi-objective optimization
- Iterative refinement

### 🔄 **Unified Optimizer**
- Automatic method selection
- Multi-stage optimization
- Unity Catalog versioning
- Result tracking

### 🧪 **A/B Testing**
- Statistical comparison
- Confidence intervals
- Automated winner selection
- Performance tracking

---

## Quick Start

### Installation

```bash
# Install with optimization support
pip install sota-agent-framework[optimization]

# Or install all features
pip install sota-agent-framework[all]
```

### Basic Usage

```python
from optimization import DSPyOptimizer, TextGradOptimizer

# Optimize task prompt with DSPy
dspy_optimizer = DSPyOptimizer()

training_data = [
    {"input": "Transaction $1000 from Nigeria", "output": "fraud"},
    {"input": "Regular grocery purchase", "output": "legitimate"},
]

result = await dspy_optimizer.optimize(
    task="fraud_detection",
    training_data=training_data
)

print(f"Improvement: {result.improvement:.2%}")
print(result.optimized_prompt)

# Optimize system prompt with TextGrad
textgrad_optimizer = TextGradOptimizer()

system_prompt = "You are a fraud detection expert."
eval_data = [
    {"input": "...", "expected": "..."},
]

result = await textgrad_optimizer.optimize(
    system_prompt=system_prompt,
    evaluation_data=eval_data,
    objective="Maximize accuracy while being concise"
)

print(f"Optimized: {result.optimized_prompt}")
```

---

## DSPy Optimizer (Task Prompts)

DSPy optimizes **task-specific prompts** through few-shot learning and chain-of-thought optimization.

### Usage

```python
from optimization import DSPyOptimizer, DSPyConfig

# Custom configuration
config = DSPyConfig(
    metric="accuracy",
    num_threads=4,
    max_bootstrapped_demos=4,
    max_labeled_demos=8,
    teacher_model="gpt-4",
    student_model="gpt-3.5-turbo",
    temperature=0.7,
    max_iterations=10
)

optimizer = DSPyOptimizer(config=config)

# Define training data
training_data = [
    {
        "input": "Analyze transaction: $5000 wire transfer to offshore account",
        "output": "HIGH_RISK: Large transfer to high-risk jurisdiction"
    },
    {
        "input": "Analyze transaction: $50 coffee shop purchase",
        "output": "LOW_RISK: Normal retail transaction"
    },
    # ... more examples
]

# Custom evaluation metric
def custom_metric(example, prediction):
    # Return 0.0 to 1.0 score
    if prediction.output == example.output:
        return 1.0
    elif prediction.output.split(":")[0] == example.output.split(":")[0]:
        return 0.5
    else:
        return 0.0

# Optimize
result = await optimizer.optimize(
    task="fraud_detection",
    training_data=training_data,
    metric=custom_metric,
    dev_data=validation_data  # Optional
)

# Use optimized prompt
print(f"Original Score: {result.original_score:.3f}")
print(f"Optimized Score: {result.optimized_score:.3f}")
print(f"Improvement: {result.improvement:.2%}")
print(f"\nOptimized Prompt:\n{result.optimized_prompt}")
print(f"\nBest Examples: {len(result.best_examples)}")

# Save compiled program
optimizer.save_optimization("fraud_detection", "fraud_detector_optimized.pkl")

# Load later
optimizer.load_optimization("fraud_detection", "fraud_detector_optimized.pkl")
```

### DSPy Configuration (YAML)

```yaml
optimization:
  dspy:
    metric: "accuracy"
    num_threads: 4
    max_bootstrapped_demos: 4
    max_labeled_demos: 8
    teacher_model: "gpt-4"
    student_model: "gpt-3.5-turbo"
    temperature: 0.7
    max_iterations: 10
```

### How DSPy Works

1. **Signature Creation**: Analyzes your training data to create a signature
2. **Few-Shot Selection**: Selects best examples using BootstrapFewShot
3. **Chain-of-Thought**: Adds reasoning steps
4. **Compilation**: Optimizes the entire prompt pipeline
5. **Evaluation**: Validates on development data

---

## TextGrad Optimizer (System Prompts)

TextGrad optimizes **system prompts** using gradient-based text optimization.

### Usage

```python
from optimization import TextGradOptimizer, TextGradConfig

# Custom configuration
config = TextGradConfig(
    max_iterations=20,
    learning_rate=0.1,
    optimizer_model="gpt-4",
    evaluation_model="gpt-4",
    batch_size=4,
    early_stopping_patience=3,
    target_metric="quality"
)

optimizer = TextGradOptimizer(config=config)

# Define system prompt
system_prompt = """
You are a fraud detection expert.
Analyze transactions carefully.
"""

# Define evaluation data
eval_data = [
    {
        "input": "Large wire transfer to unknown recipient",
        "expected": "Flag as high risk with detailed reasoning"
    },
    # ... more examples
]

# Optimize
result = await optimizer.optimize(
    system_prompt=system_prompt,
    evaluation_data=eval_data,
    objective="Maximize detection accuracy while minimizing false positives",
    constraints=[
        "Keep prompt under 300 words",
        "Use professional language",
        "Include step-by-step instructions"
    ]
)

# View results
print(f"Original:\n{result.original_prompt}")
print(f"\nOptimized:\n{result.optimized_prompt}")
print(f"\nImprovement: {result.improvement:.2%}")

# View optimization history
for step in result.optimization_history:
    print(f"Iteration {step['iteration']}: Score = {step['score']:.3f}")
```

### TextGrad Configuration (YAML)

```yaml
optimization:
  textgrad:
    max_iterations: 20
    learning_rate: 0.1
    optimizer_model: "gpt-4"
    evaluation_model: "gpt-4"
    batch_size: 4
    early_stopping_patience: 3
    target_metric: "quality"
```

### How TextGrad Works

1. **Variable Creation**: Treats system prompt as differentiable variable
2. **Gradient Computation**: Computes "gradients" for text
3. **Iterative Update**: Applies gradient descent to improve prompt
4. **Early Stopping**: Stops when no improvement for N iterations
5. **Best Selection**: Returns best prompt from all iterations

---

## Unified Optimizer

The **PromptOptimizer** automatically selects the right method based on prompt type.

### Usage

```python
from optimization import PromptOptimizer

optimizer = PromptOptimizer()

# Optimize system prompt (uses TextGrad)
system_result = await optimizer.optimize(
    prompt="You are a helpful assistant.",
    prompt_type="system",
    evaluation_data=eval_data,
    objective="Be concise and accurate"
)

# Optimize task prompt (uses DSPy)
task_result = await optimizer.optimize(
    prompt="Classify the transaction",
    prompt_type="task",
    training_data=train_data,
    task="fraud_detection"
)

# Get optimization history
history = optimizer.get_history()

# Get best candidate
best_system = optimizer.get_best_candidate("system")
best_task = optimizer.get_best_candidate("task")
```

### Unity Catalog Auto-Save

Results are automatically saved to Unity Catalog:

```python
# Results are saved to UC Volume:
# /Volumes/main/sota_agents/prompts/optimized_system_20250630_143022.json
# /Volumes/main/sota_agents/prompts/optimized_task_20250630_143022.json
```

---

## Optimization Pipelines

Run multi-stage optimization pipelines:

### Usage

```python
from optimization import OptimizationPipeline

pipeline = OptimizationPipeline()

# Agent configuration
agent_config = {
    "name": "fraud_detector",
    "system_prompt": "You are a fraud detection expert.",
    "task_prompt": "Classify the transaction as fraud or legitimate."
}

# Run full pipeline
result = await pipeline.run(
    agent_config=agent_config,
    training_data=train_data,
    evaluation_data=eval_data,
    stages=["system", "task", "test"]  # Optional: specify stages
)

# View results
print(f"Original Config: {result['original_config']}")
print(f"Optimized Config: {result['optimized_config']}")

print(f"\nSystem Prompt Improvement: {result['stages']['system']['improvement']:.2%}")
print(f"Task Prompt Improvement: {result['stages']['task']['improvement']:.2%}")
print(f"\nA/B Test Winner: {result['stages']['ab_test']['winner']}")
```

### Pipeline Stages

1. **System Prompt Optimization** (TextGrad)
   - Optimizes system-level instructions
   - Focuses on agent behavior

2. **Task Prompt Optimization** (DSPy)
   - Optimizes task-specific prompts
   - Selects best few-shot examples

3. **A/B Testing**
   - Compares original vs optimized
   - Statistical validation

---

## A/B Testing Framework

Test prompt variants statistically:

### Usage

```python
from optimization import ABTestFramework

framework = ABTestFramework(significance_level=0.05)

# Define variants
variants = [
    {
        "name": "baseline",
        "config": {
            "system_prompt": "You are a helpful assistant."
        }
    },
    {
        "name": "expert_v1",
        "config": {
            "system_prompt": "You are an expert fraud detection specialist."
        }
    },
    {
        "name": "expert_v2",
        "config": {
            "system_prompt": "You are an expert fraud analyst with 10+ years experience."
        }
    }
]

# Run test
result = await framework.run_test(
    variants=variants,
    test_data=test_cases,
    metric="accuracy"
)

# View results
print(f"Winner: {result.winner}")
print(f"Confidence: {result.confidence:.2%}")
print(f"Statistically Significant: {result.statistical_significance}")

# View variant performance
for variant in result.variants:
    print(f"{variant.name}:")
    print(f"  Average Score: {variant.average_score:.3f}")
    print(f"  Success Rate: {variant.success_rate:.2%}")
    print(f"  Trials: {variant.trials}")

# Compare two variants
comparison = framework.compare_variants("baseline", "expert_v1")
print(f"Winner: {comparison['winner']}")

# Export results
results_json = framework.export_results()
```

### Statistical Methods

- **Success Rate**: Percentage of trials meeting threshold
- **Average Score**: Mean score across all trials
- **Statistical Significance**: Z-test with p < 0.05
- **Confidence**: Based on score difference and variance

---

## Unity Catalog Integration

Optimized prompts are automatically versioned in Unity Catalog:

### Automatic Registration

```python
# Optimization results are automatically saved to UC
result = await optimizer.optimize(...)

# Saved to:
# /Volumes/main/sota_agents/prompts/optimized_task_YYYYMMDD_HHMMSS.json
```

### Manual Registration

```python
from uc_registry import PromptRegistry

registry = PromptRegistry()

# Register optimized prompt
registry.register_prompt(
    name="fraud_detector_v2",
    content=result.optimized_prompt,
    metadata={
        "optimization_method": "dspy",
        "improvement": result.improvement,
        "original_score": result.original_score,
        "optimized_score": result.optimized_score,
        "date": "2025-06-30"
    }
)

# Retrieve later
prompt = registry.get_prompt("fraud_detector_v2")
```

---

## Configuration

### Full YAML Configuration

```yaml
optimization:
  # DSPy for task prompts
  dspy:
    metric: "accuracy"
    num_threads: 4
    max_bootstrapped_demos: 4
    max_labeled_demos: 8
    teacher_model: "gpt-4"
    student_model: "gpt-3.5-turbo"
    temperature: 0.7
    max_iterations: 10
  
  # TextGrad for system prompts
  textgrad:
    max_iterations: 20
    learning_rate: 0.1
    optimizer_model: "gpt-4"
    evaluation_model: "gpt-4"
    batch_size: 4
    early_stopping_patience: 3
    target_metric: "quality"
  
  # A/B Testing
  ab_testing:
    significance_level: 0.05
    min_trials: 20
    confidence_threshold: 0.95
```

---

## Best Practices

### 1. **Prepare Quality Training Data**
```python
# Good: Diverse, representative examples
training_data = [
    {"input": "Small local purchase", "output": "legitimate"},
    {"input": "Large international transfer", "output": "review"},
    {"input": "Multiple rapid transactions", "output": "fraud"},
    {"input": "Merchant payment", "output": "legitimate"},
]

# Bad: Repetitive, non-representative
training_data = [
    {"input": "Test 1", "output": "yes"},
    {"input": "Test 2", "output": "no"},
]
```

### 2. **Use Appropriate Metrics**
```python
# Custom metric for fraud detection
def fraud_metric(example, prediction):
    # High penalty for false negatives (missing fraud)
    if example.output == "fraud" and prediction.output != "fraud":
        return 0.0
    # Medium penalty for false positives
    elif example.output != "fraud" and prediction.output == "fraud":
        return 0.3
    # Full credit for correct classification
    else:
        return 1.0
```

### 3. **Iterate and Refine**
```python
# Run multiple optimization cycles
for iteration in range(3):
    result = await optimizer.optimize(
        task=f"fraud_detection_v{iteration}",
        training_data=train_data
    )
    
    # Use result to improve training data
    train_data = improve_data_based_on_result(result)
```

### 4. **A/B Test Before Deployment**
```python
# Always validate before production
result = await ab_framework.run_test(
    variants=[
        {"name": "current_production", "config": prod_config},
        {"name": "optimized", "config": optimized_config}
    ],
    test_data=holdout_test_set
)

if result.confidence > 0.95 and result.statistical_significance:
    deploy(optimized_config)
```

### 5. **Monitor in Production**
```python
# Track performance over time
from telemetry import AgentTracer

tracer = AgentTracer()

with tracer.trace_agent_execution():
    result = agent.execute(input_data)
    
    # Log prompt performance
    tracer.log_metric("prompt_score", result.score)
```

---

## Examples

### Example 1: Fraud Detection Optimization

```python
from optimization import OptimizationPipeline

# Define agent
agent_config = {
    "name": "fraud_detector",
    "system_prompt": "You are a fraud analyst.",
    "task_prompt": "Classify: {transaction}"
}

# Training data
train_data = [
    {
        "input": "Wire $10K to Nigeria",
        "output": "FRAUD: High-risk jurisdiction, large amount"
    },
    {
        "input": "Grocery store $45",
        "output": "LEGITIMATE: Normal retail transaction"
    },
    # ... 20+ more examples
]

# Evaluation data
eval_data = [
    {
        "input": "ATM withdrawal $500",
        "expected": "LEGITIMATE: Normal withdrawal amount"
    },
    # ... 10+ more examples
]

# Run pipeline
pipeline = OptimizationPipeline()
result = await pipeline.run(
    agent_config=agent_config,
    training_data=train_data,
    evaluation_data=eval_data
)

print(f"System improvement: {result['stages']['system']['improvement']:.2%}")
print(f"Task improvement: {result['stages']['task']['improvement']:.2%}")
```

### Example 2: Customer Support Optimization

```python
from optimization import PromptOptimizer

optimizer = PromptOptimizer()

# Current system prompt
current_prompt = "You are a customer support agent. Be helpful."

# Evaluation data
eval_data = [
    {
        "input": "My order hasn't arrived",
        "expected": "Empathetic response with tracking info"
    },
    # ... more examples
]

# Optimize
result = await optimizer.optimize(
    prompt=current_prompt,
    prompt_type="system",
    evaluation_data=eval_data,
    objective="Maximize customer satisfaction while being efficient"
)

print(f"Original: {result.original_prompt}")
print(f"Optimized: {result.optimized_prompt}")
print(f"Improvement: {result.improvement:.2%}")
```

### Example 3: Multi-Variant Testing

```python
from optimization import ABTestFramework

framework = ABTestFramework()

# Test multiple system prompt variations
variants = [
    {
        "name": "baseline",
        "config": {"system_prompt": "You help customers."}
    },
    {
        "name": "empathetic",
        "config": {"system_prompt": "You are a caring support specialist who empathizes with customers."}
    },
    {
        "name": "efficient",
        "config": {"system_prompt": "You are an efficient support agent who resolves issues quickly."}
    },
    {
        "name": "expert",
        "config": {"system_prompt": "You are a senior support engineer with deep product knowledge."}
    }
]

# Run test
result = await framework.run_test(
    variants=variants,
    test_data=test_cases
)

# Results
print(f"Winner: {result.winner}")
print(f"Confidence: {result.confidence:.2%}")

for variant in result.variants:
    print(f"{variant.name}: {variant.average_score:.3f}")
```

---

## Next Steps

- 📚 **[Configuration Guide](CONFIGURATION.md)** - Full YAML configuration
- 🔍 **[Benchmarking](BENCHMARKING.md)** - Evaluate optimized prompts
- 🧠 **[Memory System](MEMORY_SYSTEM.md)** - Store optimization results
- 📊 **[Visualization](VISUALIZATION.md)** - View optimization progress

---

**Ready to optimize!** 🚀

