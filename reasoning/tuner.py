"""
RL-Style Agent Tuner

Tunes agent behavior using reward signals and reinforcement learning principles.

Features:
- Reward-based optimization
- Experience replay
- Policy gradient tuning
- Hyperparameter optimization
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import random


@dataclass
class RewardSignal:
    """A reward signal from task execution."""
    task_id: str
    agent_id: str
    reward: float  # -1.0 to 1.0
    metrics: Dict[str, float]
    config: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Experience:
    """An experience tuple for learning."""
    state: Dict[str, Any]
    action: Dict[str, Any]
    reward: float
    next_state: Dict[str, Any]
    done: bool


@dataclass
class TuningConfig:
    """Configuration for RL tuning."""
    learning_rate: float = 0.01
    discount_factor: float = 0.95
    exploration_rate: float = 0.1
    buffer_size: int = 1000
    batch_size: int = 32


class ExperienceBuffer:
    """Replay buffer for experiences."""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.buffer: List[Experience] = []
    
    def add(self, experience: Experience):
        """Add experience."""
        self.buffer.append(experience)
        if len(self.buffer) > self.max_size:
            self.buffer.pop(0)
    
    def sample(self, batch_size: int) -> List[Experience]:
        """Sample random batch."""
        return random.sample(self.buffer, min(batch_size, len(self.buffer)))
    
    def __len__(self):
        return len(self.buffer)


class AgentPolicy:
    """Agent policy (mapping from states to actions)."""
    
    def __init__(self):
        self.parameters: Dict[str, float] = {
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 1000,
            "reasoning_depth": 3
        }
    
    def get_action(self, state: Dict[str, Any], explore: bool = False) -> Dict[str, Any]:
        """Get action for state."""
        if explore and random.random() < 0.1:
            # Exploration: random perturbation
            return self._explore()
        return self.parameters.copy()
    
    def update(self, gradient: Dict[str, float], learning_rate: float):
        """Update policy parameters."""
        for key in self.parameters:
            if key in gradient:
                self.parameters[key] += learning_rate * gradient[key]
                # Clip to valid ranges
                self.parameters[key] = max(0.0, min(1.0, self.parameters[key]))
    
    def _explore(self) -> Dict[str, Any]:
        """Exploration action."""
        params = self.parameters.copy()
        for key in params:
            params[key] += random.uniform(-0.1, 0.1)
            params[key] = max(0.0, min(1.0, params[key]))
        return params


class RLTuner:
    """
    RL-style agent tuner.
    
    Optimizes agent behavior using reward signals.
    
    Usage:
        tuner = RLTuner(agent_id="fraud_detector")
        
        # Record reward
        reward = RewardSignal(
            task_id="task_001",
            agent_id="fraud_detector",
            reward=0.8,  # High reward
            metrics={"accuracy": 0.95, "latency": 230},
            config={"temperature": 0.7}
        )
        tuner.record_reward(reward)
        
        # Tune based on accumulated rewards
        optimized_config = await tuner.tune()
        
        # Use optimized config
        agent.update_config(optimized_config)
    """
    
    def __init__(
        self,
        agent_id: str,
        config: Optional[TuningConfig] = None
    ):
        """
        Initialize tuner.
        
        Args:
            agent_id: ID of agent to tune
            config: Tuning configuration
        """
        self.agent_id = agent_id
        self.config = config or TuningConfig()
        self.policy = AgentPolicy()
        self.buffer = ExperienceBuffer(self.config.buffer_size)
        self.rewards_history: List[RewardSignal] = []
    
    def record_reward(self, reward: RewardSignal):
        """Record reward signal."""
        self.rewards_history.append(reward)
        
        # Create experience
        experience = Experience(
            state={"task": reward.task_id},
            action=reward.config,
            reward=reward.reward,
            next_state={"task": reward.task_id, "done": True},
            done=True
        )
        self.buffer.add(experience)
    
    async def tune(self) -> Dict[str, Any]:
        """
        Tune agent based on accumulated rewards.
        
        Returns:
            Optimized configuration
        """
        if len(self.buffer) < self.config.batch_size:
            return self.policy.parameters
        
        # Sample experiences
        batch = self.buffer.sample(self.config.batch_size)
        
        # Compute policy gradient
        gradient = self._compute_gradient(batch)
        
        # Update policy
        self.policy.update(gradient, self.config.learning_rate)
        
        return self.policy.parameters
    
    def _compute_gradient(self, batch: List[Experience]) -> Dict[str, float]:
        """Compute policy gradient from batch."""
        gradient = {}
        
        # Simple gradient: direction of higher rewards
        high_reward = [e for e in batch if e.reward > 0.5]
        low_reward = [e for e in batch if e.reward < 0.5]
        
        if high_reward and low_reward:
            # Compute average configs for high vs low reward
            for key in self.policy.parameters:
                high_avg = sum(
                    e.action.get(key, 0.5) for e in high_reward
                ) / len(high_reward)
                
                low_avg = sum(
                    e.action.get(key, 0.5) for e in low_reward
                ) / len(low_reward)
                
                gradient[key] = high_avg - low_avg
        
        return gradient
    
    def get_best_config(self) -> Dict[str, Any]:
        """Get configuration with highest reward."""
        if not self.rewards_history:
            return self.policy.parameters
        
        best_reward = max(self.rewards_history, key=lambda r: r.reward)
        return best_reward.config
    
    def get_stats(self) -> Dict[str, Any]:
        """Get tuning statistics."""
        if not self.rewards_history:
            return {"total_episodes": 0}
        
        rewards = [r.reward for r in self.rewards_history]
        
        return {
            "total_episodes": len(self.rewards_history),
            "avg_reward": sum(rewards) / len(rewards),
            "best_reward": max(rewards),
            "current_policy": self.policy.parameters,
            "buffer_size": len(self.buffer)
        }

