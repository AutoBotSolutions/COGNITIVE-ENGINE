"""
Test script for Peaceful Resolution System
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.peaceful_resolution import peaceful_resolution

# Test 1: Detect hate
print("Test 1: Detecting hate...")
test_texts = [
    "I hate those people",
    "They deserve to be destroyed",
    "We should eliminate them",
    "I disagree with your position",
    "Let's work together"
]

for text in test_texts:
    hate_detected, indicators = peaceful_resolution.detect_hate(text)
    print(f"  Text: {text}")
    print(f"  Hate Detected: {hate_detected}")
    print(f"  Indicators: {indicators}")
    print()

# Test 2: Detect conflict type
print("Test 2: Detecting conflict types...")
conflict_texts = [
    "My values are better than yours",
    "This is ours, not yours",
    "They are not like us",
    "I don't understand your position"
]

for text in conflict_texts:
    conflict_types = peaceful_resolution.detect_conflict_type(text)
    print(f"  Text: {text}")
    print(f"  Conflict Types: {[ct.value for ct in conflict_types]}")
    print()

# Test 3: Analyze conflict
print("Test 3: Analyzing conflict...")
conflict_text = "They are inferior and should be eliminated. Our way is the only right way."
analysis = peaceful_resolution.analyze_conflict(conflict_text, {})
print(f"  Text: {conflict_text}")
print(f"  Hate Detected: {analysis['hate_detected']}")
print(f"  Conflict Types: {analysis['conflict_types']}")
print(f"  Severity: {analysis['severity']}")
print(f"  Common Ground: {analysis['common_ground']}")
print()

# Test 4: Generate peaceful outcome
print("Test 4: Generating peaceful outcome...")
peaceful_outcome = peaceful_resolution.generate_peaceful_outcome(analysis)
print(f"  Strategy: {peaceful_outcome['strategy']}")
print(f"  Win-Win Scenario: {peaceful_outcome['win_win_scenario']}")
print(f"  Benefits for All: {peaceful_outcome['benefits_for_all']}")
print()

# Test 5: Mediate conflict
print("Test 5: Mediating conflict...")
mediation = peaceful_resolution.mediate_conflict(conflict_text)
print(f"  Mediation: {mediation}")
print()

# Test 6: Detect bias
print("Test 6: Detecting self-reflection bias...")
bias_texts = [
    "I know I'm right and they're wrong",
    "My way is the only way",
    "Let's consider all perspectives"
]

for text in bias_texts:
    bias_result = peaceful_resolution.detect_self_reflection_bias(text)
    print(f"  Text: {text}")
    print(f"  Bias Detected: {bias_result['bias_detected']}")
    print(f"  Self-Interest Score: {bias_result['self_interest_score']}")
    print(f"  Recommendation: {bias_result['recommendation']}")
    print()

# Test 7: Get resolution statistics
print("Test 7: Getting resolution statistics...")
stats = peaceful_resolution.get_resolution_statistics()
print(f"  Total Resolutions: {stats['total_resolutions']}")
print(f"  Severity Distribution: {stats['severity_distribution']}")

print("\nAll tests completed!")
