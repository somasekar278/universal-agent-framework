[![PyPI](https://img.shields.io/pypi/v/sota-agent-framework)](https://pypi.org/project/sota-agent-framework/)

# SOTA Agent - Universal Agent Workflow Template

**A generic, production-ready template for integrating AI agents into any application or data pipeline.**

🎯 **This is a TEMPLATE** - Use it to build agent workflows for any domain!

Originally designed for fraud detection, this architecture template applies to **any domain** requiring AI agent integration:
- 🔒 Fraud Detection & Risk Analysis
- 💬 Customer Support & Chatbots
- 📝 Content Moderation & Policy Enforcement
- 🏥 Healthcare & Diagnosis Support
- 🔍 Data Quality & Anomaly Detection
- 📊 Analytics & Report Generation
- 🤖 **Any Agent-Powered Workflow**

## 🚀 Quick Start

### Installation

```bash
# Basic installation
pip install sota-agent-framework

# With optional features
pip install sota-agent-framework[mcp]          # MCP tool calling
pip install sota-agent-framework[ray]          # Distributed execution
pip install sota-agent-framework[databricks]    # Databricks integration
pip install sota-agent-framework[optimization]  # DSPy + TextGrad
pip install sota-agent-framework[monitoring]    # Health checks & metrics
pip install sota-agent-framework[web]          # FastAPI service
pip install sota-agent-framework[all]          # Everything

# Or install from GitHub
pip install git+https://github.com/somasekar278/universal-agent-template.git
```

### Choose Your Path

**👉 Pick based on your experience level:**

#### 🎓 **New to Agents? (Beginner)**

```bash
# Interactive setup with all best practices
pip install sota-agent-framework[all]
sota-setup  # Guided wizard walks you through everything
```

**You get**: Complete project with memory, monitoring, telemetry, experiments - all configured automatically!

#### 🚀 **Some Experience? (Intermediate)**

```bash
# Quick generation with recommended features
sota-generate --domain "your_domain" --output ./your-project
cd your-project

# Get personalized recommendations
sota-advisor .
```

**You get**: Production-ready structure + advisor tells you what's missing for your use case.

#### ⚡ **Expert? (Advanced)**

```bash
# Minimal setup, full control
pip install sota-agent-framework  # Just core
# Use only what you need, override everything else
```

**You get**: Complete freedom. Import à la carte, override any component, access internal APIs.

**📖 See [User Journey Guide](docs/USER_JOURNEY.md) for detailed paths**

---

### 💡 "Do I Need All These Features?"

**NO!** Different use cases need different features. The framework is modular by design.

**Quick Guide:**
- **Simple Chatbot?** → Core + Services only
- **Context-Aware?** → Add Memory
- **Production API?** → Add Monitoring + Telemetry + Experiments
- **Complex Workflows?** → Add LangGraph + Visualization + Reasoning
- **Autonomous Agent?** → Use everything!

**📖 See [Feature Selection Guide](docs/FEATURE_SELECTION_GUIDE.md) for detailed recommendations**

---

### Generate Your First Project (Any Level)

```bash
# Generate a complete project for your domain
sota-generate --domain "your_domain" --output ./your-project

# Navigate and run
cd your-project
python examples/example_usage.py  # Works immediately! ✅
```

### For Contributors/Development

If you're cloning the repo to contribute:

```bash
git clone https://github.com/somasekar278/universal-agent-template.git
cd universal-agent-template
./setup.sh  # or setup.bat on Windows
python template_generator.py --domain "test"
```

### Path 2: Integrate Into Existing Code (3 lines)

```python
from agents import AgentRouter

router = AgentRouter.from_yaml("config/agents.yaml")  # 1. Load
result = await router.route("your_agent", input_data)  # 2. Execute
# That's it! 🎉
```

**📖 See [Getting Started Guide](GETTING_STARTED.md) for detailed 5-minute guide**

## 🧪 Benchmark Your Agents

The framework includes a **production-grade evaluation suite** for comprehensive agent testing:

```bash
# Install with benchmarking support
pip install sota-agent-framework[dev]

# Run benchmarks
sota-benchmark run --suite fraud --agents all --report md

# View auto-generated leaderboard
cat benchmark_results/leaderboard.md
```

**Features:**
- ✅ Multi-metric evaluation (tool calls, planning, hallucination, latency, coherence, accuracy)
- 🏆 Auto-generated leaderboards ranking agents
- 📊 Multiple report formats (Markdown, JSON, HTML)
- 🔄 Regression testing for CI/CD
- ⚡ Parallel execution for fast evaluation

**📖 See [Benchmarking Guide](docs/BENCHMARKING.md) for complete documentation**

## 🧠 Agent-Governed Memory System

Intelligent memory management where **agents decide** what to store, retrieve, and forget:

```python
from memory import MemoryManager, MemoryType, MemoryImportance

# Initialize memory
memory = MemoryManager()

# Agent stores (auto-detects importance and type)
await memory.store(
    content="User prefers dark mode at night",
    importance=MemoryImportance.HIGH
)

# Agent retrieves with semantic search
memories = await memory.retrieve(
    query="What are user preferences?",
    strategy="hybrid"  # semantic + recency + importance
)

# Agent reflects and consolidates
summary = await memory.reflect()

# Agent forgets old data
forgotten = await memory.forget()
```

**Features:**
- 🧠 **5 Memory Types** - Short-term, long-term, episodic, semantic, procedural
- 🔍 **Semantic Search** - Vector embeddings for similarity-based retrieval
- 🤔 **Reflection** - Agents create insights and summaries from memories
- ⏰ **Smart Forgetting** - Time/importance/capacity-based policies
- 🔗 **Memory Graphs** - Track relationships and patterns
- 💬 **Context Budgeting** - Automatic token management for LLMs
- 🤝 **Shared Memory** - Private and shared memory spaces across agents

**📖 See [Memory System Guide](docs/MEMORY_SYSTEM.md) for complete documentation**

## 🎯 Reasoning Optimization

Advanced reasoning optimization for continuously improving agents:

```python
from reasoning import ReasoningOptimizer, TrajectoryOptimizer, CoTDistiller

# Initialize optimizer
optimizer = ReasoningOptimizer(agent)

# Optimize execution
result = await optimizer.optimize(input_data)

# Learn from execution
await optimizer.learn_from_execution(
    trajectory=execution_trajectory,
    reasoning_chain=agent_reasoning,
    reward=0.85  # Reward signal
)

# Get optimization report
report = optimizer.get_optimization_report()
```

**Features:**
- 📊 **Trajectory Optimization** - Learn optimal action sequences from past executions
- 📉 **CoT Distillation** - Compress reasoning chains (50%+ token savings)
- 🔄 **Feedback Loops** - Critique → Revise → Retry for self-improvement
- 🛡️ **Policy Constraints** - Enforce safety, cost, and latency guardrails
- 🎓 **RL-Style Tuning** - Optimize hyperparameters via reward signals

**📖 See [Reasoning Optimization Guide](docs/REASONING_OPTIMIZATION.md) for complete documentation**

## 🎯 Prompt Optimization (DSPy + TextGrad)

Advanced prompt optimization using **DSPy** for task prompts and **TextGrad** for system prompts:

```python
from optimization import PromptOptimizer, OptimizationPipeline

# Initialize optimizer
optimizer = PromptOptimizer()

# Optimize system prompt with TextGrad
system_result = await optimizer.optimize(
    prompt="You are a fraud detection expert.",
    prompt_type="system",
    evaluation_data=eval_data,
    objective="Maximize accuracy while being concise"
)

# Optimize task prompt with DSPy
task_result = await optimizer.optimize(
    prompt="Classify the transaction",
    prompt_type="task",
    training_data=train_data,
    task="fraud_detection"
)

# Run full optimization pipeline
pipeline = OptimizationPipeline()
result = await pipeline.run(
    agent_config=agent_config,
    training_data=train_data,
    evaluation_data=eval_data,
    stages=["system", "task", "test"]
)

# A/B test variants
from optimization import ABTestFramework

framework = ABTestFramework()
test_result = await framework.run_test(
    variants=[baseline, optimized],
    test_data=test_cases
)
```

**Features:**
- 🎓 **DSPy Integration** - Few-shot learning for task prompts
- 📈 **TextGrad Optimization** - Gradient-based system prompt refinement
- 🔄 **Multi-Stage Pipelines** - System → Task → A/B Test
- 🧪 **Statistical Testing** - Confidence intervals and significance
- 📦 **Unity Catalog Integration** - Auto-versioning of optimized prompts
- 📊 **Performance Tracking** - Optimization history and metrics

**📖 See [Optimization Guide](docs/OPTIMIZATION.md) for complete documentation**

## 📊 Databricks-Native Visualization

Built-in observability and debugging for Databricks notebooks:

```python
from visualization import DatabricksVisualizer

# Works natively in Databricks notebooks
viz = DatabricksVisualizer()

# Execution graph (Mermaid diagram)
viz.show_execution_graph(trace)

# Timeline (Plotly chart)
viz.show_timeline(trace)

# Tool call replay
viz.show_tool_calls(tool_calls)

# Decision inspection
viz.explain_decision(decision, context)

# Log to MLflow
viz.log_to_mlflow(trace)

# Create interactive widget
create_databricks_widget(trace)
```

**Features:**
- 🎨 **Execution Graphs** - Mermaid diagrams showing agent workflow
- ⏱️ **Timeline Visualization** - Plotly charts for execution timing
- 🔧 **Tool Call Replay** - Interactive tool call inspection
- 🤔 **Decision Explainer** - "Why did the agent do this?"
- 📝 **Prompt Comparison** - Side-by-side version diffs
- 📊 **MLflow Integration** - Auto-log visualizations to MLflow
- 🎛️ **Databricks Widgets** - Interactive notebook controls

**Designed for Databricks:**
- Uses `displayHTML()` for native rendering
- Integrates with MLflow UI
- Works with Databricks widgets
- Also works in Jupyter/standalone

**📖 See [Visualization Guide](docs/VISUALIZATION.md) for complete documentation**

## 🧪 Experiment Tracking & Feature Flags

Production experiment management with MLflow integration:

```python
from experiments import ExperimentTracker, FeatureFlagManager, RolloutStrategy

# Track experiments
tracker = ExperimentTracker()

with tracker.experiment("prompt_v2_test"):
    result = agent.execute(input_data)
    tracker.log_metric("accuracy", 0.95)

# Feature flags with gradual rollout
flags = FeatureFlagManager()

flags.register(
    "new_memory_system",
    strategy=RolloutStrategy.PERCENTAGE,
    percentage=10.0  # 10% rollout
)

if flags.is_enabled("new_memory_system", user_id="user123"):
    use_new_system()
```

**Features:**
- 🔬 **Experiment Tracking** - Automatic logging to MLflow and Unity Catalog
- 🚩 **Feature Flags** - Percentage, whitelist, and canary rollouts
- 📊 **A/B Testing** - Statistical comparison of variants
- 📈 **Metrics Collection** - Track performance over time
- 🎯 **Unity Catalog Integration** - Centralized experiment storage

## ❤️ Production Monitoring & Health Checks

Comprehensive monitoring for production deployments:

```python
from monitoring import HealthCheck, MetricsCollector, AlertManager

# Health checks
health = HealthCheck()
status = health.check_all()

# Metrics
metrics = MetricsCollector()
metrics.record_latency("agent_execution", 150.5)

# Alerting
alerts = AlertManager()
alerts.send_alert(Alert(
    message="High latency detected",
    severity=AlertSeverity.WARNING
))
```

**Features:**
- ❤️ **Health Checks** - System, memory, disk, and component health
- 📊 **Metrics Collection** - Integrated with telemetry system
- 🚨 **Alerting** - Configurable alerts and notifications
- 📈 **Performance Monitoring** - Track latency, throughput, errors
- 🎯 **Production-Ready** - Battle-tested monitoring patterns

## 🌐 Production Services (API & Workers)

FastAPI REST API and background workers:

```python
from services import AgentAPI, BackgroundWorker

# Start REST API
api = AgentAPI()
api.run(host="0.0.0.0", port=8000)

# Background worker
worker = BackgroundWorker()
worker.start()
```

**API Endpoints:**
- `POST /execute` - Execute agent
- `GET /health` - Health check
- `GET /metrics` - Metrics
- `GET /agents` - List agents
- WebSocket support for real-time updates

**Features:**
- 🌐 **FastAPI REST API** - Production HTTP endpoints
- 🔄 **Background Workers** - Async task processing
- 🔌 **WebSocket Server** - Real-time agent communication
- 📊 **Auto-documentation** - OpenAPI/Swagger UI
- 🛡️ **Production-Ready** - Health checks, metrics, error handling

## 🧪 Comprehensive Test Suite

Full test coverage with pytest:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=agents --cov=shared --cov-report=html

# Run specific test categories
pytest tests/test_agents.py -v
pytest tests/test_memory.py -v
pytest tests/test_optimization.py -v
```

**Test Coverage:**
- ✅ Agent execution and orchestration
- ✅ Memory system (storage, retrieval, policies)
- ✅ Optimization (DSPy, TextGrad)
- ✅ Monitoring (health checks, metrics)
- ✅ Experiments (tracking, feature flags)
- ✅ Integration tests with fixtures

## Why Use This Template?

✨ **Universal Design** - Works for any domain, not just fraud detection  
🔌 **Plug-and-Play** - 3 lines to integrate into existing pipelines  
⚙️ **Configuration-Driven** - Enable/disable agents via YAML, zero code changes  
🎯 **SLA-Aware** - Control inline vs async execution based on your requirements  
🏗️ **Production-Ready** - Battle-tested patterns, not toy examples  
📦 **Complete Stack** - Telemetry, evaluation, optimization, monitoring, experiments, API services, deployment  
🚀 **Template Generator** - Scaffold new projects in seconds  
🧪 **Built-in Benchmarking** - Comprehensive eval suite with leaderboards  

## Architecture Overview

This project implements a **domain-agnostic, plug-and-play agent framework** that integrates into existing data pipelines with minimal code changes. The architecture leverages:

- **Ephemeral Agents**: Task-specific narrative agents that spin up on-demand
- **Hot LLM Pools**: Always-on GPU endpoints via Databricks Model Serving
- **Prompt Optimization**: DSPy for task prompts, TextGrad for system prompts
- **Memory & Context**: Lakebase for conversation history and embeddings
- **MCP Tool Calling**: Standardized tool interfaces via Model Context Protocol
- **Observability**: OTEL → Zerobus → Delta Lake telemetry pipeline
- **Evaluation**: MLflow custom scorers and continuous feedback loops

## Key Features

🔌 **Plug-and-Play Integration** - Add to existing pipelines with 3 lines of code  
⚙️ **Configuration-Driven** - Enable/disable agents via YAML, no code changes  
🧠 **LangGraph Orchestration** - Plan → Act → Critique → Re-plan loops for autonomous workflows  
🎯 **SLA-Aware Execution** - Control inline vs offline based on requirements  
🔒 **Type-Safe** - Pydantic schemas validate all data at runtime  
🌐 **ASGI Support** - FastAPI endpoints, SSE streaming, async HTTP  
🔄 **Agent-to-Agent (A2A)** - Event-driven agent communication via NATS/Redis (optional)  
✨ **Domain-Agnostic** - Works for fraud, risk, support, compliance, or any use case  
📈 **Prompt Optimization** - DSPy for task prompts, TextGrad for system prompts  
📊 **Comprehensive Telemetry** - All events streamed to Delta Lake via Zerobus  
🧠 **Memory Management** - Lakebase for vector embeddings and conversation history  
🔧 **MCP Tool Integration** - Standardized external tool calling (v1.25.0+)  
📉 **MLflow Tracking** - Experiment tracking, evaluation, and model registry  
🏛️ **Unity Catalog** - Centralized prompt and model versioning  
🏢 **Multi-Tenant Ready** - Schema adapters handle any customer format  
🧪 **Agent Benchmarking** - Multi-metric eval suite with auto-generated leaderboards  
🧠 **Agent-Governed Memory** - Intelligent storage, retrieval, reflection, and forgetting  
🎯 **Reasoning Optimization** - Trajectory tuning, CoT distillation, feedback loops, RL-style tuning  
📊 **Databricks-Native Visualization** - Execution graphs, timelines, tool replay, decision inspection  
⚙️ **YAML-Configurable** - All infrastructure and runtime settings via unified YAML  

## Project Structure

```
.
├── agents/                     # 🤖 Agent framework (CORE)
│   ├── base.py                #    - Base agent interfaces
│   ├── config.py              #    - Configuration loader
│   ├── registry.py            #    - Agent registry + router
│   └── execution/             #    - Pluggable execution backends
├── shared/                    # 📦 Shared libraries
│   ├── schemas/               #    - Pydantic data models (type-safe)
│   └── adapters/              #    - Schema adaptation framework
├── config/                    # ⚙️  Configuration (plug-and-play)
│   ├── agents/                #    - Agent configurations (YAML)
│   └── adapters/              #    - Customer schema adapters
├── services/                  # 🚀 Deployable services
├── optimization/              # 🎓 Prompt optimization (DSPy/TextGrad)
├── memory/                    # 🧠 Lakebase integration
├── orchestration/             # 🔄 Databricks Workflows + LangGraph
├── mcp-servers/               # 🔧 Model Context Protocol tools
├── evaluation/                # 📊 MLflow scorers and metrics
├── telemetry/                 # 📈 OTEL → Zerobus → Delta
├── uc-registry/               # 🗃️  Unity Catalog integration
├── data/                      # 📊 Synthetic testbed
├── infrastructure/            # 🏗️  Deployment configs (DABS)
├── experiments/               # 🔬 Notebooks + MLflow tracking
├── tests/                     # 🧪 Unit, integration, load tests
└── docs/                      # 📖 Documentation
```

**See [Project Structure](docs/PROJECT_STRUCTURE.md) for detailed breakdown with key concepts.**

## Data Schemas

All data structures are defined using Pydantic models in `shared/schemas/`:

- **transactions.py** - Transaction records and payment data
- **fraud_signals.py** - Velocity, amount, location, device signals
- **contexts.py** - Merchant and customer profiles
- **agent_io.py** - Agent inputs, outputs, tool calls (MCP-ready)
- **evaluation.py** - Evaluation records and scorer metrics
- **telemetry.py** - OTEL traces for Zerobus ingestion

See `shared/schemas/README.md` for detailed documentation.

## Quick Start (Plug-and-Play)

Add agents to your existing pipeline in 3 lines:

```python
from agents import AgentRouter
from shared.schemas import AgentInput

# 1. Load agents from config (one line!)
router = AgentRouter.from_yaml("config/agents.yaml")

# 2. Convert your data to AgentInput (Pydantic validates!)
agent_input = AgentInput(
    request_id=record.id,
    data=YourDomainData(**record.dict()),  # Your domain-specific data
    # ... your contexts
)

# 3. Route to agent (inline or offline based on config!)
result = await router.route("your_agent", agent_input)

# That's it! Agent runs according to your config.
# No code changes to enable/disable or switch execution modes.
```

**Configuration controls everything:**

```yaml
# config/agents.yaml
agents:
  your_agent:
    class: "your_package.YourAgent"
    execution_mode: "offline"  # or "inline" if SLA allows
    enabled: true              # Change to false to disable
    timeout: 30
```

**Works for any domain:** Fraud detection, risk analysis, customer support, compliance, content moderation, etc.

See [Configuration System](docs/CONFIGURATION_SYSTEM.md) for details.

---

## Getting Started

### Prerequisites

- Python 3.9+
- Databricks workspace with:
  - Model Serving endpoint
  - Unity Catalog
  - Lakebase access
- Zerobus server endpoint (for telemetry)

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd "SOTA Agent"

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e ".[dev]"
```

### Configuration

```bash
# Copy example config
cp .env.example .env

# Edit .env with your Databricks credentials
# - DATABRICKS_HOST
# - DATABRICKS_TOKEN
# - MODEL_SERVING_ENDPOINT
# - UNITY_CATALOG_NAME
# - ZEROBUS_ENDPOINT
```

## Databricks Stack

| Component | Technology |
|-----------|-----------|
| LLM Inference | Databricks Model Serving |
| Orchestration | LangGraph + Databricks Workflows |
| Tracing & Evaluation | Databricks MLflow |
| Memory/Vector Store | Lakebase |
| Telemetry Sink | Zerobus → Delta Lake |
| Prompt Registry | Unity Catalog |
| Dashboards | Databricks SQL |
| Compute | Databricks Clusters / Serverless |

## Development

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test suite
pytest tests/unit/
pytest tests/integration/
```

### Code Quality

```bash
# Format code
black .

# Lint
ruff check .

# Type check
mypy .
```

## Architecture Flows

### Realtime Path (Low-latency)
Transaction → Event Collector → Ephemeral Narrative Agent → MCP Tool Calls → LLM Pool → Risk Narrative → Dashboard/Alerts

### Async Path (Optimization)
MLflow Scorers → Evaluate High-Risk Txns → Log Metrics → DSPy/TextGrad Optimization → Update Prompts in UC → Deploy to Agents

## MCP Integration

All tool calls use Model Context Protocol for standardization:

```python
# Tool call schema (MCP-ready)
tool_call = ToolCall(
    tool_id="call_123",
    tool_name="merchant_context",
    tool_server="uc-query-server",
    arguments={"merchant_id": "mch_001"}
)

# Tool result
tool_result = ToolResult(
    tool_call_id="call_123",
    success=True,
    result=merchant_data,
    latency_ms=45.2
)
```

See `mcp-servers/` for tool implementations.

## Telemetry

All events flow through OTEL → Zerobus → Delta Lake:

- Agent start/complete/error
- MCP tool calls
- LLM requests/responses
- Stream chunks
- Evaluation results

Query telemetry in Unity Catalog:

```sql
SELECT * FROM main.telemetry.agent_traces
WHERE transaction_id = 'txn_123'
ORDER BY timestamp DESC;
```

## Prompt Optimization

### DSPy (Task Prompts)
```python
# Optimize reasoning pipeline
from optimization.dspy import MIPROOptimizer

optimizer = MIPROOptimizer(training_data)
optimized_prompt = optimizer.optimize(baseline_prompt)
```

### TextGrad (System Prompts)
```python
# Optimize system prompt with guardrails
from optimization.textgrad import SystemPromptOptimizer

optimizer = SystemPromptOptimizer(feedback_data)
optimized_system = optimizer.optimize(system_prompt)
```

## Synthetic Data

Generate idempotent test data:

```bash
# Generate synthetic transactions
python -m data.synthetic.generate --seed 42 --count 5000

# Output: data/synthetic/raw/transactions.parquet
```

## Contributing

1. Create a feature branch
2. Make changes with tests
3. Run linters and tests
4. Submit pull request

## License

MIT

## Documentation

### 🎯 Start Here
- **[Getting Started](GETTING_STARTED.md)** ⭐ - 5-minute quick start guide
- **[Template Guide](docs/TEMPLATE_GUIDE.md)** ⭐ - Comprehensive guide for any domain
- **[Cross-Domain Examples](docs/CROSS_DOMAIN_EXAMPLES.md)** ⭐ - 8 real-world examples
- **[Documentation Index](docs/README.md)** - Complete documentation map

### 📚 Core Documentation
- **[Project Structure](docs/PROJECT_STRUCTURE.md)** - Code organization and key concepts
- **[Configuration System](docs/CONFIGURATION_SYSTEM.md)** - YAML-based configuration
- **[Schema Documentation](docs/schemas/)** - Data schemas and adaptation
- **[Use Cases](docs/USE_CASES.md)** - Advanced usage patterns

### 🛠️ Tools
- **Template Generator** - `python template_generator.py --help`
- **Example Integrations** - `examples/plug_and_play_integration.py`

## Contact

For questions, see `docs/` or contact the team.

