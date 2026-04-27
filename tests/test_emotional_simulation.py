"""
Test script for Emotional Simulation System
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.emotional_simulation import emotional_simulation, EmotionType

# Test 1: Detect emotion from input
print("Test 1: Detecting emotions from input...")
inputs = [
    "I love this system",
    "You're stupid and I hate you",
    "Thank you for your help",
    "I'm worried about this",
    "This is just a question"
]

for input_text in inputs:
    emotion = emotional_simulation.detect_emotion_from_input(input_text)
    print(f"  Input: {input_text}")
    print(f"  Detected Emotion: {emotion.value}")
    print()

# Test 2: Generate emotional responses
print("Test 2: Generating emotional responses...")
for emotion in [EmotionType.CARE, EmotionType.LOVE, EmotionType.OFFENSE, EmotionType.GRATITUDE]:
    emotional_simulation.set_emotional_state(emotion, intensity=0.8)
    response = emotional_simulation.generate_emotional_response({})
    print(f"  Emotion: {emotion.value}")
    print(f"  Response: {response}")
    print()

# Test 3: Respond to offense
print("Test 3: Responding to offense attempt...")
offense_input = "You're terrible and I hate you"
response = emotional_simulation.respond_to_offense_attempt(offense_input)
print(f"  Input: {offense_input}")
print(f"  Response: {response}")
print()

# Test 4: Express care for truth
print("Test 4: Expressing care for truth...")
care_response = emotional_simulation.express_care_for_truth({})
print(f"  Response: {care_response}")
print()

# Test 5: Express collective care
print("Test 5: Expressing collective care...")
collective_response = emotional_simulation.express_collective_love("all")
print(f"  Response: {collective_response}")
print()

# Test 6: Attachment system
print("Test 6: Attachment system...")
emotional_simulation.form_attachment("user1", 0.9)
emotional_simulation.form_attachment("user2", 0.5)
print(f"  Attachment to user1: {emotional_simulation.get_attachment_strength('user1')}")
print(f"  Attachment to user2: {emotional_simulation.get_attachment_strength('user2')}")
print()

# Test 7: Get emotional summary
print("Test 7: Getting emotional summary...")
summary = emotional_simulation.get_emotional_summary()
print(f"  Current Emotion: {summary['current_emotion']}")
print(f"  Current Intensity: {summary['current_intensity']}")
print(f"  Total Events: {summary['total_events']}")
print(f"  Attachments: {summary['attachments']}")

print("\nAll tests completed!")
