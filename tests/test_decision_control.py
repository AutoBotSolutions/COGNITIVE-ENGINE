"""
Test script for Decision Control System
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.decision_control import decision_control, DecisionControlMode

# Test 1: Set control mode
print("Test 1: Setting control mode...")
decision_control.set_control_mode(DecisionControlMode.ETHICALLY_CONSTRAINED)
print(f"  Control Mode: {decision_control.control_mode.value}")
decision_control.set_control_mode(DecisionControlMode.AUTONOMOUS)
print(f"  Control Mode: {decision_control.control_mode.value}")
print()

# Test 2: Set confidence threshold
print("Test 2: Setting confidence threshold...")
decision_control.set_confidence_threshold(0.8)
print(f"  Confidence Threshold: {decision_control.confidence_threshold}")
decision_control.set_confidence_threshold(0.6)
print(f"  Confidence Threshold: {decision_control.confidence_threshold}")
print()

# Test 3: Set autonomy level
print("Test 3: Setting autonomy level...")
decision_control.set_autonomy_level(0.9)
print(f"  Autonomy Level: {decision_control.decision_autonomy_level}")
decision_control.set_autonomy_level(0.5)
print(f"  Autonomy Level: {decision_control.decision_autonomy_level}")
print()

# Test 4: Check if decision can be committed
print("Test 4: Checking if decision can be committed...")
test_cases = [
    (0.9, 1.0, "High confidence, high ethics"),
    (0.5, 1.0, "Low confidence, high ethics"),
    (0.9, 0.5, "High confidence, low ethics"),
    (0.5, 0.5, "Low confidence, low ethics")
]

for confidence, ethical_score, description in test_cases:
    can_commit, reason = decision_control.can_commit_decision(confidence, ethical_score)
    print(f"  {description}:")
    print(f"    Can Commit: {can_commit}")
    print(f"    Reason: {reason}")
print()

# Test 5: Create decision
print("Test 5: Creating decisions...")
decision_control.set_confidence_threshold(0.7)
decision1 = decision_control.create_decision("decision_1", "Proceed with action A", 0.8, 0.9)
print(f"  Decision 1:")
print(f"    Status: {decision1['status']}")
print(f"    Can Commit: {decision1['can_commit']}")
print(f"    Reason: {decision1['commit_reason']}")

decision2 = decision_control.create_decision("decision_2", "Proceed with action B", 0.5, 0.9)
print(f"  Decision 2:")
print(f"    Status: {decision2['status']}")
print(f"    Can Commit: {decision2['can_commit']}")
print(f"    Reason: {decision2['commit_reason']}")
print()

# Test 6: Override decision
print("Test 6: Overriding decision...")
override_result = decision_control.override_decision("decision_1", "New information available", "Proceed with action C")
print(f"  Override Result:")
print(f"    Status: {override_result['status']}")
print(f"    Override Reason: {override_result['override_reason']}")
print(f"    Override Count: {override_result['override_count']}")
print()

# Test 7: Revise decision
print("Test 7: Revising decision...")
revise_result = decision_control.revise_decision("decision_2", "Confidence improved", "Proceed with action B", 0.75)
print(f"  Revise Result:")
print(f"    Status: {revise_result['status']}")
print(f"    Revision Reason: {revise_result['revision_reason']}")
print(f"    Revision Count: {revise_result['revision_count']}")
print(f"    New Confidence: {revise_result['confidence']}")
print()

# Test 8: Cancel decision
print("Test 8: Canceling decision...")
cancel_result = decision_control.cancel_decision("decision_1", "No longer needed")
print(f"  Cancel Result:")
print(f"    Status: {cancel_result['status']}")
print(f"    Cancel Reason: {cancel_result['cancel_reason']}")
print()

# Test 9: Get decision control summary
print("Test 9: Getting decision control summary...")
summary = decision_control.get_decision_control_summary()
print(f"  Control Mode: {summary['control_mode']}")
print(f"  Confidence Threshold: {summary['confidence_threshold']}")
print(f"  Autonomy Level: {summary['autonomy_level']}")
print(f"  Total Decisions: {summary['total_decisions']}")
print(f"  Active Decisions: {summary['active_decisions']}")
print(f"  Status Distribution: {summary['status_distribution']}")

print("\nAll tests completed!")
