

# User Journey Guide

**Choose your path based on your experience level:**

---

## 🎓 For Beginners: "I'm New to Agents"

### **Your Goal**: Build your first agent with all best practices built-in

### **Step 1: Interactive Setup**

```bash
# Install framework
pip install sota-agent-framework[all]

# Run interactive setup wizard
sota-setup
```

**The wizard will:**
- ✅ Ask simple questions about your project
- ✅ Configure all best practices automatically
- ✅ Generate a complete project structure
- ✅ Include helpful examples and documentation

### **Step 2: Understand What You Got**

Your project includes:

```
my_agent/
├── config/
│   ├── agents.yaml          # Agent definitions (edit this!)
│   ├── memory.yaml           # Memory configuration
│   └── monitoring.yaml       # Health checks
├── agents/
│   └── custom_agent.py      # Your agent (start here!)
├── examples/
│   └── example_usage.py     # Working example
└── framework_config.yaml    # Framework settings
```

### **Step 3: Run Your First Agent**

```bash
cd my_agent
python examples/example_usage.py
```

**What happens automatically:**
- ✅ Agent execution is traced
- ✅ Memories are stored
- ✅ Health is monitored
- ✅ Metrics are collected

### **Step 4: Customize Gradually**

**Edit `config/agents.yaml` to customize behavior:**

```yaml
agents:
  my_agent:
    class: "agents.custom_agent.MyAgent"
    enabled: true
    
    # Built-in features (no code needed!)
    memory_enabled: true
    monitoring_enabled: true
    
    # Your settings
    timeout_seconds: 30
    retry_policy:
      max_retries: 3
```

### **Step 5: Get Help When Stuck**

```bash
# Check what you might be missing
sota-advisor ./my_agent

# Read beginner docs
open docs/GETTING_STARTED.md
```

---

## 🚀 For Intermediate Users: "I Know Some Agents"

### **Your Goal**: Build a production-ready agent system with recommended features

### **Step 1: Quick Setup**

```bash
pip install sota-agent-framework[all]

# Generate with recommended preset
sota-generate --domain fraud_detection --output ./fraud-agent
```

### **Step 2: Choose Your Features**

Run the advisor to see recommendations:

```bash
sota-advisor ./fraud-agent
```

**Common patterns:**

| Use Case | Recommended Features |
|----------|---------------------|
| **Production API** | core + monitoring + telemetry + services |
| **Experimental** | core + memory + experiments + optimization |
| **Data Pipeline** | core + memory + telemetry + databricks |
| **Complex Workflows** | core + memory + langgraph + visualization |

### **Step 3: Add Features Selectively**

Edit `framework_config.yaml`:

```yaml
features:
  memory:
    enabled: true
    agent_governed: true  # Let agents decide what to remember
  
  monitoring:
    enabled: true
    health_checks: [system, memory, agents]
  
  experiments:
    enabled: true
    mlflow_tracking: true  # Track all experiments
```

### **Step 4: Override When Needed**

**Custom memory strategy:**

```python
from memory import RetrievalStrategy

class MyRetrievalStrategy(RetrievalStrategy):
    async def retrieve(self, query: str, top_k: int):
        # Your custom logic
        return custom_results
```

**Use your custom component:**

```yaml
memory:
  retrieval_strategy: "my_project.custom.MyRetrievalStrategy"
```

### **Step 5: Monitor in Production**

```bash
# Check health
curl http://localhost:8000/health

# View metrics
curl http://localhost:8000/metrics

# Run benchmarks
sota-benchmark run --suite my_suite
```

---

## ⚡ For Advanced Users: "I'm an Expert"

### **Your Goal**: Full control with complete customization

### **Step 1: Minimal Setup**

```bash
# Install only what you need
pip install sota-agent-framework

# Generate minimal project
sota-generate --domain my_domain --minimal
```

### **Step 2: Pick Components À La Carte**

**Import only what you need:**

```python
# Just the core
from agents.base import Agent
from agents.registry import AgentRegistry

# Add memory later
from memory import MemoryManager

# Add monitoring when ready
from monitoring import HealthCheck
```

### **Step 3: Override Everything**

**Custom agent base class:**

```python
from agents.base import Agent

class MyCustomAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Your custom initialization
    
    async def process(self, input_data):
        # Complete control over execution
        return custom_logic()
```

**Custom execution backend:**

```python
from agents.execution import ExecutionBackend

class MyBackend(ExecutionBackend):
    async def execute(self, agent, input_data):
        # Your custom execution logic
        return await custom_execution()
```

### **Step 4: Extend the Framework**

**Add custom metrics:**

```python
from evaluation.metrics import Metric

class MyCustomMetric(Metric):
    def evaluate(self, result, expected):
        # Your custom evaluation
        return score
```

**Register and use:**

```python
from evaluation import EvaluationHarness

harness = EvaluationHarness()
harness.add_metric(MyCustomMetric())
```

### **Step 5: Direct API Access**

**Use internal APIs directly:**

```python
# Direct memory access
from memory.stores import LongTermMemory

memory = LongTermMemory(storage_path="/custom/path")
await memory.store(data)

# Direct telemetry
from telemetry import AgentTracer

tracer = AgentTracer()
with tracer.start_span("custom_operation"):
    # Your code
    pass

# Direct visualization
from visualization import DatabricksVisualizer

viz = DatabricksVisualizer()
viz.show_execution_graph(custom_trace)
```

### **Override Configuration**

**Complete YAML control:**

```yaml
framework:
  version: "0.2.1"
  custom_mode: true  # Disable validations

agents:
  my_agent:
    class: "my_custom.agent.CustomAgent"
    backend: "my_custom.backend.MyBackend"
    
    # Any custom fields
    custom_field_1: value
    custom_field_2: value

# Override any component
memory:
  manager_class: "my_custom.memory.CustomManager"
  
monitoring:
  health_check_class: "my_custom.monitoring.CustomHealthCheck"
```

---

## 📊 Feature Enforcement & Guidance

### **For Beginners: Enforced Best Practices**

When you use `sota-setup` in beginner mode:

✅ **Automatically Enabled:**
- Memory system (agent-governed)
- Health monitoring
- Experiment tracking
- Telemetry to Delta Lake

✅ **Automatic Behaviors:**
- All agent executions are traced
- Failures trigger alerts
- Memories are stored intelligently
- Health checks run continuously

⚠️ **Warnings When Missing:**
- "Memory not enabled - agents won't remember context"
- "Monitoring disabled - no health visibility"
- "No benchmarks - can't track performance"

### **For Intermediate: Recommended Patterns**

Run `sota-advisor` to get recommendations:

```bash
$ sota-advisor ./my_project

🔴 CRITICAL Issues:
  📌 Enable Production Monitoring
     No monitoring configured for production readiness
     Action: Enable 'monitoring' feature
     Benefit: Track agent health, performance, and catch issues early

🟠 HIGH Priority:
  📌 Add Detailed Telemetry
     Monitoring is enabled but telemetry is not
     Action: Enable 'telemetry' feature
     Benefit: Get detailed traces and metrics
```

### **For Advanced: Full Freedom + Opt-In Guidance**

**You control everything:**
- ✅ Disable any feature
- ✅ Override any component
- ✅ Use internal APIs directly
- ✅ Skip validations

**Opt-in to advice:**

```bash
# Get recommendations when you want them
sota-advisor ./my_project --suggestions-only

# Validate configuration
sota-advisor ./my_project --validate-only
```

---

## 🎯 Common Scenarios

### **Scenario 1: "Just make it work"** (Beginner)

```bash
sota-setup  # Choose "beginner" mode
cd my_agent
python examples/example_usage.py  # It just works!
```

### **Scenario 2: "I want recommendations"** (Intermediate)

```bash
sota-generate --domain my_domain
cd my_domain
sota-advisor .  # See what you're missing
# Enable recommended features in framework_config.yaml
```

### **Scenario 3: "Don't tell me what to do"** (Advanced)

```bash
sota-generate --domain my_domain --minimal
# Use only what you want, override everything else
```

### **Scenario 4: "Help me improve"** (Any Level)

```bash
sota-advisor ./existing_project  # Analyze existing project
# Get actionable recommendations
```

---

## 🔧 Override Examples

### **Override Memory Strategy**

```python
# Beginner: Just enable it
# framework_config.yaml
features:
  memory:
    enabled: true

# Advanced: Custom strategy
from memory import RetrievalStrategy

class CustomStrategy(RetrievalStrategy):
    async def retrieve(self, query, top_k):
        return custom_logic()
```

### **Override Health Checks**

```python
# Beginner: Use defaults
# monitoring enabled automatically

# Advanced: Custom checks
from monitoring import HealthCheck

class MyHealthCheck(HealthCheck):
    def check(self):
        return custom_health_logic()
```

### **Override Agent Execution**

```python
# Beginner: YAML configuration
# config/agents.yaml
agents:
  my_agent:
    execution_mode: "in_process"

# Advanced: Custom backend
from agents.execution import ExecutionBackend

class MyBackend(ExecutionBackend):
    async def execute(self, agent, data):
        return await custom_execution()
```

---

## 📚 Next Steps by Level

### **Beginners:**
1. ✅ Run `sota-setup`
2. ✅ Complete examples/example_usage.py
3. ✅ Read docs/GETTING_STARTED.md
4. ✅ Customize config/agents.yaml
5. ✅ Deploy with all features enabled

### **Intermediate:**
1. ✅ Generate project with recommended preset
2. ✅ Run `sota-advisor` for recommendations
3. ✅ Enable features based on use case
4. ✅ Create benchmarks in benchmarks/
5. ✅ Monitor in production

### **Advanced:**
1. ✅ Generate minimal project
2. ✅ Import only needed components
3. ✅ Override/extend as needed
4. ✅ Access internal APIs directly
5. ✅ Contribute back to framework

---

**Remember**: The framework scales with you. Start simple, add complexity when needed! 🚀

