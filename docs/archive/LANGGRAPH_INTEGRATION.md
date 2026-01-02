## **LangGraph Integration Guide** 🔄

**Cognitive orchestration for autonomous agent workflows**

### **Overview**

The Agent Framework includes full LangGraph integration, providing:

- **🧠 Plan → Act → Critique → Re-plan loops**: Autonomous planning with self-correction
- **📊 Task decomposition**: Break complex objectives into executable steps  
- **🔍 Quality assessment**: Automatic result critique and validation
- **🔄 Dynamic re-planning**: Adaptive workflows that improve through iteration
- **🎯 Self-correcting execution**: Workflows that learn and adjust

---

### **Installation**

```bash
pip install sota-agent-framework[agent-frameworks]
```

This installs:
- `langgraph>=0.2.0`
- `langchain>=0.2.0`
- `langchain-core>=0.2.0`

---

### **Quick Start**

#### **Basic Planning Workflow**

```python
from agents import AgentRouter
from orchestration.langgraph import create_planning_workflow

# Load your agents
router = AgentRouter.from_yaml("config/agents.yaml")

# Create workflow with autonomous planning
workflow = create_planning_workflow(router, max_iterations=5)

# Execute with just an objective!
result = await workflow.execute({
    "request_id": "req-001",
    "objective": "Analyze transaction for fraud with high confidence",
    "request_data": {
        "transaction_id": "txn-123",
        "amount": 5000.00
    }
})

print(f"Success: {result['success']}")
print(f"Plan: {result['plan']}")
print(f"Results: {result['execution_results']}")
print(f"Critique: {result['critique']}")
```

**What happens:**
1. **Planner** analyzes objective & available agents → creates execution plan
2. **Executor** runs planned steps using your agents
3. **Critic** evaluates results against objective
4. **Replanner** adjusts plan if needed (up to max_iterations)

---

### **Architecture**

```
┌─────────────────────────────────────────────────────────┐
│  LangGraph StateGraph                                    │
│                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐         │
│  │ Planner  │───▶│ Executor │───▶│  Critic  │         │
│  └──────────┘    └──────────┘    └──────────┘         │
│       │               │                │                │
│       │               │           Need replan?          │
│       │               │                │                │
│       │               │          ┌──────────┐          │
│       └───────────────┴─────────▶│Replanner │          │
│                                  └──────────┘          │
└─────────────────────────────────────────────────────────┘
                     │
                     ▼
        ┌─────────────────────────┐
        │  Your SOTA Agents       │
        │  - DataEnrichmentAgent  │
        │  - FraudDetectionAgent  │
        │  - RiskScoringAgent     │
        └─────────────────────────┘
```

---

### **Workflow Nodes**

#### **1. Planner Node** 📋

**Purpose**: Autonomous task decomposition

```python
# Input: Objective + Available agents
# Output: Execution plan (list of steps)

# Example plan:
[
    {
        "step": 1,
        "agent": "data_enrichment",
        "description": "Enrich transaction with merchant/customer data",
        "dependencies": [],
        "expected_output": "enriched_data"
    },
    {
        "step": 2,
        "agent": "fraud_detection",
        "description": "Analyze enriched data for fraud patterns",
        "dependencies": [1],
        "expected_output": "fraud_score"
    }
]
```

**Features**:
- Analyzes objective and available agents
- Creates step-by-step execution plan
- Handles dependencies between steps
- TODO: LLM-based intelligent planning (currently template-based)

#### **2. Executor Node** ⚙️

**Purpose**: Execute planned agent steps

```python
# Executes one step at a time
# Passes previous results to next step
# Collects execution results

# Each result includes:
{
    "step": 1,
    "agent": "data_enrichment",
    "result": {...},
    "confidence": 0.85
}
```

**Features**:
- Sequential step execution
- Dependency resolution
- Context passing (previous results available to next steps)
- Error handling

#### **3. Critic Node** 🔍

**Purpose**: Evaluate execution quality

```python
# Analyzes results against objective
# Decides: Done? Continue? Replan?

# Critique output:
{
    "confidence": 0.92,
    "all_steps_completed": True,
    "all_successful": True,
    "should_replan": False,
    "feedback": "Successfully executed 3 steps",
    "recommendations": []
}
```

**Features**:
- Quality assessment
- Confidence scoring
- Actionable feedback
- Replan recommendations
- TODO: LLM-based intelligent critique (currently heuristic)

#### **4. Replanner Node** 🔄

**Purpose**: Adjust plan based on critique

```python
# Takes critique feedback
# Generates improved plan
# Can add/remove/modify steps

# Triggers when:
# - Confidence below threshold
# - Steps failed
# - Recommendations suggest changes
```

**Features**:
- Adaptive planning
- Learns from execution
- Adds alternative approaches
- TODO: LLM-based intelligent replanning

---

### **Workflow State**

The `WorkflowState` tracks execution through the graph:

```python
class WorkflowState(TypedDict):
    # Input
    request_id: str
    request_data: Dict[str, Any]
    objective: str  # User's goal
    
    # Planning
    plan: List[Dict[str, Any]]  # Execution plan
    current_step: int
    
    # Execution
    execution_results: List[Dict]  # Results from each step
    agent_outputs: List[Any]
    
    # Critique
    critique: Dict[str, Any]
    should_replan: bool
    iterations: int
    
    # Status
    status: str  # planning|executing|critiquing|replanning|completed|failed
    final_result: Any
```

---

### **Configuration**

```python
from orchestration.langgraph import WorkflowConfig

config = WorkflowConfig(
    max_iterations=5,           # Max replan cycles
    max_plan_steps=10,          # Max steps per plan
    critique_threshold=0.8,     # Min confidence to accept
    enable_replanning=True,     # Allow replanning
    enable_self_correction=True # Self-correct on errors
)
```

---

### **Pre-built Workflows**

#### **Simple Workflow** (no replanning)

```python
from orchestration.langgraph import create_simple_workflow

workflow = create_simple_workflow(router, max_iterations=3)
```

**Use for**: Straightforward tasks, quick execution

#### **Planning Workflow** (with critique & replan)

```python
from orchestration.langgraph import create_planning_workflow

workflow = create_planning_workflow(
    router,
    max_iterations=5,
    critique_threshold=0.85
)
```

**Use for**: Complex tasks requiring quality assurance

#### **Research Workflow** (iterative refinement)

```python
from orchestration.langgraph import create_research_workflow

workflow = create_research_workflow(router, depth=3)
```

**Use for**: Information gathering, multi-source synthesis

#### **Consensus Workflow** (multiple agents)

```python
from orchestration.langgraph import create_consensus_workflow

workflow = create_consensus_workflow(router, min_agents=3)
```

**Use for**: High-stakes decisions, cross-validation

#### **Domain-Specific Workflows**

```python
# Fraud detection
from orchestration.langgraph.examples import create_fraud_detection_workflow
workflow = create_fraud_detection_workflow(router)

# Customer support
from orchestration.langgraph.examples import create_customer_support_workflow
workflow = create_customer_support_workflow(router)
```

---

### **Advanced Usage**

#### **Streaming Execution**

```python
# Stream state updates in real-time
async for event in workflow.stream_execute(input_data):
    for node_name, state in event.items():
        print(f"Node: {node_name}, Status: {state['status']}")
```

#### **Custom Workflow Graph**

```python
from orchestration.langgraph import AgentWorkflowGraph, WorkflowConfig
from langgraph.graph import StateGraph

# Create custom graph
custom_workflow = AgentWorkflowGraph(router, custom_config)

# Visualize graph
custom_workflow.visualize("my_workflow.png")
```

#### **Agent to LangGraph Tool**

```python
from orchestration.langgraph.adapters import agent_to_langgraph_tool

# Convert Agent agent to LangGraph tool
tool_spec = agent_to_langgraph_tool(my_agent)

# Use in custom LangGraph workflows
```

---

### **Examples**

See `examples/langgraph_planning_workflow.py` for complete examples:

1. **Simple workflow** - Basic planning and execution
2. **Planning with critique** - Self-correcting workflow
3. **Streaming execution** - Real-time state updates

```bash
python examples/langgraph_planning_workflow.py
```

---

### **Comparison with Direct Agent Usage**

| Feature | Direct Agents | LangGraph Integration |
|---------|--------------|----------------------|
| **Execution** | Manual routing | Autonomous planning |
| **Orchestration** | You write the logic | Plan → Act → Critique |
| **Quality Control** | Manual validation | Automatic critique |
| **Adaptation** | Static workflow | Self-correcting |
| **Complexity** | Low | Higher (more features) |
| **Use Case** | Simple flows | Complex, adaptive tasks |

**When to use LangGraph:**
- ✅ Complex, multi-step objectives
- ✅ Quality-critical applications
- ✅ Need self-correction
- ✅ Uncertain execution paths

**When to use direct agents:**
- ✅ Simple, predictable workflows
- ✅ Performance-critical paths
- ✅ Fully deterministic flows
- ✅ Low latency requirements

---

### **Roadmap**

**Current (v0.1.7)**:
- ✅ Plan → Execute → Critique → Replan loops
- ✅ StateGraph orchestration
- ✅ Pre-built workflows
- ✅ Template-based planning

**Coming Soon**:
- 🔜 LLM-based intelligent planner
- 🔜 LLM-based intelligent critic
- 🔜 Parallel agent execution
- 🔜 Dynamic tool discovery
- 🔜 Memory/context persistence
- 🔜 Human-in-the-loop checkpoints

---

### **FAQ**

**Q: Do I need LangGraph for basic agent usage?**  
A: No! LangGraph is optional. Use direct agents for simple workflows.

**Q: How is this different from using LangGraph directly?**  
A: We integrate YOUR agents into LangGraph workflows, providing pre-built orchestration patterns for common use cases.

**Q: Can I customize the planning/critique logic?**  
A: Yes! Extend `PlannerNode` and `CriticNode` classes, or build custom StateGraphs.

**Q: Does this work with existing agents?**  
A: Yes! Your existing Agent agents work seamlessly with LangGraph workflows.

**Q: What about performance overhead?**  
A: Planning/critique adds latency (~100-500ms per iteration). For latency-critical paths, use direct agent execution.

---

### **Resources**

- **Examples**: `examples/langgraph_planning_workflow.py`
- **Source**: `orchestration/langgraph/`
- **LangGraph Docs**: https://python.langchain.com/docs/langgraph
- **Framework Docs**: `docs/`

---

**Ready to build autonomous agent workflows?** 🚀

```python
from orchestration.langgraph import create_planning_workflow

workflow = create_planning_workflow(router)
result = await workflow.execute({
    "objective": "Your complex task here",
    "request_data": {...}
})
```

