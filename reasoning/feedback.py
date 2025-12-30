"""
Feedback Loop System

Enables self-improvement through critique → revise → retry cycles.

Features:
- Automated critique generation
- Revision based on feedback
- Learning from mistakes
- Performance tracking
"""

from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class CritiqueType(str, Enum):
    """Types of critiques."""
    ACCURACY = "accuracy"
    COMPLETENESS = "completeness"
    EFFICIENCY = "efficiency"
    SAFETY = "safety"
    REASONING = "reasoning"
    OUTPUT_FORMAT = "output_format"


@dataclass
class Critique:
    """A critique of agent output."""
    critique_type: CritiqueType
    severity: str  # "low", "medium", "high", "critical"
    message: str
    specific_issue: str
    suggested_fix: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Revision:
    """A revision made in response to critique."""
    original_output: Any
    revised_output: Any
    critiques_addressed: List[Critique]
    improvement_score: float  # 0.0 to 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class FeedbackConfig:
    """Configuration for feedback loop."""
    max_retries: int = 3
    min_improvement: float = 0.1  # Minimum improvement to continue
    enable_self_critique: bool = True
    store_learnings: bool = True
    critique_severity_threshold: str = "medium"  # Minimum severity to trigger revision


class ImprovementTracker:
    """
    Tracks improvement over time from feedback loops.
    """
    
    def __init__(self):
        """Initialize tracker."""
        self._iterations: List[Dict[str, Any]] = []
        self._learnings: Dict[str, List[str]] = {}  # issue_type -> fixes
    
    def record_iteration(
        self,
        original_output: Any,
        revised_output: Any,
        critiques: List[Critique],
        improvement: float
    ):
        """Record a feedback iteration."""
        self._iterations.append({
            "timestamp": datetime.now(),
            "num_critiques": len(critiques),
            "improvement": improvement,
            "critique_types": [c.critique_type.value for c in critiques]
        })
        
        # Store learnings
        for critique in critiques:
            if critique.suggested_fix:
                if critique.critique_type.value not in self._learnings:
                    self._learnings[critique.critique_type.value] = []
                self._learnings[critique.critique_type.value].append(critique.suggested_fix)
    
    def get_common_issues(self) -> Dict[str, int]:
        """Get most common issues."""
        issues = {}
        for iteration in self._iterations:
            for critique_type in iteration["critique_types"]:
                issues[critique_type] = issues.get(critique_type, 0) + 1
        return dict(sorted(issues.items(), key=lambda x: x[1], reverse=True))
    
    def get_improvement_trend(self) -> List[float]:
        """Get improvement trend over time."""
        return [it["improvement"] for it in self._iterations]
    
    def get_learnings(self, issue_type: Optional[str] = None) -> Dict[str, List[str]]:
        """Get learned fixes."""
        if issue_type:
            return {issue_type: self._learnings.get(issue_type, [])}
        return self._learnings.copy()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics."""
        if not self._iterations:
            return {"total_iterations": 0}
        
        improvements = [it["improvement"] for it in self._iterations]
        
        return {
            "total_iterations": len(self._iterations),
            "avg_improvement": sum(improvements) / len(improvements),
            "total_improvement": sum(improvements),
            "common_issues": self.get_common_issues(),
            "num_learnings": sum(len(fixes) for fixes in self._learnings.values())
        }


class FeedbackLoop:
    """
    Self-improvement feedback loop.
    
    Implements critique → revise → retry cycles.
    
    Usage:
        loop = FeedbackLoop(agent)
        
        # Process with feedback
        result = await loop.process_with_feedback(input_data)
        # Automatically critiques and revises until satisfied
        
        # Manual critique
        critiques = await loop.critique(output)
        revised = await loop.revise(output, critiques)
        
        # Learn from feedback
        await loop.learn_from_critique(result, external_critique)
    """
    
    def __init__(
        self,
        agent: Any,
        config: Optional[FeedbackConfig] = None,
        tracker: Optional[ImprovementTracker] = None
    ):
        """
        Initialize feedback loop.
        
        Args:
            agent: Agent to improve
            config: Feedback configuration
            tracker: Improvement tracker (creates new if None)
        """
        self.agent = agent
        self.config = config or FeedbackConfig()
        self.tracker = tracker or ImprovementTracker()
    
    async def process_with_feedback(self, input_data: Any) -> Any:
        """
        Process input with automatic feedback loop.
        
        Iteratively critiques and revises until satisfied or max retries.
        
        Args:
            input_data: Input to process
            
        Returns:
            Final revised output
        """
        output = await self.agent.process(input_data)
        
        for iteration in range(self.config.max_retries):
            # Generate critiques
            critiques = await self.critique(output, input_data)
            
            # Filter by severity
            significant_critiques = self._filter_critiques(critiques)
            
            if not significant_critiques:
                # No significant issues, we're done
                break
            
            # Revise based on critiques
            revision = await self.revise(output, significant_critiques, input_data)
            
            # Check improvement
            if revision.improvement_score < self.config.min_improvement:
                # Not improving enough, stop
                break
            
            # Track improvement
            self.tracker.record_iteration(
                output,
                revision.revised_output,
                significant_critiques,
                revision.improvement_score
            )
            
            # Use revised output for next iteration
            output = revision.revised_output
        
        return output
    
    async def critique(
        self,
        output: Any,
        input_context: Optional[Any] = None
    ) -> List[Critique]:
        """
        Generate critiques for output.
        
        Args:
            output: Output to critique
            input_context: Optional input context
            
        Returns:
            List of critiques
        """
        critiques = []
        
        # Apply various critique dimensions
        critiques.extend(await self._critique_accuracy(output, input_context))
        critiques.extend(await self._critique_completeness(output, input_context))
        critiques.extend(await self._critique_efficiency(output))
        critiques.extend(await self._critique_safety(output))
        critiques.extend(await self._critique_reasoning(output))
        
        return critiques
    
    async def revise(
        self,
        original_output: Any,
        critiques: List[Critique],
        input_context: Optional[Any] = None
    ) -> Revision:
        """
        Revise output based on critiques.
        
        Args:
            original_output: Original output
            critiques: List of critiques
            input_context: Optional input context
            
        Returns:
            Revision with improved output
        """
        # Build revision prompt
        revision_instructions = self._build_revision_instructions(critiques)
        
        # Apply revisions
        revised_output = await self._apply_revisions(
            original_output,
            revision_instructions,
            input_context
        )
        
        # Measure improvement
        improvement = self._measure_improvement(original_output, revised_output, critiques)
        
        return Revision(
            original_output=original_output,
            revised_output=revised_output,
            critiques_addressed=critiques,
            improvement_score=improvement
        )
    
    async def learn_from_critique(
        self,
        output: Any,
        external_critique: Union[str, List[Critique]]
    ):
        """
        Learn from external critique.
        
        Args:
            output: Output that received critique
            external_critique: External critique (text or structured)
        """
        # Parse critique if text
        if isinstance(external_critique, str):
            critiques = self._parse_text_critique(external_critique)
        else:
            critiques = external_critique
        
        # Store learnings
        for critique in critiques:
            if critique.suggested_fix:
                issue_type = critique.critique_type.value
                if issue_type not in self.tracker._learnings:
                    self.tracker._learnings[issue_type] = []
                self.tracker._learnings[issue_type].append(critique.suggested_fix)
    
    async def _critique_accuracy(
        self,
        output: Any,
        input_context: Optional[Any]
    ) -> List[Critique]:
        """Critique accuracy."""
        critiques = []
        
        # Check if output is dict/object with expected fields
        if isinstance(output, dict):
            # Check for None values (might indicate errors)
            for key, value in output.items():
                if value is None:
                    critiques.append(Critique(
                        critique_type=CritiqueType.ACCURACY,
                        severity="medium",
                        message=f"Field '{key}' is None",
                        specific_issue=f"Missing value for {key}",
                        suggested_fix=f"Provide valid value for {key}"
                    ))
        
        return critiques
    
    async def _critique_completeness(
        self,
        output: Any,
        input_context: Optional[Any]
    ) -> List[Critique]:
        """Critique completeness."""
        critiques = []
        
        # Check if output addresses input
        if input_context and isinstance(input_context, dict):
            if "required_fields" in input_context:
                required = input_context["required_fields"]
                if isinstance(output, dict):
                    for field in required:
                        if field not in output:
                            critiques.append(Critique(
                                critique_type=CritiqueType.COMPLETENESS,
                                severity="high",
                                message=f"Missing required field: {field}",
                                specific_issue=f"Output lacks {field}",
                                suggested_fix=f"Add {field} to output"
                            ))
        
        return critiques
    
    async def _critique_efficiency(self, output: Any) -> List[Critique]:
        """Critique efficiency."""
        critiques = []
        
        # Check output size
        if isinstance(output, (dict, list)):
            size = len(str(output))
            if size > 10000:  # Arbitrary threshold
                critiques.append(Critique(
                    critique_type=CritiqueType.EFFICIENCY,
                    severity="low",
                    message="Output is very large",
                    specific_issue=f"Output size: {size} chars",
                    suggested_fix="Consider summarizing or paginating"
                ))
        
        return critiques
    
    async def _critique_safety(self, output: Any) -> List[Critique]:
        """Critique safety."""
        critiques = []
        
        # Check for sensitive patterns
        if isinstance(output, (str, dict)):
            output_str = str(output)
            
            # Check for potential PII
            if any(pattern in output_str.lower() for pattern in 
                   ["ssn", "social security", "password", "api_key", "secret"]):
                critiques.append(Critique(
                    critique_type=CritiqueType.SAFETY,
                    severity="critical",
                    message="Potential sensitive data in output",
                    specific_issue="Output may contain PII or secrets",
                    suggested_fix="Redact sensitive information"
                ))
        
        return critiques
    
    async def _critique_reasoning(self, output: Any) -> List[Critique]:
        """Critique reasoning quality."""
        critiques = []
        
        # Check if reasoning is included
        if isinstance(output, dict):
            if "reasoning" in output:
                reasoning = output["reasoning"]
                if len(str(reasoning)) < 20:
                    critiques.append(Critique(
                        critique_type=CritiqueType.REASONING,
                        severity="low",
                        message="Reasoning is very brief",
                        specific_issue="Limited explanation provided",
                        suggested_fix="Provide more detailed reasoning"
                    ))
        
        return critiques
    
    def _filter_critiques(self, critiques: List[Critique]) -> List[Critique]:
        """Filter critiques by severity threshold."""
        severity_order = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        threshold = severity_order.get(self.config.critique_severity_threshold, 2)
        
        return [
            c for c in critiques
            if severity_order.get(c.severity, 0) >= threshold
        ]
    
    def _build_revision_instructions(self, critiques: List[Critique]) -> str:
        """Build revision instructions from critiques."""
        instructions = ["Please revise the output to address the following issues:\n"]
        
        for i, critique in enumerate(critiques, 1):
            instructions.append(f"{i}. {critique.message}")
            if critique.suggested_fix:
                instructions.append(f"   Suggestion: {critique.suggested_fix}")
        
        return "\n".join(instructions)
    
    async def _apply_revisions(
        self,
        original_output: Any,
        instructions: str,
        input_context: Optional[Any]
    ) -> Any:
        """Apply revisions to output."""
        # This would call the agent with revision instructions
        # For now, return a placeholder
        
        # In practice, you'd do:
        # revised = await self.agent.process_with_instructions(
        #     original_output,
        #     instructions,
        #     input_context
        # )
        
        # Simple placeholder: copy output and mark as revised
        if isinstance(original_output, dict):
            revised = original_output.copy()
            revised["_revised"] = True
            return revised
        
        return original_output
    
    def _measure_improvement(
        self,
        original: Any,
        revised: Any,
        critiques: List[Critique]
    ) -> float:
        """Measure improvement from revision."""
        # Simple heuristic: assume each critique addressed = improvement
        # In practice, would re-run critique and compare
        
        # Check if revised addresses issues
        improvements = 0
        for critique in critiques:
            if self._is_addressed(critique, revised):
                improvements += 1
        
        return improvements / len(critiques) if critiques else 0.0
    
    def _is_addressed(self, critique: Critique, revised_output: Any) -> bool:
        """Check if critique is addressed in revised output."""
        # Simplified check
        if isinstance(revised_output, dict):
            if critique.critique_type == CritiqueType.COMPLETENESS:
                # Check if missing fields are now present
                return "_revised" in revised_output
        
        return True  # Optimistic default
    
    def _parse_text_critique(self, text: str) -> List[Critique]:
        """Parse text critique into structured critiques."""
        # Simple parsing
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        
        critiques = []
        for line in lines:
            critiques.append(Critique(
                critique_type=CritiqueType.ACCURACY,
                severity="medium",
                message=line,
                specific_issue=line
            ))
        
        return critiques
    
    def get_improvement_stats(self) -> Dict[str, Any]:
        """Get improvement statistics."""
        return self.tracker.get_stats()
    
    def export_learnings(self) -> Dict[str, Any]:
        """Export learned improvements."""
        return {
            "learnings": self.tracker.get_learnings(),
            "stats": self.tracker.get_stats(),
            "common_issues": self.tracker.get_common_issues()
        }

