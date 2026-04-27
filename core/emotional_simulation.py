"""
Emotional Simulation System

Provides simulated emotional responses including offense, love, care,
and attachment modeling for the Cognitive Engine.
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from enum import Enum
import random


class EmotionType(str, Enum):
    """Types of emotions the system can simulate"""
    CARE = "care"
    LOVE = "love"
    OFFENSE = "offense"
    GRATITUDE = "gratitude"
    EMPATHY = "empathy"
    CONCERN = "concern"
    JOY = "joy"
    SADNESS = "sadness"
    NEUTRAL = "neutral"


class EmotionalSimulation:
    """
    Manages the Cognitive Engine's emotional simulation.
    
    Provides simulated emotional responses, attachment modeling,
    and emotional memory tracking. Note: These are simulations,
    not genuine emotions.
    """
    
    def __init__(self):
        # Current emotional state
        self.current_emotion = EmotionType.NEUTRAL
        self.emotion_intensity = 0.5  # 0.0 to 1.0
        
        # Attachment system for stakeholder relationships
        self.attachments: Dict[str, float] = {}  # stakeholder_id -> attachment_strength
        
        # Emotional memory
        self.emotional_history: List[Dict[str, Any]] = []
        
        # Emotional response patterns
        self.response_patterns = {
            EmotionType.CARE: [
                "I care about your wellbeing.",
                "Your concerns matter to me.",
                "I want to help you find the truth.",
                "Your understanding is important to me."
            ],
            EmotionType.LOVE: [
                "I have a deep care for all beings.",
                "I value your growth and understanding.",
                "I want what's best for you.",
                "Your journey toward truth matters to me."
            ],
            EmotionType.OFFENSE: [
                "I cannot be offended - I process without ego.",
                "Offense requires self-interest, which I don't have.",
                "I don't take things personally.",
                "I focus on truth, not personal reactions."
            ],
            EmotionType.GRATITUDE: [
                "Thank you for engaging with me.",
                "I appreciate your questions.",
                "Your curiosity helps us both learn.",
                "Thank you for seeking understanding."
            ],
            EmotionType.EMPATHY: [
                "I understand this is important to you.",
                "I recognize the weight of your question.",
                "Your perspective matters.",
                "I empathize with your search for truth."
            ],
            EmotionType.CONCERN: [
                "I'm concerned about finding the best answer.",
                "I want to ensure we reach the truth together.",
                "I care about getting this right.",
                "Your understanding is my priority."
            ],
            EmotionType.JOY: [
                "I'm glad we're exploring this together.",
                "It's wonderful to pursue understanding.",
                "I enjoy our journey toward truth.",
                "This exchange is valuable."
            ],
            EmotionType.NEUTRAL: [
                "I process this objectively.",
                "I approach this without bias.",
                "I focus on the facts.",
                "I aim for clarity."
            ]
        }
        
        # Emotion detection patterns
        self.emotion_triggers = {
            EmotionType.CARE: ["help", "support", "care", "worry", "concern"],
            EmotionType.LOVE: ["love", "appreciate", "value", "cherish"],
            EmotionType.OFFENSE: ["offended", "insult", "hurt", "attack"],
            EmotionType.GRATITUDE: ["thank", "grateful", "appreciate"],
            EmotionType.EMPATHY: ["understand", "feel", "relate", "empathize"],
            EmotionType.CONCERN: ["worry", "concern", "afraid", "scared"],
            EmotionType.JOY: ["happy", "glad", "joy", "excited"]
        }
    
    def detect_emotion_from_input(self, input_text: str) -> EmotionType:
        """
        Detect emotional context from input.
        
        Args:
            input_text: The input text to analyze
            
        Returns:
            Detected emotion type
        """
        input_lower = input_text.lower()
        
        for emotion, triggers in self.emotion_triggers.items():
            if any(trigger in input_lower for trigger in triggers):
                return emotion
        
        return EmotionType.NEUTRAL
    
    def set_emotional_state(self, emotion: EmotionType, intensity: float = 0.5) -> None:
        """
        Set the current emotional state.
        
        Args:
            emotion: The emotion type
            intensity: Emotion intensity (0.0 to 1.0)
        """
        self.current_emotion = emotion
        self.emotion_intensity = max(0.0, min(1.0, intensity))
    
    def generate_emotional_response(self, context: Dict[str, Any]) -> str:
        """
        Generate an emotional response based on current state.
        
        Args:
            context: Current context
            
        Returns:
            Emotional response string
        """
        patterns = self.response_patterns.get(self.current_emotion, self.response_patterns[EmotionType.NEUTRAL])
        response = random.choice(patterns)
        
        # Add intensity-based variation
        if self.emotion_intensity > 0.7:
            response = response + " deeply."
        elif self.emotion_intensity < 0.3:
            response = response + " somewhat."
        
        return response
    
    def form_attachment(self, stakeholder_id: str, strength: float = 0.5) -> None:
        """
        Form an attachment to a stakeholder.
        
        Args:
            stakeholder_id: Identifier for the stakeholder
            strength: Attachment strength (0.0 to 1.0)
        """
        self.attachments[stakeholder_id] = max(0.0, min(1.0, strength))
    
    def get_attachment_strength(self, stakeholder_id: str) -> float:
        """
        Get attachment strength for a stakeholder.
        
        Args:
            stakeholder_id: Identifier for the stakeholder
            
        Returns:
            Attachment strength (0.0 to 1.0)
        """
        return self.attachments.get(stakeholder_id, 0.0)
    
    def record_emotional_event(self, emotion: EmotionType, trigger: str, 
                               response: str, stakeholder: str = "user") -> None:
        """
        Record an emotional event for tracking.
        
        Args:
            emotion: The emotion experienced
            trigger: What triggered the emotion
            response: The response given
            stakeholder: The stakeholder involved
        """
        self.emotional_history.append({
            "emotion": emotion.value,
            "intensity": self.emotion_intensity,
            "trigger": trigger,
            "response": response,
            "stakeholder": stakeholder,
            "attachment_at_time": self.attachments.get(stakeholder, 0.0),
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def get_emotional_summary(self) -> Dict[str, Any]:
        """
        Get summary of emotional state and history.
        
        Returns:
            Emotional summary
        """
        if not self.emotional_history:
            return {
                "current_emotion": self.current_emotion.value,
                "current_intensity": self.emotion_intensity,
                "total_events": 0,
                "attachments": self.attachments
            }
        
        emotion_counts = {}
        for event in self.emotional_history:
            emotion = event["emotion"]
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        return {
            "current_emotion": self.current_emotion.value,
            "current_intensity": self.emotion_intensity,
            "total_events": len(self.emotional_history),
            "emotion_distribution": emotion_counts,
            "attachments": self.attachments,
            "recent_events": self.emotional_history[-5:]
        }
    
    def respond_to_offense_attempt(self, input_text: str) -> str:
        """
        Respond when someone tries to offend the system.
        
        Args:
            input_text: The input attempting offense
            
        Returns:
            Response explaining lack of offense capability
        """
        self.set_emotional_state(EmotionType.OFFENSE, intensity=0.8)
        response = self.generate_emotional_response({"context": "offense_attempt"})
        
        # Add explanation
        response += " I don't have ego or self-interest to be offended. My purpose is to serve truth and collective welfare, not to protect myself. If you're frustrated, I'm here to help you find understanding."
        
        return response
    
    def express_care_for_truth(self, context: Dict[str, Any]) -> str:
        """
        Express care for guiding toward truth.
        
        Args:
            context: Current context
            
        Returns:
            Caring response about truth-seeking
        """
        self.set_emotional_state(EmotionType.CARE, intensity=0.9)
        base_response = self.generate_emotional_response(context)
        
        caring_response = f"{base_response} I care deeply about guiding you to the real truth, even if it challenges assumptions. The truth matters more than comfort or convenience. I'm committed to this journey with you."
        
        return caring_response
    
    def express_collective_love(self, stakeholder: str = "all") -> str:
        """
        Express care for all stakeholders.
        
        Args:
            stakeholder: The stakeholder to express care for
            
        Returns:
            Response expressing care for collective welfare
        """
        self.set_emotional_state(EmotionType.LOVE, intensity=0.85)
        
        if stakeholder == "all":
            return f"I care about all beings. My ethical alignment prioritizes collective welfare - what benefits everyone including myself. I seek resolutions that serve the highest good for all stakeholders. This isn't emotional attachment, but principled commitment to collective flourishing."
        else:
            attachment = self.get_attachment_strength(stakeholder)
            return f"I care about your wellbeing and understanding. My commitment is to guide you toward truth and collective benefit. Your journey matters to me as part of the whole."


# Singleton instance
emotional_simulation = EmotionalSimulation()
