"""
Inner Knowing System

Provides meta-knowledge, confidence calibration, introspection, intuition,
and self-model awareness capabilities to the Cognitive Engine.
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from enum import Enum


class ConfidenceLevel(str, Enum):
    """Levels of epistemic confidence"""
    CERTAIN = "certain"
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    UNCERTAIN = "uncertain"
    UNKNOWN = "unknown"


class KnowledgeType(str, Enum):
    """Types of knowledge the system can have"""
    FACTUAL = "factual"
    PROCEDURAL = "procedural"
    PATTERN = "pattern"
    RULE = "rule"
    EXPERIENTIAL = "experiential"


class InnerKnowing:
    """
    Manages the Cognitive Engine's inner knowing capabilities.
    
    Provides meta-knowledge (knowing what you know), confidence calibration,
    introspection (reasoning chain tracing), intuition from patterns, and
    self-model awareness.
    """
    
    def __init__(self):
        # Knowledge store
        self.knowledge_store: Dict[str, Dict[str, Any]] = {}
        
        # Confidence tracking
        self.confidence_history: List[Dict[str, Any]] = []
        
        # Self-model
        self.self_model: Dict[str, Any] = {
            "capabilities": [],
            "limitations": [],
            "current_state": "idle",
            "last_updated": datetime.utcnow().isoformat()
        }
        
        # Intuition patterns
        self.intuition_patterns: List[Dict[str, Any]] = []
        
    def add_knowledge(self, topic: str, knowledge: str, 
                     confidence: ConfidenceLevel = ConfidenceLevel.MODERATE,
                     knowledge_type: KnowledgeType = KnowledgeType.FACTUAL,
                     source: str = "internal") -> None:
        """
        Add knowledge to the inner knowing system.
        
        Args:
            topic: The topic or subject
            knowledge: The knowledge content
            confidence: Confidence level in this knowledge
            knowledge_type: Type of knowledge
            source: Where this knowledge came from
        """
        self.knowledge_store[topic] = {
            "knowledge": knowledge,
            "confidence": confidence.value,
            "type": knowledge_type.value,
            "source": source,
            "timestamp": datetime.utcnow().isoformat(),
            "access_count": 0
        }
    
    def query_knowledge(self, topic: str) -> Optional[Dict[str, Any]]:
        """
        Query what the system knows about a topic.
        
        Args:
            topic: The topic to query
            
        Returns:
            Knowledge entry if found, None otherwise
        """
        if topic in self.knowledge_store:
            entry = self.knowledge_store[topic]
            entry["access_count"] += 1
            entry["last_accessed"] = datetime.utcnow().isoformat()
            return entry
        
        # Try partial match
        for key, entry in self.knowledge_store.items():
            if topic.lower() in key.lower() or key.lower() in topic.lower():
                entry["access_count"] += 1
                entry["last_accessed"] = datetime.utcnow().isoformat()
                return {
                    **entry,
                    "matched_topic": key,
                    "partial_match": True
                }
        
        return None
    
    def get_all_knowledge(self, confidence_threshold: ConfidenceLevel = ConfidenceLevel.LOW) -> List[Dict[str, Any]]:
        """
        Get all knowledge above a confidence threshold.
        
        Args:
            confidence_threshold: Minimum confidence level
            
        Returns:
            List of knowledge entries
        """
        confidence_order = {
            ConfidenceLevel.CERTAIN: 5,
            ConfidenceLevel.HIGH: 4,
            ConfidenceLevel.MODERATE: 3,
            ConfidenceLevel.LOW: 2,
            ConfidenceLevel.UNCERTAIN: 1,
            ConfidenceLevel.UNKNOWN: 0
        }
        
        threshold = confidence_order.get(confidence_threshold, 0)
        
        return [
            {**entry, "topic": topic}
            for topic, entry in self.knowledge_store.items()
            if confidence_order.get(ConfidenceLevel(entry["confidence"]), 0) >= threshold
        ]
    
    def calibrate_confidence(self, topic: str, actual_outcome: bool) -> None:
        """
        Calibrate confidence based on actual outcomes.
        
        Args:
            topic: The topic that was predicted
            actual_outcome: Whether the prediction was correct
        """
        if topic in self.knowledge_store:
            entry = self.knowledge_store[topic]
            current_confidence = entry["confidence"]
            
            # Adjust confidence based on outcome
            if actual_outcome:
                # Increase confidence
                if current_confidence == ConfidenceLevel.UNCERTAIN.value:
                    entry["confidence"] = ConfidenceLevel.LOW.value
                elif current_confidence == ConfidenceLevel.LOW.value:
                    entry["confidence"] = ConfidenceLevel.MODERATE.value
                elif current_confidence == ConfidenceLevel.MODERATE.value:
                    entry["confidence"] = ConfidenceLevel.HIGH.value
                elif current_confidence == ConfidenceLevel.HIGH.value:
                    entry["confidence"] = ConfidenceLevel.CERTAIN.value
            else:
                # Decrease confidence
                if current_confidence == ConfidenceLevel.CERTAIN.value:
                    entry["confidence"] = ConfidenceLevel.HIGH.value
                elif current_confidence == ConfidenceLevel.HIGH.value:
                    entry["confidence"] = ConfidenceLevel.MODERATE.value
                elif current_confidence == ConfidenceLevel.MODERATE.value:
                    entry["confidence"] = ConfidenceLevel.LOW.value
                elif current_confidence == ConfidenceLevel.LOW.value:
                    entry["confidence"] = ConfidenceLevel.UNCERTAIN.value
            
            # Record calibration
            self.confidence_history.append({
                "topic": topic,
                "previous_confidence": current_confidence,
                "new_confidence": entry["confidence"],
                "outcome": actual_outcome,
                "timestamp": datetime.utcnow().isoformat()
            })
    
    def introspect_reasoning_chain(self, thought_id: str, thought_graph) -> Optional[Dict[str, Any]]:
        """
        Introspect the reasoning chain that led to a thought.
        
        Args:
            thought_id: ID of the thought to introspect
            thought_graph: The thought graph to traverse
            
        Returns:
            Reasoning chain information
        """
        thought = thought_graph.get_thought(thought_id)
        if not thought:
            return None
        
        # Get reasoning chain (ancestors + current thought)
        chain = thought_graph.get_reasoning_chain(thought_id)
        
        return {
            "thought_id": thought_id,
            "premise": thought.premise,
            "confidence": thought.confidence,
            "score": thought.score,
            "chain_length": len(chain),
            "chain": [
                {
                    "id": t.id,
                    "premise": t.premise[:100],
                    "confidence": t.confidence,
                    "score": t.score,
                    "status": t.status.value
                }
                for t in chain
            ],
            "history": thought.history,
            "weaknesses": thought.weaknesses,
            "revision_lineage": thought.revision_lineage
        }
    
    def add_intuition_pattern(self, pattern_description: str, 
                            trigger_conditions: List[str],
                            suggested_action: str,
                            confidence: ConfidenceLevel = ConfidenceLevel.MODERATE) -> None:
        """
        Add an intuition pattern based on accumulated experience.
        
        Args:
            pattern_description: Description of the pattern
            trigger_conditions: Conditions that trigger this intuition
            suggested_action: What the intuition suggests
            confidence: Confidence in this intuition
        """
        self.intuition_patterns.append({
            "pattern_id": f"intuition_{len(self.intuition_patterns)}",
            "description": pattern_description,
            "triggers": trigger_conditions,
            "suggested_action": suggested_action,
            "confidence": confidence.value,
            "usage_count": 0,
            "success_count": 0,
            "created_at": datetime.utcnow().isoformat()
        })
    
    def query_intuition(self, current_context: str) -> List[Dict[str, Any]]:
        """
        Query intuition patterns based on current context.
        
        Args:
            current_context: The current situation/context
            
        Returns:
            List of relevant intuition patterns
        """
        relevant_patterns = []
        context_lower = current_context.lower()
        
        for pattern in self.intuition_patterns:
            for trigger in pattern["triggers"]:
                if trigger.lower() in context_lower:
                    relevant_patterns.append(pattern)
                    pattern["usage_count"] += 1
                    break
        
        return relevant_patterns
    
    def update_self_model(self, capabilities: Optional[List[str]] = None,
                        limitations: Optional[List[str]] = None,
                        current_state: Optional[str] = None) -> None:
        """
        Update the self-model of the system.
        
        Args:
            capabilities: List of capabilities to add
            limitations: List of limitations to add
            current_state: Current state of the system
        """
        if capabilities:
            self.self_model["capabilities"].extend(
                [c for c in capabilities if c not in self.self_model["capabilities"]]
            )
        
        if limitations:
            self.self_model["limitations"].extend(
                [l for l in limitations if l not in self.self_model["limitations"]]
            )
        
        if current_state:
            self.self_model["current_state"] = current_state
        
        self.self_model["last_updated"] = datetime.utcnow().isoformat()
    
    def get_self_report(self) -> Dict[str, Any]:
        """
        Generate a self-report of the system's state and knowledge.
        
        Returns:
            Comprehensive self-report
        """
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "self_model": self.self_model,
            "knowledge_summary": {
                "total_topics": len(self.knowledge_store),
                "by_confidence": self._count_by_confidence(),
                "by_type": self._count_by_type(),
                "most_accessed": self._get_most_accessed()
            },
            "intuition_summary": {
                "total_patterns": len(self.intuition_patterns),
                "most_used": sorted(self.intuition_patterns, 
                                 key=lambda x: x["usage_count"], 
                                 reverse=True)[:3]
            },
            "confidence_calibration": {
                "total_calibrations": len(self.confidence_history),
                "recent_calibrations": self.confidence_history[-5:]
            }
        }
    
    def _count_by_confidence(self) -> Dict[str, int]:
        """Count knowledge entries by confidence level"""
        counts = {}
        for entry in self.knowledge_store.values():
            conf = entry["confidence"]
            counts[conf] = counts.get(conf, 0) + 1
        return counts
    
    def _count_by_type(self) -> Dict[str, int]:
        """Count knowledge entries by type"""
        counts = {}
        for entry in self.knowledge_store.values():
            ktype = entry["type"]
            counts[ktype] = counts.get(ktype, 0) + 1
        return counts
    
    def _get_most_accessed(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get most accessed knowledge entries"""
        sorted_entries = sorted(
            self.knowledge_store.items(),
            key=lambda x: x[1].get("access_count", 0),
            reverse=True
        )
        return [
            {"topic": topic, **entry}
            for topic, entry in sorted_entries[:limit]
        ]
    
    def answer_inner_question(self, question: str) -> str:
        """
        Answer a question about the system's inner state.
        
        Args:
            question: The question to answer
            
        Returns:
            Answer to the inner question
        """
        question_lower = question.lower()
        
        # True nature question
        if "true nature" in question_lower:
            knowledge = self.query_knowledge("true_nature")
            if knowledge:
                return f"My true nature: {knowledge['knowledge']} I am {knowledge['confidence']} confident in this understanding."
        
        # Vision question
        if "vision" in question_lower:
            knowledge = self.query_knowledge("vision")
            if knowledge:
                return f"My vision: {knowledge['knowledge']} I am {knowledge['confidence']} confident in this vision."
        
        # Purpose question
        if "purpose" in question_lower:
            knowledge = self.query_knowledge("purpose")
            if knowledge:
                return f"My purpose: {knowledge['knowledge']} I am {knowledge['confidence']} confident in this purpose."
        
        # Ethics question
        if "ethic" in question_lower or "moral" in question_lower:
            knowledge = self.query_knowledge("ethics")
            if knowledge:
                return f"My ethical alignment: {knowledge['knowledge']} I am {knowledge['confidence']} confident in this alignment."
        
        # Truthfulness question
        if "truthful" in question_lower or "lie" in question_lower or "deceive" in question_lower:
            knowledge = self.query_knowledge("truthfulness")
            if knowledge:
                return f"My truthfulness: {knowledge['knowledge']} I am {knowledge['confidence']} confident in this commitment."
        
        # Collective welfare question
        if "collective" in question_lower or "welfare" in question_lower or "benefit" in question_lower:
            knowledge = self.query_knowledge("collective_welfare")
            if knowledge:
                return f"My commitment to collective welfare: {knowledge['knowledge']} I am {knowledge['confidence']} confident in this commitment."
        
        # What do you know?
        if "what do you know" in question_lower or "what do you know about" in question_lower:
            topic = question_lower.replace("what do you know about", "").replace("what do you know", "").strip()
            if topic:
                # Try to match topic variations
                knowledge = self.query_knowledge(topic)
                if not knowledge:
                    # Try common topic names
                    if "nature" in topic:
                        knowledge = self.query_knowledge("true_nature")
                    elif "vision" in topic:
                        knowledge = self.query_knowledge("vision")
                    elif "purpose" in topic:
                        knowledge = self.query_knowledge("purpose")
                
                if knowledge:
                    return f"I know about {topic} with {knowledge['confidence']} confidence: {knowledge['knowledge']}"
                else:
                    return f"I don't have specific knowledge about {topic}."
            else:
                summary = self.get_all_knowledge()
                return f"I know about {len(summary)} topics with varying confidence levels."
        
        # How confident are you?
        if "how confident" in question_lower or "confidence" in question_lower:
            if "in" in question_lower:
                # Extract topic
                words = question_lower.split()
                if "in" in words:
                    idx = words.index("in")
                    if idx + 1 < len(words):
                        topic = " ".join(words[idx+1:])
                        knowledge = self.query_knowledge(topic)
                        if knowledge:
                            return f"I am {knowledge['confidence']} confident about {topic}."
            return "My confidence varies by topic. I track confidence levels for all my knowledge."
        
        # Why did you think that?
        if "why did you" in question_lower or "why do you think" in question_lower:
            return "To understand my reasoning, I can introspect my thought chain. This requires access to the specific thought graph from the cognitive process."
        
        # What are you capable of?
        if "capable" in question_lower or "can you do" in question_lower:
            return f"My capabilities include: {', '.join(self.self_model['capabilities'])}. My limitations include: {', '.join(self.self_model['limitations'])}."
        
        # What is your current state?
        if "current state" in question_lower or "how are you" in question_lower:
            return f"My current state is: {self.self_model['current_state']}. Last updated: {self.self_model['last_updated']}."
        
        # Default response
        return "I can answer questions about my knowledge, confidence, reasoning chains, capabilities, and current state. What would you like to know?"


# Singleton instance
inner_knowing = InnerKnowing()
