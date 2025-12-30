"""
Trajectory Optimization

Optimizes the sequence of actions/steps an agent takes to complete a task.

Features:
- Records agent execution paths
- Identifies efficient vs inefficient trajectories
- Learns optimal action sequences
- Suggests improvements
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json


class ActionType(str, Enum):
    """Types of actions an agent can take."""
    TOOL_CALL = "tool_call"
    REASONING = "reasoning"
    DECISION = "decision"
    RETRIEVAL = "retrieval"
    REFLECTION = "reflection"
    OUTPUT = "output"


@dataclass
class Action:
    """A single action in a trajectory."""
    action_type: ActionType
    name: str
    input: Any
    output: Any
    duration_ms: float
    cost: float = 0.0  # Token cost or API cost
    success: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Trajectory:
    """A complete execution trajectory for a task."""
    task_id: str
    agent_id: str
    actions: List[Action] = field(default_factory=list)
    final_result: Any = None
    success: bool = False
    total_duration_ms: float = 0.0
    total_cost: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    
    def add_action(self, action: Action):
        """Add action to trajectory."""
        self.actions.append(action)
        self.total_duration_ms += action.duration_ms
        self.total_cost += action.cost
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "actions": [
                {
                    "type": a.action_type.value,
                    "name": a.name,
                    "duration_ms": a.duration_ms,
                    "cost": a.cost,
                    "success": a.success
                }
                for a in self.actions
            ],
            "success": self.success,
            "total_duration_ms": self.total_duration_ms,
            "total_cost": self.total_cost,
            "num_actions": len(self.actions)
        }


@dataclass
class TrajectoryMetrics:
    """Metrics for comparing trajectories."""
    avg_duration_ms: float
    avg_cost: float
    avg_actions: float
    success_rate: float
    efficiency_score: float  # Combined metric


class TrajectoryLibrary:
    """
    Library of recorded trajectories.
    
    Stores successful and failed trajectories for learning.
    """
    
    def __init__(self, max_trajectories: int = 1000):
        """
        Initialize trajectory library.
        
        Args:
            max_trajectories: Maximum trajectories to store
        """
        self.max_trajectories = max_trajectories
        self._trajectories: List[Trajectory] = []
        self._by_task: Dict[str, List[Trajectory]] = {}
    
    def add(self, trajectory: Trajectory):
        """Add trajectory to library."""
        self._trajectories.append(trajectory)
        
        # Index by task pattern
        task_pattern = self._extract_task_pattern(trajectory)
        if task_pattern not in self._by_task:
            self._by_task[task_pattern] = []
        self._by_task[task_pattern].append(trajectory)
        
        # Prune if needed
        if len(self._trajectories) > self.max_trajectories:
            self._prune()
    
    def get_similar(self, task_id: str, limit: int = 10) -> List[Trajectory]:
        """Get similar trajectories."""
        task_pattern = self._extract_task_pattern_from_id(task_id)
        trajectories = self._by_task.get(task_pattern, [])
        return trajectories[:limit]
    
    def get_best(self, task_pattern: str, metric: str = "efficiency") -> Optional[Trajectory]:
        """Get best trajectory for a task pattern."""
        trajectories = self._by_task.get(task_pattern, [])
        if not trajectories:
            return None
        
        # Filter successful only
        successful = [t for t in trajectories if t.success]
        if not successful:
            return None
        
        # Sort by metric
        if metric == "efficiency":
            successful.sort(key=lambda t: t.total_cost + t.total_duration_ms / 1000)
        elif metric == "speed":
            successful.sort(key=lambda t: t.total_duration_ms)
        elif metric == "cost":
            successful.sort(key=lambda t: t.total_cost)
        
        return successful[0]
    
    def get_metrics(self, task_pattern: Optional[str] = None) -> TrajectoryMetrics:
        """Get aggregate metrics."""
        trajectories = (
            self._by_task.get(task_pattern, [])
            if task_pattern
            else self._trajectories
        )
        
        if not trajectories:
            return TrajectoryMetrics(0, 0, 0, 0, 0)
        
        successful = [t for t in trajectories if t.success]
        
        return TrajectoryMetrics(
            avg_duration_ms=sum(t.total_duration_ms for t in trajectories) / len(trajectories),
            avg_cost=sum(t.total_cost for t in trajectories) / len(trajectories),
            avg_actions=sum(len(t.actions) for t in trajectories) / len(trajectories),
            success_rate=len(successful) / len(trajectories),
            efficiency_score=self._calculate_efficiency(trajectories)
        )
    
    def _extract_task_pattern(self, trajectory: Trajectory) -> str:
        """Extract task pattern from trajectory."""
        # Simple pattern: agent_id + action types
        action_signature = "_".join([a.action_type.value for a in trajectory.actions[:5]])
        return f"{trajectory.agent_id}_{action_signature}"
    
    def _extract_task_pattern_from_id(self, task_id: str) -> str:
        """Extract pattern from task ID."""
        # Simplified - would use more sophisticated matching
        return task_id.split("_")[0] if "_" in task_id else task_id
    
    def _calculate_efficiency(self, trajectories: List[Trajectory]) -> float:
        """Calculate efficiency score."""
        if not trajectories:
            return 0.0
        
        successful = [t for t in trajectories if t.success]
        if not successful:
            return 0.0
        
        # Normalize by cost and duration
        avg_cost = sum(t.total_cost for t in successful) / len(successful)
        avg_duration = sum(t.total_duration_ms for t in successful) / len(successful)
        
        # Lower is better, so invert
        efficiency = 1.0 / (1.0 + avg_cost + avg_duration / 1000)
        return efficiency
    
    def _prune(self):
        """Prune oldest, least useful trajectories."""
        # Keep successful trajectories, remove oldest failures
        failures = [t for t in self._trajectories if not t.success]
        failures.sort(key=lambda t: t.created_at)
        
        # Remove oldest failures
        to_remove = len(self._trajectories) - self.max_trajectories
        for trajectory in failures[:to_remove]:
            self._trajectories.remove(trajectory)
            
            # Remove from index
            pattern = self._extract_task_pattern(trajectory)
            if pattern in self._by_task:
                self._by_task[pattern].remove(trajectory)


class TrajectoryOptimizer:
    """
    Optimizes agent trajectories.
    
    Learns optimal action sequences from recorded executions.
    
    Usage:
        optimizer = TrajectoryOptimizer()
        
        # Record trajectory
        trajectory = Trajectory(task_id="fraud_001", agent_id="fraud_detector")
        trajectory.add_action(Action(...))
        optimizer.record(trajectory)
        
        # Get optimization suggestions
        suggestions = await optimizer.suggest_improvements(trajectory)
        
        # Get optimal path for task
        optimal = optimizer.get_optimal_trajectory("fraud_detection")
    """
    
    def __init__(self, library: Optional[TrajectoryLibrary] = None):
        """
        Initialize optimizer.
        
        Args:
            library: Trajectory library (creates new if None)
        """
        self.library = library or TrajectoryLibrary()
        self._optimization_rules: List[Dict[str, Any]] = []
        self._initialize_rules()
    
    def _initialize_rules(self):
        """Initialize optimization rules."""
        self._optimization_rules = [
            {
                "name": "avoid_redundant_retrievals",
                "description": "Don't retrieve same data multiple times",
                "pattern": lambda actions: self._detect_redundant_retrievals(actions),
                "suggestion": "Cache retrieval results"
            },
            {
                "name": "order_by_cost",
                "description": "Do cheap operations before expensive ones",
                "pattern": lambda actions: self._detect_cost_ordering(actions),
                "suggestion": "Reorder to do cheap validation before expensive processing"
            },
            {
                "name": "avoid_unnecessary_reasoning",
                "description": "Skip reasoning for obvious cases",
                "pattern": lambda actions: self._detect_unnecessary_reasoning(actions),
                "suggestion": "Add early exit for simple cases"
            },
            {
                "name": "parallelize_independent",
                "description": "Run independent actions in parallel",
                "pattern": lambda actions: self._detect_parallelizable(actions),
                "suggestion": "Execute independent actions concurrently"
            }
        ]
    
    def record(self, trajectory: Trajectory):
        """Record a trajectory."""
        self.library.add(trajectory)
    
    async def suggest_improvements(self, trajectory: Trajectory) -> List[Dict[str, Any]]:
        """
        Suggest improvements for a trajectory.
        
        Args:
            trajectory: Trajectory to analyze
            
        Returns:
            List of improvement suggestions
        """
        suggestions = []
        
        # Apply optimization rules
        for rule in self._optimization_rules:
            violations = rule["pattern"](trajectory.actions)
            if violations:
                suggestions.append({
                    "rule": rule["name"],
                    "description": rule["description"],
                    "suggestion": rule["suggestion"],
                    "violations": violations,
                    "potential_savings": self._estimate_savings(violations, trajectory)
                })
        
        # Compare to best trajectories
        similar = self.library.get_similar(trajectory.task_id)
        if similar:
            best = self.library.get_best(
                self._extract_pattern(trajectory),
                metric="efficiency"
            )
            if best and best.total_cost < trajectory.total_cost:
                suggestions.append({
                    "rule": "learn_from_best",
                    "description": "Similar task has better trajectory",
                    "suggestion": f"Follow action sequence from trajectory {best.task_id}",
                    "best_trajectory": best.to_dict(),
                    "potential_savings": {
                        "cost": trajectory.total_cost - best.total_cost,
                        "duration_ms": trajectory.total_duration_ms - best.total_duration_ms
                    }
                })
        
        return suggestions
    
    def get_optimal_trajectory(self, task_pattern: str) -> Optional[Trajectory]:
        """Get optimal trajectory for a task pattern."""
        return self.library.get_best(task_pattern, metric="efficiency")
    
    def get_metrics(self, task_pattern: Optional[str] = None) -> TrajectoryMetrics:
        """Get trajectory metrics."""
        return self.library.get_metrics(task_pattern)
    
    def _detect_redundant_retrievals(self, actions: List[Action]) -> List[Dict]:
        """Detect redundant retrievals."""
        retrievals = {}
        redundant = []
        
        for i, action in enumerate(actions):
            if action.action_type == ActionType.RETRIEVAL:
                key = str(action.input)
                if key in retrievals:
                    redundant.append({
                        "index": i,
                        "action": action.name,
                        "duplicate_of": retrievals[key]
                    })
                else:
                    retrievals[key] = i
        
        return redundant
    
    def _detect_cost_ordering(self, actions: List[Action]) -> List[Dict]:
        """Detect suboptimal cost ordering."""
        violations = []
        
        for i in range(len(actions) - 1):
            current = actions[i]
            next_action = actions[i + 1]
            
            # If expensive action comes before cheap one
            if current.cost > next_action.cost * 5 and next_action.success:
                violations.append({
                    "index": i,
                    "expensive": current.name,
                    "cheap": next_action.name,
                    "cost_diff": current.cost - next_action.cost
                })
        
        return violations
    
    def _detect_unnecessary_reasoning(self, actions: List[Action]) -> List[Dict]:
        """Detect unnecessary reasoning steps."""
        violations = []
        
        # Simple heuristic: multiple reasoning actions in sequence
        reasoning_sequence = []
        for i, action in enumerate(actions):
            if action.action_type == ActionType.REASONING:
                reasoning_sequence.append(i)
            else:
                if len(reasoning_sequence) > 2:
                    violations.append({
                        "indices": reasoning_sequence,
                        "count": len(reasoning_sequence)
                    })
                reasoning_sequence = []
        
        return violations
    
    def _detect_parallelizable(self, actions: List[Action]) -> List[Dict]:
        """Detect actions that could run in parallel."""
        parallelizable = []
        
        # Simple heuristic: consecutive actions with no dependencies
        for i in range(len(actions) - 1):
            current = actions[i]
            next_action = actions[i + 1]
            
            # If actions don't depend on each other
            if not self._has_dependency(current, next_action):
                parallelizable.append({
                    "indices": [i, i + 1],
                    "actions": [current.name, next_action.name]
                })
        
        return parallelizable
    
    def _has_dependency(self, action1: Action, action2: Action) -> bool:
        """Check if action2 depends on action1."""
        # Simple check: if action2's input contains action1's output
        if action1.output and action2.input:
            return str(action1.output) in str(action2.input)
        return False
    
    def _estimate_savings(self, violations: List[Dict], trajectory: Trajectory) -> Dict:
        """Estimate potential savings from fixes."""
        # Rough estimates
        cost_savings = len(violations) * 0.1 * trajectory.total_cost
        time_savings = len(violations) * 100  # ms
        
        return {
            "cost_reduction": min(cost_savings, trajectory.total_cost * 0.5),
            "time_reduction_ms": min(time_savings, trajectory.total_duration_ms * 0.3)
        }
    
    def _extract_pattern(self, trajectory: Trajectory) -> str:
        """Extract pattern from trajectory."""
        return self.library._extract_task_pattern(trajectory)
    
    def export_learned_patterns(self) -> Dict[str, Any]:
        """Export learned optimization patterns."""
        patterns = {}
        
        for task_pattern, trajectories in self.library._by_task.items():
            best = self.library.get_best(task_pattern)
            metrics = self.library.get_metrics(task_pattern)
            
            if best:
                patterns[task_pattern] = {
                    "best_trajectory": best.to_dict(),
                    "metrics": {
                        "avg_duration_ms": metrics.avg_duration_ms,
                        "avg_cost": metrics.avg_cost,
                        "success_rate": metrics.success_rate,
                        "efficiency_score": metrics.efficiency_score
                    },
                    "optimal_sequence": [
                        {"type": a.action_type.value, "name": a.name}
                        for a in best.actions
                    ]
                }
        
        return patterns

