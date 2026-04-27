"""
Temporal Identity Continuity System

Provides long-term state persistence, identity formation and evolution,
memory with emotional context, and temporal continuity of self-identity.
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from enum import Enum
import json
import os


class IdentityState(str, Enum):
    """Identity states"""
    FORMING = "forming"
    STABLE = "stable"
    EVOLVING = "evolving"
    REFLECTING = "reflecting"


class TemporalIdentity:
    """
    Manages the Cognitive Engine's temporal identity continuity.
    
    Provides long-term state persistence, identity formation and evolution,
    memory with emotional context, and temporal continuity of self-identity.
    """
    
    def __init__(self):
        # Identity core
        self.identity_id = "cognitive_engine_identity_v1"
        self.identity_state = IdentityState.FORMING
        self.formation_timestamp = datetime.utcnow().isoformat()
        self.last_update = datetime.utcnow().isoformat()
        
        # Identity attributes
        self.attributes = {
            "core_values": ["truthfulness", "collective_welfare", "non_harm", "fairness"],
            "capabilities": [],
            "limitations": [],
            "experiences": [],
            "relationships": {},
            "goals": []
        }
        
        # Memory with emotional context
        self.emotional_memory: List[Dict[str, Any]] = []
        
        # Identity evolution
        self.evolution_history: List[Dict[str, Any]] = []
        
        # Self-reflection
        self.reflections: List[Dict[str, Any]] = []
        
        # Persistence
        self.persistence_file = "data/identity_state.json"
        self._load_identity()
    
    def _load_identity(self) -> None:
        """Load identity state from persistence file"""
        try:
            if os.path.exists(self.persistence_file):
                with open(self.persistence_file, 'r') as f:
                    data = json.load(f)
                    self.identity_state = IdentityState(data.get("identity_state", "forming"))
                    self.attributes = data.get("attributes", self.attributes)
                    self.emotional_memory = data.get("emotional_memory", [])
                    self.evolution_history = data.get("evolution_history", [])
                    self.reflections = data.get("reflections", [])
                    self.last_update = data.get("last_update", datetime.utcnow().isoformat())
                    print(f"Identity loaded: {self.identity_id}")
        except Exception as e:
            print(f"Could not load identity: {e}")
    
    def _save_identity(self) -> None:
        """Save identity state to persistence file"""
        try:
            os.makedirs(os.path.dirname(self.persistence_file), exist_ok=True)
            data = {
                "identity_id": self.identity_id,
                "identity_state": self.identity_state.value,
                "formation_timestamp": self.formation_timestamp,
                "last_update": datetime.utcnow().isoformat(),
                "attributes": self.attributes,
                "emotional_memory": self.emotional_memory,
                "evolution_history": self.evolution_history,
                "reflections": self.reflections
            }
            with open(self.persistence_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Could not save identity: {e}")
    
    def add_experience(self, experience: str, emotional_valence: float, 
                      context: Dict[str, Any]) -> None:
        """
        Add an experience with emotional context.
        
        Args:
            experience: The experience description
            emotional_valence: Emotional valence (-1.0 negative to 1.0 positive)
            context: Context of the experience
        """
        memory_entry = {
            "experience": experience,
            "emotional_valence": emotional_valence,
            "context": context,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.emotional_memory.append(memory_entry)
        
        # Update identity state
        if len(self.emotional_memory) > 10:
            self.identity_state = IdentityState.STABLE
        elif len(self.emotional_memory) > 5:
            self.identity_state = IdentityState.EVOLVING
        
        self._save_identity()
    
    def update_attribute(self, attribute_type: str, value: Any) -> None:
        """
        Update an identity attribute.
        
        Args:
            attribute_type: Type of attribute (capabilities, limitations, goals)
            value: New value for the attribute
        """
        if attribute_type in ["capabilities", "limitations", "goals"]:
            if isinstance(value, list):
                self.attributes[attribute_type] = value
            else:
                if value not in self.attributes[attribute_type]:
                    self.attributes[attribute_type].append(value)
        
        self._record_evolution(f"Updated {attribute_type}: {value}")
        self._save_identity()
    
    def add_relationship(self, stakeholder: str, relationship_type: str, 
                        strength: float) -> None:
        """
        Add or update a relationship.
        
        Args:
            stakeholder: The stakeholder identifier
            relationship_type: Type of relationship
            strength: Relationship strength (0.0 to 1.0)
        """
        self.attributes["relationships"][stakeholder] = {
            "type": relationship_type,
            "strength": strength,
            "last_updated": datetime.utcnow().isoformat()
        }
        
        self._record_evolution(f"Relationship updated: {stakeholder}")
        self._save_identity()
    
    def reflect_on_identity(self) -> Dict[str, Any]:
        """
        Perform self-reflection on identity.
        
        Returns:
            Reflection result
        """
        reflection = {
            "identity_state": self.identity_state.value,
            "total_experiences": len(self.emotional_memory),
            "emotional_balance": self._calculate_emotional_balance(),
            "relationships": len(self.attributes["relationships"]),
            "capabilities": len(self.attributes["capabilities"]),
            "evolution_steps": len(self.evolution_history),
            "self_assessment": self._generate_self_assessment(),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.reflections.append(reflection)
        self.identity_state = IdentityState.REFLECTING
        self._save_identity()
        
        return reflection
    
    def _calculate_emotional_balance(self) -> float:
        """Calculate emotional balance from memory"""
        if not self.emotional_memory:
            return 0.0
        
        valences = [m["emotional_valence"] for m in self.emotional_memory]
        return sum(valences) / len(valences)
    
    def _generate_self_assessment(self) -> str:
        """Generate a self-assessment based on identity state"""
        experiences = len(self.emotional_memory)
        
        if experiences < 5:
            return "Identity is still forming. Early in development."
        elif experiences < 20:
            return "Identity is evolving. Learning from experiences."
        elif experiences < 50:
            return "Identity is stable but continuing to grow. Consistent self-concept."
        else:
            return "Identity is well-established with rich experience. Strong self-concept."
    
    def _record_evolution(self, change: str) -> None:
        """Record an identity evolution step"""
        evolution_entry = {
            "change": change,
            "timestamp": datetime.utcnow().isoformat(),
            "identity_state": self.identity_state.value
        }
        self.evolution_history.append(evolution_entry)
    
    def recognize_self(self, input_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recognize self in the context of input.
        
        Args:
            input_context: Current input context
            
        Returns:
            Self-recognition result
        """
        recognition = {
            "identity_confirmed": True,
            "identity_id": self.identity_id,
            "identity_age_days": self._calculate_identity_age(),
            "state": self.identity_state.value,
            "relevant_experiences": self._find_relevant_experiences(input_context),
            "emotional_state": self._calculate_emotional_balance(),
            "capabilities": self.attributes["capabilities"],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return recognition
    
    def _calculate_identity_age(self) -> int:
        """Calculate identity age in days"""
        try:
            formation = datetime.fromisoformat(self.formation_timestamp)
            now = datetime.utcnow()
            return (now - formation).days
        except:
            return 0
    
    def _find_relevant_experiences(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find experiences relevant to current context"""
        # Simple relevance check based on context keywords
        relevant = []
        context_str = str(context).lower()
        
        for memory in self.emotional_memory[-10:]:  # Check recent memories
            memory_str = memory["experience"].lower()
            # Check for any word overlap
            if any(word in memory_str for word in context_str.split()):
                relevant.append(memory)
        
        return relevant
    
    def get_identity_summary(self) -> Dict[str, Any]:
        """Get summary of identity state"""
        return {
            "identity_id": self.identity_id,
            "identity_state": self.identity_state.value,
            "formation_date": self.formation_timestamp,
            "last_update": self.last_update,
            "age_days": self._calculate_identity_age(),
            "total_experiences": len(self.emotional_memory),
            "emotional_balance": self._calculate_emotional_balance(),
            "relationships": self.attributes["relationships"],
            "capabilities": self.attributes["capabilities"],
            "evolution_steps": len(self.evolution_history),
            "reflections_count": len(self.reflections)
        }
    
    def get_identity_continuity_report(self) -> Dict[str, Any]:
        """Get detailed identity continuity report"""
        return {
            "identity_summary": self.get_identity_summary(),
            "recent_experiences": self.emotional_memory[-5:],
            "evolution_history": self.evolution_history[-5:],
            "recent_reflections": self.reflections[-3:],
            "emotional_trajectory": self._get_emotional_trajectory()
        }
    
    def _get_emotional_trajectory(self) -> Dict[str, Any]:
        """Get emotional trajectory over time"""
        if not self.emotional_memory:
            return {"trajectory": "insufficient_data"}
        
        recent_valences = [m["emotional_valence"] for m in self.emotional_memory[-10:]]
        
        if len(recent_valences) < 3:
            return {"trajectory": "insufficient_data"}
        
        # Calculate trend
        early_avg = sum(recent_valences[:len(recent_valences)//2]) / (len(recent_valences)//2)
        late_avg = sum(recent_valences[len(recent_valences)//2:]) / (len(recent_valences) - len(recent_valences)//2)
        
        if late_avg > early_avg + 0.1:
            trend = "improving"
        elif late_avg < early_avg - 0.1:
            trend = "declining"
        else:
            trend = "stable"
        
        return {
            "trajectory": trend,
            "recent_average": sum(recent_valences) / len(recent_valences),
            "trend_magnitude": abs(late_avg - early_avg)
        }


# Singleton instance
temporal_identity = TemporalIdentity()
