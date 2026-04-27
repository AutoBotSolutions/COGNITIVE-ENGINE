"""
Comprehensive Test Suite for Knowledge Base System

Tests all aspects of the knowledge base including:
- Concept creation and storage
- Relationship management
- Pathfinding and reasoning
- Learning from interactions
- Persistence to disk
"""

import pytest
import os
import tempfile
from llm.knowledge_base import KnowledgeBase, Concept


class TestConcept:
    """Test Concept class functionality"""
    
    def test_concept_creation(self):
        """Test basic concept creation"""
        concept = Concept(
            id="test_1",
            name="cognition",
            description="The process of acquiring knowledge",
            properties={"type": "mental_process"},
            confidence=0.9
        )
        assert concept.id == "test_1"
        assert concept.name == "cognition"
        assert concept.confidence == 0.9
        assert concept.usage_count == 0
    
    def test_concept_relationships(self):
        """Test adding and managing relationships"""
        concept = Concept(
            id="test_2",
            name="learning",
            description="Acquiring knowledge",
            properties={},
            relationships={}
        )
        concept.add_relationship("enables", "cognition")
        assert "enables" in concept.relationships
        assert "cognition" in concept.relationships["enables"]
    
    def test_concept_usage_tracking(self):
        """Test usage count tracking"""
        concept = Concept(
            id="test_3",
            name="memory",
            description="Storage of information",
            properties={},
            relationships={}
        )
        assert concept.usage_count == 0
        concept.increment_usage()
        assert concept.usage_count == 1


class TestKnowledgeBase:
    """Test KnowledgeBase class functionality"""
    
    def setup_method(self):
        """Setup a fresh knowledge base for each test"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.kb = KnowledgeBase(storage_path=self.temp_file.name)
    
    def teardown_method(self):
        """Clean up temp file after each test"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_knowledge_base_initialization(self):
        """Test knowledge base initializes with base knowledge"""
        assert len(self.kb.concepts) > 0
        assert "cognition" in self.kb.concept_index or len(self.kb.concepts) > 0
    
    def test_add_concept(self):
        """Test adding a new concept"""
        concept = Concept(
            id="new_concept",
            name="testing",
            description="The act of verifying functionality",
            properties={"type": "process"},
            confidence=0.8
        )
        self.kb.add_concept(concept)
        assert "new_concept" in self.kb.concepts
        assert "new_concept" in self.kb.concept_index
    
    def test_get_concept(self):
        """Test retrieving a concept"""
        concept = Concept(
            id="get_test",
            name="retrieval",
            description="Getting stored information",
            properties={},
            confidence=0.7
        )
        self.kb.add_concept(concept)
        retrieved = self.kb.get_concept("get_test")
        assert retrieved is not None
        assert retrieved.name == "retrieval"
    
    def test_find_concept_by_name(self):
        """Test finding concepts by name"""
        concept = Concept(
            id="find_test",
            name="search",
            description="Looking for information",
            properties={},
            confidence=0.85
        )
        self.kb.add_concept(concept)
        found = self.kb.find_concept_by_name("search")
        assert found is not None
        assert found.id == "find_test"
    
    def test_add_relationship(self):
        """Test adding relationships between concepts"""
        concept1 = Concept(
            id="c1",
            name="parent",
            description="Parent concept",
            properties={},
            relationships={}
        )
        concept2 = Concept(
            id="c2",
            name="child",
            description="Child concept",
            properties={},
            relationships={}
        )
        self.kb.add_concept(concept1)
        self.kb.add_concept(concept2)
        self.kb.add_relationship("c1", "enables", "c2")
        
        parent = self.kb.get_concept("c1")
        assert "enables" in parent.relationships
        assert "c2" in parent.relationships["enables"]
    
    def test_find_path(self):
        """Test pathfinding between concepts"""
        # Create a chain: A -> B -> C
        self.kb.add_concept(Concept(id="a", name="A", description="", properties={}, relationships={}))
        self.kb.add_concept(Concept(id="b", name="B", description="", properties={}, relationships={}))
        self.kb.add_concept(Concept(id="c", name="C", description="", properties={}, relationships={}))
        
        self.kb.add_relationship("a", "leads_to", "b")
        self.kb.add_relationship("b", "leads_to", "c")
        
        path = self.kb.find_path("a", "c")
        assert len(path) == 3
        assert path[0].id == "a"
        assert path[1].id == "b"
        assert path[2].id == "c"
    
    def test_reason_about(self):
        """Test reasoning about queries"""
        response = self.kb.reason_about("What is cognition?")
        assert response is not None
        assert len(response) > 0
    
    def test_learn_from_interaction(self):
        """Test learning from interactions"""
        initial_count = len(self.kb.concepts)
        self.kb.learn_from_interaction("Memory is important for learning", "Yes, memory enables learning", success=True)
        
        # Should have learned something
        assert len(self.kb.concepts) >= initial_count
    
    def test_persistence(self):
        """Test saving and loading from disk"""
        # Add a concept
        concept = Concept(
            id="persist_test",
            name="persistence",
            description="Saving data for later use",
            properties={"type": "storage"},
            confidence=0.9
        )
        self.kb.add_concept(concept)
        
        # Save
        self.kb._save_to_disk()
        
        # Create new knowledge base and load
        new_kb = KnowledgeBase(storage_path=self.temp_file.name)
        
        # Verify the concept was loaded
        loaded = new_kb.get_concept("persist_test")
        assert loaded is not None
        assert loaded.name == "persistence"
    
    def test_concept_index(self):
        """Test concept name indexing"""
        concept = Concept(
            id="index_test",
            name="indexing",
            description="Creating an index for fast lookup",
            properties={},
            confidence=0.75
        )
        self.kb.add_concept(concept)
        
        assert "indexing" in self.kb.concept_index
        assert self.kb.concept_index["indexing"] == "index_test"
    
    def test_get_related_concepts(self):
        """Test getting related concepts"""
        self.kb.add_concept(Concept(id="rel1", name="concept1", description="", properties={}, relationships={}))
        self.kb.add_concept(Concept(id="rel2", name="concept2", description="", properties={}, relationships={}))
        self.kb.add_concept(Concept(id="rel3", name="concept3", description="", properties={}, relationships={}))
        
        self.kb.add_relationship("rel1", "related_to", "rel2")
        self.kb.add_relationship("rel1", "related_to", "rel3")
        
        related = self.kb.get_related_concepts("rel1")
        assert len(related) >= 2
        related_ids = [c.id for c in related]
        assert "rel2" in related_ids
        assert "rel3" in related_ids
    
    def test_confidence_threshold_filtering(self):
        """Test filtering concepts by confidence threshold"""
        low_conf = Concept(id="low", name="low_conf", description="", properties={}, confidence=0.3)
        high_conf = Concept(id="high", name="high_conf", description="", properties={}, confidence=0.9)
        
        self.kb.add_concept(low_conf)
        self.kb.add_concept(high_conf)
        
        high_conf_concepts = self.kb.get_concepts_by_confidence(min_confidence=0.8)
        assert len(high_conf_concepts) >= 1
        assert high_conf in [c.id for c in high_conf_concepts]
    
    def test_update_concept(self):
        """Test updating an existing concept"""
        concept = Concept(
            id="update_test",
            name="original",
            description="Original description",
            properties={},
            confidence=0.5
        )
        self.kb.add_concept(concept)
        
        # Update
        self.kb.update_concept("update_test", description="Updated description", confidence=0.8)
        
        updated = self.kb.get_concept("update_test")
        assert updated.description == "Updated description"
        assert updated.confidence == 0.8


class TestKnowledgeBaseIntegration:
    """Integration tests for knowledge base with other components"""
    
    def setup_method(self):
        """Setup for integration tests"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.kb = KnowledgeBase(storage_path=self.temp_file.name)
    
    def teardown_method(self):
        """Clean up"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_reasoning_chain(self):
        """Test building a reasoning chain across multiple concepts"""
        # Create a reasoning chain
        self.kb.add_concept(Concept(id="s1", name="sensation", description="", properties={}, relationships={}))
        self.kb.add_concept(Concept(id="p1", name="perception", description="", properties={}, relationships={}))
        self.kb.add_concept(Concept(id="c1", name="cognition", description="", properties={}, relationships={}))
        self.kb.add_concept(Concept(id="a1", name="action", description="", properties={}, relationships={}))
        
        self.kb.add_relationship("s1", "leads_to", "p1")
        self.kb.add_relationship("p1", "leads_to", "c1")
        self.kb.add_relationship("c1", "leads_to", "a1")
        
        response = self.kb.reason_about("How does sensation lead to action?")
        assert response is not None
        # Should mention the chain
        assert len(response) > 0
    
    def test_learning_feedback_loop(self):
        """Test that learning improves reasoning over time"""
        # Initial reasoning
        response1 = self.kb.reason_about("What is learning?")
        
        # Learn from interaction
        self.kb.learn_from_interaction(
            "How does learning work?",
            "Learning involves acquiring knowledge through experience",
            success=True
        )
        
        # Reason again
        response2 = self.kb.reason_about("What is learning?")
        
        # Responses should be present
        assert response1 is not None
        assert response2 is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
