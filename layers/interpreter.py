"""
Interpreter Layer

Transforms raw input into structured state: goals, constraints, knowns, unknowns.
Defines the problem space with clarity.
"""

import re
from typing import Dict, Any
import json

from models.state import ProblemState
from llm.client import llm_client
from llm.prompts import PromptTemplates
from utils.logger import logger
from utils.memory import memory


class Interpreter:
    """
    Interpretation Layer: Input → Structured Meaning
    
    Transforms raw input into structured state representation.
    """
    
    def __init__(self):
        self.use_llm = True
    
    async def interpret(self, input_text: str) -> ProblemState:
        """
        Interpret raw input into a structured ProblemState.
        
        Args:
            input_text: Raw input string
            
        Returns:
            ProblemState with structured representation
        """
        logger.log_layer("Interpreter", "starting", f"Input: {input_text[:100]}...")
        
        state = ProblemState(source_input=input_text)
        
        if self.use_llm:
            state = await self._llm_interpret(input_text, state)
        else:
            state = self._rule_based_interpret(input_text, state)
        
        # Store in episodic memory
        memory.store_episodic(
            event_type="interpretation",
            data={"input": input_text, "state": state.to_dict()},
            metadata={"layer": "interpreter"}
        )
        
        logger.log_layer("Interpreter", "completed", f"Clarity: {state.clarity_score:.2f}, Completeness: {state.completeness_score:.2f}")
        
        return state
    
    async def _llm_interpret(self, input_text: str, state: ProblemState) -> ProblemState:
        """Use LLM to interpret input"""
        prompt = PromptTemplates.format_template(
            "INTERPRETER_MAIN",
            input=input_text
        )
        
        response = await llm_client.generate(prompt)
        
        # Parse the response
        state = self._parse_interpretation_response(response, state)
        
        # If parsing failed to set scores, use rule-based as fallback
        if state.clarity_score == 0.0 and state.completeness_score == 0.0:
            state = self._rule_based_interpret(input_text, state)
        
        return state
    
    def _rule_based_interpret(self, input_text: str, state: ProblemState) -> ProblemState:
        """Rule-based interpretation (fallback)"""
        # Extract goals (questions, requests)
        if '?' in input_text:
            state.add_goal(input_text.split('?')[0] + '?')
        else:
            state.add_goal(input_text)
        
        # Extract constraints (words like "without", "except", "not")
        constraint_patterns = [r'without (.+)', r'except (.+)', r'not (.+)', r'must (.+)']
        for pattern in constraint_patterns:
            matches = re.findall(pattern, input_text, re.IGNORECASE)
            for match in matches:
                state.add_constraint(match.strip())
        
        # Extract knowns (statements with "is", "are")
        known_patterns = [r'(.+) is (.+)', r'(.+) are (.+)']
        for pattern in known_patterns:
            matches = re.findall(pattern, input_text, re.IGNORECASE)
            for match in matches:
                state.add_known(match[0].strip(), match[1].strip())
        
        # Set default scores
        state.clarity_score = 0.6
        state.completeness_score = 0.5
        
        state.intent = "general inquiry"
        
        return state
    
    def _parse_interpretation_response(self, response: str, state: ProblemState) -> ProblemState:
        """Parse LLM response into ProblemState"""
        # Extract goals
        goals = self._extract_section(response, "Goals")
        for goal in goals:
            state.add_goal(goal)
        
        # Extract constraints
        constraints = self._extract_section(response, "Constraints")
        for constraint in constraints:
            state.add_constraint(constraint)
        
        # Extract knowns
        knowns_text = self._extract_section_text(response, "Knowns")
        if knowns_text:
            try:
                knowns_dict = self._parse_dict(knowns_text)
                for key, value in knowns_dict.items():
                    state.add_known(key, value)
            except:
                pass
        
        # Extract unknowns
        unknowns = self._extract_section(response, "Unknowns")
        for unknown in unknowns:
            state.add_unknown(unknown)
        
        # Extract intent
        intent = self._extract_section_text(response, "Intent")
        if intent:
            state.intent = intent
        
        # Extract scores
        clarity = self._extract_number(response, "Clarity score")
        if clarity is not None:
            state.clarity_score = clarity
        
        completeness = self._extract_number(response, "Completeness score")
        if completeness is not None:
            state.completeness_score = completeness
        
        return state
    
    def _extract_section(self, text: str, section_name: str) -> list:
        """Extract a list section from the response"""
        pattern = rf'{section_name}:\s*(.+?)(?=\n(?:[A-Z][a-z]+:|$))'
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
        if matches:
            items = [item.strip() for item in matches[0].split('\n') if item.strip()]
            # Remove bullet points
            items = [re.sub(r'^[-•]\s*', '', item) for item in items]
            return items
        return []
    
    def _extract_section_text(self, text: str, section_name: str) -> str:
        """Extract a text section from the response"""
        pattern = rf'{section_name}:\s*(.+?)(?=\n[A-Z][a-z]+:|$)'
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return ""
    
    def _extract_number(self, text: str, label: str) -> float:
        """Extract a number from text"""
        pattern = rf'{label}\s*\(([\d.]+)\)'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except:
                pass
        return None
    
    def _parse_dict(self, text: str) -> Dict[str, Any]:
        """Parse a dictionary from text"""
        try:
            # Try JSON parsing first
            if text.strip().startswith('{'):
                return json.loads(text)
            
            # Try key: value parsing
            result = {}
            for line in text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    result[key.strip()] = value.strip()
            return result
        except:
            return {}
