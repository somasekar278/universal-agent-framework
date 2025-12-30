# How the Framework Guides Users & Enforces Best Practices

**Answer to: "How can I enforce usage of everything we built while providing override capabilities?"**

---

## 🎯 The Solution: Progressive Disclosure

The framework implements **3-tier guidance** based on user experience:

| User Type | Approach | Enforcement Level | Override Freedom |
|-----------|----------|-------------------|------------------|
| **Beginner** | Opinionated defaults | ✅ High (automatic) | ⚠️ Limited |
| **Intermediate** | Guided recommendations | ⚠️ Medium (suggested) | ✅ Moderate |
| **Advanced** | Full freedom | ❌ None (opt-in only) | ✅✅ Complete |

---

## 🛠️ Implementation: 4 CLI Tools

### 1. `sota-setup` - Interactive Wizard (Enforcement Tool)

**For Beginners: Guides through complete setup**

```bash
$ sota-setup

🚀 SOTA Agent Framework - Setup Wizard

What is your experience level with agentic solutions?
  1. Beginner - New to agents, want opinionated setup
  2. Intermediate - Some experience, want recommendations  
  3. Advanced - Expert, want full control

Select (1-3) [default: 2]: 1

✨ Beginner Mode: We'll set up all best practices for you!

📋 Configuration Summary:
- Memory System: ✅ Enabled (agent-governed)
- Monitoring: ✅ Enabled (health + metrics)
- Telemetry: ✅ Enabled (OTEL → Delta Lake)
- Experiments: ✅ Enabled (MLflow + feature flags)
- Benchmarking: ✅ Enabled (evaluation suite)

🎓 Beginner's Guide:
  ✅ Automatically track all agent executions
  ✅ Store memories intelligently  
  ✅ Monitor health and performance
  ✅ Provide helpful error messages
```

**What it does:**
- ✅ Enables ALL features automatically
- ✅ Generates complete configuration
- ✅ Creates working examples
- ✅ Shows clear next steps

**How to override:**
- Edit `framework_config.yaml`
- Disable specific features
- Subclass any component

### 2. `sota-generate` - Quick Project Generation

**For All Levels: Fast scaffolding**

```bash
# Basic generation
sota-generate --domain fraud_detection --output ./fraud-agent

# Minimal (advanced users)
sota-generate --domain my_domain --minimal
```

**What it does:**
- ✅ Creates project structure
- ✅ Includes examples
- ✅ Generates configs
- ⚠️ Uses recommended defaults (can be changed)

### 3. `sota-advisor` - Analysis & Recommendations (Enforcement Tool)

**For All Levels: Personalized guidance**

```bash
$ sota-advisor ./my_project

🔍 Analyzing project: ./my_project

====================================================================
📊 Framework Analysis Report
====================================================================

🔴 CRITICAL Issues:
  📌 Enable Production Monitoring
     No monitoring configured for production readiness
     Action: Enable 'monitoring' feature
     Benefit: Track agent health, performance, catch issues early

🟠 HIGH Priority:
  📌 Enable Agent Memory System
     Your agents don't have memory enabled
     Action: Add 'memory' to enabled features
     Benefit: Agents will remember context across interactions

🟡 MEDIUM Priority:
  📌 Add Agent Benchmarking
     No benchmarking suite configured
     Action: Enable 'benchmarking' and create test suites
     Benefit: Track agent performance over time

====================================================================
Total Recommendations: 3
====================================================================
```

**What it does:**
- ✅ Analyzes existing projects
- ✅ Recommends missing features
- ✅ Prioritizes suggestions (critical → low)
- ✅ Explains benefits
- ⚠️ **Suggests but doesn't force**

### 4. `sota-benchmark` - Performance Validation

**For Production: Continuous evaluation**

```bash
sota-benchmark run --suite fraud_detection --report md
```

**What it does:**
- ✅ Runs evaluation suites
- ✅ Generates reports
- ✅ Tracks regressions
- ⚠️ Can be skipped (but recommended)

---

## 📋 Feature Enforcement by Level

### Level 1: Beginner (Strong Guidance)

**Automatically Enabled:**

| Feature | Why Enforced | Override |
|---------|--------------|----------|
| **Memory** | Context is critical | Edit config YAML |
| **Monitoring** | Production requirement | Edit config YAML |
| **Telemetry** | Observability essential | Edit config YAML |
| **Experiments** | Track changes safely | Edit config YAML |

**Runtime Behaviors:**

```python
# These happen automatically (no code needed):
✅ All agent.execute() calls are traced
✅ Exceptions trigger health alerts
✅ Memories stored after interactions
✅ Metrics exported to Delta Lake
✅ Experiments logged to MLflow
```

**How Beginners Override:**

```yaml
# framework_config.yaml
features:
  memory:
    enabled: false  # Disable if really needed
```

### Level 2: Intermediate (Recommendations)

**Suggested (Not Forced):**

```bash
# Run advisor to see suggestions
$ sota-advisor ./my_project

💡 Consider enabling memory for context-aware agents
⚠️  Recommendation: Enable monitoring for production
💡 Add benchmarking to track performance over time
```

**Configuration-Driven:**

```yaml
# framework_config.yaml - Full control via YAML
features:
  memory: {enabled: true}
  monitoring: {enabled: false}  # Your choice
  optimization: {enabled: true}
  benchmarking: {enabled: false}
```

**How Intermediates Override:**

```python
# Subclass any component
from memory import MemoryManager

class CustomMemoryManager(MemoryManager):
    def __init__(self):
        super().__init__()
        # Your custom logic
```

### Level 3: Advanced (Zero Enforcement)

**Nothing Automatic:**

```python
# Import only what you need
from agents.base import Agent

# Memory? Optional
from memory import MemoryManager  

# Monitoring? Optional  
from monitoring import HealthCheck

# You decide!
```

**Direct API Access:**

```python
# Use internal APIs directly
from memory.stores import LongTermMemory
from telemetry import AgentTracer
from visualization import DatabricksVisualizer

# Complete control
memory = LongTermMemory(custom_config)
tracer = AgentTracer(custom_backend)
viz = DatabricksVisualizer(custom_settings)
```

**How Advanced Users Override:**

```python
# Override EVERYTHING
class MyCustomAgent(Agent):
    def __init__(self):
        pass  # Don't even call super()
    
    async def process(self, input_data):
        return my_completely_custom_logic()
```

---

## 🔧 Override Examples at Each Level

### Example 1: Memory System

**Beginner:**
```yaml
# Just enable/disable
features:
  memory: {enabled: true}
# Framework handles the rest
```

**Intermediate:**
```yaml
# Configure details
features:
  memory:
    enabled: true
    short_term_capacity: 100
    long_term_storage: "unity_catalog"
    agent_governed: true
```

**Advanced:**
```python
# Custom implementation
from memory import MemoryManager, MemoryStore

class MyMemory(MemoryStore):
    async def store(self, data):
        # Your logic
        pass

# Use it
manager = MemoryManager()
manager.register_store("custom", MyMemory())
```

### Example 2: Monitoring

**Beginner:**
```yaml
# Enabled automatically with defaults
monitoring:
  enabled: true
# Health checks run automatically
```

**Intermediate:**
```yaml
# Select specific checks
monitoring:
  enabled: true
  health_checks: [system, memory, agents]
  alerting: true
  metrics:
    export_interval_seconds: 60
```

**Advanced:**
```python
# Custom health checks
from monitoring import HealthCheck

class MyHealthCheck(HealthCheck):
    def check(self):
        return custom_health_logic()

# Register
health = HealthCheck()
health.register("my_check", MyHealthCheck())
```

### Example 3: Agent Execution

**Beginner:**
```yaml
# YAML configuration only
agents:
  my_agent:
    execution_mode: "in_process"
    timeout_seconds: 30
# Framework handles execution
```

**Intermediate:**
```yaml
# Choose execution backend
agents:
  my_agent:
    execution_mode: "ray_task"  # or process_pool, ray_actor
    backend_config:
      num_workers: 4
```

**Advanced:**
```python
# Custom execution backend
from agents.execution import ExecutionBackend

class MyBackend(ExecutionBackend):
    async def execute(self, agent, data):
        # Your execution logic
        return await custom_execution()

# Use it
agent.execution_backend = MyBackend()
```

---

## 📊 Validation & Warnings

### Beginner Validations (Strong)

```python
# Framework validates and warns:

⚠️  WARNING: Memory not enabled
→ Agents won't remember context between calls
→ Action: Set features.memory.enabled = true

❌ ERROR: No monitoring in production mode
→ Can't track agent health
→ Action: Enable monitoring or set environment = "development"

⚠️  WARNING: No benchmarks defined
→ Can't track performance regressions  
→ Action: Create benchmarks/ directory with test suites
```

### Intermediate Validations (Suggestions)

```python
# Advisor suggests improvements:

💡 SUGGESTION: Consider enabling optimization
→ Benefit: Automatically improve prompts
→ Optional: Run sota-advisor for more details

💡 SUGGESTION: Add telemetry for observability
→ Benefit: Get detailed traces and metrics
→ Optional: Can skip if you have other monitoring
```

### Advanced Validations (Opt-in)

```python
# No automatic validation unless requested

$ sota-advisor ./my_project --validate-only
# Only runs if you explicitly ask
```

---

## 🎯 The Answer to Your Question

### For Beginners: **Enforce Through Defaults**

1. ✅ `sota-setup` enables everything automatically
2. ✅ Runtime behaviors built-in (tracing, memory, health)
3. ✅ Validation warnings guide them
4. ✅ Clear error messages with actions
5. ⚠️ **But they CAN override via config**

### For Advanced Users: **Enable Through Opt-in**

1. ✅ Zero features enforced
2. ✅ Import only what you need
3. ✅ Override any component
4. ✅ Direct API access
5. ✅ `sota-advisor` available when wanted

### For Both: **Clear Upgrade/Downgrade Path**

```bash
# Start opinionated
sota-setup  # Beginner mode

# Get more control
Edit framework_config.yaml  # Intermediate

# Full freedom
Import components directly  # Advanced
```

---

## 🚀 Summary

**The framework achieves both goals:**

### ✅ **Guides Beginners:**
- Opinionated `sota-setup` wizard
- All features enabled by default
- Runtime behaviors automatic
- Clear validation warnings
- Helpful error messages

### ✅ **Empowers Experts:**
- Minimal `pip install` option
- À la carte imports
- Complete override capability
- Direct API access
- Optional guidance via `sota-advisor`

### ✅ **Scales with Users:**
- Start with `sota-setup` (beginner)
- Graduate to YAML configs (intermediate)
- End with custom implementations (advanced)
- **One framework, three modes**

---

**Try it:**

```bash
# Beginner: Full guidance
sota-setup

# Intermediate: Recommendations  
sota-generate my_domain && sota-advisor .

# Advanced: Full control
pip install sota-agent-framework && python
>>> from agents.base import Agent  # Use what you want
```

**The framework never gets in your way, but always has your back!** 🚀

