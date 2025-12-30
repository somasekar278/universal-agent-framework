"""Test Suite for Monitoring"""

import pytest
from monitoring import HealthCheck, HealthStatus


class TestHealthCheck:
    """Test health check system."""
    
    def test_health_check_initialization(self):
        """Test health check initialization."""
        health = HealthCheck()
        assert health is not None
    
    def test_check_all(self):
        """Test checking all components."""
        health = HealthCheck()
        results = health.check_all()
        
        assert isinstance(results, dict)
        assert len(results) > 0
    
    def test_is_healthy(self):
        """Test overall health status."""
        health = HealthCheck()
        is_healthy = health.is_healthy()
        
        assert isinstance(is_healthy, bool)
    
    def test_status_summary(self):
        """Test status summary."""
        health = HealthCheck()
        summary = health.get_status_summary()
        
        assert "status" in summary
        assert "components" in summary


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

