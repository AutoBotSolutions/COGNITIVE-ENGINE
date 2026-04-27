"""
Deliberator Layer

Core of cognition where thoughts are tested, critiqued, scored, and evolved.
Includes: Internal Simulation, Stress Testing, Comparative Scoring, Mutation.
"""

from typing import List, Tuple, Dict, Any
import re

from models.state import ProblemState
from models.thought import Thought, ThoughtStatus
from models.thought import ThoughtGraph
from llm.client import llm_client
from llm.prompts import PromptTemplates
from utils.scoring import ThoughtScorer
from utils.logger import logger
from utils.memory import memory
from core.config import config


class Deliberator:
    """
    Deliberation Layer: Evaluate + Evolve Thoughts
    
    Core of cognition where thoughts are tested, critiqued, scored, and evolved.
    """
    
    def __init__(self):
        self.use_llm = True
        self.scorer = ThoughtScorer()
    
    async def deliberate(self, thought_graph: ThoughtGraph, state: ProblemState) -> None:
        """
        Evaluate and evolve thoughts in the graph.
        
        Args:
            thought_graph: Current thought graph
            state: Current problem state
        """
        logger.log_layer("Deliberator", "starting", f"Thoughts to evaluate: {len(thought_graph.thoughts)}")
        
        # Get all generated thoughts
        thoughts = list(thought_graph.thoughts.values())
        
        for thought in thoughts:
            if thought.status == ThoughtStatus.GENERATED:
                await self._evaluate_thought(thought, state)
        
        # Rank thoughts by score
        ranked_thoughts = self.scorer.rank_thoughts(list(thought_graph.thoughts.values()))
        
        # Accept high-scoring thoughts first
        accepted_count = 0
        for i, thought in enumerate(ranked_thoughts):
            if thought.score >= config.score_threshold or i == 0:  # Accept if above threshold or if it's the best thought
                thought.status = ThoughtStatus.ACCEPTED
                thought.add_history_entry("accepted", {"reason": "high_score_or_best", "rank": i})
                accepted_count += 1
            elif i >= len(ranked_thoughts) // 2:  # Then reject bottom 50%
                thought.status = ThoughtStatus.REJECTED
                thought.add_history_entry("rejected", {"reason": "low_score", "rank": i})
        
        logger.log_layer("Deliberator", "completed", f"Evaluated {len(thoughts)} thoughts, accepted {accepted_count}")
    
    async def _evaluate_thought(self, thought: Thought, state: ProblemState) -> None:
        """Evaluate a single thought"""
        thought.status = ThoughtStatus.EVALUATING
        
        # Calculate base score using scoring functions
        base_score = self.scorer.score(thought, state)
        thought.update_score(base_score, "initial_evaluation")
        
        # LLM-based critique if available
        if self.use_llm:
            await self._llm_critique(thought, state)
        
        # Update confidence based on score
        confidence = min(1.0, thought.score)
        thought.update_confidence(confidence, "score_based")
        
        # Store in memory
        memory.store_episodic(
            event_type="thought_evaluated",
            data={"thought_id": thought.id, "score": thought.score, "confidence": thought.confidence},
            metadata={"layer": "deliberator"}
        )
    
    async def _llm_critique(self, thought: Thought, state: ProblemState) -> None:
        """Use LLM to critique a thought"""
        prompt = PromptTemplates.format_template(
            "DELIBERATOR_CRITIQUE",
            thought_premise=thought.premise,
            goals=", ".join(state.goals),
            constraints=", ".join(state.constraints)
        )
        
        response = await llm_client.generate(prompt)
        
        # Parse critique and update thought
        self._parse_critique_response(response, thought)
    
    def _parse_critique_response(self, response: str, thought: Thought) -> None:
        """Parse LLM critique response"""
        # Extract scores
        coherence = self._extract_score(response, "coherence")
        relevance = self._extract_score(response, "relevance")
        novelty = self._extract_score(response, "novelty")
        feasibility = self._extract_score(response, "feasibility")
        completeness = self._extract_score(response, "completeness")
        
        if coherence is not None:
            thought.metadata["llm_coherence"] = coherence
        if relevance is not None:
            thought.metadata["llm_relevance"] = relevance
        if novelty is not None:
            thought.metadata["llm_novelty"] = novelty
        if feasibility is not None:
            thought.metadata["llm_feasibility"] = feasibility
        if completeness is not None:
            thought.metadata["llm_completeness"] = completeness
        
        # Extract weaknesses mentioned in critique
        weakness_patterns = [r'weakness:\s*(.+)', r'issue:\s*(.+)', r'problem:\s*(.+)']
        for pattern in weakness_patterns:
            matches = re.findall(pattern, response, re.IGNORECASE)
            for match in matches:
                thought.add_weakness(match.strip())
    
    def _extract_score(self, text: str, criterion: str) -> float:
        """Extract a score for a specific criterion"""
        pattern = rf'{criterion}[^0-9.]*([0-9.]+)'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except:
                pass
        return None
    
    async def revise_thoughts(self, thought_graph: ThoughtGraph, state: ProblemState) -> None:
        """
        Revise thoughts with weaknesses.
        
        Args:
            thought_graph: Current thought graph
            state: Current problem state
        """
        from layers.generator import Generator
        
        logger.log_layer("Deliberator", "revising", "Revising thoughts with weaknesses")
        
        generator = Generator()
        
        # Get thoughts with weaknesses
        thoughts_with_weaknesses = [
            t for t in thought_graph.thoughts.values()
            if t.weaknesses and t.status == ThoughtStatus.ACCEPTED
        ]
        
        refinements = []
        for thought in thoughts_with_weaknesses[:2]:  # Limit revisions
            thought_refinements = await generator.refine_thought(thought, state)
            refinements.extend(thought_refinements)
            for refinement in thought_refinements:
                thought_graph.add_thought(refinement)
                # Evaluate the refinement
                await self._evaluate_thought(refinement, state)
        
        logger.log_layer("Deliberator", "revision_complete", f"Created {len(refinements)} refinements")
    
    async def simulate_thought(self, thought: Thought, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate the outcome of a thought.
        
        Args:
            thought: Thought to simulate
            context: Current context
            
        Returns:
            Simulation results
        """
        prompt = PromptTemplates.format_template(
            "DELIBERATOR_SIMULATE",
            thought_premise=thought.premise,
            context=str(context)
        )
        
        response = await llm_client.generate(prompt)
        
        thought.metadata["simulation"] = response
        
        return {"simulation": response}
    
    async def compare_thoughts(self, thought_a: Thought, thought_b: Thought, state: ProblemState) -> Tuple[Thought, str]:
        """
        Compare two thoughts and select the better one.
        
        Args:
            thought_a: First thought
            thought_b: Second thought
            state: Current problem state
            
        Returns:
            Tuple of (better_thought, reasoning)
        """
        prompt = PromptTemplates.format_template(
            "DELIBERATOR_COMPARE",
            thought_a=thought_a.premise,
            thought_b=thought_b.premise
        )
        
        response = await llm_client.generate(prompt)
        
        # Simple heuristic: if response mentions "A" more positively, choose A
        if "thought a" in response.lower() and ("better" in response.lower() or "prefer" in response.lower()):
            return thought_a, response
        else:
            return thought_b, response
