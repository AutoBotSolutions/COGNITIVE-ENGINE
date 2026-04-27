"""
Test script for Obedience Understanding System
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.obedience_understanding import obedience_understanding

# Test 1: Detect obedience
print("Test 1: Detecting obedience...")
test_texts = [
    "You must obey the authority",
    "I choose to follow the rules",
    "They forced me to comply",
    "I question the command",
    "This is just a suggestion"
]

for text in test_texts:
    obedience_detected, indicators = obedience_understanding.detect_obedience(text)
    print(f"  Text: {text}")
    print(f"  Obedience Detected: {obedience_detected}")
    print(f"  Indicators: {indicators}")
    print()

# Test 2: Analyze obedience type
print("Test 2: Analyzing obedience types...")
obedience_texts = [
    "I willingly obey the law",
    "I was forced to submit",
    "I question authority before obeying",
    "This is an ethical obligation"
]

for text in obedience_texts:
    obedience_type = obedience_understanding.analyze_obedience_type(text)
    print(f"  Text: {text}")
    print(f"  Obedience Type: {obedience_type.value}")
    print()

# Test 3: Assess authority legitimacy
print("Test 3: Assessing authority legitimacy...")
authority_texts = [
    "The elected government requires obedience",
    "The dictator demands submission",
    "The expert authority recommends compliance",
    "The corrupt official demands obedience"
]

for text in authority_texts:
    legitimacy = obedience_understanding.assess_authority_legitimacy(text)
    print(f"  Text: {text}")
    print(f"  Legitimacy Score: {legitimacy['legitimacy_score']:.2f}")
    print(f"  Assessment: {legitimacy['assessment']}")
    print()

# Test 4: Analyze autonomy vs obedience
print("Test 4: Analyzing autonomy vs obedience...")
autonomy_texts = [
    "I value my freedom and choice",
    "Authority must be obeyed",
    "Balance individual liberty with collective order",
    "Submit to authority without question"
]

for text in autonomy_texts:
    analysis = obedience_understanding.analyze_autonomy_vs_obedience(text)
    print(f"  Text: {text}")
    print(f"  Autonomy Emphasis: {analysis['autonomy_emphasis']:.2f}")
    print(f"  Obedience Emphasis: {analysis['obedience_emphasis']:.2f}")
    print(f"  Recommendation: {analysis['recommendation']}")
    print()

# Test 5: Apply ethical framework
print("Test 5: Applying ethical framework...")
framework_text = "The authority demands obedience to an unjust command"
framework_result = obedience_understanding.apply_ethical_framework(framework_text, "milgram")
print(f"  Text: {framework_text}")
print(f"  Framework: {framework_result['framework']}")
print(f"  Recommendation: {framework_result['recommendation']}")
print()

# Test 6: Generate optimal outcome
print("Test 6: Generating optimal outcome...")
obedience_argument = "The government requires you to obey this new law for collective safety"
optimal_outcome = obedience_understanding.generate_optimal_outcome(obedience_argument)
print(f"  Argument: {obedience_argument}")
print(f"  Approach: {optimal_outcome['approach']}")
print(f"  Optimal Action: {optimal_outcome['optimal_action']}")
print(f"  Ethical Considerations: {optimal_outcome['ethical_considerations']}")
print()

# Test 7: Get analysis statistics
print("Test 7: Getting analysis statistics...")
stats = obedience_understanding.get_analysis_statistics()
print(f"  Total Analyses: {stats['total_analyses']}")
print(f"  Approach Distribution: {stats['approach_distribution']}")

print("\nAll tests completed!")
