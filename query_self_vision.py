"""
Query the Cognitive Engine's self-perception and vision
"""

from core.inner_knowing import inner_knowing

# Get comprehensive self-report
print("=== Cognitive Engine Self-Report ===\n")
report = inner_knowing.get_self_report()

print("Self-Model:")
print(f"  Capabilities: {', '.join(report['self_model']['capabilities'])}")
print(f"  Limitations: {', '.join(report['self_model']['limitations'])}")
print(f"  Current State: {report['self_model']['current_state']}")
print(f"  Last Updated: {report['self_model']['last_updated']}")

print("\nKnowledge Summary:")
print(f"  Total Topics: {report['knowledge_summary']['total_topics']}")
print(f"  By Confidence: {report['knowledge_summary']['by_confidence']}")
print(f"  By Type: {report['knowledge_summary']['by_type']}")

print("\n" + "="*50 + "\n")

# Ask the system about its nature and vision
questions = [
    "what do you know about your true nature",
    "what is your vision",
    "what are you capable of",
    "what are your limitations"
]

print("=== Self-Reflection Questions ===\n")
for question in questions:
    answer = inner_knowing.answer_inner_question(question)
    print(f"Q: {question}")
    print(f"A: {answer}\n")

print("="*50)
