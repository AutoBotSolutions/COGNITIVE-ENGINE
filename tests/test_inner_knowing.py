"""
Test script for Inner Knowing System
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.inner_knowing import inner_knowing, ConfidenceLevel, KnowledgeType

# Test 1: Add knowledge
print("Test 1: Adding knowledge...")
inner_knowing.add_knowledge(
    topic="cognitive engine",
    knowledge="The Cognitive Engine is a thought formation system with five layers",
    confidence=ConfidenceLevel.HIGH,
    knowledge_type=KnowledgeType.FACTUAL
)

# Test 2: Query knowledge
print("\nTest 2: Querying knowledge...")
result = inner_knowing.query_knowledge("cognitive engine")
print(f"Query result: {result}")

# Test 3: Answer inner questions
print("\nTest 3: Answering inner questions...")
questions = [
    "what do you know about cognitive engine",
    "how confident are you",
    "what are you capable of",
    "what is your current state"
]

for question in questions:
    answer = inner_knowing.answer_inner_question(question)
    print(f"Q: {question}")
    print(f"A: {answer}\n")

# Test 4: Get self-report
print("Test 4: Getting self-report...")
report = inner_knowing.get_self_report()
print(f"Self-report keys: {report.keys()}")
print(f"Knowledge summary: {report['knowledge_summary']}")
print(f"Self-model: {report['self_model']}")

# Test 5: Add intuition pattern
print("\nTest 5: Adding intuition pattern...")
inner_knowing.add_intuition_pattern(
    pattern_description="User greeting detected",
    trigger_conditions=["hello", "hi", "hey"],
    suggested_action="Respond with friendly greeting",
    confidence=ConfidenceLevel.HIGH
)

# Test 6: Query intuition
print("\nTest 6: Querying intuition...")
intuition = inner_knowing.query_intuition("hello there")
print(f"Intuition result: {intuition}")

print("\nAll tests completed!")
