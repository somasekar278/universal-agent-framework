"""
Dynamic Tool Registry with Semantic Search

Modern tool registry that supports:
- Runtime tool registration
- Semantic tool discovery (vector-based)
- Rich metadata (cost, version, deprecation)
- Capability search
- Input/output schemas
"""

from typing import Dict, Any, List, Optional, Callable, TypedDict
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime


class ToolStatus(str, Enum):
    """Tool availability status."""
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    EXPERIMENTAL = "experimental"
    BETA = "beta"


@dataclass
class ToolMetadata:
    """
    Rich metadata for registered tools.
    
    Enables semantic search, cost estimation, and lifecycle management.
    """
    # Identity
    name: str
    version: str
    description: str  # Semantic searchable description
    
    # Schemas
    input_schema: Dict[str, Any]  # JSON Schema for inputs
    output_schema: Dict[str, Any]  # JSON Schema for outputs
    
    # Discovery
    capabilities: List[str] = field(default_factory=list)  # Searchable capabilities
    tags: List[str] = field(default_factory=list)  # Tags for filtering
    category: Optional[str] = None  # Tool category
    
    # Cost & Performance
    estimated_latency_ms: Optional[int] = None  # Expected latency
    estimated_cost: Optional[float] = None  # Cost per invocation
    rate_limit: Optional[int] = None  # Calls per minute
    
    # Lifecycle
    status: ToolStatus = ToolStatus.ACTIVE
    deprecated: bool = False
    deprecated_in_favor_of: Optional[str] = None
    min_version: Optional[str] = None
    max_version: Optional[str] = None
    
    # Documentation
    examples: List[Dict[str, Any]] = field(default_factory=list)
    documentation_url: Optional[str] = None
    
    # Registration
    registered_at: datetime = field(default_factory=datetime.utcnow)
    registered_by: Optional[str] = None


class DynamicToolRegistry:
    """
    Dynamic tool registry with semantic search capabilities.
    
    Features:
    - Runtime tool registration
    - Vector-based semantic search
    - Capability-based discovery
    - Cost-aware tool selection
    - Version management
    
    Example:
        ```python
        registry = DynamicToolRegistry()
        
        # Register tool at runtime
        @registry.register_tool(
            name="fraud_detector",
            version="1.0.0",
            description="Detects fraud patterns in transactions",
            capabilities=["fraud_detection", "risk_analysis"],
            estimated_latency_ms=250,
            estimated_cost=0.001
        )
        async def detect_fraud(transaction: Dict) -> Dict:
            # Implementation
            return {"fraud_score": 0.85}
        
        # Semantic search
        tools = registry.search_tools("find fraud in payments")
        
        # Capability search
        fraud_tools = registry.find_by_capability("fraud_detection")
        ```
    """
    
    def __init__(self, enable_vector_search: bool = True):
        """
        Initialize tool registry.
        
        Args:
            enable_vector_search: Enable semantic vector search (requires embeddings)
        """
        self.tools: Dict[str, ToolMetadata] = {}
        self.tool_functions: Dict[str, Callable] = {}
        self.enable_vector_search = enable_vector_search
        
        # Vector embeddings for semantic search
        self._tool_embeddings: Dict[str, List[float]] = {}
        self._embedding_model = None
        
        if enable_vector_search:
            self._initialize_embeddings()
    
    def _initialize_embeddings(self):
        """Initialize embedding model for semantic search."""
        try:
            # Try to use sentence-transformers if available
            from sentence_transformers import SentenceTransformer
            self._embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        except ImportError:
            # Fallback: use simple keyword matching
            self._embedding_model = None
            self.enable_vector_search = False
    
    def register_tool(
        self,
        name: str,
        version: str,
        description: str,
        input_schema: Dict[str, Any],
        output_schema: Dict[str, Any],
        capabilities: List[str] = None,
        **kwargs
    ) -> Callable:
        """
        Decorator to register a tool at runtime.
        
        Args:
            name: Tool name
            version: Tool version
            description: Semantic description
            input_schema: JSON Schema for inputs
            output_schema: JSON Schema for outputs
            capabilities: List of capabilities
            **kwargs: Additional ToolMetadata fields
            
        Returns:
            Decorator function
            
        Example:
            ```python
            @registry.register_tool(
                name="enrich_data",
                version="1.0.0",
                description="Enriches transaction with external data",
                input_schema={...},
                output_schema={...},
                capabilities=["data_enrichment"],
                estimated_latency_ms=150
            )
            async def enrich(data: Dict) -> Dict:
                return enriched_data
            ```
        """
        def decorator(func: Callable) -> Callable:
            metadata = ToolMetadata(
                name=name,
                version=version,
                description=description,
                input_schema=input_schema,
                output_schema=output_schema,
                capabilities=capabilities or [],
                **kwargs
            )
            
            self.tools[name] = metadata
            self.tool_functions[name] = func
            
            # Generate embedding for semantic search
            if self.enable_vector_search and self._embedding_model:
                text = f"{name} {description} {' '.join(capabilities or [])}"
                self._tool_embeddings[name] = self._embedding_model.encode(text).tolist()
            
            return func
        
        return decorator
    
    def register_tool_instance(
        self,
        metadata: ToolMetadata,
        func: Callable
    ):
        """
        Register a tool instance directly.
        
        Args:
            metadata: Tool metadata
            func: Tool function
        """
        self.tools[metadata.name] = metadata
        self.tool_functions[metadata.name] = func
        
        if self.enable_vector_search and self._embedding_model:
            text = f"{metadata.name} {metadata.description} {' '.join(metadata.capabilities)}"
            self._tool_embeddings[metadata.name] = self._embedding_model.encode(text).tolist()
    
    def search_tools(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ToolMetadata]:
        """
        Semantic search for tools.
        
        Args:
            query: Natural language query
            top_k: Number of results to return
            filters: Optional filters (status, category, etc.)
            
        Returns:
            List of matching tools, ranked by relevance
            
        Example:
            ```python
            # Natural language search
            tools = registry.search_tools("detect fraudulent transactions")
            
            # With filters
            tools = registry.search_tools(
                "analyze data",
                filters={"status": "active", "category": "analytics"}
            )
            ```
        """
        if not self.enable_vector_search or not self._embedding_model:
            # Fallback to keyword search
            return self._keyword_search(query, top_k, filters)
        
        # Generate query embedding
        query_embedding = self._embedding_model.encode(query).tolist()
        
        # Calculate similarities
        similarities = []
        for tool_name, tool_embedding in self._tool_embeddings.items():
            tool = self.tools[tool_name]
            
            # Apply filters
            if filters and not self._matches_filters(tool, filters):
                continue
            
            # Calculate cosine similarity
            similarity = self._cosine_similarity(query_embedding, tool_embedding)
            similarities.append((tool_name, similarity))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top k
        return [self.tools[name] for name, _ in similarities[:top_k]]
    
    def _keyword_search(
        self,
        query: str,
        top_k: int,
        filters: Optional[Dict[str, Any]]
    ) -> List[ToolMetadata]:
        """Fallback keyword-based search."""
        query_lower = query.lower()
        matches = []
        
        for tool_name, tool in self.tools.items():
            if filters and not self._matches_filters(tool, filters):
                continue
            
            # Simple keyword matching
            score = 0
            if query_lower in tool.name.lower():
                score += 3
            if query_lower in tool.description.lower():
                score += 2
            for cap in tool.capabilities:
                if query_lower in cap.lower():
                    score += 1
            
            if score > 0:
                matches.append((tool, score))
        
        matches.sort(key=lambda x: x[1], reverse=True)
        return [tool for tool, _ in matches[:top_k]]
    
    def find_by_capability(
        self,
        capability: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ToolMetadata]:
        """
        Find tools by capability.
        
        Args:
            capability: Capability to search for
            filters: Optional additional filters
            
        Returns:
            List of matching tools
            
        Example:
            ```python
            fraud_tools = registry.find_by_capability("fraud_detection")
            ```
        """
        results = []
        for tool in self.tools.values():
            if capability in tool.capabilities:
                if not filters or self._matches_filters(tool, filters):
                    results.append(tool)
        
        return results
    
    def find_by_category(
        self,
        category: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ToolMetadata]:
        """Find tools by category."""
        results = []
        for tool in self.tools.values():
            if tool.category == category:
                if not filters or self._matches_filters(tool, filters):
                    results.append(tool)
        
        return results
    
    def get_cheapest_tool(
        self,
        capability: str
    ) -> Optional[ToolMetadata]:
        """
        Find cheapest tool for a capability.
        
        Args:
            capability: Required capability
            
        Returns:
            Tool with lowest cost, or None
        """
        matching_tools = self.find_by_capability(capability)
        
        # Filter tools with cost info
        costed_tools = [t for t in matching_tools if t.estimated_cost is not None]
        
        if not costed_tools:
            return None
        
        return min(costed_tools, key=lambda t: t.estimated_cost)
    
    def get_fastest_tool(
        self,
        capability: str
    ) -> Optional[ToolMetadata]:
        """
        Find fastest tool for a capability.
        
        Args:
            capability: Required capability
            
        Returns:
            Tool with lowest latency, or None
        """
        matching_tools = self.find_by_capability(capability)
        
        # Filter tools with latency info
        timed_tools = [t for t in matching_tools if t.estimated_latency_ms is not None]
        
        if not timed_tools:
            return None
        
        return min(timed_tools, key=lambda t: t.estimated_latency_ms)
    
    def get_active_tools(self) -> List[ToolMetadata]:
        """Get all active (non-deprecated) tools."""
        return [
            tool for tool in self.tools.values()
            if tool.status == ToolStatus.ACTIVE and not tool.deprecated
        ]
    
    def deprecate_tool(
        self,
        name: str,
        in_favor_of: Optional[str] = None
    ):
        """
        Deprecate a tool.
        
        Args:
            name: Tool name
            in_favor_of: Replacement tool name
        """
        if name in self.tools:
            self.tools[name].deprecated = True
            self.tools[name].status = ToolStatus.DEPRECATED
            self.tools[name].deprecated_in_favor_of = in_favor_of
    
    def get_tool_info(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get complete tool information.
        
        Args:
            name: Tool name
            
        Returns:
            Tool info dict or None
        """
        if name not in self.tools:
            return None
        
        tool = self.tools[name]
        return {
            "name": tool.name,
            "version": tool.version,
            "description": tool.description,
            "capabilities": tool.capabilities,
            "input_schema": tool.input_schema,
            "output_schema": tool.output_schema,
            "estimated_latency_ms": tool.estimated_latency_ms,
            "estimated_cost": tool.estimated_cost,
            "status": tool.status.value,
            "deprecated": tool.deprecated,
            "deprecated_in_favor_of": tool.deprecated_in_favor_of,
            "examples": tool.examples,
            "documentation_url": tool.documentation_url
        }
    
    def list_capabilities(self) -> List[str]:
        """List all available capabilities across all tools."""
        capabilities = set()
        for tool in self.tools.values():
            capabilities.update(tool.capabilities)
        return sorted(capabilities)
    
    def list_categories(self) -> List[str]:
        """List all tool categories."""
        categories = {tool.category for tool in self.tools.values() if tool.category}
        return sorted(categories)
    
    def export_registry(self) -> Dict[str, Any]:
        """
        Export registry to JSON-serializable format.
        
        Returns:
            Dict representation of the registry
        """
        return {
            "tools": {
                name: {
                    **tool.__dict__,
                    "status": tool.status.value,
                    "registered_at": tool.registered_at.isoformat()
                }
                for name, tool in self.tools.items()
            },
            "capabilities": self.list_capabilities(),
            "categories": self.list_categories()
        }
    
    def _matches_filters(
        self,
        tool: ToolMetadata,
        filters: Dict[str, Any]
    ) -> bool:
        """Check if tool matches filters."""
        for key, value in filters.items():
            tool_value = getattr(tool, key, None)
            if tool_value != value:
                return False
        return True
    
    @staticmethod
    def _cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        import math
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)


# Global registry instance
_global_registry = None


def get_global_registry() -> DynamicToolRegistry:
    """Get or create global tool registry."""
    global _global_registry
    if _global_registry is None:
        _global_registry = DynamicToolRegistry()
    return _global_registry

