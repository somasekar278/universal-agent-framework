# 🧱 Databricks Deployment Guide - SOTA Agent Framework

**Complete guide to deploying agent solutions natively on Databricks.**

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Databricks Apps Deployment](#databricks-apps-deployment)
3. [Model Serving Integration](#model-serving-integration)
4. [Unity Catalog Integration](#unity-catalog-integration)
5. [Complete Architecture](#complete-architecture)
6. [Step-by-Step Deployment](#step-by-step-deployment)
7. [Configuration Management](#configuration-management)
8. [Monitoring & Observability](#monitoring--observability)
9. [Scaling & Performance](#scaling--performance)
10. [Production Best Practices](#production-best-practices)

---

## 🎯 Overview

### Why Databricks for Agent Deployment?

**Databricks provides a complete, integrated platform for AI agents:**

| Component | Databricks Solution | Framework Integration |
|-----------|-------------------|----------------------|
| **Agent Runtime** | Databricks Apps | FastAPI service with agent router |
| **LLM Inference** | Model Serving | Unified inference API |
| **Prompt Management** | Unity Catalog Volumes | Version-controlled prompts |
| **Model Registry** | Unity Catalog Models | Agent model versioning |
| **Configuration** | Unity Catalog Volumes | Environment configs |
| **Vector Store** | Lakebase (Vector Search) | Memory system integration |
| **Telemetry** | Delta Lake | Zerobus pattern for tracing |
| **Orchestration** | Workflows | LangGraph + Databricks Jobs |
| **Monitoring** | Databricks SQL + MLflow | Built-in dashboards |

### Production Architecture - Component Placement

**Where each component lives in production:**

| Plane | Where it lives | Details |
|-------|----------------|---------|
| **Agent Mesh (reasoning agents)** | Containers in **K8s hot pools** *or* **Databricks Apps hot pools** | Your custom agents running in managed containers |
| **A2A transport layer** | FastAPI/Starlette server **inside Databricks Apps container** | Peer-to-peer agent communication |
| **MCP servers** | FastAPI/Starlette **inside Databricks Apps container** | Tool/resource servers |
| **Agent memory** | Lakebase/Delta (UC tables), queried async | Vector embeddings + structured data |
| **LLM inference** | **Always-on Model Serving / external API** (no scale-to-zero) | Production-grade, low-latency inference |
| **Prompt optimization** | Offline Databricks Jobs (DSPy/TextGrad) | Batch optimization on schedules |
| **Monitoring** | OTEL from Apps → ZeroBus → Delta | Telemetry pipeline |

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                      Databricks Workspace                            │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │               Databricks Apps (Hot Pool)                       │ │
│  │  ┌─────────────────────────────────────────────────────────┐ │ │
│  │  │         Container (FastAPI/Starlette)                    │ │ │
│  │  │                                                           │ │ │
│  │  │  ┌──────────────────────────────────────────────────┐  │ │ │
│  │  │  │  Agent Mesh (Your Custom Agents)                 │  │ │ │
│  │  │  │  - FraudDetectorAgent                            │  │ │ │
│  │  │  │  - RiskScorerAgent                               │  │ │ │
│  │  │  │  - NarrativeAgent                                │  │ │ │
│  │  │  └──────────────────────────────────────────────────┘  │ │ │
│  │  │                      │                                   │ │ │
│  │  │  ┌──────────────────┴───────────────────────────────┐  │ │ │
│  │  │  │  A2A Server (Agent-to-Agent Communication)       │  │ │ │
│  │  │  │  - JSON-RPC 2.0 endpoint                         │  │ │ │
│  │  │  │  - Agent discovery                               │  │ │ │
│  │  │  └──────────────────────────────────────────────────┘  │ │ │
│  │  │                      │                                   │ │ │
│  │  │  ┌──────────────────┴───────────────────────────────┐  │ │ │
│  │  │  │  MCP Servers (Tools & Resources)                 │  │ │ │
│  │  │  │  - Tool discovery                                │  │ │ │
│  │  │  │  - Resource access                               │  │ │ │
│  │  │  └──────────────────────────────────────────────────┘  │ │ │
│  │  │                      │                                   │ │ │
│  │  │  ┌──────────────────┴───────────────────────────────┐  │ │ │
│  │  │  │  OTEL Instrumentation                            │  │ │ │
│  │  │  │  - Traces, Metrics, Logs                         │  │ │ │
│  │  │  └──────────────────────────────────────────────────┘  │ │ │
│  │  └─────────────────────────────────────────────────────────┘ │ │
│  └──────────┬──────────────┬────────────────┬──────────────────┘ │
│             │              │                │                      │
│             │              │                │                      │
└─────────────┼──────────────┼────────────────┼──────────────────────┘
              │              │                │
              │ (1) Inference│ (2) Memory    │ (3) Telemetry
              ▼              ▼                ▼
     ┌────────────────┐  ┌─────────────┐  ┌──────────────┐
     │ Model Serving  │  │  Lakebase   │  │ Delta Lake   │
     │ (Always-On)    │  │  + Delta    │  │  (ZeroBus)   │
     │                │  │  (UC Tables)│  │              │
     │ - DBRX         │  │             │  │ - Traces     │
     │ - MPT-7B       │  │ - Vectors   │  │ - Metrics    │
     │ - Custom       │  │ - Metadata  │  │ - Logs       │
     └────────────────┘  └─────────────┘  └──────────────┘
              │                                   │
              └───────────────┬───────────────────┘
                              ▼
                   ┌──────────────────────┐
                   │ Databricks SQL       │
                   │ Dashboards           │
                   └──────────────────────┘
                              
     ┌───────────────────────────────────────────────────────┐
     │  Offline: Databricks Jobs (Scheduled)                 │
     │  - DSPy prompt optimization                           │
     │  - TextGrad system prompt tuning                      │
     │  - Model fine-tuning pipelines                        │
     └───────────────────────────────────────────────────────┘
```

---

## 🏗️ Hot Pools vs. Cold Start

### Understanding Hot Pools

**Hot Pools** keep containers warm and ready to serve requests:

| Aspect | Hot Pool | Cold Start (Scale-to-Zero) |
|--------|----------|----------------------------|
| **Latency** | < 50ms | 5-30 seconds |
| **Cost** | Always running | Pay only when used |
| **Use Case** | Production agents | Dev/test environments |
| **Availability** | High | Medium |

**For production agent deployments, we recommend hot pools.**

### Databricks Apps Hot Pools

```yaml
# databricks-app.yml
compute:
  type: serverless
  min_instances: 2      # Always keep 2 containers warm (hot pool)
  max_instances: 20     # Scale up to 20 under load
  scale_to_zero: false  # Never scale to zero
  warm_up_time: 30s     # How long to prepare a new instance
```

**Why hot pools for agents?**
- ✅ Sub-second response times
- ✅ No cold start delays for reasoning chains
- ✅ Persistent in-memory caches (prompts, configs)
- ✅ Stable WebSocket/A2A connections

---

## 📦 Single Container Architecture

### All-in-One Container Design

**Your Databricks App runs a single container with multiple services:**

```
┌────────────────────────────────────────────────────────┐
│  Databricks Apps Container (FastAPI/Starlette)        │
│                                                        │
│  Port 8000: Main FastAPI App                          │
│  ├─ /execute          → AgentRouter                   │
│  ├─ /health           → Health checks                 │
│  ├─ /metrics          → Prometheus metrics            │
│  │                                                     │
│  Port 8001: A2A Server                                │
│  ├─ /a2a/rpc          → JSON-RPC 2.0 endpoint        │
│  ├─ /a2a/discover     → Agent discovery               │
│  │                                                     │
│  Port 8002: MCP Server                                │
│  ├─ /mcp/tools        → Tool discovery                │
│  ├─ /mcp/resources    → Resource access               │
│  │                                                     │
│  Background Workers                                    │
│  ├─ OTEL batch exporter (every 10s)                  │
│  ├─ Memory consolidation (every 5m)                  │
│  └─ Health check pings (every 30s)                   │
└────────────────────────────────────────────────────────┘
```

### Implementation: Multi-Port FastAPI

```python
# app.py - Single container with multiple services
from fastapi import FastAPI
from starlette.applications import Starlette
from starlette.routing import Mount
import uvicorn
from multiprocessing import Process

# Import your services
from services.api import create_agent_api
from agents.a2a.server import create_a2a_server
from agents.mcp_server import create_mcp_server
from telemetry.otel_tracer import start_telemetry_worker

# Main agent API (port 8000)
agent_app = create_agent_api()

# A2A server (port 8001)
a2a_app = create_a2a_server()

# MCP server (port 8002)
mcp_app = create_mcp_server()

def run_agent_api():
    """Run main agent API."""
    uvicorn.run(agent_app, host="0.0.0.0", port=8000)

def run_a2a_server():
    """Run A2A transport layer."""
    uvicorn.run(a2a_app, host="0.0.0.0", port=8001)

def run_mcp_server():
    """Run MCP tool server."""
    uvicorn.run(mcp_app, host="0.0.0.0", port=8002)

if __name__ == "__main__":
    # Start background telemetry worker
    start_telemetry_worker()
    
    # Start all servers in parallel
    processes = [
        Process(target=run_agent_api),
        Process(target=run_a2a_server),
        Process(target=run_mcp_server)
    ]
    
    for p in processes:
        p.start()
    
    for p in processes:
        p.join()
```

**Alternative: Single Port with Path Routing**

```python
# app.py - Single port, path-based routing
from fastapi import FastAPI
from starlette.routing import Mount

app = FastAPI()

# Mount sub-applications
app.mount("/api", create_agent_api())
app.mount("/a2a", create_a2a_server())
app.mount("/mcp", create_mcp_server())

# All accessible on port 8000:
# - http://your-app.databricks.com/api/execute
# - http://your-app.databricks.com/a2a/rpc
# - http://your-app.databricks.com/mcp/tools
```

---

## 🚀 Databricks Apps Deployment

### What are Databricks Apps?

**Databricks Apps** are serverless web applications that run directly in your Databricks workspace:

- ✅ **Native Integration** - Direct access to Unity Catalog, Model Serving, Delta Lake
- ✅ **Scalable** - Auto-scaling compute resources
- ✅ **Secure** - Built-in authentication, RBAC
- ✅ **Cost-Effective** - Pay only for compute used
- ✅ **Simple Deployment** - Git integration, CI/CD ready

### Framework Integration

Your SOTA agent solution becomes a Databricks App:

```python
# app.py - Databricks App entry point
from databricks.sdk import WorkspaceClient
from agents import AgentRouter
from services.api import create_app

# Initialize Databricks client
w = WorkspaceClient()

# Load configuration from Unity Catalog
config = load_config_from_uc(
    volume_path="/Volumes/main/agents/configs/sota_config.yaml"
)

# Initialize agent router with Databricks integrations
router = AgentRouter(
    config=config,
    model_serving_endpoint="databricks-dbrx-instruct",  # Model Serving
    vector_search_index="main.agents.memory_index",      # Lakebase
    telemetry_table="main.agents.telemetry"              # Delta Lake
)

# Create FastAPI app
app = create_app(router)

# Databricks Apps will serve this
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### App Configuration File

```yaml
# databricks-app.yml
name: fraud-detection-agent
description: Fraud detection agent with memory and reasoning

# Compute configuration
compute:
  type: serverless
  min_instances: 1
  max_instances: 10
  auto_scale: true

# Environment variables (from secrets)
env:
  - name: DATABRICKS_HOST
    value: ${workspace.host}
  - name: DATABRICKS_TOKEN
    secret: agents/databricks-token

# Unity Catalog access
unity_catalog:
  catalogs:
    - main
  schemas:
    - main.agents
  volumes:
    - main.agents.configs
    - main.agents.prompts

# Model Serving endpoints
model_serving:
  endpoints:
    - databricks-dbrx-instruct
    - databricks-mpt-7b-instruct

# Source code
source:
  git:
    url: https://github.com/yourorg/fraud-detection-agent
    branch: main
    path: /
```

### Deployment Commands

```bash
# Method 1: Using Databricks CLI
databricks apps create --config databricks-app.yml

# Method 2: Using Python SDK
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

app = w.apps.create(
    name="fraud-detection-agent",
    source_code_path="/Workspace/apps/fraud-detection-agent",
    compute={"size": "Small"},
    description="SOTA Agent Framework deployment"
)

print(f"App created: {app.url}")

# Method 3: Using sota-deploy CLI
sota-deploy init --platform databricks-app
sota-deploy apply --environment production
```

### App Structure

```
fraud-detection-agent/
├── app.py                      # Main entry point
├── databricks-app.yml          # App configuration
├── requirements.txt            # Python dependencies
├── agents/                     # Your custom agents
│   ├── __init__.py
│   └── fraud_detector.py
├── config/
│   └── sota_config.yaml        # Framework config (synced to UC)
├── services/
│   └── api.py                  # FastAPI routes
└── notebooks/                  # Optional: Databricks notebooks
    └── setup_uc.py            # UC initialization
```

---

## 🤖 Model Serving Integration

### Overview

**Databricks Model Serving** provides scalable, production-ready LLM endpoints:

- ✅ **Foundation Models** - DBRX, MPT, Llama, Mistral
- ✅ **Custom Models** - Fine-tuned models from MLflow
- ✅ **Auto-scaling** - Scale to zero when idle
- ✅ **Multi-model** - Serve multiple models on same endpoint
- ✅ **A/B Testing** - Traffic splitting between model versions

### Creating Model Serving Endpoints

#### Production Configuration: Always-On (No Scale-to-Zero)

**For production agent systems, always keep Model Serving endpoints running:**

✅ **Why always-on?**
- **Low latency**: Sub-second response times (no cold start)
- **Predictable performance**: No variability from cold starts
- **Reasoning chains**: Multi-turn agent conversations require fast responses
- **Cost predictability**: Fixed costs, easier to budget

❌ **When NOT to use scale-to-zero:**
- Production workloads with latency SLAs
- Interactive agent conversations
- High-frequency inference (agents making multiple LLM calls)

#### Option 1: Foundation Models (DBRX, MPT) - Always-On

```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import (
    EndpointCoreConfigInput,
    ServedEntityInput,
    AutoCaptureConfigInput
)

w = WorkspaceClient()

# Create endpoint for DBRX-Instruct (PRODUCTION CONFIG)
endpoint = w.serving_endpoints.create(
    name="fraud-agent-llm",
    config=EndpointCoreConfigInput(
        served_entities=[
            ServedEntityInput(
                entity_name="databricks-dbrx-instruct",
                entity_version="1",
                workload_size="Medium",  # Medium or Large for production
                scale_to_zero_enabled=False,  # ⚠️ ALWAYS-ON for production
                min_provisioned_throughput=100,  # Min tokens/sec
                max_provisioned_throughput=2000  # Max tokens/sec
            )
        ],
        # Enable request/response logging
        auto_capture_config=AutoCaptureConfigInput(
            catalog_name="main",
            schema_name="agents",
            table_name_prefix="llm_inference"
        )
    )
)

print(f"Endpoint created: {endpoint.name}")
print(f"URL: {endpoint.config.served_entities[0].serving_url}")
print(f"⚠️ Always-on: scale_to_zero_enabled=False")
```

**Sizing Guidelines:**

| Workload | Workload Size | Throughput | Concurrent Requests |
|----------|---------------|------------|---------------------|
| **Dev/Test** | Small | 10-50 tok/s | 1-5 |
| **Production (Low)** | Medium | 100-500 tok/s | 5-20 |
| **Production (High)** | Large | 500-2000 tok/s | 20-100 |
| **Enterprise** | X-Large | 2000+ tok/s | 100+ |

#### Option 2: Custom Fine-tuned Models

```python
# Register model to Unity Catalog
import mlflow

mlflow.set_registry_uri("databricks-uc")

# Log model
with mlflow.start_run():
    mlflow.pyfunc.log_model(
        artifact_path="model",
        python_model=YourCustomAgent(),
        registered_model_name="main.agents.fraud_detector_v1"
    )

# Create serving endpoint
endpoint = w.serving_endpoints.create(
    name="fraud-agent-custom",
    config=EndpointCoreConfigInput(
        served_entities=[
            ServedEntityInput(
                entity_name="main.agents.fraud_detector_v1",
                entity_version="1",  # Or use alias: "Champion"
                workload_size="Medium",
                scale_to_zero_enabled=True
            )
        ]
    )
)
```

### Framework Integration

**Unified Model Serving Client:**

```python
# services/model_serving_client.py
from databricks.sdk import WorkspaceClient
from typing import Dict, Any, List, Optional
import asyncio

class ModelServingClient:
    """
    Unified client for Databricks Model Serving.
    
    Supports:
    - Foundation models (DBRX, MPT, Llama)
    - Custom models from MLflow/UC
    - Multi-model routing
    - Automatic retries and fallback
    """
    
    def __init__(
        self,
        workspace_client: Optional[WorkspaceClient] = None,
        default_endpoint: str = "databricks-dbrx-instruct"
    ):
        self.client = workspace_client or WorkspaceClient()
        self.default_endpoint = default_endpoint
    
    async def predict(
        self,
        prompt: str,
        endpoint: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Call model serving endpoint.
        
        Args:
            prompt: Input prompt
            endpoint: Endpoint name (defaults to default_endpoint)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional model parameters
            
        Returns:
            Model response dict
        """
        endpoint = endpoint or self.default_endpoint
        
        # Format request based on model type
        if "dbrx" in endpoint.lower() or "mpt" in endpoint.lower():
            # Foundation model format
            request = {
                "prompt": prompt,
                "temperature": temperature,
                "max_tokens": max_tokens,
                **kwargs
            }
        else:
            # Custom model format (depends on your model)
            request = {
                "inputs": prompt,
                "params": {
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    **kwargs
                }
            }
        
        # Call endpoint
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.serving_endpoints.query(
                name=endpoint,
                inputs=request
            )
        )
        
        return {
            "text": response.predictions[0],
            "endpoint": endpoint,
            "metadata": response.metadata
        }
    
    async def predict_batch(
        self,
        prompts: List[str],
        endpoint: Optional[str] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Batch prediction for multiple prompts."""
        tasks = [
            self.predict(prompt, endpoint, **kwargs)
            for prompt in prompts
        ]
        return await asyncio.gather(*tasks)
    
    async def get_embeddings(
        self,
        texts: List[str],
        endpoint: str = "databricks-mpt-7b-instruct"
    ) -> List[List[float]]:
        """Get embeddings from model serving."""
        response = await self.predict_batch(
            prompts=texts,
            endpoint=endpoint,
            return_embeddings=True
        )
        return [r["embedding"] for r in response]
```

### Using Model Serving in Agents

```python
# agents/fraud_detector.py
from agents.base import CriticalPathAgent
from services.model_serving_client import ModelServingClient
from shared.schemas import AgentInput, AgentOutput

class FraudDetectorAgent(CriticalPathAgent):
    """
    Fraud detection agent using Databricks Model Serving.
    """
    
    def __init__(self, config: dict):
        super().__init__(config)
        
        # Initialize model serving client
        self.model_client = ModelServingClient(
            default_endpoint=config.get("llm_endpoint", "databricks-dbrx-instruct")
        )
        
        # Load prompt from Unity Catalog
        self.prompt_template = self._load_prompt_from_uc(
            "main.agents.prompts.fraud_detection_v2"
        )
    
    async def process(self, request: AgentInput) -> AgentOutput:
        """
        Process transaction through fraud detection.
        """
        transaction = request.data
        
        # Format prompt
        prompt = self.prompt_template.format(
            amount=transaction["amount"],
            merchant=transaction["merchant"],
            location=transaction["location"],
            history=transaction.get("history", "")
        )
        
        # Call Model Serving
        response = await self.model_client.predict(
            prompt=prompt,
            endpoint="fraud-agent-llm",  # Your serving endpoint
            temperature=0.3,  # Low temp for consistency
            max_tokens=300
        )
        
        # Parse response
        fraud_score = self._extract_score(response["text"])
        narrative = self._extract_narrative(response["text"])
        
        return AgentOutput(
            agent_name=self.agent_id,
            result={
                "fraud_score": fraud_score,
                "narrative": narrative,
                "confidence": 0.95,
                "model_endpoint": response["endpoint"]
            },
            confidence=0.95,
            metadata={
                "model_used": response["endpoint"],
                "tokens_used": response["metadata"].get("tokens"),
                "latency_ms": response["metadata"].get("latency_ms")
            }
        )
```

### Multi-Model Strategy

```python
# services/model_router.py
from typing import Dict, Any

class ModelRouter:
    """
    Route requests to different model serving endpoints based on requirements.
    """
    
    ENDPOINT_MAP = {
        "fast": "databricks-mpt-7b-instruct",      # 7B model, faster
        "quality": "databricks-dbrx-instruct",     # DBRX, higher quality
        "custom": "fraud-agent-custom",             # Fine-tuned model
        "embeddings": "databricks-mpt-7b-instruct" # For embeddings
    }
    
    def __init__(self, model_client: ModelServingClient):
        self.client = model_client
    
    async def route(
        self,
        prompt: str,
        priority: str = "quality",  # fast, quality, custom
        **kwargs
    ) -> Dict[str, Any]:
        """Route to appropriate endpoint based on priority."""
        
        endpoint = self.ENDPOINT_MAP.get(priority, self.ENDPOINT_MAP["quality"])
        
        try:
            return await self.client.predict(prompt, endpoint, **kwargs)
        except Exception as e:
            # Fallback to fast model if quality fails
            if priority == "quality":
                return await self.client.predict(
                    prompt,
                    self.ENDPOINT_MAP["fast"],
                    **kwargs
                )
            raise
```

---

## 📁 Unity Catalog Integration

### Overview

**Unity Catalog (UC)** is the central metadata and governance layer:

```
Unity Catalog
├── main (Catalog)
    ├── agents (Schema)
        ├── configs/ (Volume)
        │   ├── sota_config.yaml
        │   ├── sota_config.production.yaml
        │   └── agents.yaml
        │
        ├── prompts/ (Volume)
        │   ├── fraud_detection_v1.txt
        │   ├── fraud_detection_v2.txt
        │   ├── risk_scoring_v1.txt
        │   └── narrative_generation_v1.txt
        │
        ├── models/ (Models)
        │   ├── fraud_detector_v1 (registered model)
        │   ├── fraud_detector_v2
        │   └── risk_scorer_v1
        │
        ├── memory_index (Vector Search Index)
        │   └── embeddings table → Delta Lake
        │
        └── telemetry (Table)
            ├── agent_executions
            ├── model_inference_logs
            └── performance_metrics
```

### Setting Up Unity Catalog

#### Create Catalog Structure

```python
# notebooks/setup_unity_catalog.py
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

# 1. Create catalog (if not exists)
try:
    w.catalogs.create(name="main", comment="Main production catalog")
except Exception:
    print("Catalog 'main' already exists")

# 2. Create schema for agents
w.schemas.create(
    catalog_name="main",
    name="agents",
    comment="SOTA Agent Framework artifacts"
)

# 3. Create volumes for configs and prompts
w.volumes.create(
    catalog_name="main",
    schema_name="agents",
    name="configs",
    volume_type="MANAGED",
    comment="Agent configuration files"
)

w.volumes.create(
    catalog_name="main",
    schema_name="agents",
    name="prompts",
    volume_type="MANAGED",
    comment="Prompt templates (versioned)"
)

# 4. Create tables for telemetry
w.tables.create(
    catalog_name="main",
    schema_name="agents",
    name="telemetry",
    table_type="MANAGED",
    columns=[
        {"name": "timestamp", "type_name": "TIMESTAMP"},
        {"name": "agent_id", "type_name": "STRING"},
        {"name": "execution_id", "type_name": "STRING"},
        {"name": "input_data", "type_name": "STRING"},
        {"name": "output_data", "type_name": "STRING"},
        {"name": "latency_ms", "type_name": "DOUBLE"},
        {"name": "success", "type_name": "BOOLEAN"},
        {"name": "error_message", "type_name": "STRING"}
    ],
    comment="Agent execution telemetry"
)

print("✅ Unity Catalog structure created")
```

### Syncing Configuration to UC

```python
# scripts/sync_config_to_uc.py
from databricks.sdk import WorkspaceClient
from pathlib import Path

def sync_configs_to_uc(local_config_dir: Path, uc_volume_path: str):
    """
    Sync local config files to Unity Catalog Volumes.
    
    Args:
        local_config_dir: Local directory with configs
        uc_volume_path: UC volume path (e.g., /Volumes/main/agents/configs/)
    """
    w = WorkspaceClient()
    
    for config_file in local_config_dir.glob("*.yaml"):
        # Read local file
        content = config_file.read_text()
        
        # Write to UC Volume
        uc_path = f"{uc_volume_path}/{config_file.name}"
        w.files.upload(
            file_path=uc_path,
            contents=content.encode(),
            overwrite=True
        )
        
        print(f"✅ Synced {config_file.name} to {uc_path}")

# Usage
sync_configs_to_uc(
    local_config_dir=Path("config/"),
    uc_volume_path="/Volumes/main/agents/configs"
)
```

### Loading Configuration from UC

```python
# config/uc_loader.py
from databricks.sdk import WorkspaceClient
import yaml
from typing import Dict, Any

class UCConfigLoader:
    """Load configuration from Unity Catalog Volumes."""
    
    def __init__(self, workspace_client: Optional[WorkspaceClient] = None):
        self.client = workspace_client or WorkspaceClient()
    
    def load_config(
        self,
        uc_path: str,
        environment: str = "production"
    ) -> Dict[str, Any]:
        """
        Load config from UC Volume.
        
        Args:
            uc_path: UC volume path (e.g., /Volumes/main/agents/configs/sota_config.yaml)
            environment: Environment name for overrides
            
        Returns:
            Merged configuration dict
        """
        # Load base config
        base_config = self._load_file(uc_path)
        
        # Load environment-specific overrides
        env_path = uc_path.replace(".yaml", f".{environment}.yaml")
        try:
            env_config = self._load_file(env_path)
            # Deep merge
            base_config = self._deep_merge(base_config, env_config)
        except FileNotFoundError:
            pass
        
        return base_config
    
    def _load_file(self, uc_path: str) -> Dict[str, Any]:
        """Load YAML file from UC."""
        response = self.client.files.download(uc_path)
        content = response.contents.read().decode()
        return yaml.safe_load(content)
    
    def _deep_merge(self, base: dict, override: dict) -> dict:
        """Deep merge two dicts."""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

# Usage in app.py
loader = UCConfigLoader()
config = loader.load_config(
    uc_path="/Volumes/main/agents/configs/sota_config.yaml",
    environment="production"
)
```

### Prompt Management in UC

```python
# services/prompt_manager.py
from databricks.sdk import WorkspaceClient
from typing import Optional
from datetime import datetime

class PromptManager:
    """
    Manage prompt templates in Unity Catalog Volumes.
    
    Features:
    - Version control (v1, v2, etc.)
    - Rollback capability
    - A/B testing support
    """
    
    def __init__(self, workspace_client: Optional[WorkspaceClient] = None):
        self.client = workspace_client or WorkspaceClient()
        self.base_path = "/Volumes/main/agents/prompts"
    
    def get_prompt(
        self,
        prompt_name: str,
        version: Optional[str] = None
    ) -> str:
        """
        Get prompt template from UC.
        
        Args:
            prompt_name: Name of prompt (e.g., "fraud_detection")
            version: Version (e.g., "v2") or None for latest
            
        Returns:
            Prompt template string
        """
        if version:
            file_name = f"{prompt_name}_{version}.txt"
        else:
            # Get latest version
            file_name = self._get_latest_version(prompt_name)
        
        uc_path = f"{self.base_path}/{file_name}"
        response = self.client.files.download(uc_path)
        return response.contents.read().decode()
    
    def save_prompt(
        self,
        prompt_name: str,
        content: str,
        version: str
    ):
        """Save new prompt version to UC."""
        file_name = f"{prompt_name}_{version}.txt"
        uc_path = f"{self.base_path}/{file_name}"
        
        self.client.files.upload(
            file_path=uc_path,
            contents=content.encode(),
            overwrite=True
        )
        
        print(f"✅ Saved prompt: {uc_path}")
    
    def _get_latest_version(self, prompt_name: str) -> str:
        """Get latest version file name for a prompt."""
        files = self.client.files.list_directory_contents(self.base_path)
        
        # Filter files for this prompt
        prompt_files = [
            f for f in files
            if f.name.startswith(f"{prompt_name}_v")
        ]
        
        if not prompt_files:
            raise FileNotFoundError(f"No prompts found for {prompt_name}")
        
        # Sort by version number
        prompt_files.sort(key=lambda x: x.name, reverse=True)
        return prompt_files[0].name

# Usage in agents
prompt_manager = PromptManager()

# Get latest version
prompt = prompt_manager.get_prompt("fraud_detection")

# Get specific version
prompt_v1 = prompt_manager.get_prompt("fraud_detection", version="v1")

# Save new version
prompt_manager.save_prompt(
    prompt_name="fraud_detection",
    content="You are a fraud detection expert...",
    version="v3"
)
```

### Agent Memory: Async Access to Lakebase + Delta

**Agent memory uses async patterns to avoid blocking the agent execution:**

```
Agent receives request
    ↓
    ├─→ [Async] Query Lakebase for relevant memories (vector similarity)
    ├─→ [Async] Query Delta for structured metadata
    ↓
Wait for both (asyncio.gather)
    ↓
Combine results → Continue agent reasoning
```

#### Async Memory Access Implementation

```python
# memory/databricks_vector_store.py
from databricks.sdk import WorkspaceClient
from databricks.vector_search.client import VectorSearchClient
from typing import List, Dict, Any, Optional
import asyncio

class DatabricksVectorStore:
    """
    Vector store using Databricks Vector Search (Lakebase) + Delta Lake.
    
    Key Features:
    - Async queries (non-blocking)
    - Vector similarity (Lakebase)
    - Structured metadata (Delta Lake)
    - Automatic embedding via Model Serving
    """
    
    def __init__(
        self,
        index_name: str = "main.agents.memory_index",
        delta_table: str = "main.agents.memory_metadata",
        embedding_endpoint: str = "databricks-mpt-7b-instruct"
    ):
        self.vector_client = VectorSearchClient()
        self.workspace_client = WorkspaceClient()
        self.index_name = index_name
        self.delta_table = delta_table
        self.embedding_endpoint = embedding_endpoint
    
    async def store(
        self,
        text: str,
        metadata: Dict[str, Any],
        agent_id: str
    ):
        """
        Store memory asynchronously.
        
        Writes to:
        1. Lakebase (vector embeddings)
        2. Delta Lake (structured metadata)
        """
        memory_id = f"{agent_id}_{metadata['timestamp']}"
        
        # Get embedding asynchronously
        embedding = await self._get_embedding(text)
        
        # Store in parallel
        await asyncio.gather(
            self._store_vector(memory_id, text, embedding, agent_id),
            self._store_metadata(memory_id, metadata)
        )
    
    async def _store_vector(
        self,
        memory_id: str,
        text: str,
        embedding: List[float],
        agent_id: str
    ):
        """Store vector in Lakebase."""
        loop = asyncio.get_event_loop()
        
        # Run sync client in thread pool
        await loop.run_in_executor(
            None,
            lambda: self.vector_client.get_index(self.index_name).upsert(
                documents=[{
                    "id": memory_id,
                    "text": text,
                    "embedding": embedding,
                    "agent_id": agent_id
                }]
            )
        )
    
    async def _store_metadata(self, memory_id: str, metadata: Dict[str, Any]):
        """Store metadata in Delta Lake."""
        import json
        
        sql = f"""
        INSERT INTO {self.delta_table} (id, metadata, timestamp)
        VALUES ('{memory_id}', '{json.dumps(metadata)}', CURRENT_TIMESTAMP())
        """
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: self.workspace_client.statement_execution.execute_statement(
                warehouse_id=self.workspace_client.config.warehouse_id,
                statement=sql
            )
        )
    
    async def retrieve(
        self,
        query: str,
        agent_id: Optional[str] = None,
        top_k: int = 5,
        include_metadata: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Retrieve similar memories asynchronously.
        
        Queries:
        1. Lakebase (vector similarity)
        2. Delta Lake (metadata) - if include_metadata=True
        """
        # Get query embedding
        query_embedding = await self._get_embedding(query)
        
        # Query Lakebase for similar vectors
        vector_results = await self._query_vectors(
            query_embedding,
            agent_id,
            top_k
        )
        
        if not include_metadata:
            return vector_results
        
        # Enrich with metadata from Delta Lake
        memory_ids = [r["id"] for r in vector_results]
        metadata_map = await self._query_metadata(memory_ids)
        
        # Combine results
        for result in vector_results:
            result["metadata"] = metadata_map.get(result["id"], {})
        
        return vector_results
    
    async def _query_vectors(
        self,
        query_embedding: List[float],
        agent_id: Optional[str],
        top_k: int
    ) -> List[Dict[str, Any]]:
        """Query Lakebase vector index."""
        loop = asyncio.get_event_loop()
        
        filters = {"agent_id": agent_id} if agent_id else None
        
        results = await loop.run_in_executor(
            None,
            lambda: self.vector_client.get_index(self.index_name).similarity_search(
                query_vector=query_embedding,
                filters=filters,
                num_results=top_k
            )
        )
        
        return [
            {
                "id": r["id"],
                "text": r["text"],
                "score": r["score"]
            }
            for r in results["result"]["data_array"]
        ]
    
    async def _query_metadata(
        self,
        memory_ids: List[str]
    ) -> Dict[str, Dict[str, Any]]:
        """Query Delta Lake for metadata."""
        import json
        
        ids_str = ", ".join([f"'{id}'" for id in memory_ids])
        sql = f"SELECT id, metadata FROM {self.delta_table} WHERE id IN ({ids_str})"
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: self.workspace_client.statement_execution.execute_statement(
                warehouse_id=self.workspace_client.config.warehouse_id,
                statement=sql
            )
        )
        
        # Parse results
        metadata_map = {}
        if result.result and result.result.data_array:
            for row in result.result.data_array:
                memory_id = row[0]
                metadata = json.loads(row[1])
                metadata_map[memory_id] = metadata
        
        return metadata_map
    
    async def _get_embedding(self, text: str) -> List[float]:
        """Get embedding from Model Serving (always-on endpoint)."""
        from services.model_serving_client import ModelServingClient
        
        client = ModelServingClient()
        embeddings = await client.get_embeddings(
            texts=[text],
            endpoint=self.embedding_endpoint
        )
        return embeddings[0]

# Usage in agents
class FraudDetectorAgent(CriticalPathAgent):
    def __init__(self, config: dict):
        super().__init__(config)
        self.memory = DatabricksVectorStore()
    
    async def process(self, request: AgentInput) -> AgentOutput:
        # Retrieve relevant memories asynchronously (non-blocking)
        similar_cases = await self.memory.retrieve(
            query=f"transaction {request.data['transaction_id']}",
            agent_id=self.agent_id,
            top_k=5
        )
        
        # Continue with reasoning...
        # (memory retrieval didn't block the agent)
```

---

## 🔧 Offline Prompt Optimization (Databricks Jobs)

**Prompt optimization runs offline as scheduled Databricks Jobs, not in the hot path:**

### Why Offline?

| Aspect | Offline (Databricks Jobs) | Online (in agent) |
|--------|---------------------------|-------------------|
| **Performance** | Doesn't block agent execution | Would add 10-60s latency |
| **Cost** | Batch processing, efficient | Expensive per-request |
| **Quality** | More iterations, better results | Limited iterations |
| **Timing** | Scheduled (nightly, weekly) | Every agent call |

### Architecture: Offline Optimization

```
┌────────────────────────────────────────────────────────────┐
│  Databricks Jobs (Scheduled - e.g., nightly at 2am)       │
│                                                            │
│  Job 1: DSPy Task Prompt Optimization                     │
│  ├─ Load training examples from Delta Lake                │
│  ├─ Run DSPy optimization (MIPRO, BootstrapFewShot)      │
│  ├─ Evaluate optimized prompts                            │
│  └─ Save best prompt to UC Volume (/prompts/v3.txt)      │
│                                                            │
│  Job 2: TextGrad System Prompt Optimization              │
│  ├─ Load agent traces from telemetry                      │
│  ├─ Run TextGrad gradient descent                         │
│  ├─ Evaluate system prompt variants                       │
│  └─ Save optimized system prompt to UC                    │
│                                                            │
│  Job 3: A/B Test Evaluation                               │
│  ├─ Compare v2 vs v3 prompts on holdout set              │
│  ├─ Compute metrics (accuracy, latency, cost)            │
│  └─ Decide: promote v3 to production or rollback         │
└────────────────────────────────────────────────────────────┘
         │
         ▼ (saves to)
┌────────────────────────────────────────────────────────────┐
│  Unity Catalog Volumes: /main/agents/prompts/             │
│  ├─ fraud_detection_v2.txt  (current production)          │
│  ├─ fraud_detection_v3.txt  (newly optimized)             │
│  └─ fraud_detection_v3_metadata.json  (metrics)           │
└────────────────────────────────────────────────────────────┘
         │
         ▼ (agents read from)
┌────────────────────────────────────────────────────────────┐
│  Databricks Apps (Hot Pool)                               │
│  - Agents load prompts from UC at startup                 │
│  - Periodically refresh (every 5 minutes)                 │
│  - No optimization overhead in hot path                   │
└────────────────────────────────────────────────────────────┘
```

### Implementation: DSPy Optimization Job

```python
# jobs/optimize_prompts_dspy.py
import dspy
from databricks.sdk import WorkspaceClient
from datetime import datetime
import mlflow

def optimize_fraud_detection_prompt():
    """
    Databricks Job: Optimize fraud detection prompt using DSPy.
    
    Runs: Nightly at 2am
    Duration: ~30-60 minutes
    Cost: Batch compute (cost-effective)
    """
    
    # Initialize
    w = WorkspaceClient()
    mlflow.set_experiment("/Shared/agent-optimization/fraud-detection")
    
    # 1. Load training examples from Delta Lake
    training_data = spark.sql("""
        SELECT 
            transaction_data as input,
            expert_decision as expected_output
        FROM main.agents.training_examples
        WHERE agent_id = 'fraud_detector'
        AND timestamp >= CURRENT_DATE - INTERVAL 30 DAYS
    """).toPandas()
    
    print(f"Loaded {len(training_data)} training examples")
    
    # 2. Set up DSPy with Databricks Model Serving
    lm = dspy.Databricks(
        model="databricks-dbrx-instruct",
        endpoint="fraud-agent-llm"
    )
    dspy.settings.configure(lm=lm)
    
    # 3. Define signature
    class FraudDetection(dspy.Signature):
        """Detect fraudulent transactions."""
        transaction = dspy.InputField()
        fraud_score = dspy.OutputField(desc="0.0-1.0 fraud probability")
        reasoning = dspy.OutputField(desc="Explanation of decision")
    
    # 4. Compile with optimizer
    fraud_detector = dspy.ChainOfThought(FraudDetection)
    
    optimizer = dspy.MIPROv2(
        metric=fraud_detection_metric,
        num_candidates=10,
        init_temperature=1.0
    )
    
    # 5. Optimize (this takes 30-60 minutes)
    with mlflow.start_run(run_name=f"optimization_{datetime.now().isoformat()}"):
        optimized_program = optimizer.compile(
            fraud_detector,
            trainset=training_data,
            num_trials=50
        )
        
        # Log metrics
        mlflow.log_metric("num_examples", len(training_data))
        mlflow.log_metric("num_trials", 50)
    
    # 6. Save optimized prompt to Unity Catalog
    optimized_prompt = optimized_program.extended_signature
    
    version = f"v{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    uc_path = f"/Volumes/main/agents/prompts/fraud_detection_{version}.txt"
    
    w.files.upload(
        file_path=uc_path,
        contents=optimized_prompt.encode(),
        overwrite=False
    )
    
    print(f"✅ Optimized prompt saved to {uc_path}")
    
    # 7. Evaluate on holdout set
    holdout_data = spark.sql("""
        SELECT * FROM main.agents.holdout_examples
        WHERE agent_id = 'fraud_detector'
    """).toPandas()
    
    accuracy = evaluate_prompt(optimized_program, holdout_data)
    
    mlflow.log_metric("holdout_accuracy", accuracy)
    
    print(f"✅ Optimization complete. Accuracy: {accuracy:.2%}")
    print(f"Next: Run A/B test to compare with current production prompt")

def fraud_detection_metric(example, prediction):
    """Metric for DSPy optimization."""
    expected = float(example.expected_output["fraud_score"])
    predicted = float(prediction.fraud_score)
    
    # Penalize large errors
    error = abs(expected - predicted)
    return 1.0 - error

# Databricks Job entry point
if __name__ == "__main__":
    optimize_fraud_detection_prompt()
```

### Databricks Job Configuration

```json
{
  "name": "Optimize Fraud Detection Prompt",
  "tasks": [
    {
      "task_key": "optimize_dspy",
      "description": "Run DSPy optimization on fraud detection prompt",
      "python_wheel_task": {
        "package_name": "fraud_agent",
        "entry_point": "jobs.optimize_prompts_dspy",
        "parameters": []
      },
      "new_cluster": {
        "spark_version": "14.3.x-scala2.12",
        "node_type_id": "i3.xlarge",
        "num_workers": 4,
        "spark_conf": {
          "spark.databricks.delta.preview.enabled": "true"
        }
      },
      "libraries": [
        {"pypi": {"package": "dspy-ai>=2.4.0"}},
        {"pypi": {"package": "sota-agent-framework[optimization]"}}
      ]
    }
  ],
  "schedule": {
    "quartz_cron_expression": "0 0 2 * * ?",
    "timezone_id": "America/Los_Angeles",
    "pause_status": "UNPAUSED"
  },
  "email_notifications": {
    "on_success": ["data-science@company.com"],
    "on_failure": ["oncall@company.com"]
  }
}
```

### Agent Prompt Refresh Strategy

```python
# agents/base.py
from datetime import datetime, timedelta
from typing import Optional

class Agent:
    def __init__(self, config: dict):
        self.config = config
        self.prompt_manager = PromptManager()
        
        # Cache prompt with periodic refresh
        self._prompt_cache: Optional[str] = None
        self._prompt_loaded_at: Optional[datetime] = None
        self._prompt_refresh_interval = timedelta(minutes=5)
    
    def get_prompt(self, prompt_name: str, version: Optional[str] = None) -> str:
        """
        Get prompt with caching and periodic refresh.
        
        This allows agents to pick up newly optimized prompts
        without restarting the container.
        """
        now = datetime.now()
        
        # Check if cache is still valid
        if (
            self._prompt_cache is not None
            and self._prompt_loaded_at is not None
            and now - self._prompt_loaded_at < self._prompt_refresh_interval
        ):
            return self._prompt_cache
        
        # Refresh from Unity Catalog
        self._prompt_cache = self.prompt_manager.get_prompt(
            prompt_name,
            version=version  # None = latest
        )
        self._prompt_loaded_at = now
        
        return self._prompt_cache
```

---

## 🏗️ Complete Architecture

### Integrated System Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                    External Clients / Users                         │
└───────────────────────────┬────────────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────────────┐
│                      Databricks Apps                                │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  FastAPI Service (your agent solution)                       │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │ │
│  │  │ Agent Router│  │  API Layer  │  │  WebSocket  │         │ │
│  │  └──────┬──────┘  └─────────────┘  └─────────────┘         │ │
│  │         │                                                     │ │
│  │         ▼                                                     │ │
│  │  ┌─────────────────────────────────────────────────────┐   │ │
│  │  │  Your Custom Agents                                   │   │ │
│  │  │  - FraudDetectorAgent                                │   │ │
│  │  │  - RiskScorerAgent                                   │   │ │
│  │  │  - NarrativeAgent                                    │   │ │
│  │  └─────────────────────────────────────────────────────┘   │ │
│  └──────────────────────────────────────────────────────────────┘ │
└───┬───────────────┬──────────────┬──────────────┬─────────────────┘
    │               │              │              │
    │ (1) LLM       │ (2) Config   │ (3) Memory   │ (4) Telemetry
    │ Inference     │ & Prompts    │ Storage      │ & Logs
    ▼               ▼              ▼              ▼
┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐
│   Model   │   │  Unity    │   │  Vector   │   │   Delta   │
│  Serving  │   │  Catalog  │   │  Search   │   │   Lake    │
│  Endpoint │   │  Volumes  │   │ (Lakebase)│   │   Tables  │
├───────────┤   ├───────────┤   ├───────────┤   ├───────────┤
│ - DBRX    │   │ - Configs │   │ - Memory  │   │ - Metrics │
│ - MPT-7B  │   │ - Prompts │   │   Index   │   │ - Traces  │
│ - Custom  │   │ - Models  │   │ - Embed   │   │ - Logs    │
└───────────┘   └───────────┘   └───────────┘   └───────────┘
                                                       │
                                                       ▼
                                                 ┌───────────┐
                                                 │  Databricks│
                                                 │    SQL     │
                                                 │ Dashboards │
                                                 └───────────┘
```

### Data Flow Example: Fraud Detection

```
1. Request arrives at Databricks App (FastAPI)
   POST /execute {"agent": "fraud_detector", "data": {...}}

2. AgentRouter loads configuration from Unity Catalog
   /Volumes/main/agents/configs/sota_config.yaml

3. FraudDetectorAgent is instantiated
   - Loads prompt from UC: /Volumes/main/agents/prompts/fraud_detection_v2.txt
   - Initializes Model Serving client
   - Connects to Vector Search for memory

4. Agent retrieves similar past cases from Vector Search
   memory_index.similarity_search(query="transaction 12345", top_k=5)

5. Agent formats prompt with transaction data + context

6. Agent calls Model Serving endpoint
   databricks-dbrx-instruct.predict(prompt, temperature=0.3)

7. Agent parses LLM response into structured output

8. Agent stores interaction in Vector Search (memory)
   memory_index.upsert(text=narrative, embedding=embedding)

9. Telemetry logged to Delta Lake
   INSERT INTO main.agents.telemetry VALUES (...)

10. Response returned to client
    {"fraud_score": 0.85, "narrative": "...", "confidence": 0.95}
```

---

## 📝 Step-by-Step Deployment

### Prerequisites

```bash
# 1. Install Databricks CLI
pip install databricks-cli databricks-sdk

# 2. Configure authentication
databricks configure --token
# Enter workspace URL and personal access token

# 3. Install framework with Databricks extras
pip install sota-agent-framework[databricks]
```

### Step 1: Set Up Unity Catalog

```bash
# Run UC setup notebook
databricks workspace import notebooks/setup_unity_catalog.py
databricks notebooks run /Workspace/notebooks/setup_unity_catalog.py

# Verify
databricks catalogs list
databricks schemas list --catalog main
databricks volumes list --catalog main --schema agents
```

### Step 2: Upload Configuration & Prompts

```python
# scripts/deploy_to_databricks.py
from databricks.sdk import WorkspaceClient
from pathlib import Path

w = WorkspaceClient()

# Upload configs
for config_file in Path("config").glob("*.yaml"):
    w.files.upload(
        file_path=f"/Volumes/main/agents/configs/{config_file.name}",
        contents=config_file.read_bytes(),
        overwrite=True
    )
    print(f"✅ Uploaded {config_file.name}")

# Upload prompts
for prompt_file in Path("prompts").glob("*.txt"):
    w.files.upload(
        file_path=f"/Volumes/main/agents/prompts/{prompt_file.name}",
        contents=prompt_file.read_bytes(),
        overwrite=True
    )
    print(f"✅ Uploaded {prompt_file.name}")
```

### Step 3: Create Model Serving Endpoints

```python
# scripts/create_model_serving.py
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import EndpointCoreConfigInput, ServedEntityInput

w = WorkspaceClient()

# Create LLM endpoint
w.serving_endpoints.create(
    name="fraud-agent-llm",
    config=EndpointCoreConfigInput(
        served_entities=[
            ServedEntityInput(
                entity_name="databricks-dbrx-instruct",
                entity_version="1",
                workload_size="Small",
                scale_to_zero_enabled=True
            )
        ]
    )
)

# Create embedding endpoint
w.serving_endpoints.create(
    name="fraud-agent-embeddings",
    config=EndpointCoreConfigInput(
        served_entities=[
            ServedEntityInput(
                entity_name="databricks-mpt-7b-instruct",
                entity_version="1",
                workload_size="Small",
                scale_to_zero_enabled=True
            )
        ]
    )
)

print("✅ Model Serving endpoints created")
```

### Step 4: Create Vector Search Index

```python
# scripts/create_vector_index.py
from databricks.vector_search.client import VectorSearchClient

client = VectorSearchClient()

# Create endpoint
endpoint = client.create_endpoint(
    name="fraud-agent-vector-search"
)

# Create index
index = client.create_delta_sync_index(
    endpoint_name="fraud-agent-vector-search",
    index_name="main.agents.memory_index",
    source_table_name="main.agents.memory_embeddings",
    pipeline_type="TRIGGERED",
    primary_key="id",
    embedding_dimension=768,  # MPT-7B embedding size
    embedding_vector_column="embedding"
)

print(f"✅ Vector Search index created: {index.name}")
```

### Step 5: Deploy Databricks App

```bash
# Using sota-deploy CLI
cd your-agent-solution/
sota-deploy init --platform databricks-app

# Review generated files
cat deployment/databricks/app-config.yml

# Deploy
databricks apps create \
  --name fraud-detection-agent \
  --source-code-path /Workspace/apps/fraud-detection-agent \
  --config deployment/databricks/app-config.yml

# Check status
databricks apps get fraud-detection-agent
```

### Step 6: Verify Deployment

```bash
# Test health endpoint
APP_URL=$(databricks apps get fraud-detection-agent --json | jq -r '.url')
curl $APP_URL/health

# Test agent execution
curl -X POST $APP_URL/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "fraud_detector",
    "data": {
      "transaction_id": "txn_12345",
      "amount": 5000,
      "merchant": "Electronics Store"
    }
  }'

# Check telemetry in Delta Lake
databricks sql execute \
  --statement "SELECT * FROM main.agents.telemetry ORDER BY timestamp DESC LIMIT 10"
```

---

## ⚙️ Configuration Management

### Environment-Specific Configs

```yaml
# config/sota_config.yaml (base)
databricks:
  workspace_host: "${DATABRICKS_HOST}"
  
execution:
  default_mode: "process_pool"
  pool_size: 8

model_serving:
  default_endpoint: "databricks-dbrx-instruct"
  timeout: 30
```

```yaml
# config/sota_config.production.yaml (production overrides)
databricks:
  workspace_host: "${DATABRICKS_PROD_HOST}"
  
execution:
  pool_size: 32  # More workers in production

model_serving:
  default_endpoint: "fraud-agent-llm-prod"  # Production endpoint
  timeout: 60
  
telemetry:
  enabled: true
  sample_rate: 0.1  # Sample 10% for cost
  
unity_catalog:
  catalog: "main"
  schema: "agents_prod"
```

### Loading Config in App

```python
# app.py
import os
from config.uc_loader import UCConfigLoader

# Determine environment
environment = os.getenv("ENVIRONMENT", "development")

# Load config from Unity Catalog
loader = UCConfigLoader()
config = loader.load_config(
    uc_path="/Volumes/main/agents/configs/sota_config.yaml",
    environment=environment
)

print(f"Loaded config for environment: {environment}")
print(f"Model Serving endpoint: {config['model_serving']['default_endpoint']}")
```

---

## 📊 Monitoring & Observability: OTEL → ZeroBus → Delta

### Monitoring Architecture

**Telemetry pipeline using the ZeroBus pattern:**

```
┌────────────────────────────────────────────────────────────┐
│  Databricks Apps Container                                 │
│                                                            │
│  ┌──────────────────────────────────────────────────┐    │
│  │  OpenTelemetry Instrumentation (OTEL)            │    │
│  │  - Traces (agent execution spans)                │    │
│  │  - Metrics (latency, success rate, etc.)         │    │
│  │  - Logs (structured logging)                     │    │
│  └────────────────┬─────────────────────────────────┘    │
│                   │                                        │
│                   ▼                                        │
│  ┌──────────────────────────────────────────────────┐    │
│  │  ZeroBus Pattern (Batch Exporter)                │    │
│  │  - Accumulates telemetry in memory               │    │
│  │  - Batches writes every 10s or 1000 events       │    │
│  │  - Async, non-blocking                           │    │
│  └────────────────┬─────────────────────────────────┘    │
└────────────────────┼──────────────────────────────────────┘
                     │
                     ▼ (batch write)
         ┌───────────────────────────┐
         │  Delta Lake Tables        │
         │  (Unity Catalog)          │
         │                           │
         │  main.agents.traces       │
         │  main.agents.metrics      │
         │  main.agents.logs         │
         └───────────────────────────┘
                     │
                     ▼ (query)
         ┌───────────────────────────┐
         │  Databricks SQL           │
         │  - Dashboards             │
         │  - Alerts                 │
         │  - Ad-hoc analysis        │
         └───────────────────────────┘
```

### What is the ZeroBus Pattern?

**ZeroBus** = Zero-latency bus for telemetry

Key principles:
1. **Non-blocking writes**: Telemetry never blocks agent execution
2. **Batch processing**: Accumulate events, write in batches
3. **In-memory buffer**: Fast writes to memory, async flush to Delta
4. **Fault tolerance**: Retry on failure, dead-letter queue for errors

### Implementation: OTEL → ZeroBus → Delta

```python
# telemetry/zerobus_exporter.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from databricks.sdk import WorkspaceClient
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio
import json
from queue import Queue
from threading import Thread

class ZeroBusExporter:
    """
    ZeroBus pattern exporter for OpenTelemetry.
    
    Features:
    - Batches spans before writing to Delta Lake
    - Non-blocking (writes happen in background thread)
    - Configurable batch size and flush interval
    - Automatic retries
    """
    
    def __init__(
        self,
        delta_table: str = "main.agents.traces",
        batch_size: int = 1000,
        flush_interval_seconds: int = 10,
        workspace_client: Optional[WorkspaceClient] = None
    ):
        self.delta_table = delta_table
        self.batch_size = batch_size
        self.flush_interval = flush_interval_seconds
        self.client = workspace_client or WorkspaceClient()
        
        # In-memory buffer (thread-safe queue)
        self.buffer: Queue = Queue(maxsize=10000)
        
        # Background flusher thread
        self.flusher_thread = Thread(target=self._flush_loop, daemon=True)
        self.flusher_thread.start()
        
        print(f"✅ ZeroBus exporter started: {delta_table}")
    
    def export_span(self, span: trace.Span):
        """
        Export span to buffer (non-blocking).
        
        This is called by OTEL for every span. It must be FAST.
        """
        try:
            # Convert span to dict
            span_data = {
                "trace_id": format(span.context.trace_id, "032x"),
                "span_id": format(span.context.span_id, "016x"),
                "parent_span_id": format(span.parent.span_id, "016x") if span.parent else None,
                "name": span.name,
                "start_time": span.start_time,
                "end_time": span.end_time,
                "duration_ms": (span.end_time - span.start_time) / 1_000_000,  # ns to ms
                "attributes": dict(span.attributes) if span.attributes else {},
                "status": span.status.status_code.name,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Add to buffer (non-blocking, drops if full)
            self.buffer.put_nowait(span_data)
            
        except Exception as e:
            # Never raise exceptions in export path
            print(f"Warning: Failed to buffer span: {e}")
    
    def _flush_loop(self):
        """
        Background thread that flushes buffer to Delta Lake.
        
        Runs continuously, flushing:
        - Every `flush_interval` seconds, OR
        - When buffer reaches `batch_size` items
        """
        batch = []
        last_flush = datetime.now()
        
        while True:
            try:
                # Check if we should flush
                should_flush = (
                    len(batch) >= self.batch_size
                    or (datetime.now() - last_flush).total_seconds() >= self.flush_interval
                )
                
                if should_flush and batch:
                    self._write_batch_to_delta(batch)
                    batch = []
                    last_flush = datetime.now()
                
                # Get next item from buffer (with timeout)
                try:
                    span_data = self.buffer.get(timeout=1.0)
                    batch.append(span_data)
                except:
                    # Timeout, no new items
                    pass
                    
            except Exception as e:
                print(f"Error in flush loop: {e}")
                asyncio.sleep(5)  # Back off on error
    
    def _write_batch_to_delta(self, batch: List[Dict[str, Any]]):
        """
        Write batch of spans to Delta Lake.
        
        Uses Delta Lake's COPY INTO for efficient batch loading.
        """
        try:
            # Convert batch to JSON Lines format
            json_lines = "\n".join([json.dumps(span) for span in batch])
            
            # Write to temporary location in UC Volume
            temp_file = f"/Volumes/main/agents/temp/traces_{datetime.now().timestamp()}.jsonl"
            self.client.files.upload(
                file_path=temp_file,
                contents=json_lines.encode(),
                overwrite=True
            )
            
            # COPY INTO Delta Lake (fast bulk insert)
            sql = f"""
            COPY INTO {self.delta_table}
            FROM '{temp_file}'
            FILEFORMAT = JSON
            FORMAT_OPTIONS ('inferSchema' = 'true')
            """
            
            self.client.statement_execution.execute_statement(
                warehouse_id=self.client.config.warehouse_id,
                statement=sql
            )
            
            # Clean up temp file
            self.client.files.delete(temp_file)
            
            print(f"✅ Flushed {len(batch)} spans to {self.delta_table}")
            
        except Exception as e:
            print(f"Error writing batch to Delta: {e}")
            # TODO: Send to dead-letter queue for retry

# Initialize OTEL with ZeroBus exporter
def setup_telemetry():
    """Set up OpenTelemetry with ZeroBus exporter."""
    
    # Create tracer provider
    provider = TracerProvider()
    
    # Add ZeroBus exporter with batch processor
    zerobus_exporter = ZeroBusExporter(
        delta_table="main.agents.traces",
        batch_size=1000,
        flush_interval_seconds=10
    )
    
    # Wrap in BatchSpanProcessor (OTEL's batching layer)
    processor = BatchSpanProcessor(
        span_exporter=zerobus_exporter,
        max_queue_size=10000,
        max_export_batch_size=1000,
        schedule_delay_millis=10000  # 10 seconds
    )
    
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    
    print("✅ Telemetry configured: OTEL → ZeroBus → Delta")

# Usage in app.py
from telemetry.zerobus_exporter import setup_telemetry

# Set up at app startup
setup_telemetry()

# Instrument your agents
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

class FraudDetectorAgent(CriticalPathAgent):
    async def process(self, request: AgentInput) -> AgentOutput:
        # Create span (automatically exported via ZeroBus)
        with tracer.start_as_current_span(
            "fraud_detector.process",
            attributes={
                "agent.id": self.agent_id,
                "transaction.id": request.data.get("transaction_id")
            }
        ) as span:
            
            # Your agent logic
            result = await self._detect_fraud(request)
            
            # Add result attributes
            span.set_attribute("fraud.score", result["fraud_score"])
            span.set_attribute("fraud.decision", result["decision"])
            
            return result
```

### Metrics Exporter (Similar Pattern)

```python
# telemetry/metrics_exporter.py
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

class ZeroBusMetricsExporter:
    """
    Export metrics to Delta Lake using ZeroBus pattern.
    
    Similar to span exporter but for metrics:
    - Counter (e.g., total_requests)
    - Histogram (e.g., latency_distribution)
    - Gauge (e.g., active_agents)
    """
    
    def __init__(self, delta_table: str = "main.agents.metrics"):
        self.delta_table = delta_table
        self.buffer = []
    
    def export(self, metrics_data):
        """Export metrics batch to Delta Lake."""
        # Similar batching logic as spans
        pass

# Set up metrics
def setup_metrics():
    reader = PeriodicExportingMetricReader(
        exporter=ZeroBusMetricsExporter(),
        export_interval_millis=10000  # 10 seconds
    )
    
    provider = MeterProvider(metric_readers=[reader])
    metrics.set_meter_provider(provider)
    
    print("✅ Metrics configured: OTEL → ZeroBus → Delta")
```

### Complete Startup Integration

```python
# app.py
from telemetry.zerobus_exporter import setup_telemetry, setup_metrics

# Set up monitoring at app startup (before any agent execution)
setup_telemetry()
setup_metrics()

# Now all agent executions are automatically instrumented
app = create_app()
```

### Dashboard in Databricks SQL

```sql
-- Dashboard: Agent Performance Metrics

-- 1. Executions over time
SELECT
  DATE_TRUNC('hour', timestamp) as hour,
  agent_id,
  COUNT(*) as executions,
  AVG(latency_ms) as avg_latency_ms,
  PERCENTILE(latency_ms, 0.95) as p95_latency_ms,
  SUM(CASE WHEN success = false THEN 1 ELSE 0 END) as errors
FROM main.agents.telemetry
WHERE timestamp >= CURRENT_TIMESTAMP - INTERVAL 24 HOURS
GROUP BY hour, agent_id
ORDER BY hour DESC

-- 2. Error rate by agent
SELECT
  agent_id,
  COUNT(*) as total_executions,
  SUM(CASE WHEN success = false THEN 1 ELSE 0 END) as errors,
  (SUM(CASE WHEN success = false THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as error_rate_pct
FROM main.agents.telemetry
WHERE timestamp >= CURRENT_TIMESTAMP - INTERVAL 1 DAY
GROUP BY agent_id
ORDER BY error_rate_pct DESC

-- 3. Slowest agent executions
SELECT
  agent_id,
  execution_id,
  timestamp,
  latency_ms,
  input_data,
  error_message
FROM main.agents.telemetry
WHERE timestamp >= CURRENT_TIMESTAMP - INTERVAL 1 DAY
ORDER BY latency_ms DESC
LIMIT 100
```

---

## 🎯 Scaling & Performance

### Auto-Scaling Configuration

```yaml
# databricks-app.yml
compute:
  type: serverless
  min_instances: 2    # Always 2 running
  max_instances: 20   # Scale up to 20
  auto_scale: true
  
  # Scaling triggers
  scale_up:
    cpu_threshold: 70%
    memory_threshold: 80%
    queue_depth: 100
    
  scale_down:
    cooldown_minutes: 5
    idle_threshold: 10%
```

### Performance Optimization

**1. Connection Pooling**
```python
# Use singleton pattern for Databricks clients
_workspace_client = None

def get_workspace_client():
    global _workspace_client
    if _workspace_client is None:
        _workspace_client = WorkspaceClient()
    return _workspace_client
```

**2. Batch Processing**
```python
# Process multiple requests in batch
async def process_batch(requests: List[AgentInput]) -> List[AgentOutput]:
    # Call Model Serving once with batch
    prompts = [format_prompt(r) for r in requests]
    responses = await model_client.predict_batch(prompts)
    return [parse_response(r) for r in responses]
```

**3. Caching**
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_prompt_from_uc(prompt_name: str) -> str:
    """Cache prompts in memory."""
    return prompt_manager.get_prompt(prompt_name)
```

---

## ✅ Production Best Practices

### 1. **Security**
```python
# Use secrets for sensitive data
databricks secrets create-scope fraud-agents

databricks secrets put --scope fraud-agents \
  --key databricks-token \
  --string-value $DATABRICKS_TOKEN

# Reference in app
token = dbutils.secrets.get(scope="fraud-agents", key="databricks-token")
```

### 2. **Cost Optimization**
- Enable scale-to-zero for Model Serving endpoints
- Use serverless compute for Databricks Apps
- Batch writes to Delta Lake
- Cache frequently accessed configs/prompts
- Sample telemetry (e.g., 10%) for high-volume apps

### 3. **Reliability**
- Implement retries for Model Serving calls
- Fallback to simpler models if primary fails
- Health checks in Databricks Apps
- Graceful degradation

### 4. **Monitoring**
- Set up alerts on error rate
- Monitor Model Serving endpoint latency
- Track Unity Catalog API usage
- Dashboard for agent performance

---

---

## 🎯 Complete End-to-End Deployment Example

### Deploying a Fraud Detection Agent to Databricks

**This example ties together all the components:**

#### Step 1: Project Structure

```
fraud-detection-agent/
├── app.py                           # Main entry point (all services)
├── databricks-app.yml               # App configuration
├── requirements.txt                 # Dependencies
│
├── agents/
│   ├── __init__.py
│   ├── fraud_detector.py           # Your custom agent
│   └── a2a/                         # A2A server implementation
│       ├── server.py
│       └── client.py
│
├── services/
│   ├── api.py                       # FastAPI routes
│   ├── model_serving_client.py     # Model Serving client
│   └── prompt_manager.py            # UC Volumes prompt loader
│
├── memory/
│   └── databricks_vector_store.py  # Lakebase + Delta memory
│
├── telemetry/
│   ├── zerobus_exporter.py         # OTEL → ZeroBus → Delta
│   └── metrics_exporter.py
│
├── config/
│   └── sota_config.yaml            # Framework config (synced to UC)
│
├── jobs/
│   └── optimize_prompts_dspy.py    # Offline optimization job
│
└── deployment/
    ├── setup_unity_catalog.py      # UC setup script
    └── create_model_serving.py     # Model Serving setup
```

#### Step 2: Deploy Infrastructure

```bash
# 1. Set up Unity Catalog
python deployment/setup_unity_catalog.py

# 2. Create Model Serving endpoints (always-on)
python deployment/create_model_serving.py

# 3. Upload configs and prompts to UC
python deployment/sync_to_uc.py
```

#### Step 3: Deploy Databricks App

```bash
# Create app (hot pool with min 2 instances)
databricks apps create \
  --name fraud-detection-agent \
  --source-code-path /Workspace/apps/fraud-detection-agent \
  --config databricks-app.yml

# Get app URL
APP_URL=$(databricks apps get fraud-detection-agent --json | jq -r '.url')
echo "App deployed: $APP_URL"
```

#### Step 4: Schedule Offline Optimization Job

```bash
# Create Databricks Job for nightly prompt optimization
databricks jobs create --json @jobs/optimize_prompts_job.json
```

#### Step 5: Verify Deployment

```bash
# Health check
curl $APP_URL/health

# Test agent execution
curl -X POST $APP_URL/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "fraud_detector",
    "data": {
      "transaction_id": "txn_12345",
      "amount": 5000,
      "merchant": "Electronics Store"
    }
  }'

# Check telemetry in Delta Lake
databricks sql execute \
  --statement "SELECT * FROM main.agents.traces ORDER BY timestamp DESC LIMIT 10"

# View dashboard
open "https://your-workspace.databricks.com/sql/dashboards/agent-monitoring"
```

---

## 📋 Production Architecture Summary

### Where Components Live (Production Configuration)

| Plane | Where it lives | Configuration |
|-------|----------------|---------------|
| **Agent Mesh (reasoning agents)** | Containers in **K8s hot pools** *or* **Databricks Apps hot pools** | `min_instances: 2+`, `scale_to_zero: false` |
| **A2A transport layer** | FastAPI/Starlette server **inside Databricks Apps container** | Port 8001 or path `/a2a/*` |
| **MCP servers** | FastAPI/Starlette **inside Databricks Apps container** | Port 8002 or path `/mcp/*` |
| **Agent memory** | Lakebase/Delta (UC tables), queried async | `main.agents.memory_index`, async queries |
| **LLM inference** | **Always-on Model Serving / external API** (no scale-to-zero) | `scale_to_zero_enabled: false`, `min_provisioned_throughput: 100+` |
| **Prompt optimization** | Offline Databricks Jobs (DSPy/TextGrad) | Scheduled (nightly), batch compute |
| **Monitoring** | OTEL from Apps → ZeroBus → Delta | Batch exporter, 10s flush interval |

### Key Production Settings

**Databricks Apps (Hot Pool):**
```yaml
compute:
  min_instances: 2       # Always keep 2 warm
  max_instances: 20      # Scale up under load
  scale_to_zero: false   # Never cold start
```

**Model Serving (Always-On):**
```python
ServedEntityInput(
    workload_size="Medium",
    scale_to_zero_enabled=False,  # Always-on
    min_provisioned_throughput=100
)
```

**Telemetry (ZeroBus):**
```python
ZeroBusExporter(
    batch_size=1000,           # Batch 1000 events
    flush_interval_seconds=10  # Flush every 10s
)
```

**Memory (Async):**
```python
# Always use async queries (non-blocking)
results = await memory.retrieve(query, top_k=5)
```

**Prompt Optimization (Offline):**
```json
{
  "schedule": {
    "quartz_cron_expression": "0 0 2 * * ?",  // 2am daily
    "timezone_id": "America/Los_Angeles"
  }
}
```

---

## 🎯 Benefits of This Architecture

✅ **Low Latency**
- Hot pools: < 50ms cold start (vs. 5-30s)
- Always-on Model Serving: sub-second inference
- Async memory: non-blocking queries

✅ **Cost Efficiency**
- Hot pools: only 2 min instances, scale up as needed
- Offline optimization: batch processing, not per-request
- ZeroBus: efficient batched writes to Delta

✅ **Production Ready**
- No cold starts in critical path
- Telemetry doesn't block agents
- Prompts updated without container restarts
- Built-in monitoring and alerting

✅ **Databricks Native**
- Unity Catalog: single source of truth for configs, prompts, models
- Model Serving: managed LLM endpoints
- Lakebase: native vector search
- Delta Lake: scalable storage for telemetry
- Databricks SQL: built-in dashboards

✅ **Developer Experience**
- Single container (easy to debug)
- All-in-one deployment (FastAPI + A2A + MCP)
- Hot reload for prompts (no redeploy needed)
- Comprehensive observability

---

## 🚀 Quick Start Commands

```bash
# Deploy complete fraud detection agent to Databricks
git clone https://github.com/yourorg/fraud-detection-agent
cd fraud-detection-agent

# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up infrastructure
python deployment/setup_all.py

# 3. Deploy to Databricks Apps
sota-deploy init --platform databricks-app
sota-deploy apply --environment production

# 4. Verify
sota-deploy status

# Done! Agent is live at:
# https://your-workspace.databricks.com/apps/fraud-detection-agent
```

---

## 📚 Additional Resources

- **[Model Serving API Reference](https://docs.databricks.com/en/machine-learning/model-serving/index.html)**
- **[Unity Catalog Volumes](https://docs.databricks.com/en/data-governance/unity-catalog/volumes.html)**
- **[Databricks Apps](https://docs.databricks.com/en/apps/index.html)**
- **[Vector Search (Lakebase)](https://docs.databricks.com/en/generative-ai/vector-search.html)**
- **[Delta Lake](https://docs.databricks.com/en/delta/index.html)**

---

**🎉 Your SOTA agent solution is now production-ready on Databricks!**

