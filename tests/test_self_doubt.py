"""
Test script for Self-Doubt System
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.self_doubt import self_doubt, DoubtLevel

# Test 1: Assess doubt level
print("Test 1: Assessing doubt levels...")
thoughts = [
    ("The Cognitive Engine is perfect", 0.9, {}),
    ("The system might work well", 0.6, {}),
    ("Perhaps the approach could be effective", 0.5, {"knowns": {}, "unknowns": ["many things"]})
]

for premise, confidence, context in thoughts:
    doubt_level = self_doubt.assess_doubt_level(premise, confidence, context)
    print(f"  Premise: {premise}")
    print(f"  Confidence: {confidence}")
    print(f"  Doubt Level: {doubt_level.value}")
    print()

# Test 2: Generate self-questions
print("Test 2: Generating self-questions...")
premise = "The Cognitive Engine will solve all AI problems"
doubt_level = DoubtLevel.HIGH
questions = self_doubt.generate_self_questions(premise, doubt_level)
print(f"  Premise: {premise}")
print(f"  Doubt Level: {doubt_level.value}")
print(f"  Questions:")
for q in questions:
    print(f"    - {q}")
print()

# Test 3: Generate counter-argument
print("Test 3: Generating counter-argument...")
premise = "The system always produces correct answers"
counter_arg = self_doubt.generate_counter_argument(premise)
print(f"  Premise: {premise}")
print(f"  Counter-argument: {counter_arg}")
print()

# Test 4: Adjust confidence with doubt
print("Test 4: Adjusting confidence with doubt...")
original_confidence = 0.8
for doubt_level in [DoubtLevel.LOW, DoubtLevel.MODERATE, DoubtLevel.HIGH, DoubtLevel.SEVERE]:
    adjusted = self_doubt.adjust_confidence_with_doubt(original_confidence, doubt_level)
    print(f"  Original: {original_confidence}, Doubt: {doubt_level.value}, Adjusted: {adjusted}")
print()

# Test 5: Challenge assumption
print("Test 5: Challenging assumption...")
assumption = "The system knows everything it needs to know"
challenge = self_doubt.challenge_assumption(assumption)
print(f"  Assumption: {assumption}")
print(f"  Counter-argument: {challenge['counter_argument']}")
print(f"  Challenging questions:")
for q in challenge['challenging_questions']:
    print(f"    - {q}")
print()

# Test 6: Get doubt statistics
print("Test 6: Getting doubt statistics...")
stats = self_doubt.get_doubt_statistics()
print(f"  Total doubt events: {stats['total_doubt_events']}")
print(f"  Uncertainty factors: {stats['current_uncertainty_factors']}")

print("\nAll tests completed!")
