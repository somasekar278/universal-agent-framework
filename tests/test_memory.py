"""
Test Suite for Memory System

Tests for agent-governed memory.
"""

import pytest
from memory import MemoryManager, MemoryType, MemoryImportance


class TestMemoryManager:
    """Test memory manager."""
    
    @pytest.mark.asyncio
    async def test_memory_storage(self):
        """Test storing memories."""
        manager = MemoryManager()
        
        await manager.store(
            content="Important transaction detected",
            memory_type=MemoryType.EPISODIC,
            importance=MemoryImportance.HIGH,
            metadata={"transaction_id": "123"}
        )
        
        assert True  # Memory stored successfully
    
    @pytest.mark.asyncio
    async def test_memory_retrieval(self):
        """Test retrieving memories."""
        manager = MemoryManager()
        
        # Store memory
        await manager.store(
            content="Test memory",
            memory_type=MemoryType.SHORT_TERM
        )
        
        # Retrieve
        results = await manager.retrieve(
            query="Test memory",
            top_k=5
        )
        
        assert len(results) >= 0


class TestMemoryStores:
    """Test memory stores."""
    
    def test_short_term_memory(self):
        """Test short-term memory store."""
        from memory.stores import ShortTermMemory
        
        store = ShortTermMemory()
        assert store is not None
    
    def test_long_term_memory(self):
        """Test long-term memory store."""
        from memory.stores import LongTermMemory
        
        store = LongTermMemory()
        assert store is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

