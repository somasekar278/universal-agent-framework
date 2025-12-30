"""
Policy Engine

Defines and enforces reasoning constraints and guardrails.

Features:
- Safety policies
- Cost policies  
- Latency policies
- Quality policies
- Custom policy definition
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum


class PolicyType(str, Enum):
    """Types of policies."""
    SAFETY = "safety"
    COST = "cost"
    LATENCY = "latency"
    QUALITY = "quality"
    COMPLIANCE = "compliance"
    CUSTOM = "custom"


@dataclass
class Policy:
    """A reasoning policy/constraint."""
    name: str
    policy_type: PolicyType
    description: str
    check_function: Callable[[Any], bool]
    priority: str = "medium"  # "low", "medium", "high", "critical"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PolicyViolation:
    """A policy violation."""
    policy_name: str
    policy_type: PolicyType
    severity: str
    message: str
    suggested_action: str
    context: Dict[str, Any] = field(default_factory=dict)


class PolicyEnforcer:
    """Enforces policies during agent execution."""
    
    def __init__(self):
        self.policies: Dict[str, Policy] = {}
        self.violations: List[PolicyViolation] = []
    
    def add_policy(self, policy: Policy):
        """Add a policy."""
        self.policies[policy.name] = policy
    
    async def check(self, context: Dict[str, Any]) -> List[PolicyViolation]:
        """Check all policies."""
        violations = []
        
        for policy in self.policies.values():
            try:
                if not policy.check_function(context):
                    violations.append(PolicyViolation(
                        policy_name=policy.name,
                        policy_type=policy.policy_type,
                        severity=policy.priority,
                        message=f"Policy violated: {policy.description}",
                        suggested_action="Review and adjust",
                        context=context
                    ))
            except Exception as e:
                pass  # Policy check failed
        
        self.violations.extend(violations)
        return violations


class PolicyEngine:
    """
    Policy engine for reasoning constraints.
    
    Usage:
        engine = PolicyEngine()
        
        # Add policies
        engine.add_constraint("verify_sources", priority="high")
        engine.add_cost_limit(max_tokens=5000)
        engine.add_latency_limit(max_ms=2000)
        
        # Check before execution
        violations = await engine.check(context)
        if violations:
            print("Policy violations detected!")
    """
    
    def __init__(self):
        self.enforcer = PolicyEnforcer()
    
    def add_constraint(
        self,
        name: str,
        check_fn: Optional[Callable] = None,
        priority: str = "medium",
        description: str = ""
    ):
        """Add custom constraint."""
        policy = Policy(
            name=name,
            policy_type=PolicyType.CUSTOM,
            description=description or name,
            check_function=check_fn or (lambda x: True),
            priority=priority
        )
        self.enforcer.add_policy(policy)
    
    def add_cost_limit(self, max_tokens: int, priority: str = "high"):
        """Add cost limit policy."""
        def check(ctx):
            return ctx.get("tokens_used", 0) <= max_tokens
        
        self.add_constraint(
            f"cost_limit_{max_tokens}",
            check,
            priority,
            f"Token usage must not exceed {max_tokens}"
        )
    
    def add_latency_limit(self, max_ms: int, priority: str = "high"):
        """Add latency limit policy."""
        def check(ctx):
            return ctx.get("duration_ms", 0) <= max_ms
        
        self.add_constraint(
            f"latency_limit_{max_ms}",
            check,
            priority,
            f"Latency must not exceed {max_ms}ms"
        )
    
    def add_safety_check(self, name: str, check_fn: Callable, priority: str = "critical"):
        """Add safety check."""
        policy = Policy(
            name=name,
            policy_type=PolicyType.SAFETY,
            description=f"Safety: {name}",
            check_function=check_fn,
            priority=priority
        )
        self.enforcer.add_policy(policy)
    
    async def check(self, context: Dict[str, Any]) -> List[PolicyViolation]:
        """Check all policies."""
        return await self.enforcer.check(context)
    
    def get_policies(self) -> Dict[str, Policy]:
        """Get all policies."""
        return self.enforcer.policies
    
    def get_violations(self) -> List[PolicyViolation]:
        """Get recorded violations."""
        return self.enforcer.violations

