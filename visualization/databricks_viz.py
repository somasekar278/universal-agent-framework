"""
Databricks-Native Visualization

Production-grade visualizations designed for Databricks notebooks:
- Works natively with displayHTML()
- Integrates with MLflow
- Interactive widgets
- Execution graphs using Mermaid
- Timeline charts using Plotly
- Can also run standalone

Usage in Databricks:
    from visualization import DatabricksVisualizer
    
    viz = DatabricksVisualizer()
    viz.show_execution_graph(trace)  # Renders in notebook
    viz.show_timeline(trace)
    viz.show_decision_tree(decisions)
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class DatabricksVisualizer:
    """
    Databricks-native visualizer for agent workflows.
    
    Features:
    - Execution graph (Mermaid diagram)
    - Timeline (Plotly chart)
    - Decision inspector
    - Tool call replay
    - Prompt comparison
    
    Works in:
    - Databricks notebooks (displayHTML)
    - Jupyter notebooks
    - Standalone Python
    """
    
    def __init__(self):
        """Initialize visualizer."""
        self._check_environment()
    
    def _check_environment(self):
        """Check if running in Databricks."""
        try:
            import IPython
            self.ipython = IPython.get_ipython()
            self.in_databricks = hasattr(self.ipython, 'run_cell')
        except:
            self.ipython = None
            self.in_databricks = False
    
    def show_execution_graph(self, trace: Dict[str, Any]):
        """
        Show execution graph as Mermaid diagram.
        
        Args:
            trace: Execution trace with actions/decisions
        """
        mermaid = self._generate_mermaid(trace)
        html = f"""
        <div class="mermaid">
        {mermaid}
        </div>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
        </script>
        """
        
        self._display(html)
    
    def show_timeline(self, trace: Dict[str, Any]):
        """
        Show execution timeline using Plotly.
        
        Args:
            trace: Execution trace
        """
        html = self._generate_timeline_html(trace)
        self._display(html)
    
    def show_decision_tree(self, decisions: List[Dict[str, Any]]):
        """
        Show decision tree with explanations.
        
        Args:
            decisions: List of agent decisions
        """
        html = self._generate_decision_tree_html(decisions)
        self._display(html)
    
    def show_tool_calls(self, tool_calls: List[Dict[str, Any]]):
        """
        Show interactive tool call viewer.
        
        Args:
            tool_calls: List of tool calls with inputs/outputs
        """
        html = self._generate_tool_calls_html(tool_calls)
        self._display(html)
    
    def compare_prompts(self, versions: List[Dict[str, Any]]):
        """
        Compare prompt versions side-by-side.
        
        Args:
            versions: List of prompt versions
        """
        html = self._generate_prompt_comparison_html(versions)
        self._display(html)
    
    def explain_decision(self, decision: Dict[str, Any], context: Dict[str, Any]):
        """
        Explain why agent made a decision.
        
        Args:
            decision: Decision to explain
            context: Context information
        """
        html = self._generate_explanation_html(decision, context)
        self._display(html)
    
    def create_dashboard(self, trace: Dict[str, Any]):
        """
        Create comprehensive dashboard with all visualizations.
        
        Args:
            trace: Complete execution trace
        """
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
                .dashboard {{ max-width: 1400px; margin: 0 auto; }}
                .section {{ background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .section h2 {{ margin-top: 0; color: #333; border-bottom: 2px solid #0066cc; padding-bottom: 10px; }}
                .tabs {{ display: flex; gap: 10px; margin-bottom: 20px; }}
                .tab {{ padding: 10px 20px; background: #e0e0e0; border-radius: 4px; cursor: pointer; }}
                .tab.active {{ background: #0066cc; color: white; }}
            </style>
        </head>
        <body>
            <div class="dashboard">
                <h1>🔍 Agent Execution Dashboard</h1>
                
                <div class="section">
                    <h2>📊 Execution Graph</h2>
                    <div id="graph"></div>
                </div>
                
                <div class="section">
                    <h2>⏱️ Timeline</h2>
                    <div id="timeline"></div>
                </div>
                
                <div class="section">
                    <h2>🔧 Tool Calls</h2>
                    <div id="toolcalls"></div>
                </div>
                
                <div class="section">
                    <h2>🤔 Decisions</h2>
                    <div id="decisions"></div>
                </div>
            </div>
        </body>
        </html>
        """
        self._display(html)
    
    def _generate_mermaid(self, trace: Dict[str, Any]) -> str:
        """Generate Mermaid diagram from trace."""
        actions = trace.get("actions", [])
        
        lines = ["graph TD"]
        lines.append("    Start([Start]) --> A1")
        
        for i, action in enumerate(actions):
            node_id = f"A{i+1}"
            action_type = action.get("type", "unknown")
            action_name = action.get("name", "Unknown")
            
            # Style based on action type
            if action_type == "tool_call":
                lines.append(f"    {node_id}[{action_name}]:::tool")
            elif action_type == "reasoning":
                lines.append(f"    {node_id}{{{action_name}}}:::reasoning")
            elif action_type == "decision":
                lines.append(f"    {node_id}{{{action_name}}}:::decision")
            else:
                lines.append(f"    {node_id}[{action_name}]")
            
            # Add edge to next
            if i < len(actions) - 1:
                lines.append(f"    {node_id} --> A{i+2}")
        
        # Final node
        if actions:
            last_id = f"A{len(actions)}"
            lines.append(f"    {last_id} --> End([End])")
        
        # Styling
        lines.append("    classDef tool fill:#90EE90,stroke:#2E8B57")
        lines.append("    classDef reasoning fill:#FFD700,stroke:#FF8C00")
        lines.append("    classDef decision fill:#87CEEB,stroke:#4682B4")
        
        return "\n".join(lines)
    
    def _generate_timeline_html(self, trace: Dict[str, Any]) -> str:
        """Generate Plotly timeline."""
        actions = trace.get("actions", [])
        
        # Build Plotly data
        tasks = []
        for i, action in enumerate(actions):
            tasks.append({
                "Task": action.get("name", f"Action {i}"),
                "Start": action.get("start_time", 0),
                "Duration": action.get("duration_ms", 100)
            })
        
        html = f"""
        <div id="timeline"></div>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <script>
            var data = {json.dumps(tasks)};
            var traces = data.map(function(task, i) {{
                return {{
                    x: [task.Duration],
                    y: [task.Task],
                    name: task.Task,
                    type: 'bar',
                    orientation: 'h',
                    text: task.Duration + 'ms',
                    textposition: 'auto'
                }};
            }});
            
            var layout = {{
                title: 'Execution Timeline',
                xaxis: {{ title: 'Duration (ms)' }},
                barmode: 'stack',
                height: 400
            }};
            
            Plotly.newPlot('timeline', traces, layout);
        </script>
        """
        
        return html
    
    def _generate_decision_tree_html(self, decisions: List[Dict]) -> str:
        """Generate decision tree visualization."""
        html = "<div style='font-family: monospace;'>"
        
        for i, decision in enumerate(decisions):
            indent = "  " * decision.get("depth", 0)
            name = decision.get("name", "Decision")
            reason = decision.get("reason", "No reason provided")
            
            html += f"""
            <div style='margin: 10px 0; padding: 10px; background: #f0f0f0; border-left: 4px solid #0066cc;'>
                <strong>{indent}├─ {name}</strong><br>
                <span style='color: #666;'>{indent}   {reason}</span>
            </div>
            """
        
        html += "</div>"
        return html
    
    def _generate_tool_calls_html(self, tool_calls: List[Dict]) -> str:
        """Generate tool calls viewer."""
        html = "<div>"
        
        for i, call in enumerate(tool_calls):
            tool_name = call.get("tool", "Unknown")
            input_data = json.dumps(call.get("input", {}), indent=2)
            output_data = json.dumps(call.get("output", {}), indent=2)
            duration = call.get("duration_ms", 0)
            
            html += f"""
            <details style='margin: 10px 0; padding: 15px; background: white; border: 1px solid #ddd; border-radius: 4px;'>
                <summary style='cursor: pointer; font-weight: bold; color: #0066cc;'>
                    🔧 {tool_name} <span style='color: #666; font-weight: normal;'>({duration}ms)</span>
                </summary>
                <div style='margin-top: 10px;'>
                    <h4>Input:</h4>
                    <pre style='background: #f5f5f5; padding: 10px; border-radius: 4px;'>{input_data}</pre>
                    <h4>Output:</h4>
                    <pre style='background: #f5f5f5; padding: 10px; border-radius: 4px;'>{output_data}</pre>
                </div>
            </details>
            """
        
        html += "</div>"
        return html
    
    def _generate_prompt_comparison_html(self, versions: List[Dict]) -> str:
        """Generate prompt comparison view."""
        html = """
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px;'>
        """
        
        for version in versions:
            version_name = version.get("version", "Unknown")
            prompt = version.get("prompt", "")
            metrics = version.get("metrics", {})
            
            html += f"""
            <div style='border: 1px solid #ddd; border-radius: 4px; padding: 15px; background: white;'>
                <h3 style='margin-top: 0; color: #0066cc;'>{version_name}</h3>
                <pre style='background: #f5f5f5; padding: 10px; border-radius: 4px; white-space: pre-wrap;'>{prompt}</pre>
                <div style='margin-top: 10px; padding-top: 10px; border-top: 1px solid #ddd;'>
                    <strong>Metrics:</strong>
                    <ul style='margin: 5px 0;'>
                        {"".join(f"<li>{k}: {v}</li>" for k, v in metrics.items())}
                    </ul>
                </div>
            </div>
            """
        
        html += "</div>"
        return html
    
    def _generate_explanation_html(self, decision: Dict, context: Dict) -> str:
        """Generate decision explanation."""
        html = f"""
        <div style='background: #fff3cd; border-left: 4px solid #ffc107; padding: 20px; margin: 20px 0;'>
            <h3 style='margin-top: 0;'>🤔 Why did the agent decide: "{decision.get('action', 'Unknown')}"?</h3>
            
            <div style='margin: 15px 0;'>
                <h4>Decision Factors:</h4>
                <ul>
        """
        
        factors = decision.get("factors", [])
        for factor in factors:
            html += f"<li><strong>{factor.get('name', 'Factor')}:</strong> {factor.get('value', 'N/A')} (weight: {factor.get('weight', 0)})</li>"
        
        html += """
                </ul>
            </div>
            
            <div style='margin: 15px 0;'>
                <h4>Context:</h4>
                <pre style='background: white; padding: 10px; border-radius: 4px;'>{}</pre>
            </div>
            
            <div style='margin: 15px 0;'>
                <h4>Reasoning:</h4>
                <p>{}</p>
            </div>
        </div>
        """.format(
            json.dumps(context, indent=2),
            decision.get("reasoning", "No reasoning provided")
        )
        
        return html
    
    def _display(self, html: str):
        """Display HTML in appropriate environment."""
        if self.in_databricks and self.ipython:
            # Databricks notebook
            from IPython.display import HTML, display
            display(HTML(html))
        elif self.ipython:
            # Jupyter notebook
            from IPython.display import HTML, display
            display(HTML(html))
        else:
            # Standalone - save to file
            with open("visualization_output.html", "w") as f:
                f.write(html)
            print("Visualization saved to visualization_output.html")
    
    def log_to_mlflow(self, trace: Dict[str, Any], run_id: Optional[str] = None):
        """
        Log visualizations to MLflow.
        
        Args:
            trace: Execution trace
            run_id: MLflow run ID (uses active run if None)
        """
        try:
            import mlflow
            
            # Generate visualizations
            graph_html = f"<div class='mermaid'>{self._generate_mermaid(trace)}</div>"
            timeline_html = self._generate_timeline_html(trace)
            
            # Log as artifacts
            with mlflow.start_run(run_id=run_id):
                mlflow.log_text(graph_html, "visualizations/execution_graph.html")
                mlflow.log_text(timeline_html, "visualizations/timeline.html")
                
                # Log metrics
                actions = trace.get("actions", [])
                mlflow.log_metric("total_actions", len(actions))
                mlflow.log_metric("total_duration_ms", sum(a.get("duration_ms", 0) for a in actions))
                
                print("✅ Visualizations logged to MLflow")
                
        except ImportError:
            print("⚠️  MLflow not available")
        except Exception as e:
            print(f"⚠️  Failed to log to MLflow: {e}")


def create_databricks_widget(trace: Dict[str, Any]):
    """
    Create interactive Databricks widget for exploration.
    
    Usage in Databricks notebook:
        from visualization import create_databricks_widget
        create_databricks_widget(execution_trace)
    """
    try:
        # Check if in Databricks
        import dbutils
        
        # Create dropdown widget for view selection
        dbutils.widgets.dropdown("view", "graph", ["graph", "timeline", "tools", "decisions"], "Select View")
        
        # Get selected view
        view = dbutils.widgets.get("view")
        
        # Show appropriate visualization
        viz = DatabricksVisualizer()
        
        if view == "graph":
            viz.show_execution_graph(trace)
        elif view == "timeline":
            viz.show_timeline(trace)
        elif view == "tools":
            viz.show_tool_calls(trace.get("tool_calls", []))
        elif view == "decisions":
            viz.show_decision_tree(trace.get("decisions", []))
            
    except:
        # Not in Databricks, use standard visualizer
        viz = DatabricksVisualizer()
        viz.create_dashboard(trace)

