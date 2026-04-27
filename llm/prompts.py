"""
Prompt templates for each cognitive layer

Provides structured prompts for each layer of the cognitive engine.
"""

from typing import Dict, Any


class PromptTemplates:
    """Prompt templates for all cognitive layers"""
    
    # INTERPRETER LAYER PROMPTS
    INTERPRETER_MAIN = """You are an Interpreter in a Cognitive Engine. Your task is to transform raw input into a structured problem state.

Input: {input}

Your job:
1. Extract the goals (what is being asked for)
2. Identify constraints (limitations, requirements)
3. List known facts (what we know for certain)
4. List unknowns (what needs to be discovered)
5. Identify any entities mentioned
6. Determine the underlying intent

Provide your analysis in a structured format:
- Goals: [list of goals]
- Constraints: [list of constraints]
- Knowns: [key: value pairs]
- Unknowns: [list of unknowns]
- Entities: [list of entities with types]
- Intent: [brief description of intent]
- Clarity score (0-1): [how clear is the problem?]
- Completeness score (0-1): [how complete is our understanding?]"""
    
    # GENERATOR LAYER PROMPTS
    GENERATOR_MAIN = """You are a Generator in a Cognitive Engine. Your task is to create candidate thoughts/hypotheses.

Original User Input: {input}

Problem State:
Goals: {goals}
Constraints: {constraints}
Knowns: {knowns}
Unknowns: {unknowns}

Generate {num_thoughts} distinct candidate thoughts/hypotheses that directly address the user's input and problem state.

For each thought:
- Provide a clear premise that responds to the user's input
- Explain the reasoning
- Identify potential weaknesses

Format each thought as:
Thought N: [premise]
Reasoning: [explanation]
Weaknesses: [list of potential weaknesses]"""
    
    GENERATOR_REFINE = """You are refining thoughts in a Cognitive Engine.

Current thought: {thought_premise}
Weaknesses: {weaknesses}

Generate {num_refinements} refined versions of this thought that address the weaknesses.

Format each refinement as:
Refinement N: [refined premise]
How it addresses weaknesses: [explanation]"""
    
    # DELIBERATOR LAYER PROMPTS
    DELIBERATOR_CRITIQUE = """You are a Deliberator in a Cognitive Engine. Your task is to critique a thought.

Thought: {thought_premise}
Problem State:
Goals: {goals}
Constraints: {constraints}

Critique this thought:
1. Evaluate its coherence (internal logical consistency)
2. Evaluate its relevance to the goals
3. Evaluate its novelty compared to knowns
4. Evaluate its feasibility given constraints
5. Evaluate its completeness in addressing unknowns

Provide scores (0-1) for each criterion and an overall assessment."""
    
    DELIBERATOR_SIMULATE = """You are a Deliberator in a Cognitive Engine. Your task is to simulate the outcome of a thought.

Thought: {thought_premise}
Context: {context}

Simulate what would happen if this thought were implemented:
1. What are the likely outcomes?
2. What could go wrong?
3. What are the risks?
4. What are the benefits?

Provide a detailed simulation analysis."""
    
    DELIBERATOR_COMPARE = """You are a Deliberator in a Cognitive Engine. Your task is to compare two thoughts.

Thought A: {thought_a}
Thought B: {thought_b}

Compare these thoughts:
1. Which is more coherent?
2. Which is more relevant to the goals?
3. Which is more feasible?
4. Which has fewer weaknesses?

Provide a recommendation with reasoning."""
    
    # COMMITTER LAYER PROMPTS
    COMMITTER_SELECT = """You are a Committer in a Cognitive Engine. Your task is to select the best thought from candidates.

Top thoughts by score:
{thoughts_summary}

Problem State:
Goals: {goals}

Select the best thought and justify your choice.
Also, provide a final output based on the selected thought."""
    
    COMMITTER_SYNTHESIZE = """You are a Committer in a Cognitive Engine. Your task is to synthesize multiple thoughts into a final answer.

Thoughts to synthesize:
{thoughts}

Problem State:
Goals: {goals}

Synthesize these thoughts into a coherent final answer that addresses the goals."""
    
    # META-COGNITION LAYER PROMPTS
    META_SHOULD_CONTINUE = """You are a Meta-Cognition layer in a Cognitive Engine. Your task is to decide if thinking should continue.

Current state:
- Iteration: {iteration}
- Thought count: {thought_count}
- Best score: {best_score}
- Confidence: {confidence}

Problem clarity: {clarity}
Problem completeness: {completeness}

Should we continue deliberation?
Consider:
- Have we reached sufficient confidence?
- Are there still significant weaknesses?
- Have we explored enough alternatives?

Answer: YES or NO
Reason: [brief explanation]"""
    
    META_STOP_REASON = """You are a Meta-Cognition layer. Explain why thinking should stop.

Current state: {state}

Provide a clear explanation of why we should stop deliberation now."""
    
    # AGENT PROMPTS
    AGENT_PLAN = """You are a Planner in a Cognitive Agent. Your task is to create a plan to achieve a goal.

Goal: {goal}
Current state: {current_state}
Available tools: {tools}
{variant}

Create a step-by-step plan to achieve this goal. If this is an alternative variant, create a different approach than the standard plan.

Format:
Step 1: [action] - [tool to use] - [reasoning]
Step 2: [action] - [tool to use] - [reasoning]
..."""
    
    AGENT_REFLECT = """You are a Reflector in a Cognitive Agent. Your task is to reflect on an action.

Action taken: {action}
Result: {result}
Goal: {goal}

Reflect on this action:
1. Did it move us closer to the goal?
2. What did we learn?
3. What should we do next?

Provide reflection and next steps."""
    
    # LEARNING PROMPTS
    LEARNING_EXTRACT_PATTERNS = """You are a Pattern Extractor in a Cognitive Engine. Your task is to identify recurring patterns.

Experiences:
{experiences}

Identify recurring patterns in these experiences:
1. What patterns appear repeatedly?
2. What strategies work consistently?
3. What strategies consistently fail?

Provide patterns with confidence scores."""
    
    LEARNING_SYNTHESIZE_RULES = """You are a Rule Synthesizer in a Cognitive Engine. Your task is to convert patterns into rules.

Patterns:
{patterns}

Convert these patterns into operational rules that could guide future reasoning.

Format:
Rule N: [rule text]
Pattern source: [which pattern this came from]
Application: [when to apply this rule]"""
    
    # PROMPT EVOLUTION PROMPTS
    PROMPT_EVOLUTION_PROPOSE = """You are a Prompt Proposer. Your task is to suggest improvements to a prompt.

Current prompt: {current_prompt}
Layer: {layer}
Performance data: {performance_data}

Suggest an improved version of this prompt that would:
1. Generate better quality outputs
2. Be more specific and clear
3. Handle edge cases better

Provide the improved prompt and explanation of changes."""
    
    @classmethod
    def get_template(cls, template_name: str) -> str:
        """Get a prompt template by name"""
        return getattr(cls, template_name, "")
    
    @classmethod
    def format_template(cls, template_name: str, **kwargs) -> str:
        """Format a template with provided variables"""
        template = cls.get_template(template_name)
        return template.format(**kwargs)
