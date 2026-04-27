"""
Internal Knowledge Base for the Cognitive Engine.

This implements a true cognitive knowledge system that:
- Stores concepts and their relationships
- Enables reasoning and inference
- Learns from experience
- Provides the foundation for internal cognition
"""

from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import json
import os


@dataclass
class Concept:
    """A concept in the knowledge base"""
    id: str
    name: str
    description: str = ""
    properties: Dict[str, str] = field(default_factory=dict)
    relationships: Dict[str, Set[str]] = field(default_factory=lambda: defaultdict(set))  # relationship_type -> set of concept_ids
    confidence: float = 1.0
    usage_count: int = 0
    last_accessed: Optional[str] = None
    
    def add_relationship(self, relationship_type: str, target_concept_id: str):
        """Add a relationship to another concept"""
        self.relationships[relationship_type].add(target_concept_id)
    
    def get_related_concepts(self, relationship_type: str) -> Set[str]:
        """Get all concepts related by a specific relationship type"""
        return self.relationships.get(relationship_type, set())
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "properties": self.properties,
            "relationships": {k: list(v) for k, v in self.relationships.items()},
            "confidence": self.confidence,
            "usage_count": self.usage_count,
            "last_accessed": self.last_accessed
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Concept':
        """Create from dictionary"""
        concept = cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            properties=data.get("properties", {}),
            confidence=data.get("confidence", 1.0),
            usage_count=data.get("usage_count", 0),
            last_accessed=data.get("last_accessed")
        )
        # Restore relationships
        for rel_type, targets in data.get("relationships", {}).items():
            for target_id in targets:
                concept.add_relationship(rel_type, target_id)
        return concept


class KnowledgeBase:
    """
    Internal knowledge base for the Cognitive Engine.
    
    This stores concepts and their relationships, enabling:
    - Concept retrieval and traversal
    - Reasoning and inference
    - Learning from interactions
    """
    
    def __init__(self, storage_path: str = "cognitive_knowledge.json"):
        self.storage_path = storage_path
        self.concepts: Dict[str, Concept] = {}
        self.concept_index: Dict[str, str] = {}  # name -> id mapping for quick lookup
        self._initialize_base_knowledge()
        self._load_from_disk()
    
    def _initialize_base_knowledge(self):
        """Initialize with base knowledge about the Cognitive Engine"""
        # Core concepts
        self.add_concept("cognitive_engine", "Cognitive Engine", 
                        "A system designed for explicit, inspectable thought formation")
        self.add_concept("cognition", "Cognition", 
                        "The process of acquiring knowledge and understanding through thought")
        self.add_concept("thought", "Thought", 
                        "A structured entity with state, history, and evaluative properties")
        self.add_concept("reasoning", "Reasoning", 
                        "The process of thinking about something in a logical way")
        self.add_concept("memory", "Memory", 
                        "The faculty by which the mind stores and remembers information")
        self.add_concept("learning", "Learning", 
                        "The acquisition of knowledge or skills through experience")
        self.add_concept("consciousness", "Consciousness", 
                        "The state of being aware of and responsive to one's surroundings")
        
        # Relationships
        self.add_relationship("cognitive_engine", "has_component", "cognition")
        self.add_relationship("cognitive_engine", "has_component", "reasoning")
        self.add_relationship("cognitive_engine", "has_component", "memory")
        self.add_relationship("cognitive_engine", "has_component", "learning")
        self.add_relationship("cognition", "requires", "thought")
        self.add_relationship("cognition", "involves", "reasoning")
        self.add_relationship("reasoning", "produces", "thought")
        self.add_relationship("learning", "requires", "memory")
        self.add_relationship("learning", "improves", "cognition")
        self.add_relationship("memory", "stores", "thought")
        self.add_relationship("consciousness", "emerges_from", "cognition")
    
    def add_concept(self, concept_id: str, name: str, description: str = "", 
                    properties: Dict[str, str] = None) -> Concept:
        """Add a new concept to the knowledge base"""
        if concept_id in self.concepts:
            return self.concepts[concept_id]
        
        concept = Concept(
            id=concept_id,
            name=name,
            description=description,
            properties=properties or {}
        )
        self.concepts[concept_id] = concept
        self.concept_index[name.lower()] = concept_id
        return concept
    
    def get_concept(self, concept_id: str) -> Optional[Concept]:
        """Get a concept by ID"""
        concept = self.concepts.get(concept_id)
        if concept:
            concept.usage_count += 1
        return concept
    
    def find_concept_by_name(self, name: str) -> Optional[Concept]:
        """Find a concept by name"""
        concept_id = self.concept_index.get(name.lower())
        if concept_id:
            return self.get_concept(concept_id)
        return None
    
    def add_relationship(self, source_id: str, relationship_type: str, target_id: str):
        """Add a relationship between two concepts"""
        if source_id not in self.concepts or target_id not in self.concepts:
            return
        
        self.concepts[source_id].add_relationship(relationship_type, target_id)
    
    def get_related(self, concept_id: str, relationship_type: str = None) -> List[Concept]:
        """Get concepts related to a given concept"""
        concept = self.concepts.get(concept_id)
        if not concept:
            return []
        
        if relationship_type:
            target_ids = concept.get_related_concepts(relationship_type)
        else:
            # Get all related concepts
            target_ids = set()
            for rel_type, targets in concept.relationships.items():
                target_ids.update(targets)
        
        return [self.concepts[tid] for tid in target_ids if tid in self.concepts]
    
    def find_path(self, start_id: str, end_id: str, max_depth: int = 5) -> List[str]:
        """Find a path between two concepts using BFS"""
        if start_id not in self.concepts or end_id not in self.concepts:
            return []
        
        if start_id == end_id:
            return [start_id]
        
        from collections import deque
        queue = deque([(start_id, [start_id])])
        visited = {start_id}
        
        while queue:
            current_id, path = queue.popleft()
            
            if len(path) > max_depth:
                continue
            
            # Get all related concepts
            current = self.concepts[current_id]
            for rel_type, targets in current.relationships.items():
                for target_id in targets:
                    if target_id == end_id:
                        return path + [target_id]
                    if target_id not in visited:
                        visited.add(target_id)
                        queue.append((target_id, path + [target_id]))
        
        return []
    
    def reason_about(self, query: str) -> str:
        """
        Reason about a query using the knowledge base.
        
        This implements basic reasoning by:
        1. Extracting concepts from the query
        2. Finding relationships between them
        3. Traversing the knowledge graph to derive insights
        """
        query_lower = query.lower()
        
        # Find concepts mentioned in the query
        mentioned_concepts = []
        for concept_id, concept in self.concepts.items():
            if concept.name.lower() in query_lower or concept_id.lower() in query_lower:
                mentioned_concepts.append(concept)
        
        if not mentioned_concepts:
            return self._generate_default_response(query)
        
        # If asking about a specific concept
        if len(mentioned_concepts) == 1:
            concept = mentioned_concepts[0]
            response = f"{concept.name}: {concept.description}"
            
            # Add related information
            related = self.get_related(concept.id)
            if related:
                related_names = [c.name for c in related[:3]]
                response += f"\nRelated to: {', '.join(related_names)}"
            
            return response
        
        # If multiple concepts, find relationships
        if len(mentioned_concepts) >= 2:
            c1, c2 = mentioned_concepts[0], mentioned_concepts[1]
            path = self.find_path(c1.id, c2.id)
            
            if path:
                path_names = [self.concepts[pid].name for pid in path]
                return f"Connection between {c1.name} and {c2.name}: {' → '.join(path_names)}"
            else:
                return f"{c1.name} and {c2.name} are both concepts in the knowledge base, but no direct relationship found."
        
        return self._generate_default_response(query)
    
    def _generate_default_response(self, query: str) -> str:
        """Generate a default response when no concepts are found"""
        return f"I understand you're asking about '{query}', but I don't have specific knowledge about that yet. I'm still learning."
    
    def learn_from_interaction(self, input_text: str, response_text: str, success: bool = True):
        """
        Learn from an interaction by extracting and storing new knowledge.
        
        This implements learning by:
        1. Extracting potential new concepts
        2. Identifying relationships
        3. Updating confidence scores
        """
        # Simple learning: extract key terms and create concepts
        words = input_text.lower().split()
        
        # Look for patterns like "X is Y" or "X means Y"
        if " is " in input_text.lower() or " means " in input_text.lower():
            parts = input_text.split(" is " if " is " in input_text else " means ")
            if len(parts) == 2:
                concept_name = parts[0].strip().lower()
                concept_desc = parts[1].strip()
                
                # Create or update concept
                concept_id = concept_name.replace(" ", "_")
                if concept_id not in self.concepts:
                    self.add_concept(concept_id, concept_name, concept_desc)
                    print(f"Learned new concept: {concept_name}")
                else:
                    self.concepts[concept_id].description = concept_desc
                    self.concepts[concept_id].confidence = min(1.0, self.concepts[concept_id].confidence + 0.1)
        
        self._save_to_disk()
    
    def _save_to_disk(self):
        """Save knowledge base to disk"""
        try:
            data = {
                "concepts": {cid: c.to_dict() for cid, c in self.concepts.items()},
                "concept_index": self.concept_index
            }
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving knowledge base: {e}")
    
    def _load_from_disk(self):
        """Load knowledge base from disk"""
        if not os.path.exists(self.storage_path):
            return
        
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
            
            for cid, cdata in data.get("concepts", {}).items():
                self.concepts[cid] = Concept.from_dict(cdata)
            
            self.concept_index = data.get("concept_index", {})
            print(f"Loaded knowledge base with {len(self.concepts)} concepts")
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
    
    def get_statistics(self) -> dict:
        """Get statistics about the knowledge base"""
        total_relationships = sum(len(c.relationships) for c in self.concepts.values())
        return {
            "total_concepts": len(self.concepts),
            "total_relationships": total_relationships,
            "most_used_concepts": sorted(
                [(c.name, c.usage_count) for c in self.concepts.values()],
                key=lambda x: x[1], reverse=True
            )[:5]
        }
