"""
Goal definitions for the Cognitive Agent

Defines goal structures and goal management.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
import uuid


class GoalStatus(str, Enum):
    """Status of a goal"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ABANDONED = "abandoned"


class GoalPriority(str, Enum):
    """Priority levels for goals"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Goal:
    """
    Represents a goal for the autonomous agent.
    """
    
    def __init__(
        self,
        description: str,
        priority: GoalPriority = GoalPriority.MEDIUM,
        deadline: Optional[datetime] = None,
        metadata: Dict[str, Any] = None
    ):
        self.id = str(uuid.uuid4())
        self.description = description
        self.priority = priority
        self.status = GoalStatus.PENDING
        self.deadline = deadline
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.progress = 0.0  # 0.0 to 1.0
        self.metadata = metadata or {}
        self.subgoals: List[str] = []  # IDs of subgoals
        self.parent_goal: Optional[str] = None  # ID of parent goal
    
    def update_progress(self, progress: float) -> None:
        """Update goal progress"""
        self.progress = max(0.0, min(1.0, progress))
        self.updated_at = datetime.utcnow()
        
        if self.progress >= 1.0:
            self.status = GoalStatus.COMPLETED
    
    def set_status(self, status: GoalStatus) -> None:
        """Set goal status"""
        self.status = status
        self.updated_at = datetime.utcnow()
    
    def add_subgoal(self, goal_id: str) -> None:
        """Add a subgoal"""
        if goal_id not in self.subgoals:
            self.subgoals.append(goal_id)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "description": self.description,
            "priority": self.priority.value,
            "status": self.status.value,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "progress": self.progress,
            "metadata": self.metadata,
            "subgoals": self.subgoals,
            "parent_goal": self.parent_goal
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Goal':
        """Create from dictionary"""
        goal = cls(
            description=data["description"],
            priority=GoalPriority(data.get("priority", "medium")),
            metadata=data.get("metadata", {})
        )
        goal.id = data["id"]
        goal.status = GoalStatus(data.get("status", "pending"))
        goal.progress = data.get("progress", 0.0)
        if data.get("deadline"):
            goal.deadline = datetime.fromisoformat(data["deadline"])
        goal.subgoals = data.get("subgoals", [])
        goal.parent_goal = data.get("parent_goal")
        return goal


class GoalManager:
    """
    Manages goals for the autonomous agent.
    """
    
    def __init__(self):
        self.goals: Dict[str, Goal] = {}
    
    def add_goal(self, goal: Goal) -> str:
        """Add a goal"""
        self.goals[goal.id] = goal
        return goal.id
    
    def get_goal(self, goal_id: str) -> Optional[Goal]:
        """Get a goal by ID"""
        return self.goals.get(goal_id)
    
    def get_active_goals(self) -> List[Goal]:
        """Get all active (pending or in_progress) goals"""
        return [
            g for g in self.goals.values()
            if g.status in [GoalStatus.PENDING, GoalStatus.IN_PROGRESS]
        ]
    
    def get_goals_by_priority(self, priority: GoalPriority) -> List[Goal]:
        """Get goals by priority"""
        return [g for g in self.goals.values() if g.priority == priority]
    
    def get_highest_priority_goal(self) -> Optional[Goal]:
        """Get the highest priority active goal"""
        active_goals = self.get_active_goals()
        if not active_goals:
            return None
        
        priority_order = [GoalPriority.CRITICAL, GoalPriority.HIGH, GoalPriority.MEDIUM, GoalPriority.LOW]
        for priority in priority_order:
            goals = [g for g in active_goals if g.priority == priority]
            if goals:
                # Return the one with earliest deadline or created date
                return min(goals, key=lambda g: g.deadline or g.created_at)
        
        return active_goals[0]
    
    def update_goal(self, goal_id: str, **kwargs) -> bool:
        """Update a goal"""
        goal = self.get_goal(goal_id)
        if not goal:
            return False
        
        if "progress" in kwargs:
            goal.update_progress(kwargs["progress"])
        if "status" in kwargs:
            goal.set_status(GoalStatus(kwargs["status"]))
        
        return True
    
    def complete_goal(self, goal_id: str) -> bool:
        """Mark a goal as completed"""
        return self.update_goal(goal_id, progress=1.0, status="completed")
    
    def fail_goal(self, goal_id: str) -> bool:
        """Mark a goal as failed"""
        goal = self.get_goal(goal_id)
        if goal:
            goal.set_status(GoalStatus.FAILED)
            return True
        return False
    
    def abandon_goal(self, goal_id: str) -> bool:
        """Mark a goal as abandoned"""
        goal = self.get_goal(goal_id)
        if goal:
            goal.set_status(GoalStatus.ABANDONED)
            return True
        return False
    
    def get_goal_statistics(self) -> Dict[str, Any]:
        """Get statistics about goals"""
        total = len(self.goals)
        completed = len([g for g in self.goals.values() if g.status == GoalStatus.COMPLETED])
        failed = len([g for g in self.goals.values() if g.status == GoalStatus.FAILED])
        active = len(self.get_active_goals())
        
        return {
            "total": total,
            "completed": completed,
            "failed": failed,
            "active": active,
            "completion_rate": completed / total if total > 0 else 0.0
        }
