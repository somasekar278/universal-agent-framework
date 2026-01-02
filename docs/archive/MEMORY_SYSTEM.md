# Agent-Governed Memory System

**Comprehensive memory management for AI agents with intelligent storage, retrieval, and forgetting.**

## Overview

The Agent Framework includes a **production-grade memory system** where **agents decide** what to store, retrieve, and forget - not just passive storage.

### What Makes It Agent?

✅ **Agent-Governed** - Agents control memory decisions, not just read/write  
✅ **Multi-Store Architecture** - Short-term, long-term, episodic, semantic, procedural  
✅ **Intelligent Retrieval** - Semantic similarity + recency + importance + access patterns  
✅ **Reflection & Consolidation** - Agents create insights from memories  
✅ **Context Window Management** - Automatic token budgeting for LLMs  
✅ **Forgetting Policies** - Intelligent removal of old/irrelevant data  
✅ **Shared & Private Memory** - Cross-agent coordination with access control  
✅ **Memory Graphs** - Track relationships and patterns  
✅ **Semantic Embeddings** - Vector-based similarity search  

---

## Quick Start

### Installation

```bash
# Basic memory system
pip install sota-agent-framework

# With semantic search
pip install sota-agent-framework[semantic-search]

# Everything
pip install sota-agent-framework[all]
```

### Basic Usage

```python
from memory import MemoryManager, MemoryType, MemoryImportance

# Initialize
memory = MemoryManager()

# Agent stores (decides where and how)
await memory.store(
    content="User prefers dark mode at night",
    importance=MemoryImportance.HIGH
)

# Agent retrieves relevant context
memories = await memory.retrieve(
    query="What are user preferences?",
    limit=5
)

# Agent reflects on memories
summary = await memory.reflect()

# Agent forgets old data
forgotten = await memory.forget()
```

---

## Core Components

### 1. Memory Manager

Central orchestrator for all memory operations.

```python
from memory import MemoryManager, MemoryConfig

# Configure
config = MemoryConfig(
    short_term_capacity=20,
    short_term_ttl_seconds=3600,
    long_term_capacity=10000,
    max_context_tokens=8000,
    enable_forgetting=True
)

# Initialize
memory = MemoryManager(config)
```

**Configuration Options:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `short_term_capacity` | 20 | Max items in working memory |
| `short_term_ttl_seconds` | 3600 | TTL for short-term memories |
| `long_term_capacity` | 10000 | Max items in long-term storage |
| `max_context_tokens` | 8000 | Token budget for LLM context |
| `context_reservation` | 0.2 | Reserve 20% for system prompts |
| `reflection_interval_hours` | 24 | Auto-reflect every 24 hours |
| `enable_forgetting` | True | Enable automatic forgetting |

### 2. Memory Types

Five distinct memory stores:

```python
from memory import MemoryType

# Short-term (working memory, immediate context)
await memory.store(
    content="User just asked about pricing",
    memory_type=MemoryType.SHORT_TERM
)

# Long-term (persistent storage)
await memory.store(
    content="User signed up on 2024-01-15",
    memory_type=MemoryType.LONG_TERM
)

# Episodic (events and experiences)
await memory.store(
    content={"event": "user_login", "timestamp": "..."},
    memory_type=MemoryType.EPISODIC
)

# Semantic (facts and knowledge)
await memory.store(
    content="User's timezone is PST",
    memory_type=MemoryType.SEMANTIC
)

# Procedural (skills and how-to)
await memory.store(
    content={"procedure": "password_reset", "steps": [...]},
    memory_type=MemoryType.PROCEDURAL
)
```

### 3. Intelligent Storage

The **Storage Decision Agent** decides:
- Where to store (which memory type)
- Importance level
- Compression/summarization needs
- Tags and relationships

```python
# Auto-detection and assessment
memory_entry = await memory.store(
    content="CRITICAL: User reported security issue",
    # Agent detects: HIGH importance
    # Agent decides: LONG_TERM + EPISODIC
    # Agent tags: ["security", "critical"]
)

# Manual control
memory_entry = await memory.store(
    content="User prefers email notifications",
    memory_type=MemoryType.SEMANTIC,
    importance=MemoryImportance.HIGH,
    tags=["preferences", "notifications"],
    source="support_agent_001"
)
```

### 4. Intelligent Retrieval

The **Retrieval Agent** uses multiple strategies:

```python
# Semantic similarity (default with embeddings)
memories = await memory.retrieve(
    query="What does the user prefer for notifications?",
    limit=5
)

# Recency-based
memories = await memory.retrieve(
    query="Recent user actions",
    strategy="recency"
)

# Importance-based
memories = await memory.retrieve(
    query="Critical user information",
    strategy="importance"
)

# Hybrid (combines all factors)
memories = await memory.retrieve(
    query="User preferences",
    strategy="hybrid",  # recency + importance + access count
    memory_types=[MemoryType.SEMANTIC, MemoryType.LONG_TERM]
)
```

### 5. Reflection & Consolidation

The **Reflection Agent** periodically:
- Analyzes recent memories
- Identifies patterns
- Creates summaries
- Consolidates related memories
- Promotes insights to semantic memory

```python
# Manual reflection
summary = await memory.reflect()
# Returns:
# {
#     "total_memories": 47,
#     "by_importance": {"high": 12, "medium": 30, "low": 5},
#     "by_tags": {"preferences": 8, "security": 3},
#     "insights": ["High security activity - needs review"]
# }

# Auto-reflection (configured)
config = MemoryConfig(
    reflection_interval_hours=24,  # Every 24 hours
    reflection_trigger_count=100,  # Or after 100 new memories
    enable_auto_reflection=True
)
```

### 6. Context Window Management

Automatic token budgeting for LLM calls:

```python
# Build optimized context
context = await memory.build_context(
    query="Help me schedule a meeting",
    include_system="You are a scheduling assistant"
)

# Returns:
# {
#     "messages": [
#         {"role": "system", "content": "You are..."},
#         {"role": "system", "content": "Relevant context:\n..."},
#         {"role": "user", "content": "Help me..."}
#     ],
#     "token_budget": 8000,
#     "memories_included": 5,
#     "total_memories": 23
# }
```

**Budget Management:**
- Reserves 20% for system prompts
- Retrieves relevant memories
- Prioritizes by importance + relevance
- Fits within token limit
- Most relevant memories first

### 7. Forgetting Policies

The **Forget Agent** applies intelligent forgetting:

```python
# Manual forgetting
forgotten_count = await memory.forget()
# Agent removed 47 memories based on:
# - Time since last access
# - Importance (kept all CRITICAL)
# - Capacity (90% full threshold)
# - Relevance to current context

# Specific criteria
forgotten_count = await memory.forget(criteria={
    "max_age_days": 30,
    "min_importance": MemoryImportance.LOW
})
```

**Policies:**

```python
from memory.policies import (
    TimeBasedForgetting,
    ImportanceBasedForgetting,
    CapacityBasedForgetting
)

# Time-based: forget after 30 days
time_policy = TimeBasedForgetting(max_age_days=30)

# Importance-based: forget below threshold
importance_policy = ImportanceBasedForgetting(
    min_importance=MemoryImportance.MEDIUM
)

# Capacity-based: forget when 90% full
capacity_policy = CapacityBasedForgetting(
    capacity_threshold=0.9
)
```

### 8. Shared vs Private Memory

Cross-agent coordination with access control:

```python
from memory.shared import (
    SharedMemoryCoordinator,
    MemoryAccess
)

coordinator = SharedMemoryCoordinator()

# Agent A: Private memory
private_space = coordinator.get_private_space("agent_a")
await private_space.add(memory)  # Only agent_a can access

# Agent A: Share with others
await coordinator.share_memory(
    memory,
    owner="agent_a",
    access=MemoryAccess.SHARED  # All can read/write
)

# Or read-only sharing
await coordinator.share_memory(
    memory,
    owner="agent_a",
    access=MemoryAccess.READ_ONLY  # Others can only read
)

# Agent B: Retrieve accessible memories
memories = await coordinator.retrieve_for_agent(
    "agent_b",
    include_shared=True  # Gets shared + own private
)
```

---

## Advanced Features

### Semantic Embeddings

Vector-based similarity search:

```python
from memory.embeddings import (
    SentenceTransformerEmbeddings,
    SemanticMemorySearch
)

# Initialize embedder
embedder = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# Create semantic search
search = SemanticMemorySearch(embedder)

# Find similar memories
similar = await search.find_similar(
    query="What does user prefer?",
    memories=all_memories,
    top_k=5,
    min_similarity=0.7
)

# Returns: [(memory, similarity_score), ...]
for memory, score in similar:
    print(f"{memory.content} (similarity: {score:.2f})")
```

**Supported Embedders:**

```python
# Local: Sentence Transformers
from memory.embeddings import SentenceTransformerEmbeddings
embedder = SentenceTransformerEmbeddings("all-mpnet-base-v2")

# API: OpenAI
from memory.embeddings import OpenAIEmbeddings
embedder = OpenAIEmbeddings(api_key="...", model="text-embedding-ada-002")

# Databricks Model Serving
from memory.embeddings import DatabricksEmbeddings
embedder = DatabricksEmbeddings(endpoint_url="...", token="...")

# Cached (avoid recomputing)
from memory.embeddings import CachedEmbeddings
base = SentenceTransformerEmbeddings()
embedder = CachedEmbeddings(base, max_cache_size=10000)
```

### Memory Graphs

Track relationships and patterns:

```python
from memory.graphs import MemoryGraph, RelationType

# Create graph
graph = MemoryGraph()

# Add memories as nodes
graph.add_node(memory1)
graph.add_node(memory2)
graph.add_node(memory3)

# Add relationships
graph.add_relation(
    from_id=memory1.id,
    to_id=memory2.id,
    relation_type=RelationType.CAUSED_BY,
    strength=0.9
)

graph.add_relation(
    from_id=memory2.id,
    to_id=memory3.id,
    relation_type=RelationType.FOLLOWS,
    strength=1.0
)

# Find related memories
related = graph.get_related(
    memory1.id,
    depth=2,  # 2 hops away
    min_strength=0.5
)

# Find paths between memories
paths = graph.find_paths(memory1.id, memory3.id)
# Returns: [[memory1, memory2, memory3]]

# Find memory clusters
clusters = graph.find_clusters(min_cluster_size=3)

# Get most connected memories
top_connected = graph.get_most_connected(top_k=10)
# Returns: [(memory_id, connection_count), ...]

# Graph statistics
stats = graph.get_stats()
# {
#     "total_nodes": 47,
#     "total_edges": 123,
#     "avg_degree": 2.6,
#     "by_relation_type": {"related_to": 50, "follows": 30, ...}
# }
```

**Relationship Types:**

- `RELATED_TO` - General relationship
- `CAUSED_BY` - Causal relationship
- `FOLLOWS` - Temporal sequence
- `CONTRADICTS` - Conflicting information
- `SUPPORTS` - Supporting evidence
- `SUMMARIZES` - Summary relationship
- `DERIVED_FROM` - Derived insight
- `SIMILAR_TO` - Semantic similarity

**Auto-Detection:**

```python
from memory.graphs import AutoRelationDetector

detector = AutoRelationDetector(similarity_threshold=0.75)

# Automatically detect relationships
relations = await detector.detect_relations(
    memory=new_memory,
    existing_memories=all_memories,
    embedder=embedder  # Optional for semantic similarity
)

# Add to graph
for relation in relations:
    graph.add_relation(
        relation.from_memory_id,
        relation.to_memory_id,
        relation.relation_type,
        relation.strength
    )
```

---

## Integration with Agents

### Memory-Aware Agent

```python
from agents.base import EnrichmentAgent
from memory import MemoryManager, MemoryType, MemoryImportance

class MemoryAwareAgent(EnrichmentAgent):
    """Agent with memory capabilities."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.memory = MemoryManager()
    
    async def process_internal(self, input_data):
        # 1. Retrieve relevant context
        context_memories = await self.memory.retrieve(
            query=input_data.data.get("query"),
            limit=10
        )
        
        # 2. Build LLM context with memories
        context = await self.memory.build_context(
            query=input_data.data.get("query"),
            include_system=self.get_system_prompt()
        )
        
        # 3. Process with context
        result = await self.process_with_context(
            input_data,
            context_memories
        )
        
        # 4. Store interaction
        await self.memory.store(
            content={
                "input": input_data.data,
                "output": result,
                "timestamp": datetime.now()
            },
            memory_type=MemoryType.EPISODIC,
            importance=self.assess_importance(result)
        )
        
        # 5. Periodic reflection
        if self.should_reflect():
            summary = await self.memory.reflect()
            await self.process_reflection(summary)
        
        return result
    
    def assess_importance(self, result) -> MemoryImportance:
        """Assess interaction importance."""
        if result.get("critical") or result.get("error"):
            return MemoryImportance.CRITICAL
        elif result.get("user_satisfaction", 0) > 4:
            return MemoryImportance.HIGH
        return MemoryImportance.MEDIUM
    
    def should_reflect(self) -> bool:
        """Check if reflection is needed."""
        stats = self.memory.get_stats()
        return stats["short_term_count"] > 50
```

### Multi-Agent Memory Sharing

```python
from memory import MemoryManager
from memory.shared import SharedMemoryCoordinator, MemoryAccess

class AgentTeam:
    """Team of agents with shared memory."""
    
    def __init__(self, agent_ids: List[str]):
        self.coordinator = SharedMemoryCoordinator()
        self.agents = {
            agent_id: self.create_agent(agent_id)
            for agent_id in agent_ids
        }
    
    def create_agent(self, agent_id: str):
        """Create agent with memory."""
        agent = MemoryAwareAgent(agent_id=agent_id, ...)
        agent.memory_space = self.coordinator.get_private_space(agent_id)
        return agent
    
    async def share_insight(self, from_agent: str, memory, access=MemoryAccess.SHARED):
        """Share memory across team."""
        await self.coordinator.share_memory(
            memory,
            owner=from_agent,
            access=access
        )
    
    async def get_team_context(self, agent_id: str):
        """Get all accessible memories for an agent."""
        return await self.coordinator.retrieve_for_agent(
            agent_id,
            include_shared=True
        )
```

---

## Best Practices

### 1. Importance Assessment

```python
def assess_importance(content: Any) -> MemoryImportance:
    """Assess content importance."""
    
    # Critical: Security, errors, user complaints
    if any(keyword in str(content).lower() for keyword in 
           ["security", "error", "critical", "urgent", "complaint"]):
        return MemoryImportance.CRITICAL
    
    # High: User preferences, important decisions
    if any(keyword in str(content).lower() for keyword in
           ["prefer", "important", "decision", "key"]):
        return MemoryImportance.HIGH
    
    # Medium: Normal interactions
    return MemoryImportance.MEDIUM
```

### 2. Retrieval Strategies

```python
# Use semantic for conceptual queries
memories = await memory.retrieve(
    query="What kind of features does the user want?",
    strategy="semantic"  # or default hybrid
)

# Use recency for "what happened recently"
memories = await memory.retrieve(
    query="Recent user activity",
    strategy="recency"
)

# Use importance for critical information
memories = await memory.retrieve(
    query="Critical user information",
    strategy="importance"
)
```

### 3. Context Budgeting

```python
# Adjust budget based on model
config = MemoryConfig(
    max_context_tokens=32000,  # GPT-4 Turbo
    context_reservation=0.15   # 15% for system
)

# Or for smaller models
config = MemoryConfig(
    max_context_tokens=4000,   # GPT-3.5
    context_reservation=0.25   # 25% for system
)
```

### 4. Reflection Triggers

```python
# Time-based reflection
config = MemoryConfig(
    reflection_interval_hours=12,  # Every 12 hours
    enable_auto_reflection=True
)

# Count-based reflection
if memory.get_stats()["short_term_count"] > 50:
    summary = await memory.reflect()
```

### 5. Forgetting Policies

```python
# Conservative: Keep more
config = MemoryConfig(
    enable_forgetting=True,
    min_importance_to_keep=MemoryImportance.LOW
)

# Aggressive: Remove more
config = MemoryConfig(
    enable_forgetting=True,
    min_importance_to_keep=MemoryImportance.MEDIUM,
    short_term_ttl_seconds=1800  # 30 minutes
)
```

---

## Performance Optimization

### Batch Embedding Generation

```python
# Inefficient: One at a time
for memory in memories:
    memory.metadata.embedding = await embedder.embed(str(memory.content))

# Efficient: Batch processing
texts = [str(mem.content) for mem in memories]
embeddings = await embedder.embed_batch(texts)
for mem, embedding in zip(memories, embeddings):
    mem.metadata.embedding = embedding
```

### Caching

```python
from memory.embeddings import CachedEmbeddings

# Wrap embedder with cache
base_embedder = SentenceTransformerEmbeddings()
embedder = CachedEmbeddings(base_embedder, max_cache_size=10000)

# Subsequent calls for same text use cache
embedding1 = await embedder.embed("User prefers dark mode")  # Computed
embedding2 = await embedder.embed("User prefers dark mode")  # Cached!
```

### Memory Graphs

```python
# Build graph incrementally
graph = MemoryGraph()

for memory in new_memories:
    graph.add_node(memory)
    
    # Auto-detect relations
    relations = await detector.detect_relations(
        memory,
        existing_memories,
        embedder
    )
    
    for relation in relations:
        graph.add_relation(...)
```

---

## Statistics & Monitoring

```python
# Get memory statistics
stats = memory.get_stats()
# {
#     "total_stored": 523,
#     "total_retrieved": 1847,
#     "total_forgotten": 147,
#     "reflections_count": 12,
#     "short_term_count": 18,
#     "long_term_count": 358,
#     "config": {...}
# }

# Log to MLflow
import mlflow

with mlflow.start_run():
    for key, value in stats.items():
        if isinstance(value, (int, float)):
            mlflow.log_metric(f"memory_{key}", value)
```

---

## Troubleshooting

### High Memory Usage

```python
# Reduce capacities
config = MemoryConfig(
    short_term_capacity=10,  # Reduced from 20
    long_term_capacity=5000,  # Reduced from 10000
    enable_forgetting=True
)

# Trigger manual forgetting
forgotten = await memory.forget()
```

### Slow Retrieval

```python
# Use caching
from memory.embeddings import CachedEmbeddings
embedder = CachedEmbeddings(base_embedder)

# Limit search space
memories = await memory.retrieve(
    query="...",
    memory_types=[MemoryType.SEMANTIC],  # Narrow scope
    limit=5  # Reduce results
)
```

### Poor Relevance

```python
# Tune similarity threshold
search = SemanticMemorySearch(embedder)
results = await search.find_similar(
    query="...",
    memories=memories,
    min_similarity=0.8  # Increase from 0.7
)

# Use better embeddings
embedder = SentenceTransformerEmbeddings(
    model_name="all-mpnet-base-v2"  # Better quality
)
```

---

## Next Steps

- **[Main Documentation](../README.md)** - Framework overview
- **[Agent Development Guide](AGENT_DEVELOPMENT.md)** - Building agents
- **[Benchmarking Guide](BENCHMARKING.md)** - Testing agents
- **[LangGraph Integration](LANGGRAPH_INTEGRATION.md)** - Autonomous workflows

---

**Ready to use agent-governed memory?** Install now:

```bash
pip install sota-agent-framework[semantic-search]
```

