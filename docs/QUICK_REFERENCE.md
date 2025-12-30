# Quick Reference Card

## 🎯 Choose Your Experience Level

| Level | Command | What You Get | Override Capability |
|-------|---------|--------------|---------------------|
| **Beginner** | `sota-setup` | ✅ All features enabled<br>✅ Best practices built-in<br>✅ Guided wizard | ⚠️ Limited (opinionated) |
| **Intermediate** | `sota-generate` + `sota-advisor` | ✅ Recommended features<br>✅ Personalized advice<br>✅ Feature selection | ✅ Moderate (configurable) |
| **Advanced** | `pip install` + à la carte imports | ✅ Minimal setup<br>✅ Full control<br>✅ No opinions | ✅✅ Complete (everything) |

---

## 📦 4 CLI Commands to Know

### 1. `sota-setup` - Interactive Wizard (Beginners)

```bash
sota-setup
# Asks questions, generates complete project with all features
```

**When to use**: First time, want guidance, production-ready setup

### 2. `sota-generate` - Quick Generation (All Levels)

```bash
sota-generate --domain fraud_detection --output ./fraud-agent
```

**When to use**: Fast project creation, customize later

### 3. `sota-advisor` - Get Recommendations (All Levels)

```bash
sota-advisor ./my_project
# Analyzes project, recommends missing features
```

**When to use**: Check what you're missing, optimize setup

### 4. `sota-benchmark` - Run Evaluations (Production)

```bash
sota-benchmark run --suite my_suite --report md
```

**When to use**: Test agent performance, track metrics

---

## 🎛️ Feature Control

### Beginner Mode: Features Enabled by Default

| Feature | Auto-Enabled | Why |
|---------|--------------|-----|
| **Memory** | ✅ Yes | Context across interactions |
| **Monitoring** | ✅ Yes | Track health & performance |
| **Telemetry** | ✅ Yes | Full observability |
| **Experiments** | ✅ Yes | Track changes safely |

**Override**: Edit `framework_config.yaml`

### Intermediate Mode: Choose Your Features

```yaml
# framework_config.yaml
features:
  memory: {enabled: true}      # Context
  monitoring: {enabled: true}  # Health
  telemetry: {enabled: false}  # Optional
  optimization: {enabled: true} # Prompt tuning
```

**Override**: YAML configuration

### Advanced Mode: Import What You Need

```python
# No enforced features - use what you want
from agents.base import Agent
from memory import MemoryManager  # Optional
from monitoring import HealthCheck  # Optional
```

**Override**: Everything is overridable

---

## 🔧 Override Examples

### Override #1: Memory Strategy

```python
# Beginner: Enabled automatically (no code)
# Intermediate: Configure in YAML
# Advanced: Custom implementation

from memory import RetrievalStrategy

class MyStrategy(RetrievalStrategy):
    async def retrieve(self, query, top_k):
        # Your logic here
        return results
```

### Override #2: Agent Execution

```python
# Beginner: Configured via YAML
# Intermediate: Pick from backends (in_process, ray, etc.)
# Advanced: Custom backend

from agents.execution import ExecutionBackend

class MyBackend(ExecutionBackend):
    async def execute(self, agent, input_data):
        # Your execution logic
        return result
```

### Override #3: Health Checks

```python
# Beginner: Default checks (system, memory, disk)
# Intermediate: Select checks in YAML
# Advanced: Custom checks

from monitoring import HealthCheck

class MyHealthCheck(HealthCheck):
    def check(self):
        # Your health logic
        return status
```

---

## 📊 What Gets Enforced at Each Level?

### Beginner (Highly Opinionated)

✅ **Automatically Enforced:**
- All agent executions traced
- Memories stored after each interaction
- Health checks run continuously
- Failures trigger alerts
- Experiments logged to MLflow

⚠️ **Warnings Shown:**
- "Memory not configured - agents won't remember context"
- "No monitoring - can't track health"
- "Missing telemetry - limited observability"

**Override**: Edit `framework_config.yaml` to disable

### Intermediate (Recommended)

✅ **Advisor Recommendations:**
- "Consider enabling memory for context"
- "Add monitoring for production readiness"
- "Enable benchmarking to track performance"

⚠️ **Validation Warnings:**
- "Monitoring enabled but no health checks defined"
- "Memory enabled but storage path not configured"

**Override**: Ignore recommendations, disable validation

### Advanced (No Opinions)

✅ **Nothing Enforced**
- Use any component or none
- Override everything
- No validations unless requested

**Opt-in Guidance:**
```bash
sota-advisor ./my_project --suggestions-only
```

---

## 🚦 Decision Tree

```
Are you new to agents?
├─ YES → Use `sota-setup` (Beginner Mode)
│         ✅ All features enabled
│         ✅ Best practices built-in
│         ✅ Production-ready immediately
│
└─ NO → Do you want recommendations?
   ├─ YES → Use `sota-generate` + `sota-advisor` (Intermediate)
   │         ✅ Choose your features
   │         ✅ Get personalized advice
   │         ✅ Configure via YAML
   │
   └─ NO → Use minimal install (Advanced)
             ✅ Import only what you need
             ✅ Override everything
             ✅ Full control
```

---

## 📚 Documentation by Level

### Beginners Start Here:
1. ✅ Run `sota-setup`
2. ✅ Read [GETTING_STARTED.md](GETTING_STARTED.md)
3. ✅ Follow [User Journey - Beginner](USER_JOURNEY.md#-for-beginners-im-new-to-agents)

### Intermediate Users:
1. ✅ Read [User Journey - Intermediate](USER_JOURNEY.md#-for-intermediate-users-i-know-some-agents)
2. ✅ Check [Configuration Guide](CONFIGURATION.md)
3. ✅ Run `sota-advisor` for recommendations

### Advanced Users:
1. ✅ Read [User Journey - Advanced](USER_JOURNEY.md#-for-advanced-users-im-an-expert)
2. ✅ Browse API docs in source code
3. ✅ Extend framework as needed

---

## 🎯 Common Questions

**Q: Can I start as beginner and graduate to advanced?**
✅ YES! The framework scales with you. Start opinionated, remove constraints later.

**Q: Can advanced users still get recommendations?**
✅ YES! Run `sota-advisor` anytime for suggestions.

**Q: Can I override everything even in beginner mode?**
✅ YES! Edit `framework_config.yaml` or subclass any component.

**Q: Do I have to use all features?**
❌ NO! Disable in config or don't import them.

**Q: How do I know what features I'm missing?**
✅ Run `sota-advisor ./my_project`

---

## 🚀 Quick Start By Goal

### Goal: "Just make it work"
```bash
sota-setup  # Choose beginner mode
# Done! Everything configured.
```

### Goal: "Production-ready with best practices"
```bash
sota-setup  # Choose recommended preset
sota-advisor .  # Check what else you might want
```

### Goal: "Maximum control, minimal magic"
```bash
pip install sota-agent-framework
# Import only what you need
```

### Goal: "Improve existing project"
```bash
sota-advisor ./existing_project
# Get recommendations for what's missing
```

---

**Remember**: The framework **guides beginners** while giving **experts complete freedom**! 🎯

