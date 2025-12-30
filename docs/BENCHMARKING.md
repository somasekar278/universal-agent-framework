

# Agent Benchmarking & Evaluation Guide

Comprehensive evaluation suite for testing agent quality, performance, and reliability.

## Overview

The SOTA Agent Framework includes a **production-grade benchmarking system** that provides:

- ✅ **Automated Testing** - Run comprehensive test suites against agents
- 📊 **Multi-Metric Evaluation** - Tool calls, planning, hallucination, latency, coherence, accuracy
- 🏆 **Leaderboards** - Auto-generated rankings comparing agents
- 📈 **Multiple Report Formats** - Markdown, JSON, HTML
- 🔄 **Regression Testing** - Detect performance degradation
- ⚡ **Parallel Execution** - Fast evaluation with concurrent testing

---

## Quick Start

### 1. Install with Benchmarking Support

```bash
pip install sota-agent-framework[dev]
```

### 2. Run Your First Benchmark

```bash
sota-benchmark run --suite fraud --agents all --report md
```

### 3. View Results

Results are saved to `benchmark_results/`:
- `benchmark_report.md` - Full report
- `leaderboard.md` - Agent rankings
- `benchmark_results.json` - Raw data

---

## CLI Commands

### Run Benchmarks

```bash
sota-benchmark run [OPTIONS]
```

**Options:**
- `--suite <name>` - Suite(s) to run (default: all)
- `--agents <name>` - Agent(s) to evaluate (default: all)
- `--metrics <list>` - Metrics to use (comma-separated)
- `--parallel` - Run tests in parallel
- `--max-workers N` - Max parallel workers (default: 4)
- `--output-dir <path>` - Output directory (default: benchmark_results)
- `--report <formats>` - Report formats: md,json,html (default: md)
- `--no-leaderboard` - Skip leaderboard generation
- `--benchmark-dir <path>` - Benchmark suite directory (default: benchmarks)
- `--agents-dir <path>` - Agent modules directory (default: benchmark_agents)

**Examples:**

```bash
# Run all benchmarks
sota-benchmark run --suite all --agents all

# Test specific agent
sota-benchmark run --suite fraud --agents myagent

# Parallel execution with all report formats
sota-benchmark run --suite all --agents all --parallel --report md,json,html

# Custom metrics
sota-benchmark run --suite fraud --agents all --metrics tool_call_success,accuracy,latency
```

### Create Benchmark Suite

```bash
sota-benchmark create --suite <name> [OPTIONS]
```

**Options:**
- `--suite <name>` - Suite name (required)
- `--output <path>` - Output directory (default: benchmarks)
- `--num-tests N` - Number of test cases (default: 5)

**Example:**

```bash
sota-benchmark create --suite customer_support --num-tests 10
```

### List Suites and Agents

```bash
sota-benchmark list [OPTIONS]
```

**Example:**

```bash
sota-benchmark list
```

---

## Evaluation Metrics

The framework includes 6 core metrics:

### 1. Tool Call Success Rate

Evaluates tool usage quality:
- ✅ Correct tool selection
- ✅ Valid tool arguments
- ✅ Tool call ordering
- ✅ Success rate

**Threshold:** 0.9 (90%)

**Example:**
```python
from evaluation.metrics import ToolCallMetric

metric = ToolCallMetric(threshold=0.9)
result = await metric.evaluate(agent_output, expected_output, context)
print(f"Score: {result.score}, Passed: {result.passed}")
```

### 2. Plan Correctness

Evaluates planning quality:
- ✅ Required steps present
- ✅ Correct ordering
- ✅ Dependency satisfaction
- ✅ Plan completeness

**Threshold:** 0.8 (80%)

### 3. Hallucination Rate

Detects fabricated information:
- ❌ Made-up tool names
- ❌ Invalid data
- ❌ Incorrect references
- ❌ Missing required fields

**Threshold:** 0.9 (90% accuracy)

### 4. Latency

Compares execution time against budget:
- ⚡ Within budget: score = 1.0
- ⚡ Over budget: penalty applied

**Threshold:** 0.8 (80%)
**Default Budget:** 1000ms

### 5. Coherence

Evaluates output coherence:
- ✅ Logical consistency
- ✅ Completeness
- ✅ Relevance to input

**Threshold:** 0.7 (70%)

### 6. Accuracy

Compares against ground truth:
- ✅ Correct classification
- ✅ Accurate values
- ✅ Domain-specific correctness

**Threshold:** 0.8 (80%)

---

## Creating Benchmark Suites

### Suite Structure

Benchmark suites are YAML files in the `benchmarks/` directory:

```yaml
name: fraud_detection
description: Benchmark suite for fraud detection agents

default_metrics:
  - tool_call_success
  - plan_correctness
  - hallucination_rate
  - latency
  - coherence
  - accuracy

metadata:
  domain: fraud_detection
  version: "1.0"

test_cases:
  - id: fraud_001
    name: High-risk transaction detection
    input:
      transaction_id: "TXN_12345"
      amount: 5000.00
      merchant: "Electronics Store XYZ"
    expected:
      ground_truth:
        is_fraud: true
        risk_score: 0.85
      expected_tools:
        - tool: "analyze_transaction_pattern"
        - tool: "check_merchant_reputation"
      latency_budget_ms: 500
      required_fields:
        - is_fraud
        - risk_score
    metrics:
      - tool_call_success
      - accuracy
      - latency
    tags:
      - high_priority
      - critical
```

### Test Case Fields

**Input:**
- Any data your agent needs

**Expected Output:**
- `ground_truth` - Correct answer
- `expected_tools` - Tools agent should call
- `expected_plan` - Required planning steps
- `latency_budget_ms` - Max acceptable latency
- `required_fields` - Fields that must be present
- `numeric_ranges` - Valid ranges for numeric values
- `structure` - Expected output structure

**Metrics:**
- List of metrics to evaluate

**Tags:**
- For filtering and organization

---

## Creating Benchmark Agents

Agents can be either **function-based** or **class-based**.

### Function-Based Agent

Create `benchmark_agents/myagent.py`:

```python
async def evaluate(input_data: dict) -> dict:
    """
    Evaluate the input and return results.
    
    Args:
        input_data: Test case input
        
    Returns:
        Agent's output
    """
    # Your agent logic here
    result = {
        "is_fraud": True,
        "risk_score": 0.85,
        "reasons": ["High amount"]
    }
    
    # Include metadata for tool call tracking
    result["metadata"] = {
        "tool_calls": [
            {"tool": "analyze_transaction_pattern"}
        ]
    }
    
    return result
```

### Class-Based Agent

```python
class Agent:
    """Agent class."""
    
    async def process(self, input_data: dict) -> dict:
        """Process input and return result."""
        # Your agent logic
        return {"result": "..."}
```

### Integrating SOTA Framework Agents

```python
from agents.base import EnrichmentAgent
from shared.schemas.agent_schemas import AgentInput, AgentOutput

class MyBenchmarkAgent(EnrichmentAgent):
    async def process_internal(self, input_data: AgentInput) -> AgentOutput:
        # Your logic
        pass

# Wrapper for benchmarking
async def evaluate(input_data: dict) -> dict:
    agent = MyBenchmarkAgent(
        agent_id="benchmark_agent",
        agent_name="My Agent"
    )
    
    agent_input = AgentInput(
        request_id="bench_001",
        data=input_data
    )
    
    result = await agent.process(agent_input)
    return result.result
```

---

## Interpreting Results

### Markdown Report

The markdown report includes:

1. **Summary** - Pass rates, avg scores, avg latency per agent
2. **Detailed Results** - Per test case breakdown
3. **Metric Breakdown** - Aggregated metric scores

Example:

```markdown
## Agent: fraud_detector

**Pass Rate:** 80.0% (4/5)
**Average Score:** 0.782
**Average Latency:** 234.5ms

### Detailed Results

| Test Case | Status | Score | Latency (ms) | Metrics |
|-----------|--------|-------|--------------|---------|
| fraud_001 | ✅ PASS | 0.850 | 245.2 | tool_call:✓, accuracy:✓ |
| fraud_002 | ✅ PASS | 0.920 | 189.3 | accuracy:✓, latency:✓ |
```

### Leaderboard

Auto-generated rankings:

```markdown
# 🏆 Agent Leaderboard

| Rank | Agent | Composite Score | Avg Score | Pass Rate | Avg Latency |
|------|-------|-----------------|-----------|-----------|-------------|
| 🥇 1 | agent_v2 | 0.856 | 0.883 | 95.0% | 234.5ms |
| 🥈 2 | agent_v1 | 0.742 | 0.782 | 80.0% | 456.2ms |
```

**Composite Score Formula:**
- 70% Accuracy (avg score)
- 20% Pass Rate
- 10% Speed (normalized to 5000ms)

### JSON Report

Machine-readable format for integration:

```json
{
  "generated_at": "2025-12-30T10:30:00",
  "agents": {
    "fraud_detector": {
      "total_tests": 5,
      "passed": 4,
      "failed": 1,
      "average_score": 0.782,
      "average_latency_ms": 234.5,
      "results": [...]
    }
  }
}
```

---

## Advanced Usage

### Custom Metrics

Create your own metrics:

```python
from evaluation.metrics import Metric, MetricResult

class DomainSpecificMetric(Metric):
    def __init__(self):
        super().__init__("domain_specific", threshold=0.75)
    
    async def evaluate(self, agent_output, expected_output, context):
        # Your evaluation logic
        score = self._calculate_score(agent_output)
        
        return MetricResult(
            metric_name=self.name,
            score=score,
            passed=score >= self.threshold,
            threshold=self.threshold,
            details={"custom_info": "..."}
        )
```

### Programmatic Evaluation

```python
from evaluation.runner import BenchmarkRunner, BenchmarkConfig
from pathlib import Path

# Configure
config = BenchmarkConfig(
    suite_names=["fraud_detection"],
    agent_names=["myagent"],
    parallel=True,
    output_dir=Path("my_results")
)

# Run
runner = BenchmarkRunner(config)
results = await runner.run()

# Analyze
for agent_name, agent_results in results.items():
    avg_score = sum(r.overall_score for r in agent_results) / len(agent_results)
    print(f"{agent_name}: {avg_score:.3f}")
```

### Filtering Test Cases

Add filters to run specific tests:

```python
config = BenchmarkConfig(
    suite_names=["fraud_detection"],
    filters={
        "tags": ["critical"],
        "metadata": {"severity": "high"}
    }
)
```

### MLflow Integration

Track benchmarks in MLflow:

```python
import mlflow

with mlflow.start_run(run_name="agent_benchmark"):
    runner = BenchmarkRunner(config)
    results = await runner.run()
    
    # Log metrics
    for agent_name, agent_results in results.items():
        avg_score = sum(r.overall_score for r in agent_results) / len(agent_results)
        mlflow.log_metric(f"{agent_name}_score", avg_score)
        
        # Log artifacts
        mlflow.log_artifact("benchmark_results/benchmark_report.md")
```

---

## CI/CD Integration

### GitHub Actions

```yaml
name: Agent Benchmarks

on: [push, pull_request]

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install sota-agent-framework[dev]
      
      - name: Run benchmarks
        run: |
          sota-benchmark run --suite all --agents all --report md,json
      
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: benchmark-results
          path: benchmark_results/
      
      - name: Comment PR with results
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('benchmark_results/leaderboard.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '## Benchmark Results\n\n' + report
            });
```

### Regression Detection

Fail CI if scores drop:

```python
# scripts/check_regression.py
import json
import sys

with open('benchmark_results/benchmark_results.json') as f:
    results = json.load(f)

THRESHOLD = 0.75

for agent, data in results['agents'].items():
    if data['average_score'] < THRESHOLD:
        print(f"❌ {agent} score {data['average_score']} below threshold {THRESHOLD}")
        sys.exit(1)

print("✅ All agents passed regression check")
```

---

## Best Practices

### 1. Comprehensive Test Coverage

- Cover happy paths and edge cases
- Include various difficulty levels
- Test failure modes
- Use realistic data

### 2. Clear Expectations

- Provide precise ground truth
- Specify required tools
- Define acceptable ranges
- Document expected behavior

### 3. Meaningful Metrics

- Choose metrics relevant to your domain
- Set realistic thresholds
- Weight metrics appropriately
- Track trends over time

### 4. Regular Benchmarking

- Run benchmarks on every commit
- Track performance trends
- Compare agent versions
- Detect regressions early

### 5. Iterative Improvement

- Start with simple benchmarks
- Gradually increase complexity
- Add domain-specific metrics
- Refine test cases based on learnings

---

## Example: Complete Workflow

### 1. Create Suite

```bash
sota-benchmark create --suite customer_support --num-tests 10
```

### 2. Customize Test Cases

Edit `benchmarks/customer_support.yaml`:

```yaml
test_cases:
  - id: cs_001
    name: Angry customer escalation
    input:
      customer_message: "This is the WORST service ever!"
      sentiment: "angry"
      history: [...]
    expected:
      ground_truth:
        should_escalate: true
        response_tone: "empathetic"
      expected_tools:
        - tool: "analyze_sentiment"
        - tool: "check_escalation_criteria"
      latency_budget_ms: 800
```

### 3. Create Agent

Create `benchmark_agents/support_agent.py`:

```python
async def evaluate(input_data: dict) -> dict:
    # Your agent logic
    return {
        "should_escalate": True,
        "response_tone": "empathetic",
        "suggested_response": "..."
    }
```

### 4. Run Benchmarks

```bash
sota-benchmark run --suite customer_support --agents support_agent --report md,html
```

### 5. Review Results

Open `benchmark_results/benchmark_report.html` in browser.

### 6. Iterate

- Analyze failures
- Improve agent
- Re-run benchmarks
- Track improvements

---

## Troubleshooting

### No suites found

**Issue:** "No benchmark suites found!"

**Solution:** 
- Ensure `benchmarks/` directory exists
- Check YAML files are valid
- Use `--benchmark-dir` to specify custom location

### No agents found

**Issue:** "No agents found!"

**Solution:**
- Create agent files in `benchmark_agents/`
- Ensure files have `evaluate()` function or `Agent` class
- Use `--agents-dir` to specify custom location

### Import errors

**Issue:** Module import failures

**Solution:**
- Install framework: `pip install sota-agent-framework[dev]`
- Ensure agents can import required modules
- Check PYTHONPATH if using custom structure

### Low scores

**Issue:** Agents scoring poorly

**Solution:**
- Review test case expectations
- Check if thresholds are realistic
- Examine detailed metric results
- Add logging to agent code

---

## Reference

### Directory Structure

```
your_project/
├── benchmarks/              # Benchmark suites (YAML)
│   ├── fraud_detection.yaml
│   └── customer_support.yaml
├── benchmark_agents/        # Agent implementations
│   ├── fraud_detector.py
│   └── support_agent.py
└── benchmark_results/       # Generated reports
    ├── benchmark_report.md
    ├── benchmark_results.json
    ├── benchmark_report.html
    └── leaderboard.md
```

### Metric Thresholds

| Metric | Default Threshold | Recommended |
|--------|------------------|-------------|
| Tool Call Success | 0.9 | 0.85-0.95 |
| Plan Correctness | 0.8 | 0.75-0.90 |
| Hallucination Rate | 0.9 | 0.85-0.95 |
| Latency | 0.8 | 0.70-0.90 |
| Coherence | 0.7 | 0.65-0.80 |
| Accuracy | 0.8 | 0.75-0.95 |

---

## Next Steps

- **Create your first benchmark:** `sota-benchmark create --suite mysuite`
- **Explore examples:** See `benchmarks/fraud_detection.yaml`
- **Add custom metrics:** Extend `Metric` class
- **Integrate with CI/CD:** Add to GitHub Actions
- **Track trends:** Use MLflow or similar

For more information, see:
- [Main Documentation](../README.md)
- [Agent Development Guide](AGENT_DEVELOPMENT.md)
- [MLflow Integration](TELEMETRY_SETUP.md)

