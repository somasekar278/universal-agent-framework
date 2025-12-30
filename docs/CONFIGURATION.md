# YAML Configuration Guide

**Complete guide to configuring SOTA Agent Framework via YAML**

## Overview

The SOTA Agent Framework uses a **unified YAML configuration** for all infrastructure and runtime components. This provides:

✅ **Single source of truth** - One file controls everything  
✅ **Environment-specific** - Dev/staging/prod overrides  
✅ **Version controlled** - Configuration as code  
✅ **Databricks-native** - Stored in Unity Catalog Volumes  
✅ **No code changes** - Reconfigure without redeployment  

---

## Quick Start

### 1. Create Configuration

```yaml
# config/sota_config.yaml
environment: production

databricks:
  unity_catalog:
    catalog_name: my_agents
    schema_name: production

telemetry:
  enabled: true
  exporters:
    delta_lake:
      table: agent_telemetry

memory:
  short_term:
    capacity: 20
  long_term:
    capacity: 10000
```

### 2. Load Configuration

```python
from shared.config_loader import load_config

# Load config
config = load_config("config/sota_config.yaml")

# Access values
catalog = config.get("databricks.unity_catalog.catalog_name")
# Returns: "my_agents"

# Typed access
enabled = config.get_bool("telemetry.enabled")
capacity = config.get_int("memory.short_term.capacity")
```

### 3. Components Use Config Automatically

```python
from telemetry import init_telemetry
from uc_registry import PromptRegistry
from memory import MemoryManager

# All auto-load from YAML
init_telemetry()  # Uses telemetry.* config
registry = PromptRegistry()  # Uses uc_registry.prompts.* config
memory = MemoryManager()  # Uses memory.* config
```

---

## Configuration Structure

### Complete Schema

```
sota_config.yaml
├── environment              # Current environment (dev/staging/production)
├── databricks
│   ├── workspace           # Workspace connection
│   ├── unity_catalog       # UC configuration
│   ├── model_serving       # Model endpoints
│   ├── clusters            # Compute clusters
│   └── jobs                # Scheduled jobs
├── telemetry
│   ├── otel                # OpenTelemetry settings
│   └── exporters           # Delta Lake, MLflow, Console
├── uc_registry
│   ├── prompts             # Prompt versioning
│   ├── models              # Model registry
│   └── configs             # Config storage
├── memory
│   ├── short_term          # Working memory
│   ├── long_term           # Persistent memory
│   ├── context_window      # LLM context
│   └── embeddings          # Vector embeddings
├── reasoning
│   ├── trajectory_optimization
│   ├── distillation
│   ├── feedback_loops
│   └── rl_tuning
├── evaluation              # Benchmarking
├── visualization           # Viz settings
├── agents                  # Agent defaults
└── deployment
    └── environments        # Environment overrides
```

---

## Databricks Configuration

### Unity Catalog

```yaml
databricks:
  unity_catalog:
    enabled: true
    catalog_name: sota_agents
    schema_name: production
    
    # Volumes for storage
    volumes:
      prompts:
        name: prompts
        type: MANAGED
        comment: "Versioned prompts"
      
      configs:
        name: agent_configs
        type: MANAGED
    
    # Delta tables
    tables:
      telemetry:
        name: agent_telemetry
        partitioned_by: ["date"]
      
      trajectories:
        name: agent_trajectories
        partitioned_by: ["date", "agent_id"]
```

**Creates:**
- `/Volumes/sota_agents/production/prompts`
- `/Volumes/sota_agents/production/agent_configs`
- `sota_agents.production.agent_telemetry`
- `sota_agents.production.agent_trajectories`

### Model Serving

```yaml
databricks:
  model_serving:
    enabled: true
    endpoints:
      - name: sota-agent-llm
        model_name: gpt-4
        model_version: latest
        workload_size: Small  # Small, Medium, Large
        scale_to_zero: true
        min_replicas: 1
        max_replicas: 5
```

### Clusters

```yaml
databricks:
  clusters:
    agent_cluster:
      name: sota-agent-cluster
      spark_version: 13.3.x-scala2.12
      node_type_id: i3.xlarge
      autotermination_minutes: 30
      autoscale:
        min_workers: 1
        max_workers: 8
      libraries:
        - pypi:
            package: sota-agent-framework[all]
```

---

## Telemetry Configuration

### OpenTelemetry

```yaml
telemetry:
  enabled: true
  service_name: my-agent-service
  
  otel:
    traces:
      enabled: true
      sample_rate: 1.0  # 0.0 to 1.0
      batch_size: 100
      flush_interval_seconds: 30
    
    metrics:
      enabled: true
      export_interval_seconds: 60
```

### Exporters

```yaml
telemetry:
  exporters:
    # Delta Lake exporter
    delta_lake:
      enabled: true
      catalog: sota_agents
      schema: production
      table: agent_telemetry
      batch_size: 100
      flush_interval_seconds: 30
    
    # MLflow exporter
    mlflow:
      enabled: true
      tracking_uri: databricks
      experiment_name: /Users/${USER}/my-agents
    
    # Console exporter (dev only)
    console:
      enabled: false
```

---

## Memory Configuration

### Memory Types

```yaml
memory:
  enabled: true
  
  # Short-term (working memory)
  short_term:
    capacity: 20
    ttl_seconds: 3600
  
  # Long-term (persistent)
  long_term:
    capacity: 10000
    storage: delta_lake
    catalog: sota_agents
    schema: production
    table: agent_memory
```

### Context Window

```yaml
memory:
  context_window:
    max_tokens: 8000
    reservation: 0.2  # Reserve 20% for system
```

### Reflection & Forgetting

```yaml
memory:
  # Reflection
  reflection:
    enabled: true
    interval_hours: 24
    trigger_count: 100
  
  # Forgetting policies
  forgetting:
    enabled: true
    policies:
      - type: time_based
        max_age_days: 30
      - type: importance_based
        min_importance: LOW
      - type: capacity_based
        threshold: 0.9
```

### Embeddings

```yaml
memory:
  embeddings:
    provider: sentence_transformers  # or openai, databricks
    model: all-MiniLM-L6-v2
    cache_enabled: true
    cache_size: 10000
```

---

## Unity Catalog Registry

### Prompt Versioning

```yaml
uc_registry:
  prompts:
    catalog: sota_agents
    schema: production
    volume: prompts
    versioning:
      enabled: true
      auto_increment: true
      track_metrics: true
```

**Storage Location:**
```
/Volumes/sota_agents/production/prompts/
├── fraud_detector/
│   ├── v1/prompt.json
│   ├── v2/prompt.json
│   └── latest → v2
└── customer_support/
    └── v1/prompt.json
```

---

## Reasoning Optimization

### Trajectory Optimization

```yaml
reasoning:
  trajectory_optimization:
    enabled: true
    library_size: 1000  # Max trajectories to store
```

### CoT Distillation

```yaml
reasoning:
  distillation:
    enabled: true
    target_compression: 0.5  # Target 50% compression
    method: importance  # importance, summarization, dspy
```

### Feedback Loops

```yaml
reasoning:
  feedback_loops:
    enabled: true
    max_retries: 3
    min_improvement: 0.1
```

### Policies

```yaml
reasoning:
  policies:
    enabled: true
    cost_limit_tokens: 10000
    latency_limit_ms: 5000
```

---

## Environment-Specific Overrides

### Define Environments

```yaml
deployment:
  environments:
    dev:
      telemetry:
        otel:
          traces:
            sample_rate: 1.0  # Full sampling in dev
        exporters:
          console:
            enabled: true  # Console output in dev
      
      databricks:
        clusters:
          agent_cluster:
            autoscale:
              min_workers: 1
              max_workers: 2  # Smaller cluster in dev
    
    staging:
      telemetry:
        otel:
          traces:
            sample_rate: 0.5  # 50% sampling in staging
      
      databricks:
        unity_catalog:
          catalog_name: sota_agents_staging
    
    production:
      telemetry:
        otel:
          traces:
            sample_rate: 0.1  # 10% sampling in prod
      
      databricks:
        model_serving:
          endpoints:
            - name: sota-agent-llm-prod
              workload_size: Large
              scale_to_zero: false
              min_replicas: 2
```

### Select Environment

```python
# Via YAML
config = load_config("config/sota_config.yaml", environment="dev")

# Via environment variable
os.environ["SOTA_ENVIRONMENT"] = "staging"
config = load_config("config/sota_config.yaml")

# Via code
config = load_config("config/sota_config.yaml", environment="production")
```

---

## Environment Variables

### Substitution Syntax

Use `${VAR}` for environment variable substitution:

```yaml
databricks:
  workspace:
    host: ${DATABRICKS_HOST}
    token: ${DATABRICKS_TOKEN}

mlflow:
  experiment_name: /Users/${USER}/sota-agents

secrets:
  api_key: ${OPENAI_API_KEY}
```

### Set Variables

```bash
# In shell
export DATABRICKS_HOST="https://my-workspace.databricks.com"
export DATABRICKS_TOKEN="dapi..."
export USER="me@company.com"

# In Databricks
dbutils.widgets.text("DATABRICKS_HOST", "https://...")
```

---

## Databricks Integration

### Store Config in Unity Catalog

```python
# Upload to UC Volume
dbutils.fs.cp(
    "file:/Workspace/config/sota_config.yaml",
    "/Volumes/sota_agents/production/agent_configs/sota_config.yaml"
)

# Load from UC Volume
config = load_config("/Volumes/sota_agents/production/agent_configs/sota_config.yaml")
```

### Auto-Load from UC

The config loader automatically checks UC Volumes if file not found locally:

```python
# Automatically tries:
# 1. Local path
# 2. /Volumes/sota_agents/production/agent_configs/sota_config.yaml
config = load_config("sota_config.yaml")
```

---

## Terraform Integration

### Generate Terraform from YAML

```python
from infra.terraform_generator import generate_terraform

# Read YAML
config = load_config("config/sota_config.yaml")

# Generate Terraform
generate_terraform(config, output_dir="infra/generated/")
```

**Generates:**
- `main.tf` - Unity Catalog resources
- `clusters.tf` - Compute configuration
- `model_serving.tf` - Serving endpoints
- `variables.tf` - Terraform variables

### Apply Infrastructure

```bash
cd infra/generated/
terraform init
terraform apply
```

---

## Usage Examples

### Complete Workflow

```python
from shared.config_loader import load_config
from telemetry import init_telemetry
from uc_registry import PromptRegistry
from memory import MemoryManager
from reasoning import ReasoningOptimizer

# Load config (once at startup)
config = load_config("config/sota_config.yaml", environment="production")

# Initialize components (auto-use config)
init_telemetry()

# Create registry (uses uc_registry.prompts.* from YAML)
registry = PromptRegistry()

# Register prompt
registry.register_prompt("my_agent", "...")

# Create memory (uses memory.* from YAML)
memory = MemoryManager()

# Create optimizer (uses reasoning.* from YAML)
optimizer = ReasoningOptimizer(agent)

# All configured from YAML!
```

### Override at Runtime

```python
# Load config
config = load_config("config/sota_config.yaml")

# Override specific values
custom_config = config.to_dict()
custom_config["memory"]["short_term"]["capacity"] = 50

# Use custom config
memory = MemoryManager(config=custom_config)
```

---

## Best Practices

### 1. Version Control Configuration

```bash
git add config/sota_config.yaml
git commit -m "Update production config"
```

### 2. Separate Configs per Environment

```
config/
├── sota_config.yaml          # Base/shared config
├── dev_config.yaml           # Dev overrides
├── staging_config.yaml       # Staging overrides
└── production_config.yaml    # Production overrides
```

### 3. Secrets Management

**Don't store secrets in YAML:**
```yaml
# ❌ BAD
databricks:
  token: "dapi1234..."

# ✅ GOOD
databricks:
  token: ${DATABRICKS_TOKEN}
```

**Use Databricks Secrets:**
```python
token = dbutils.secrets.get(scope="sota-agents", key="databricks-token")
os.environ["DATABRICKS_TOKEN"] = token
```

### 4. Environment Detection

```yaml
# Auto-detect from env var
environment: ${SOTA_ENVIRONMENT:production}  # Default to production
```

### 5. Validate Configuration

```python
from shared.config_loader import load_config

try:
    config = load_config("config/sota_config.yaml")
    print("✅ Configuration valid")
except Exception as e:
    print(f"❌ Configuration error: {e}")
```

---

## Troubleshooting

### Config Not Found

```python
# Check search paths
from shared.config_loader import ConfigLoader

loader = ConfigLoader()
print(f"Project root: {loader._find_project_root()}")
print(f"In Databricks: {loader._in_databricks()}")
```

### Environment Variables Not Substituted

```bash
# Verify env vars are set
echo $DATABRICKS_HOST
echo $DATABRICKS_TOKEN

# Set if missing
export DATABRICKS_HOST="https://..."
```

### Wrong Environment Loaded

```python
# Check environment
config = load_config("config/sota_config.yaml")
print(f"Environment: {config.environment}")

# Force specific environment
config = load_config("config/sota_config.yaml", environment="dev")
```

---

## Next Steps

- **[Main Documentation](../README.md)** - Framework overview
- **[Databricks Deployment](DATABRICKS_DEPLOYMENT.md)** - Deploy to Databricks
- **[Infrastructure Guide](../infra/README.md)** - Terraform setup

---

**Everything is now YAML-configurable!** 🎉

