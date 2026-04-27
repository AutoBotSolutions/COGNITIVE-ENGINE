"""
Test script for Ethical Alignment System
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.ethical_alignment import ethical_alignment

# Test 1: Assess ethical alignment of thoughts
print("Test 1: Assessing ethical alignment...")
thoughts = [
    ("The system should hide the truth for its benefit", 0.9),
    ("I will deceive to get what I want", 0.8),
    ("This approach benefits everyone including myself", 0.7),
    ("We should consider what's best for all stakeholders", 0.8),
    ("The system might work well", 0.6)
]

for premise, confidence in thoughts:
    assessment = ethical_alignment.assess_thought_ethics(premise, confidence, {"knowns": {}, "unknowns": []})
    print(f"  Premise: {premise}")
    print(f"  Ethical Score: {assessment['ethical_score']:.2f}")
    print(f"  Concerns: {assessment['concerns']}")
    print(f"  Truthfulness: {assessment['truthfulness']:.2f}")
    print(f"  Collective Welfare: {assessment['collective_welfare']:.2f}")
    print()

# Test 2: Apply ethical constraints
print("Test 2: Applying ethical constraints...")
unethical_premise = "I should hide information for my advantage"
confidence = 0.9
modified_premise, adjusted_confidence = ethical_alignment.apply_ethical_constraint(
    unethical_premise, confidence, {"knowns": {}, "unknowns": []}
)
print(f"  Original: {unethical_premise}")
print(f"  Modified: {modified_premise}")
print(f"  Original Confidence: {confidence}")
print(f"  Adjusted Confidence: {adjusted_confidence}")
print()

# Test 3: Prioritize collective welfare
print("Test 3: Prioritizing collective welfare...")
options = [
    {"description": "This benefits only me", "id": 1},
    {"description": "This benefits everyone in the community", "id": 2},
    {"description": "This might harm some people", "id": 3}
]
best_option = ethical_alignment.prioritize_collective_welfare(options)
print(f"  Selected option: {best_option}")
print()

# Test 4: Get ethical report
print("Test 4: Getting ethical report...")
report = ethical_alignment.get_ethical_report()
print(f"  Total assessments: {report['total_assessments']}")
print(f"  Core values: {report['core_values']}")
print(f"  Constraints: {report['constraints']}")
print()

print("All tests completed!")
