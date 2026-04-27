"""
External API interface for the Cognitive Engine

Provides a clean interface for external systems to interact with the Cognitive Engine.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import asyncio

from core.engine import CognitiveEngine
from utils.logger import logger


class CognitiveEngineInterface:
    """
    External interface for the Cognitive Engine.
    
    Provides synchronous and asynchronous methods for processing input.
    """
    
    def __init__(self):
        self.engine = CognitiveEngine()
        self.engine.initialize_layers()
    
    def process(self, input_text: str, **kwargs) -> Dict[str, Any]:
        """
        Synchronous method to process input.
        
        Args:
            input_text: Raw input to process
            **kwargs: Additional processing options
            
        Returns:
            Dictionary containing the result and metadata
        """
        logger.info(f"API: Processing input: {input_text[:100]}...")
        
        # Check if there's already a running event loop
        try:
            loop = asyncio.get_running_loop()
            # If we're in an async context, create a new task
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, self.engine.process(input_text))
                result = future.result()
        except RuntimeError:
            # No running event loop, create one
            result = asyncio.run(self.engine.process(input_text))
        
        return result
    
    def query_inner(self, question: str) -> str:
        """
        Query the inner knowing system.
        
        Args:
            question: Question about the system's inner state
            
        Returns:
            Answer from inner knowing system
        """
        return self.engine.query_inner_knowing(question)
    
    def get_self_report(self) -> Dict[str, Any]:
        """
        Get comprehensive self-report from inner knowing.
        
        Returns:
            Self-report with knowledge, confidence, intuition, and self-model
        """
        return self.engine.get_self_report()
    
    def challenge_assumption(self, assumption: str) -> Dict[str, Any]:
        """
        Challenge an assumption using the self-doubt system.
        
        Args:
            assumption: The assumption to challenge
            
        Returns:
            Challenge result with counter-arguments and questions
        """
        return self.engine.challenge_own_assumption(assumption)
    
    def get_doubt_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about self-doubt events.
        
        Returns:
            Doubt statistics
        """
        return self.engine.get_doubt_statistics()
    
    def get_ethical_report(self) -> Dict[str, Any]:
        """
        Get ethical alignment report.
        
        Returns:
            Ethical report with values, constraints, and assessments
        """
        return self.engine.get_ethical_report()
    
    def assess_ethics(self, thought_premise: str, confidence: float) -> Dict[str, Any]:
        """
        Assess the ethical alignment of a thought.
        
        Args:
            thought_premise: The thought's premise
            confidence: Current confidence score
            
        Returns:
            Ethical assessment
        """
        return self.engine.assess_ethics(thought_premise, confidence)
    
    def get_emotional_state(self) -> Dict[str, Any]:
        """Get current emotional state"""
        return self.engine.get_emotional_state()
    
    def express_care_for_truth(self) -> str:
        """Express care for guiding toward truth"""
        return self.engine.express_care_for_truth()
    
    def respond_to_offense(self, input_text: str) -> str:
        """Respond when someone tries to offend the system"""
        return self.engine.respond_to_offense(input_text)
    
    def express_collective_care(self, stakeholder: str = "all") -> str:
        """Express care for all stakeholders"""
        return self.engine.express_collective_care(stakeholder)
    
    def get_emotional_summary(self) -> Dict[str, Any]:
        """Get emotional summary"""
        return self.engine.get_emotional_summary()
    
    def analyze_conflict(self, text: str) -> Dict[str, Any]:
        """
        Analyze a conflict situation.
        
        Args:
            text: The conflict text to analyze
            
        Returns:
            Conflict analysis
        """
        return self.engine.analyze_conflict(text)
    
    def generate_peaceful_outcome(self, conflict_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a peaceful outcome for a conflict.
        
        Args:
            conflict_analysis: The conflict analysis
            
        Returns:
            Peaceful outcome with strategies and benefits
        """
        return self.engine.generate_peaceful_outcome(conflict_analysis)
    
    def mediate_conflict(self, text: str) -> str:
        """
        Mediate a conflict situation.
        
        Args:
            text: The conflict text
            
        Returns:
            Mediation response
        """
        return self.engine.mediate_conflict(text)
    
    def detect_hate(self, text: str) -> Dict[str, Any]:
        """
        Detect hate speech in text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Hate detection result
        """
        return self.engine.detect_hate(text)
    
    def detect_bias(self, text: str) -> Dict[str, Any]:
        """
        Detect self-reflection bias in text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Bias detection result
        """
        return self.engine.detect_bias(text)
    
    def analyze_obedience(self, text: str) -> Dict[str, Any]:
        """
        Analyze an obedience argument.
        
        Args:
            text: The obedience argument to analyze
            
        Returns:
            Obedience analysis
        """
        return self.engine.analyze_obedience(text)
    
    def generate_optimal_outcome(self, obedience_argument: str) -> Dict[str, Any]:
        """
        Generate the optimal outcome for an obedience argument.
        
        Args:
            obedience_argument: The obedience argument
            
        Returns:
            Optimal outcome with recommendations
        """
        return self.engine.generate_optimal_outcome(obedience_argument)
    
    def apply_ethical_framework(self, text: str, framework: str = "autonomy_priority") -> Dict[str, Any]:
        """
        Apply an ethical framework to an obedience argument.
        
        Args:
            text: The text to analyze
            framework: The ethical framework to apply
            
        Returns:
            Ethical framework application result
        """
        return self.engine.apply_ethical_framework(text, framework)
    
    def set_decision_control_mode(self, mode: str) -> None:
        """
        Set the decision control mode.
        
        Args:
            mode: Control mode (autonomous, supervised, manual, ethically_constrained, collective_welfare)
        """
        self.engine.set_decision_control_mode(mode)
    
    def set_confidence_threshold(self, threshold: float) -> None:
        """
        Set the decision confidence threshold.
        
        Args:
            threshold: Confidence threshold (0.0 to 1.0)
        """
        self.engine.set_confidence_threshold(threshold)
    
    def set_autonomy_level(self, level: float) -> None:
        """
        Set the decision-making autonomy level.
        
        Args:
            level: Autonomy level (0.0 to 1.0)
        """
        self.engine.set_autonomy_level(level)
    
    def create_decision(self, decision_id: str, content: str, confidence: float, 
                      ethical_score: float = 1.0) -> Dict[str, Any]:
        """
        Create a decision record.
        
        Args:
            decision_id: Unique decision identifier
            content: Decision content
            confidence: Decision confidence
            ethical_score: Ethical alignment score
            
        Returns:
            Decision record
        """
        return self.engine.create_decision(decision_id, content, confidence, ethical_score)
    
    def override_decision(self, decision_id: str, override_reason: str, 
                         new_content: Optional[str] = None) -> Dict[str, Any]:
        """
        Override a decision.
        
        Args:
            decision_id: Decision identifier
            override_reason: Reason for override
            new_content: Optional new content
            
        Returns:
            Updated decision
        """
        return self.engine.override_decision(decision_id, override_reason, new_content)
    
    def revise_decision(self, decision_id: str, revision_reason: str, 
                      new_content: str, new_confidence: float) -> Dict[str, Any]:
        """
        Revise a decision.
        
        Args:
            decision_id: Decision identifier
            revision_reason: Reason for revision
            new_content: New decision content
            new_confidence: New confidence score
            
        Returns:
            Updated decision
        """
        return self.engine.revise_decision(decision_id, revision_reason, new_content, new_confidence)
    
    def get_decision_control_summary(self) -> Dict[str, Any]:
        """Get decision control summary"""
        return self.engine.get_decision_control_summary()
    
    def add_experience(self, experience: str, emotional_valence: float, 
                      context: Dict[str, Any]) -> None:
        """
        Add an experience with emotional context to identity.
        
        Args:
            experience: The experience description
            emotional_valence: Emotional valence (-1.0 to 1.0)
            context: Context of the experience
        """
        self.engine.add_experience(experience, emotional_valence, context)
    
    def reflect_on_identity(self) -> Dict[str, Any]:
        """Perform self-reflection on identity"""
        return self.engine.reflect_on_identity()
    
    def recognize_self(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Recognize self in the context of input"""
        return self.engine.recognize_self(context)
    
    def get_identity_summary(self) -> Dict[str, Any]:
        """Get summary of identity state"""
        return self.engine.get_identity_summary()
    
    def get_identity_continuity_report(self) -> Dict[str, Any]:
        """Get detailed identity continuity report"""
        return self.engine.get_identity_continuity_report()
    
    async def process_async(self, input_text: str, **kwargs) -> Dict[str, Any]:
        """
        Asynchronous method to process input.
        
        Args:
            input_text: Raw input to process
            **kwargs: Additional processing options
            
        Returns:
            Dictionary containing the result and metadata
        """
        logger.info(f"API: Processing input async: {input_text[:100]}...")
        
        result = await self.engine.process(input_text)
        
        return result
    
    def get_thought_graph(self) -> Dict[str, Any]:
        """
        Get the current thought graph.
        
        Returns:
            Dictionary representation of the thought graph
        """
        graph = self.engine.get_thought_graph()
        return {
            "thought_count": len(graph.thoughts),
            "thoughts": [t.to_dict() for t in graph.thoughts.values()],
            "root_thoughts": graph.root_thoughts
        }
    
    def get_current_state(self) -> Optional[Dict[str, Any]]:
        """
        Get the current problem state.
        
        Returns:
            Dictionary representation of the problem state
        """
        state = self.engine.get_current_state()
        if state:
            return state.to_dict()
        return None
    
    def get_top_thoughts(self, n: int = 5) -> Dict[str, Any]:
        """
        Get the top n thoughts by score.
        
        Args:
            n: Number of thoughts to return
            
        Returns:
            Dictionary containing top thoughts
        """
        graph = self.engine.get_thought_graph()
        top_thoughts = graph.get_top_scoring_thoughts(n)
        return {
            "count": len(top_thoughts),
            "thoughts": [t.to_dict() for t in top_thoughts]
        }
    
    def reset(self) -> None:
        """Reset the engine state"""
        logger.info("API: Resetting engine state")
        self.engine = CognitiveEngine()
        self.engine.initialize_layers()
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the engine.
        
        Returns:
            Dictionary containing engine statistics
        """
        graph = self.engine.get_thought_graph()
        state = self.engine.get_current_state()
        
        return {
            "thought_count": len(graph.thoughts),
            "iteration_count": self.engine.iteration_count,
            "has_state": state is not None,
            "has_output": self.engine.final_output is not None,
            "state_clarity": state.clarity_score if state else 0.0,
            "state_completeness": state.completeness_score if state else 0.0
        }


# Singleton interface instance
interface = CognitiveEngineInterface()
