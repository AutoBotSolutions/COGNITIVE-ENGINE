"""
Committer Layer

Selects best-performing thought, converts to usable output,
optionally exposes reasoning trace, stores result in memory.
"""

from typing import Optional, List

from models.state import ProblemState
from models.thought import Thought, ThoughtGraph, ThoughtStatus
from llm.client import llm_client
from llm.prompts import PromptTemplates
from utils.logger import logger
from utils.memory import memory
from core.config import config


class Committer:
    """
    Commitment Layer: Finalize + Express
    
    Selects best-performing thought and converts to usable output.
    """
    
    def __init__(self):
        self.use_llm = True
        self.expose_reasoning = True
    
    async def commit(self, thought_graph: ThoughtGraph, state: ProblemState) -> str:
        """
        Select the best thought and commit to a final output.
        
        Args:
            thought_graph: Current thought graph
            state: Current problem state
            
        Returns:
            Final output string
        """
        logger.log_layer("Committer", "starting", "Selecting best thought")
        
        # Get accepted thoughts
        accepted_thoughts = [
            t for t in thought_graph.thoughts.values()
            if t.status == ThoughtStatus.ACCEPTED
        ]
        
        if not accepted_thoughts:
            # Fall back to top-scoring thoughts
            accepted_thoughts = thought_graph.get_top_scoring_thoughts(3)
        
        if not accepted_thoughts:
            # No thoughts available, return error
            logger.log_layer("Committer", "failed", "No thoughts to commit")
            return "Unable to generate a response. No valid thoughts were generated."
        
        # Select the best thought
        best_thought = max(accepted_thoughts, key=lambda t: t.score)
        
        logger.log_layer("Committer", "selected", f"Thought {best_thought.id} with score {best_thought.score:.2f}")
        
        # Generate final output
        if self.use_llm:
            final_output = await self._llm_commit(best_thought, accepted_thoughts, state)
        else:
            final_output = best_thought.premise
        
        # Store in memory
        memory.store_episodic(
            event_type="commitment",
            data={
                "selected_thought_id": best_thought.id,
                "final_output": final_output,
                "reasoning_trace": self._build_reasoning_trace(best_thought, thought_graph) if self.expose_reasoning else None
            },
            metadata={"layer": "committer", "state_id": state.id}
        )
        
        logger.log_layer("Committer", "completed", f"Output length: {len(final_output)}")
        
        return final_output
    
    async def _llm_commit(self, best_thought: Thought, all_thoughts: List[Thought], state: ProblemState) -> str:
        """Use dynamic generation to create final output"""
        # Generate dynamic response based on the best thought and original input
        prompt = f"Original User Input: {state.source_input}\n\nBased on thought: {best_thought.premise} with goals: {', '.join(state.goals)}"
        
        # Use dynamic generation with the custom provider
        response = await llm_client.generate(prompt, mode='response')
        
        return response
    
    async def synthesize(self, thoughts: List[Thought], state: ProblemState) -> str:
        """
        Synthesize multiple thoughts into a final answer.
        
        Args:
            thoughts: Thoughts to synthesize
            state: Current problem state
            
        Returns:
            Synthesized output
        """
        logger.log_layer("Committer", "synthesizing", f"Synthesizing {len(thoughts)} thoughts")
        
        thoughts_text = "\n".join([f"- {t.premise}" for t in thoughts])
        
        prompt = PromptTemplates.format_template(
            "COMMITTER_SYNTHESIZE",
            thoughts=thoughts_text,
            goals=", ".join(state.goals)
        )
        
        response = await llm_client.generate(prompt)
        
        return response
    
    def _build_reasoning_trace(self, thought: Thought, thought_graph: ThoughtGraph) -> str:
        """Build a reasoning trace for the selected thought"""
        trace = []
        
        trace.append(f"Selected Thought: {thought.premise}")
        trace.append(f"Score: {thought.score:.2f}")
        trace.append(f"Confidence: {thought.confidence:.2f}")
        
        if thought.weaknesses:
            trace.append(f"Weaknesses: {', '.join(thought.weaknesses)}")
        
        # Get ancestors
        ancestors = thought_graph.get_ancestors(thought.id)
        if ancestors:
            trace.append("\nAncestry:")
            for ancestor in ancestors:
                trace.append(f"  - {ancestor.premise} (score: {ancestor.score:.2f})")
        
        # Get history
        if thought.history:
            trace.append("\nHistory:")
            for entry in thought.history[-5:]:  # Last 5 entries
                trace.append(f"  - {entry['event_type']}: {entry.get('details', '')}")
        
        return "\n".join(trace)
    
    def get_commitment_summary(self, thought_graph: ThoughtGraph, final_output: str) -> dict:
        """
        Get a summary of the commitment process.
        
        Args:
            thought_graph: Current thought graph
            final_output: Final output string
            
        Returns:
            Summary dictionary
        """
        accepted = len([t for t in thought_graph.thoughts.values() if t.status == ThoughtStatus.ACCEPTED])
        rejected = len([t for t in thought_graph.thoughts.values() if t.status == ThoughtStatus.REJECTED])
        
        return {
            "total_thoughts": len(thought_graph.thoughts),
            "accepted": accepted,
            "rejected": rejected,
            "output_length": len(final_output),
            "best_score": max((t.score for t in thought_graph.thoughts.values()), default=0.0)
        }
