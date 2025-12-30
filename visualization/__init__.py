"""
Visualization & Debugging Module

Production-grade visualization and debugging tools for agent workflows:
- Execution graph visualizer
- Trace timeline
- Tool call replay
- Prompt version comparison
- Agent decision inspection
- Explainability ("why did the agent do this?")
- Gradio UI for interactive exploration

Install:
    pip install sota-agent-framework[ui]

Usage:
    from visualization import ExecutionVisualizer, TraceTimeline, launch_ui
    
    # Visualize execution
    viz = ExecutionVisualizer()
    graph = viz.create_graph(execution_trace)
    
    # Launch UI
    launch_ui(port=7860)
"""

from .databricks_viz import DatabricksVisualizer

__all__ = [
    "DatabricksVisualizer",
]

