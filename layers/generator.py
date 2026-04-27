"""
Generator Layer

Creates candidate thoughts/hypotheses instead of single answers.
Each thought is a candidate interpretation or solution path.
"""

from typing import List
import re

from models.state import ProblemState
from models.thought import Thought, ThoughtStatus
from llm.client import llm_client
from llm.prompts import PromptTemplates
from utils.logger import logger
from utils.memory import memory
from core.config import config


class Generator:
    """
    Generation Layer: Create Thought Candidates
    
    Produces multiple competing hypotheses instead of single answer.
    """
    
    def __init__(self):
        self.use_llm = True
    
    async def generate(self, state: ProblemState) -> List[Thought]:
        """
        Generate candidate thoughts based on problem state.
        
        Args:
            state: Current problem state
            
        Returns:
            List of candidate thoughts
        """
        logger.log_layer("Generator", "starting", f"State: {state.get_summary()}")
        
        if self.use_llm:
            thoughts = await self._llm_generate(state)
        else:
            thoughts = self._rule_based_generate(state)
        
        # Store in episodic memory
        for thought in thoughts:
            memory.store_episodic(
                event_type="thought_generated",
                data={"thought_id": thought.id, "premise": thought.premise},
                metadata={"layer": "generator", "state_id": state.id}
            )
        
        logger.log_layer("Generator", "completed", f"Generated {len(thoughts)} thoughts")
        
        return thoughts
    
    async def _llm_generate(self, state: ProblemState) -> List[Thought]:
        """Use LLM to generate thoughts"""
        prompt = PromptTemplates.format_template(
            "GENERATOR_MAIN",
            input=state.source_input,
            goals=", ".join(state.goals),
            constraints=", ".join(state.constraints),
            knowns=str(state.knowns),
            unknowns=", ".join(state.unknowns),
            num_thoughts=config.max_thoughts_per_generation
        )
        
        response = await llm_client.generate(prompt, mode='thought')
        
        # Parse the response into thoughts
        thoughts = self._parse_generation_response(response, state)
        
        return thoughts
    
    def _rule_based_generate(self, state: ProblemState) -> List[Thought]:
        """Rule-based generation (fallback)"""
        thoughts = []
        
        # Generate variations based on goals
        for goal in state.goals[:3]:
            thought = Thought(
                premise=f"Approach: {goal}",
                layer_source="generator",
                metadata={"generation_method": "rule_based"}
            )
            thoughts.append(thought)
        
        # Generate constraint-based thoughts
        if state.constraints:
            constraint = state.constraints[0]
            thought = Thought(
                premise=f"Alternative approach respecting: {constraint}",
                layer_source="generator",
                metadata={"generation_method": "rule_based"}
            )
            thoughts.append(thought)
        
        return thoughts[:config.max_thoughts_per_generation]
    
    def _parse_generation_response(self, response: str, state: ProblemState) -> List[Thought]:
        """Parse LLM response into Thought objects"""
        thoughts = []
        
        # Split by "Thought N:" pattern
        pattern = r'Thought\s+(\d+):\s*(.+?)(?=Thought\s+\d+:|$)'
        matches = re.findall(pattern, response, re.DOTALL)
        
        for match in matches:
            thought_num, thought_text = match
            premise = thought_text.strip().split('\n')[0]  # First line is premise
            
            thought = Thought(
                premise=premise,
                layer_source="generator",
                metadata={"llm_generated": True}
            )
            
            # Extract reasoning if present
            reasoning_match = re.search(r'Reasoning:\s*(.+?)(?=Weaknesses:|$)', thought_text, re.DOTALL)
            if reasoning_match:
                thought.metadata["reasoning"] = reasoning_match.group(1).strip()
            
            # Extract weaknesses if present
            weaknesses_match = re.search(r'Weaknesses:\s*(.+?)(?=Thought\s+\d+:|$)', thought_text, re.DOTALL)
            if weaknesses_match:
                weaknesses_text = weaknesses_match.group(1).strip()
                weaknesses = [w.strip() for w in weaknesses_text.split('\n') if w.strip()]
                for weakness in weaknesses:
                    thought.add_weakness(weakness)
            
            thoughts.append(thought)
        
        # If parsing failed, create a single thought from the whole response
        if not thoughts and response.strip():
            thought = Thought(
                premise=response.strip()[:200],
                layer_source="generator",
                metadata={"llm_generated": True, "parse_failed": True}
            )
            thoughts.append(thought)
        
        return thoughts[:config.max_thoughts_per_generation]
    
    async def refine_thought(self, thought: Thought, state: ProblemState) -> List[Thought]:
        """
        Refine a thought by addressing its weaknesses.
        
        Args:
            thought: Thought to refine
            state: Current problem state
            
        Returns:
            List of refined thoughts
        """
        logger.log_layer("Generator", "refining", f"Thought {thought.id}")
        
        prompt = PromptTemplates.format_template(
            "GENERATOR_REFINE",
            thought_premise=thought.premise,
            weaknesses=", ".join(thought.weaknesses),
            num_refinements=3
        )
        
        response = await llm_client.generate(prompt)
        
        # Parse refinements
        refinements = self._parse_refinement_response(response, thought)
        
        return refinements
    
    def _parse_refinement_response(self, response: str, parent_thought: Thought) -> List[Thought]:
        """Parse refinement response into Thought objects"""
        refinements = []
        
        pattern = r'Refinement\s+(\d+):\s*(.+?)(?=Refinement\s+\d+:|$)'
        matches = re.findall(pattern, response, re.DOTALL)
        
        for match in matches:
            refinement_num, refinement_text = match
            premise = refinement_text.strip().split('\n')[0]
            
            refined = parent_thought.revise(premise, "addressed weaknesses")
            refinements.append(refined)
        
        return refinements
