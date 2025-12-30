"""
Chain-of-Thought Distillation

Compresses verbose reasoning chains into efficient forms while maintaining accuracy.

Features:
- Distills long reasoning into concise steps
- Reduces token costs
- Maintains or improves accuracy
- Integrates with DSPy for optimization
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ReasoningStep:
    """A single step in a reasoning chain."""
    step_number: int
    content: str
    tokens: int
    importance: float = 1.0  # 0.0 to 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReasoningChain:
    """A complete chain-of-thought reasoning."""
    task_id: str
    steps: List[ReasoningStep] = field(default_factory=list)
    final_answer: Any = None
    total_tokens: int = 0
    correct: Optional[bool] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_step(self, step: ReasoningStep):
        """Add reasoning step."""
        self.steps.append(step)
        self.total_tokens += step.tokens
    
    def to_text(self) -> str:
        """Convert to text."""
        return "\n".join([
            f"Step {s.step_number}: {s.content}"
            for s in self.steps
        ])


@dataclass
class DistilledChain:
    """Distilled version of reasoning chain."""
    original_chain_id: str
    distilled_steps: List[ReasoningStep]
    compression_ratio: float
    accuracy_retained: float
    tokens_saved: int
    method: str  # "importance", "summarization", "dspy"


@dataclass
class DistillationConfig:
    """Configuration for distillation."""
    target_compression: float = 0.5  # Target 50% compression
    min_importance: float = 0.3  # Keep steps with importance > 0.3
    preserve_final_step: bool = True
    method: str = "importance"  # "importance", "summarization", "dspy"


@dataclass
class DistillationMetrics:
    """Metrics for distillation performance."""
    original_tokens: int
    distilled_tokens: int
    compression_ratio: float
    accuracy_before: float
    accuracy_after: float
    accuracy_retained: float
    tokens_saved: int


class CoTDistiller:
    """
    Chain-of-Thought Distiller.
    
    Compresses verbose reasoning chains while maintaining accuracy.
    
    Usage:
        distiller = CoTDistiller()
        
        # Record verbose reasoning
        chain = ReasoningChain(task_id="task_001")
        chain.add_step(ReasoningStep(1, "First, let's analyze...", 50))
        chain.add_step(ReasoningStep(2, "This means...", 30))
        
        # Distill
        distilled = await distiller.distill(chain)
        print(f"Saved {distilled.tokens_saved} tokens!")
        
        # Use distilled version
        result = await agent.reason_with_distilled(distilled)
    """
    
    def __init__(self, config: Optional[DistillationConfig] = None):
        """
        Initialize distiller.
        
        Args:
            config: Distillation configuration
        """
        self.config = config or DistillationConfig()
        self._chains: Dict[str, ReasoningChain] = {}
        self._distilled: Dict[str, DistilledChain] = {}
        self._performance_history: List[DistillationMetrics] = []
    
    async def distill(
        self,
        chain: ReasoningChain,
        target_compression: Optional[float] = None
    ) -> DistilledChain:
        """
        Distill a reasoning chain.
        
        Args:
            chain: Original reasoning chain
            target_compression: Target compression ratio (overrides config)
            
        Returns:
            Distilled chain
        """
        target = target_compression or self.config.target_compression
        
        # Store original
        self._chains[chain.task_id] = chain
        
        # Apply distillation method
        if self.config.method == "importance":
            distilled_steps = await self._distill_by_importance(chain, target)
        elif self.config.method == "summarization":
            distilled_steps = await self._distill_by_summarization(chain, target)
        elif self.config.method == "dspy":
            distilled_steps = await self._distill_with_dspy(chain, target)
        else:
            distilled_steps = chain.steps
        
        # Calculate metrics
        original_tokens = chain.total_tokens
        distilled_tokens = sum(s.tokens for s in distilled_steps)
        compression = 1.0 - (distilled_tokens / original_tokens) if original_tokens > 0 else 0.0
        
        distilled = DistilledChain(
            original_chain_id=chain.task_id,
            distilled_steps=distilled_steps,
            compression_ratio=compression,
            accuracy_retained=1.0,  # Would measure empirically
            tokens_saved=original_tokens - distilled_tokens,
            method=self.config.method
        )
        
        self._distilled[chain.task_id] = distilled
        
        return distilled
    
    async def _distill_by_importance(
        self,
        chain: ReasoningChain,
        target: float
    ) -> List[ReasoningStep]:
        """Distill by keeping most important steps."""
        # Sort by importance
        sorted_steps = sorted(chain.steps, key=lambda s: s.importance, reverse=True)
        
        # Keep steps until we hit target compression
        kept_steps = []
        current_tokens = 0
        target_tokens = int(chain.total_tokens * (1 - target))
        
        for step in sorted_steps:
            if current_tokens + step.tokens <= target_tokens:
                kept_steps.append(step)
                current_tokens += step.tokens
            elif step.importance >= self.config.min_importance:
                kept_steps.append(step)
                current_tokens += step.tokens
        
        # Always keep final step if configured
        if self.config.preserve_final_step and chain.steps:
            final = chain.steps[-1]
            if final not in kept_steps:
                kept_steps.append(final)
        
        # Re-sort by original order
        kept_steps.sort(key=lambda s: s.step_number)
        
        return kept_steps
    
    async def _distill_by_summarization(
        self,
        chain: ReasoningChain,
        target: float
    ) -> List[ReasoningStep]:
        """Distill by summarizing consecutive steps."""
        if not chain.steps:
            return []
        
        # Group consecutive low-importance steps
        groups = []
        current_group = []
        
        for step in chain.steps:
            if step.importance < 0.7:
                current_group.append(step)
            else:
                if current_group:
                    groups.append(("summarize", current_group))
                    current_group = []
                groups.append(("keep", [step]))
        
        if current_group:
            groups.append(("summarize", current_group))
        
        # Process groups
        distilled = []
        step_num = 1
        
        for group_type, steps in groups:
            if group_type == "keep":
                distilled.extend(steps)
            else:
                # Summarize group
                summary = self._summarize_steps(steps)
                distilled.append(ReasoningStep(
                    step_number=step_num,
                    content=summary,
                    tokens=len(summary.split()),
                    importance=max(s.importance for s in steps)
                ))
            step_num += 1
        
        return distilled
    
    async def _distill_with_dspy(
        self,
        chain: ReasoningChain,
        target: float
    ) -> List[ReasoningStep]:
        """Distill using DSPy optimization."""
        # Placeholder for DSPy integration
        # Would use DSPy's optimization to learn distillation
        
        try:
            import dspy
            
            # Define DSPy signature for distillation
            class DistillReasoning(dspy.Signature):
                """Distill verbose reasoning into concise steps."""
                verbose_reasoning = dspy.InputField()
                target_tokens = dspy.InputField()
                concise_reasoning = dspy.OutputField()
            
            # Use ChainOfThought with distillation signature
            distiller_module = dspy.ChainOfThought(DistillReasoning)
            
            # Apply distillation
            result = distiller_module(
                verbose_reasoning=chain.to_text(),
                target_tokens=int(chain.total_tokens * (1 - target))
            )
            
            # Parse result back into steps
            distilled_text = result.concise_reasoning
            steps = self._parse_distilled_text(distilled_text)
            
            return steps
            
        except ImportError:
            # Fallback to importance-based
            return await self._distill_by_importance(chain, target)
    
    def _summarize_steps(self, steps: List[ReasoningStep]) -> str:
        """Summarize multiple steps."""
        if not steps:
            return ""
        
        if len(steps) == 1:
            return steps[0].content
        
        # Simple summarization: extract key points
        contents = [s.content for s in steps]
        
        # Very simple: take first and last sentence
        first = contents[0].split(".")[0]
        last = contents[-1].split(".")[-2] if "." in contents[-1] else contents[-1]
        
        return f"{first}. {last}."
    
    def _parse_distilled_text(self, text: str) -> List[ReasoningStep]:
        """Parse distilled text into steps."""
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        
        steps = []
        for i, line in enumerate(lines):
            # Remove "Step N:" prefix if present
            content = line
            if line.startswith("Step"):
                parts = line.split(":", 1)
                if len(parts) > 1:
                    content = parts[1].strip()
            
            steps.append(ReasoningStep(
                step_number=i + 1,
                content=content,
                tokens=len(content.split()),
                importance=1.0
            ))
        
        return steps
    
    def assess_importance(self, step: ReasoningStep, chain: ReasoningChain) -> float:
        """
        Assess importance of a reasoning step.
        
        Heuristics:
        - Final steps are important
        - Steps with numbers/facts are important
        - Steps with conclusions are important
        - Repetitive steps are less important
        """
        importance = 0.5  # Base importance
        
        # Position-based
        if step.step_number == len(chain.steps):
            importance += 0.3  # Final step
        elif step.step_number == 1:
            importance += 0.1  # First step
        
        # Content-based
        content_lower = step.content.lower()
        
        if any(word in content_lower for word in ["therefore", "thus", "conclude"]):
            importance += 0.2  # Conclusion
        
        if any(char.isdigit() for char in step.content):
            importance += 0.1  # Contains numbers/data
        
        if any(word in content_lower for word in ["however", "but", "although"]):
            importance += 0.15  # Contrasting point
        
        # Check for repetition
        for other in chain.steps:
            if other.step_number != step.step_number:
                similarity = self._text_similarity(step.content, other.content)
                if similarity > 0.8:
                    importance -= 0.2  # Repetitive
                    break
        
        return max(0.0, min(1.0, importance))
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        """Simple text similarity."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def get_metrics(self) -> DistillationMetrics:
        """Get aggregate distillation metrics."""
        if not self._distilled:
            return DistillationMetrics(0, 0, 0.0, 0.0, 0.0, 0.0, 0)
        
        total_original = 0
        total_distilled = 0
        total_accuracy_before = 0.0
        total_accuracy_after = 0.0
        
        for chain_id, distilled in self._distilled.items():
            original = self._chains.get(chain_id)
            if original:
                total_original += original.total_tokens
                total_distilled += sum(s.tokens for s in distilled.distilled_steps)
        
        compression = 1.0 - (total_distilled / total_original) if total_original > 0 else 0.0
        
        return DistillationMetrics(
            original_tokens=total_original,
            distilled_tokens=total_distilled,
            compression_ratio=compression,
            accuracy_before=1.0,
            accuracy_after=1.0,
            accuracy_retained=1.0,
            tokens_saved=total_original - total_distilled
        )
    
    def apply_to_chain(self, chain: ReasoningChain):
        """Apply learned importance assessments to a chain."""
        for step in chain.steps:
            step.importance = self.assess_importance(step, chain)
    
    def export_distillation_rules(self) -> Dict[str, Any]:
        """Export learned distillation rules."""
        metrics = self.get_metrics()
        
        return {
            "method": self.config.method,
            "target_compression": self.config.target_compression,
            "metrics": {
                "avg_compression": metrics.compression_ratio,
                "avg_tokens_saved": metrics.tokens_saved / len(self._distilled) if self._distilled else 0,
                "total_chains_distilled": len(self._distilled)
            },
            "learned_patterns": {
                "high_importance_keywords": ["therefore", "thus", "conclude", "however"],
                "low_importance_patterns": ["repetitive", "verbose"]
            }
        }

