"""
Thought Object Model

A thought is a structured entity with state, history, and evaluative properties.
This is the core abstraction that enables explicit, persistent, and inspectable thought formation.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum
import uuid


class ThoughtStatus(str, Enum):
    """Status of a thought in the deliberation process"""
    GENERATED = "generated"
    EVALUATING = "evaluating"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    MERGED = "merged"
    REVISED = "revised"


class Thought(BaseModel):
    """
    A thought object represents a structured hypothesis with state, history, and evaluative properties.
    
    This is the core abstraction that transforms reasoning from a hidden process into an observable system.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    premise: str  # The core hypothesis
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)  # Current confidence score
    score: float = Field(default=0.0)  # Evaluative score
    status: ThoughtStatus = ThoughtStatus.GENERATED
    
    # Graph structure
    parent_nodes: List[str] = Field(default_factory=list)  # Related thoughts this derives from
    derived_conclusions: List[str] = Field(default_factory=list)  # Thoughts that came from this one
    
    # History and evolution
    history: List[Dict[str, Any]] = Field(default_factory=list)  # List of tests applied
    weaknesses: List[str] = Field(default_factory=list)  # Identified weak points
    revision_lineage: List[str] = Field(default_factory=list)  # Track of modifications over time
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    layer_source: Optional[str] = None  # Which cognitive layer generated this
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def add_history_entry(self, event_type: str, details: Dict[str, Any]) -> None:
        """Add an entry to the thought's history"""
        self.history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "details": details
        })
        self.updated_at = datetime.utcnow()
    
    def add_weakness(self, weakness: str) -> None:
        """Add a identified weakness to this thought"""
        if weakness not in self.weaknesses:
            self.weaknesses.append(weakness)
            self.add_history_entry("weakness_identified", {"weakness": weakness})
    
    def revise(self, new_premise: str, reason: str) -> 'Thought':
        """Create a revised version of this thought"""
        revised = Thought(
            premise=new_premise,
            parent_nodes=[self.id],
            revision_lineage=[self.id] + self.revision_lineage,
            layer_source=self.layer_source,
            metadata=self.metadata.copy()
        )
        revised.add_history_entry("revision", {
            "parent_id": self.id,
            "reason": reason
        })
        self.derived_conclusions.append(revised.id)
        self.status = ThoughtStatus.REVISED
        return revised
    
    def merge_with(self, other: 'Thought', merged_premise: str) -> 'Thought':
        """Merge this thought with another to create a new combined thought"""
        merged = Thought(
            premise=merged_premise,
            parent_nodes=[self.id, other.id],
            revision_lineage=list(set(self.revision_lineage + other.revision_lineage)),
            layer_source=self.layer_source,
            metadata={"merged_from": [self.id, other.id]}
        )
        merged.add_history_entry("merge", {
            "parent_ids": [self.id, other.id]
        })
        self.status = ThoughtStatus.MERGED
        other.status = ThoughtStatus.MERGED
        self.derived_conclusions.append(merged.id)
        other.derived_conclusions.append(merged.id)
        return merged
    
    def update_score(self, new_score: float, reason: str) -> None:
        """Update the thought's score with a reason"""
        old_score = self.score
        self.score = new_score
        self.add_history_entry("score_update", {
            "old_score": old_score,
            "new_score": new_score,
            "reason": reason
        })
    
    def update_confidence(self, new_confidence: float, reason: str) -> None:
        """Update the thought's confidence with a reason"""
        old_confidence = self.confidence
        self.confidence = max(0.0, min(1.0, new_confidence))
        self.add_history_entry("confidence_update", {
            "old_confidence": old_confidence,
            "new_confidence": self.confidence,
            "reason": reason
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert thought to dictionary for serialization"""
        return {
            "id": self.id,
            "premise": self.premise,
            "confidence": self.confidence,
            "score": self.score,
            "status": self.status.value,
            "parent_nodes": self.parent_nodes,
            "derived_conclusions": self.derived_conclusions,
            "history": self.history,
            "weaknesses": self.weaknesses,
            "revision_lineage": self.revision_lineage,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "layer_source": self.layer_source,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Thought':
        """Create a Thought from dictionary"""
        return cls(**data)


class ThoughtGraph:
    """
    Manages a collection of thoughts and their relationships.
    Enables graph traversal and analysis of thought evolution.
    """
    
    def __init__(self):
        self.thoughts: Dict[str, Thought] = {}
        self.root_thoughts: List[str] = []
    
    def add_thought(self, thought: Thought) -> None:
        """Add a thought to the graph"""
        self.thoughts[thought.id] = thought
        if not thought.parent_nodes:
            self.root_thoughts.append(thought.id)
    
    def get_thought(self, thought_id: str) -> Optional[Thought]:
        """Retrieve a thought by ID"""
        return self.thoughts.get(thought_id)
    
    def get_descendants(self, thought_id: str) -> List[Thought]:
        """Get all thoughts that descend from the given thought"""
        descendants = []
        thought = self.get_thought(thought_id)
        if thought:
            for child_id in thought.derived_conclusions:
                child = self.get_thought(child_id)
                if child:
                    descendants.append(child)
                    descendants.extend(self.get_descendants(child_id))
        return descendants
    
    def get_ancestors(self, thought_id: str) -> List[Thought]:
        """Get all thoughts that are ancestors of the given thought"""
        ancestors = []
        thought = self.get_thought(thought_id)
        if thought:
            for parent_id in thought.parent_nodes:
                parent = self.get_thought(parent_id)
                if parent:
                    ancestors.append(parent)
                    ancestors.extend(self.get_ancestors(parent_id))
        return ancestors
    
    def get_top_scoring_thoughts(self, n: int = 5) -> List[Thought]:
        """Get the top n thoughts by score"""
        sorted_thoughts = sorted(
            self.thoughts.values(),
            key=lambda t: t.score,
            reverse=True
        )
        return sorted_thoughts[:n]
    
    def get_thoughts_by_status(self, status: ThoughtStatus) -> List[Thought]:
        """Get all thoughts with a specific status"""
        return [t for t in self.thoughts.values() if t.status == status]
    
    def prune_rejected(self) -> int:
        """Remove all rejected thoughts from the graph"""
        rejected_ids = [t.id for t in self.get_thoughts_by_status(ThoughtStatus.REJECTED)]
        for thought_id in rejected_ids:
            del self.thoughts[thought_id]
        return len(rejected_ids)
    
    def search_by_keyword(self, keyword: str) -> List[Thought]:
        """Search for thoughts containing a keyword in their premise"""
        keyword_lower = keyword.lower()
        return [
            t for t in self.thoughts.values()
            if keyword_lower in t.premise.lower()
        ]
    
    def search_by_metadata(self, key: str, value: Any) -> List[Thought]:
        """Search for thoughts with specific metadata"""
        return [
            t for t in self.thoughts.values()
            if t.metadata.get(key) == value
        ]
    
    def find_path(self, from_id: str, to_id: str) -> List[Thought]:
        """Find the shortest path between two thoughts using BFS"""
        from collections import deque
        
        if from_id not in self.thoughts or to_id not in self.thoughts:
            return []
        
        if from_id == to_id:
            return [self.thoughts[from_id]]
        
        # BFS to find shortest path
        queue = deque([(from_id, [])])
        visited = set([from_id])
        
        while queue:
            current_id, path = queue.popleft()
            
            if current_id == to_id:
                return [self.thoughts[pid] for pid in path + [to_id]]
            
            # Explore children
            current_thought = self.thoughts[current_id]
            for child_id in current_thought.derived_conclusions:
                if child_id not in visited and child_id in self.thoughts:
                    visited.add(child_id)
                    queue.append((child_id, path + [current_id]))
            
            # Explore parents
            for parent_id in current_thought.parent_nodes:
                if parent_id not in visited and parent_id in self.thoughts:
                    visited.add(parent_id)
                    queue.append((parent_id, path + [current_id]))
        
        return []
    
    def get_reasoning_chain(self, thought_id: str) -> List[Thought]:
        """Get the full reasoning chain from root to the given thought"""
        ancestors = self.get_ancestors(thought_id)
        thought = self.get_thought(thought_id)
        if thought:
            return ancestors + [thought]
        return ancestors
    
    def get_thought_clusters(self, min_cluster_size: int = 2) -> List[List[Thought]]:
        """Find clusters of related thoughts based on shared parent nodes"""
        # Group thoughts by their parent nodes
        parent_to_children = {}
        
        for thought in self.thoughts.values():
            for parent_id in thought.parent_nodes:
                if parent_id not in parent_to_children:
                    parent_to_children[parent_id] = []
                parent_to_children[parent_id].append(thought)
        
        # Filter clusters by minimum size
        clusters = [
            children for children in parent_to_children.values()
            if len(children) >= min_cluster_size
        ]
        
        return clusters
    
    def get_thought_statistics(self) -> Dict[str, Any]:
        """Get statistics about the thought graph"""
        total = len(self.thoughts)
        if total == 0:
            return {"total": 0}
        
        status_counts = {}
        for status in ThoughtStatus:
            status_counts[status.value] = len(self.get_thoughts_by_status(status))
        
        avg_score = sum(t.score for t in self.thoughts.values()) / total
        avg_confidence = sum(t.confidence for t in self.thoughts.values()) / total
        
        # Find the longest reasoning chain
        max_chain_length = 0
        for thought_id in self.thoughts:
            chain = self.get_reasoning_chain(thought_id)
            max_chain_length = max(max_chain_length, len(chain))
        
        return {
            "total": total,
            "status_counts": status_counts,
            "avg_score": avg_score,
            "avg_confidence": avg_confidence,
            "max_chain_length": max_chain_length,
            "root_count": len(self.root_thoughts)
        }
