"""
FastAPI Service

Production REST API for agent execution.
"""

from typing import Dict, Any, Optional
from datetime import datetime


class AgentAPI:
    """
    FastAPI service for agents.
    
    Usage:
        api = AgentAPI()
        api.run(host="0.0.0.0", port=8000)
        
    Endpoints:
        POST /execute - Execute agent
        GET /health - Health check
        GET /metrics - Metrics
        GET /agents - List agents
    """
    
    def __init__(self):
        """Initialize API."""
        self.app = None
        self._init_app()
    
    def _init_app(self):
        """Initialize FastAPI app."""
        try:
            from fastapi import FastAPI, HTTPException
            from fastapi.responses import JSONResponse
            
            app = FastAPI(
                title="SOTA Agent API",
                description="Production API for AI agents",
                version="0.2.1"
            )
            
            @app.post("/execute")
            async def execute_agent(request: Dict[str, Any]):
                """Execute an agent."""
                try:
                    from agents import AgentRouter
                    
                    router = AgentRouter.from_yaml("config/agents.yaml")
                    
                    result = await router.route(
                        request.get("agent_name"),
                        request.get("input_data")
                    )
                    
                    return {"status": "success", "result": result}
                
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))
            
            @app.get("/health")
            async def health_check():
                """Health check endpoint."""
                from monitoring import HealthCheck
                
                health = HealthCheck()
                status = health.get_status_summary()
                
                return status
            
            @app.get("/metrics")
            async def get_metrics():
                """Get metrics."""
                from telemetry import AgentMetrics
                
                metrics = AgentMetrics()
                return metrics.get_all_metrics()
            
            @app.get("/agents")
            async def list_agents():
                """List available agents."""
                from agents import AgentRegistry
                
                registry = AgentRegistry()
                return {"agents": registry.list_agents()}
            
            self.app = app
            print("✅ FastAPI app initialized")
            
        except ImportError:
            print("⚠️  FastAPI not available. Install: pip install fastapi uvicorn")
    
    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """Run the API server."""
        if self.app is None:
            print("❌ FastAPI not available")
            return
        
        try:
            import uvicorn
            uvicorn.run(self.app, host=host, port=port)
        except ImportError:
            print("⚠️  uvicorn not available. Install: pip install uvicorn")


def create_app():
    """Create FastAPI app."""
    api = AgentAPI()
    return api.app

