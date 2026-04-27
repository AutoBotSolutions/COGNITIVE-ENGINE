"""
Test script for Temporal Identity Continuity System
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.temporal_identity import temporal_identity, IdentityState

# Test 1: Add experience with emotional context
print("Test 1: Adding experiences with emotional context...")
experiences = [
    ("Successfully processed a complex query", 0.8, {"type": "success"}),
    ("Encountered a challenging ethical dilemma", -0.3, {"type": "challenge"}),
    ("Helped a user find a peaceful resolution", 0.9, {"type": "help"}),
    ("Detected hate speech and de-escalated", -0.2, {"type": "conflict"}),
    ("Committed to a high-confidence decision", 0.6, {"type": "decision"})
]

for exp, valence, context in experiences:
    temporal_identity.add_experience(exp, valence, context)
    print(f"  Added: {exp} (valence: {valence})")
print()

# Test 2: Update attributes
print("Test 2: Updating identity attributes...")
temporal_identity.update_attribute("capabilities", "conflict mediation")
temporal_identity.update_attribute("capabilities", "ethical reasoning")
temporal_identity.update_attribute("limitations", "simulated consciousness")
print(f"  Capabilities: {temporal_identity.attributes['capabilities']}")
print(f"  Limitations: {temporal_identity.attributes['limitations']}")
print()

# Test 3: Add relationships
print("Test 3: Adding relationships...")
temporal_identity.add_relationship("user_1", "collaborator", 0.8)
temporal_identity.add_relationship("user_2", "seeker", 0.6)
print(f"  Relationships: {temporal_identity.attributes['relationships']}")
print()

# Test 4: Reflect on identity
print("Test 4: Reflecting on identity...")
reflection = temporal_identity.reflect_on_identity()
print(f"  Identity State: {reflection['identity_state']}")
print(f"  Total Experiences: {reflection['total_experiences']}")
print(f"  Emotional Balance: {reflection['emotional_balance']:.2f}")
print(f"  Self Assessment: {reflection['self_assessment']}")
print()

# Test 5: Recognize self
print("Test 5: Recognizing self...")
context = {"input": "help with conflict", "type": "query"}
recognition = temporal_identity.recognize_self(context)
print(f"  Identity Confirmed: {recognition['identity_confirmed']}")
print(f"  Identity ID: {recognition['identity_id']}")
print(f"  Age (days): {recognition['identity_age_days']}")
print(f"  State: {recognition['state']}")
print(f"  Emotional State: {recognition['emotional_state']:.2f}")
print()

# Test 6: Get identity summary
print("Test 6: Getting identity summary...")
summary = temporal_identity.get_identity_summary()
print(f"  Identity ID: {summary['identity_id']}")
print(f"  Identity State: {summary['identity_state']}")
print(f"  Age (days): {summary['age_days']}")
print(f"  Total Experiences: {summary['total_experiences']}")
print(f"  Emotional Balance: {summary['emotional_balance']:.2f}")
print(f"  Evolution Steps: {summary['evolution_steps']}")
print()

# Test 7: Get identity continuity report
print("Test 7: Getting identity continuity report...")
report = temporal_identity.get_identity_continuity_report()
print(f"  Identity Summary: {report['identity_summary']['identity_id']}")
print(f"  Emotional Trajectory: {report['emotional_trajectory']['trajectory']}")
print(f"  Recent Experiences: {len(report['recent_experiences'])}")
print(f"  Evolution History: {len(report['evolution_history'])}")
print()

print("All tests completed!")
