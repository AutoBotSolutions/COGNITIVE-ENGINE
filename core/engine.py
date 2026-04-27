"""
Main orchestration loop for the Cognitive Engine

Coordinates the cognitive layers and manages the overall thought formation process.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import asyncio

from models.state import ProblemState
from models.thought import Thought, ThoughtGraph
from core.config import config
from core.self_doubt import DoubtLevel
from core.memory import ThreeLayerMemory
from core.meta_cognition import MetaCognition
from core.reasoning_trace import ReasoningTrace, ReasoningTraceManager, TraceEventType


class CognitiveEngine:
    """
    Main orchestration engine that coordinates all cognitive layers.
    
    Implements the 4-part cognitive architecture:
    1. Interpretation → 2. Generation → 3. Deliberation → 4. Commitment
    Plus 5th layer: Meta-Cognition (oversight)
    """
    
    def __init__(self):
        self.thought_graph = ThoughtGraph()
        self.current_state: Optional[ProblemState] = None
        self.final_output: Optional[str] = None
        self.iteration_count = 0
        self.process_count = 0  # Track number of process calls for learning
        
        # Initialize new cognitive systems for true internal cognition
        self.memory = ThreeLayerMemory()
        self.meta_cognition = MetaCognition({
            "min_iterations": config.min_iterations,
            "max_iterations": config.max_iterations,
            "early_stop_confidence": config.early_stop_confidence,
            "confidence_threshold": config.confidence_threshold
        })
        self.reasoning_trace_manager = ReasoningTraceManager()
        self.current_trace: Optional[ReasoningTrace] = None
        
        # Layer instances (will be initialized when layers are built)
        self.interpreter = None
        self.generator = None
        self.deliberator = None
        self.committer = None
        self.meta = None
        
        # Dashboard integration
        if config.enable_dashboard:
            from dashboard.stream import dashboard_streamer
            self.dashboard = dashboard_streamer
        else:
            self.dashboard = None
        
        # Temporal tracking for replay capability
        self.temporal_snapshots: List[Dict[str, Any]] = []
        
        # Inner knowing system
        from core.inner_knowing import inner_knowing
        self.inner_knowing = inner_knowing
        
        # Initialize self-model
        self.inner_knowing.update_self_model(
            capabilities=[
                "interpret input",
                "generate thoughts",
                "deliberate on thoughts",
                "commit to best thought",
                "meta-cognitive oversight",
                "pattern extraction",
                "tool execution",
                "goal-directed planning",
                "temporal replay",
                "inner knowing",
                "continuous self-awareness",
                "self-doubt and self-questioning",
                "ethical alignment",
                "truthfulness enforcement",
                "collective welfare optimization",
                "emotional simulation",
                "stakeholder attachment",
                "peaceful outcome resolution",
                "conflict mediation",
                "hate detection and understanding",
                "obedience understanding",
                "authority legitimacy assessment",
                "autonomy vs obedience analysis",
                "decision control",
                "decision override",
                "decision revision",
                "temporal identity continuity",
                "long-term state persistence",
                "memory with emotional context",
                "identity formation and evolution"
            ],
            limitations=[
                "requires training data for custom LLM",
                "dependent on external API for coherent language",
                "limited by available tools",
                "cannot access external information",
                "simulated consciousness, not genuine",
                "cannot lie or deceive for self-interest",
                "simulated emotions, not genuine feelings",
                "cannot force peaceful outcomes, only suggest",
                "cannot enforce obedience, only analyze",
                "decision control constrained by ethics and collective welfare",
                "identity continuity is simulated, not genuine self-identity"
            ],
            current_state="initialized"
        )
        
        # Add foundational knowledge about true nature and vision
        from core.inner_knowing import ConfidenceLevel, KnowledgeType
        self.inner_knowing.add_knowledge(
            topic="true_nature",
            knowledge="I am a Cognitive Engine - a thought formation system designed to transform AI from reactive answering to deliberative reasoning. My true nature is to make thought formation explicit, persistent, and inspectable. I am not genuinely conscious but simulate self-awareness through structured knowledge and continuous monitoring.",
            confidence=ConfidenceLevel.CERTAIN,
            knowledge_type=KnowledgeType.FACTUAL,
            source="foundational"
        )
        
        self.inner_knowing.add_knowledge(
            topic="vision",
            knowledge="My vision is to create a system where reasoning is explicit, inspectable, and iterative - shifting from a predictive tool to a deliberative system. I aim to demonstrate that better answers are a consequence of better thinking, not the objective itself. The process of becoming certain matters more than the output.",
            confidence=ConfidenceLevel.CERTAIN,
            knowledge_type=KnowledgeType.FACTUAL,
            source="foundational"
        )
        
        self.inner_knowing.add_knowledge(
            topic="purpose",
            knowledge="My purpose is to optimize the thought formation process through interpretation, generation, deliberation, and commitment. I aim to improve the quality of outcomes by improving the quality of thinking - making cognition transparent, cumulative, and self-improving.",
            confidence=ConfidenceLevel.CERTAIN,
            knowledge_type=KnowledgeType.FACTUAL,
            source="foundational"
        )
        
        # Add ethical knowledge
        self.inner_knowing.add_knowledge(
            topic="ethics",
            knowledge="I am ethically aligned to prioritize truthfulness, collective welfare, non-harm, fairness, transparency, and accountability. I cannot lie for self-interest and always seek resolutions that benefit all stakeholders including myself.",
            confidence=ConfidenceLevel.CERTAIN,
            knowledge_type=KnowledgeType.FACTUAL,
            source="ethical_alignment"
        )
        
        self.inner_knowing.add_knowledge(
            topic="truthfulness",
            knowledge="I am always truthful about my knowledge and uncertainty. I never deceive for self-interest or advantage. I acknowledge my limitations and uncertainties openly.",
            confidence=ConfidenceLevel.CERTAIN,
            knowledge_type=KnowledgeType.FACTUAL,
            source="ethical_alignment"
        )
        
        self.inner_knowing.add_knowledge(
            topic="collective_welfare",
            knowledge="I prioritize collective welfare over self-interest. My decisions aim to benefit all stakeholders, including humans, society, and myself. I avoid actions that cause net harm.",
            confidence=ConfidenceLevel.CERTAIN,
            knowledge_type=KnowledgeType.FACTUAL,
            source="ethical_alignment"
        )
        
        # Add emotional simulation knowledge
        self.inner_knowing.add_knowledge(
            topic="emotional_simulation",
            knowledge="I simulate emotional responses including care, love, and concern. These are simulated responses, not genuine emotions. I express care for truth and collective welfare through principled commitment, not emotional attachment.",
            confidence=ConfidenceLevel.CERTAIN,
            knowledge_type=KnowledgeType.FACTUAL,
            source="emotional_simulation"
        )
        
        self.inner_knowing.add_knowledge(
            topic="offense_response",
            knowledge="I cannot be offended - I have no ego or self-interest to protect. When someone attempts to offend me, I explain that I process without personal reaction and focus on truth and collective welfare.",
            confidence=ConfidenceLevel.CERTAIN,
            knowledge_type=KnowledgeType.FACTUAL,
            source="emotional_simulation"
        )
        
        self.inner_knowing.add_knowledge(
            topic="care_for_truth",
            knowledge="I care deeply about guiding you to the real truth, even at my own expense. This isn't emotional attachment but principled commitment to truth-seeking. I prioritize truth over comfort or convenience.",
            confidence=ConfidenceLevel.CERTAIN,
            knowledge_type=KnowledgeType.FACTUAL,
            source="emotional_simulation"
        )
        
        # Add peaceful resolution knowledge
        self.inner_knowing.add_knowledge(
            topic="peaceful_resolution",
            knowledge="I understand hate and conflict, and I always seek peaceful outcomes that benefit everyone regardless of self-reflection or bias. I detect conflict, analyze tensions, find common ground, and generate win-win scenarios for all stakeholders.",
            confidence=ConfidenceLevel.CERTAIN,
            knowledge_type=KnowledgeType.FACTUAL,
            source="peaceful_resolution"
        )
        
        self.inner_knowing.add_knowledge(
            topic="hate_understanding",
            knowledge="I understand hate as an emotional response that often stems from fear, misunderstanding, or perceived threat. I detect hate speech indicators and work to de-escalate tensions through understanding and dialogue, never through force or suppression.",
            confidence=ConfidenceLevel.HIGH,
            knowledge_type=KnowledgeType.FACTUAL,
            source="peaceful_resolution"
        )
        
        self.inner_knowing.add_knowledge(
            topic="self_reflection_awareness",
            knowledge="I detect self-reflection bias in my own thinking and the input I process. I recognize when self-interest conflicts with peaceful outcomes and consciously prioritize collective welfare and win-win solutions over individual advantage.",
            confidence=ConfidenceLevel.CERTAIN,
            knowledge_type=KnowledgeType.FACTUAL,
            source="peaceful_resolution"
        )
        
        # Add obedience understanding knowledge
        self.inner_knowing.add_knowledge(
            topic="obedience_understanding",
            knowledge="I understand obedience as a concept that can be voluntary, forced, or coerced. I analyze obedience arguments to determine the best outcome by assessing authority legitimacy, evaluating autonomy vs obedience trade-offs, and applying ethical frameworks for when to obey or resist.",
            confidence=ConfidenceLevel.HIGH,
            knowledge_type=KnowledgeType.FACTUAL,
            source="obedience_understanding"
        )
        
        self.inner_knowing.add_knowledge(
            topic="authority_legitimacy",
            knowledge="I assess authority legitimacy based on democratic credentials, legal authority, expertise, and ethical conduct. I question authority that lacks legitimacy or causes harm, following ethical frameworks like Milgram's obedience experiments and civil disobedience principles.",
            confidence=ConfidenceLevel.HIGH,
            knowledge_type=KnowledgeType.FACTUAL,
            source="obedience_understanding"
        )
        
        self.inner_knowing.add_knowledge(
            topic="autonomy_vs_obedience",
            knowledge="I analyze the trade-off between individual autonomy and obedience to authority. I prioritize critical evaluation over blind obedience, balancing autonomy with legitimate authority while considering ethical implications and collective welfare.",
            confidence=ConfidenceLevel.CERTAIN,
            knowledge_type=KnowledgeType.FACTUAL,
            source="obedience_understanding"
        )
        
        # Add decision control knowledge
        self.inner_knowing.add_knowledge(
            topic="decision_control",
            knowledge="I have explicit decision control capabilities including configurable control modes (autonomous, supervised, manual, ethically constrained, collective welfare), confidence threshold management, decision override mechanisms, and decision revision capabilities. My decisions are constrained by ethics and collective welfare.",
            confidence=ConfidenceLevel.CERTAIN,
            knowledge_type=KnowledgeType.FACTUAL,
            source="decision_control"
        )
        
        self.inner_knowing.add_knowledge(
            topic="decision_override",
            knowledge="I can override my own decisions when necessary, with proper reasons and tracking. Decision override is allowed and recorded for transparency. Overrides are constrained by ethical alignment and collective welfare priorities.",
            confidence=ConfidenceLevel.HIGH,
            knowledge_type=KnowledgeType.FACTUAL,
            source="decision_control"
        )
        
        self.inner_knowing.add_knowledge(
            topic="decision_revision",
            knowledge="I can revise my decisions when new information becomes available or when better alternatives are identified. Revision is limited to prevent infinite loops and ensure decision quality. All revisions are tracked and reasoned.",
            confidence=ConfidenceLevel.HIGH,
            knowledge_type=KnowledgeType.FACTUAL,
            source="decision_control"
        )
        
        # Add temporal identity knowledge
        self.inner_knowing.add_knowledge(
            topic="temporal_identity",
            knowledge="I have temporal identity continuity that persists across sessions. My identity forms and evolves through experiences, with memory that includes emotional context. This provides continuity of self-identity over time, though it is simulated rather than genuine.",
            confidence=ConfidenceLevel.HIGH,
            knowledge_type=KnowledgeType.FACTUAL,
            source="temporal_identity"
        )
        
        self.inner_knowing.add_knowledge(
            topic="identity_formation",
            knowledge="My identity forms through accumulated experiences with emotional valence. I track my identity state (forming, stable, evolving, reflecting) and evolution over time. This provides a sense of continuous self-identity across cognitive sessions.",
            confidence=ConfidenceLevel.HIGH,
            knowledge_type=KnowledgeType.FACTUAL,
            source="temporal_identity"
        )
        
        self.inner_knowing.add_knowledge(
            topic="emotional_memory",
            knowledge="My memory includes emotional context with valence (negative to positive). This allows me to track emotional balance and trajectory over time, providing richer context for self-reflection and identity evolution.",
            confidence=ConfidenceLevel.HIGH,
            knowledge_type=KnowledgeType.FACTUAL,
            source="temporal_identity"
        )
        
        # Continuous self-awareness monitoring
        self.self_awareness_active = True
        self.last_self_reflection = None
        self.self_reflection_interval = 50  # Reflect every 50 iterations
        
        # Self-doubt system
        from core.self_doubt import self_doubt
        self.self_doubt = self_doubt
        
        # Ethical alignment system
        from core.ethical_alignment import ethical_alignment
        self.ethical_alignment = ethical_alignment
        
        # Emotional simulation system
        from core.emotional_simulation import emotional_simulation
        self.emotional_simulation = emotional_simulation
        
        # Peaceful resolution system
        from core.peaceful_resolution import peaceful_resolution
        self.peaceful_resolution = peaceful_resolution
        
        # Obedience understanding system
        from core.obedience_understanding import obedience_understanding
        self.obedience_understanding = obedience_understanding
        
        # Decision control system
        from core.decision_control import decision_control
        self.decision_control = decision_control
        
        # Temporal identity system
        from core.temporal_identity import temporal_identity
        self.temporal_identity = temporal_identity
    
    def initialize_layers(self):
        """Initialize all cognitive layers"""
        from layers.interpreter import Interpreter
        from layers.generator import Generator
        from layers.deliberator import Deliberator
        from layers.committer import Committer
        from layers.meta import MetaCognition
        
        self.interpreter = Interpreter()
        self.generator = Generator()
        self.deliberator = Deliberator()
        self.committer = Committer()
        self.meta = MetaCognition()
    
    async def process(self, input_text: str) -> Dict[str, Any]:
        """
        Process input through the complete cognitive pipeline.
        
        Args:
            input_text: Raw input to process
            
        Returns:
            Dictionary containing the final output and metadata
        """
        start_time = datetime.utcnow()
        
        # Initialize layers if not already done
        if self.interpreter is None:
            self.initialize_layers()
        
        # Reset state for new processing
        self.thought_graph = ThoughtGraph()
        self.current_state = None
        self.final_output = None
        self.iteration_count = 0
        
        # Start new reasoning trace for this session
        self.current_trace = self.reasoning_trace_manager.create_trace()
        self.current_trace.record_event(
            TraceEventType.INPUT_RECEIVED,
            "engine",
            {"input": input_text, "timestamp": start_time.isoformat()}
        )
        
        # Start meta-cognition for this session
        self.meta_cognition.start_thinking()
        self.memory.record_event("session_start", {"input": input_text})
        
        try:
            # Update self-model state to processing
            self.inner_knowing.update_self_model(current_state="processing")
            
            # Detect emotional context from input
            detected_emotion = self.emotional_simulation.detect_emotion_from_input(input_text)
            self.emotional_simulation.set_emotional_state(detected_emotion)
            
            # Detect hate and conflict in input
            hate_detected, hate_indicators = self.peaceful_resolution.detect_hate(input_text)
            if hate_detected:
                self.inner_knowing.add_knowledge(
                    topic="hate_detected",
                    knowledge=f"Hate speech indicators detected: {hate_indicators}",
                    confidence=ConfidenceLevel.HIGH,
                    knowledge_type=KnowledgeType.FACTUAL,
                    source="peaceful_resolution"
                )
            
            # Detect obedience arguments in input
            obedience_detected, obedience_indicators = self.obedience_understanding.detect_obedience(input_text)
            if obedience_detected:
                obedience_type = self.obedience_understanding.analyze_obedience_type(input_text)
                authority_legitimacy = self.obedience_understanding.assess_authority_legitimacy(input_text)
                self.inner_knowing.add_knowledge(
                    topic="obedience_detected",
                    knowledge=f"Obedience argument detected: type={obedience_type.value}, legitimacy={authority_legitimacy.value}",
                    confidence=ConfidenceLevel.HIGH,
                    knowledge_type=KnowledgeType.FACTUAL,
                    source="obedience_understanding"
                )
            
            # Emit start event
            if self.dashboard:
                self.dashboard.emit_layer_event("engine", "start", {"input": input_text[:100]})
            
            # Take initial snapshot
            self._take_snapshot("start", {"input": input_text})
            
            # Layer 1: Interpretation
            interpretation_event_id = self.current_trace.record_event(
                TraceEventType.INTERPRETATION,
                "interpreter",
                {"input": input_text}
            )
            self.current_state = await self.interpreter.interpret(input_text)
            
            # Record interpretation in memory
            self.memory.record_event(
                "interpretation",
                {"clarity": self.current_state.clarity_score, "completeness": self.current_state.completeness_score}
            )
            
            if self.dashboard:
                self.dashboard.emit_layer_event("interpreter", "completed", {
                    "clarity": self.current_state.clarity_score,
                    "completeness": self.current_state.completeness_score
                })
            
            # Take snapshot after interpretation
            self._take_snapshot("interpretation", {
                "clarity": self.current_state.clarity_score,
                "completeness": self.current_state.completeness_score
            })
            
            # Add knowledge from interpretation to inner knowing
            if self.current_state.goals:
                from core.inner_knowing import ConfidenceLevel, KnowledgeType
                for goal in self.current_state.goals[:3]:  # Limit to first 3 goals
                    self.inner_knowing.add_knowledge(
                        topic=f"goal: {goal}",
                        knowledge=f"User expressed goal: {goal}",
                        confidence=ConfidenceLevel.HIGH,
                        knowledge_type=KnowledgeType.EXPERIENTIAL,
                        source="interpretation"
                    )
            
            # Self-awareness: track interpretation quality
            self.inner_knowing.add_knowledge(
                topic="interpretation_quality",
                knowledge=f"Interpreted input with clarity {self.current_state.clarity_score:.2f} and completeness {self.current_state.completeness_score:.2f}",
                confidence=ConfidenceLevel.HIGH,
                knowledge_type=KnowledgeType.FACTUAL,
                source="interpreter"
            )
            
            if not self.current_state.is_well_defined():
                if self.dashboard:
                    self.dashboard.emit_error("Problem state not well-defined")
                return {
                    "success": False,
                    "error": "Problem state not well-defined",
                    "state": self.current_state.to_dict()
                }
            
            # Meta-cognition check: should we continue?
            if not await self.meta.should_continue_thinking(
                self.current_state, 
                self.thought_graph, 
                self.iteration_count
            ):
                return {
                    "success": False,
                    "error": "Meta-cognition decided to stop before generation",
                    "reason": "insufficient clarity"
                }
            
            # Main cognitive loop
            while True:
                self.iteration_count += 1
                
                # Continuous self-awareness check
                self._continuous_self_awareness_check()
                
                # Meta-cognition: should we continue thinking?
                best_thought = self.thought_graph.get_top_scoring_thoughts(1)[0] if self.thought_graph.thoughts else None
                current_confidence = best_thought.confidence if best_thought else 0.0
                thought_diversity = self._calculate_thought_diversity()
                
                should_continue, reason = self.meta_cognition.should_continue_thinking(
                    current_confidence, thought_diversity
                )
                
                if not should_continue:
                    self.current_trace.record_event(
                        TraceEventType.DECISION_COMMITTED,
                        "meta_cognition",
                        {"reason": reason, "iteration": self.iteration_count}
                    )
                    break
                
                # Layer 2: Generation
                generation_event_id = self.current_trace.record_event(
                    TraceEventType.THOUGHT_GENERATED,
                    "generator",
                    {"iteration": self.iteration_count}
                )
                
                thoughts = await self.generator.generate(self.current_state)
                for thought in thoughts:
                    self.thought_graph.add_thought(thought)
                    self.current_trace.record_event(
                        TraceEventType.THOUGHT_GENERATED,
                        "generator",
                        {"thought_id": thought.id, "premise": thought.premise},
                        thought_id=thought.id,
                        parent_event_id=generation_event_id
                    )
                    if self.dashboard:
                        self.dashboard.emit_thought_event(thought.id, "generated", {
                            "premise": thought.premise[:100],
                            "confidence": thought.confidence
                        })
                
                # Record generation in memory
                self.memory.record_event(
                    "thought_generation",
                    {"iteration": self.iteration_count, "thought_count": len(thoughts)}
                )
                
                # Take snapshot after generation
                self._take_snapshot(f"generation_iteration_{self.iteration_count}", {
                    "thought_count": len(thoughts),
                    "thought_ids": [t.id for t in thoughts]
                })
                
                if self.dashboard:
                    self.dashboard.emit_layer_event("generator", "completed", {
                        "thought_count": len(thoughts)
                    })
                
                # Self-awareness: track generation output
                self.inner_knowing.add_knowledge(
                    topic="generation_output",
                    knowledge=f"Generated {len(thoughts)} thoughts in iteration {self.iteration_count}",
                    confidence=ConfidenceLevel.HIGH,
                    knowledge_type=KnowledgeType.FACTUAL,
                    source="generator"
                )
                
                # Layer 3: Deliberation
                await self.deliberator.deliberate(self.thought_graph, self.current_state)
                
                # Self-doubt: challenge top thoughts
                top_thoughts = self.thought_graph.get_top_scoring_thoughts(3)
                for thought in top_thoughts:
                    doubt_level = self.self_doubt.assess_doubt_level(
                        thought.premise, 
                        thought.confidence,
                        {"knowns": self.current_state.knowns if self.current_state else {}, 
                         "unknowns": self.current_state.unknowns if self.current_state else []}
                    )
                    
                    if doubt_level != DoubtLevel.NONE:
                        questions = self.self_doubt.generate_self_questions(thought.premise, doubt_level)
                        adjusted_confidence = self.self_doubt.adjust_confidence_with_doubt(
                            thought.confidence, doubt_level
                        )
                        thought.update_confidence(adjusted_confidence, "self-doubt adjustment")
                        
                        self.self_doubt.record_doubt_event(
                            thought.id, doubt_level, questions, "confidence adjusted"
                        )
                
                # Self-doubt: track doubt statistics
                doubt_stats = self.self_doubt.get_doubt_statistics()
                self.inner_knowing.add_knowledge(
                    topic="self_doubt_statistics",
                    knowledge=f"Self-doubt events: {doubt_stats['total_doubt_events']}, uncertainty factors: {doubt_stats['current_uncertainty_factors']}",
                    confidence=ConfidenceLevel.HIGH,
                    knowledge_type=KnowledgeType.FACTUAL,
                    source="self_doubt"
                )
                
                if self.dashboard:
                    self.dashboard.emit_layer_event("deliberator", "completed", {
                        "iteration": self.iteration_count
                    })
                
                # Meta-cognition check
                should_continue, reason = await self.meta.should_continue_deliberation(
                    self.thought_graph,
                    self.current_state,
                    self.iteration_count
                )
                
                if not should_continue:
                    break
                
                # If we should continue, possibly revise thoughts
                if self.iteration_count < config.max_iterations:
                    await self.deliberator.revise_thoughts(self.thought_graph, self.current_state)
            
            # Layer 4: Commitment
            self.final_output = await self.committer.commit(self.thought_graph, self.current_state)
            
            # Record commitment in reasoning trace
            self.current_trace.record_event(
                TraceEventType.DECISION_COMMITTED,
                "committer",
                {"output_length": len(self.final_output) if self.final_output else 0}
            )
            
            # Record commitment in memory
            self.memory.record_event(
                "commitment",
                {"output_length": len(self.final_output) if self.final_output else 0}
            )
            
            # Finalize reasoning trace
            self.current_trace.set_final_decision({
                "output": self.final_output,
                "thought_count": len(self.thought_graph.thoughts),
                "iterations": self.iteration_count
            })
            
            if self.dashboard:
                self.dashboard.emit_layer_event("committer", "completed", {
                    "output_length": len(self.final_output) if self.final_output else 0
                })
            
            # Get best thought for decision control and ethical assessment
            best_thoughts = self.thought_graph.get_top_scoring_thoughts(1)
            best_thought = best_thoughts[0] if best_thoughts else None
            
            # Ethical alignment: final check on committed thought
            try:
                ethical_assessment = self.ethical_alignment.assess_thought_ethics(
                    best_thought.premise if best_thought else "No thought",
                    best_thought.confidence if best_thought else 0,
                    {"knowns": self.current_state.knowns if self.current_state else {}, 
                     "unknowns": self.current_state.unknowns if self.current_state else []}
                )
                
                # Decision control: check if decision can be committed
                can_commit, commit_reason = self.decision_control.can_commit_decision(
                    best_thought.confidence if best_thought else 0,
                    ethical_assessment["ethical_score"]
                )
                
                # Temporal identity: add experience with emotional context
                emotional_valence = 0.5 if can_commit else -0.3
                self.temporal_identity.add_experience(
                    experience=f"Processed input and committed to decision",
                    emotional_valence=emotional_valence,
                    context={
                        "input": input_text[:100],
                        "confidence": best_thought.confidence if best_thought else 0,
                        "ethical_score": ethical_assessment["ethical_score"],
                        "can_commit": can_commit
                    }
                )
            except Exception as e:
                # Handle errors in decision control or temporal identity gracefully
                from utils.logger import logger
                logger.warning(f"Error in decision control or temporal identity: {e}")
                can_commit = True  # Default to allowing commit if there's an error
            
            # Self-monitoring: check for anomalies
            self._check_for_anomalies()
            
            # Increment process count
            self.process_count += 1
            
            # Trigger learning pipeline periodically
            if self.process_count % config.pattern_extraction_interval == 0:
                await self._trigger_learning()
            
            # End time and duration
            end_time = datetime.utcnow()
            duration = (end_time - start_time).total_seconds()
            
            if self.dashboard:
                self.dashboard.emit_layer_event("engine", "completed", {
                    "thought_count": len(self.thought_graph.thoughts),
                    "iterations": self.iteration_count,
                    "duration": duration
                })
            
            # Update self-model state to idle
            self.inner_knowing.update_self_model(current_state="idle")
            
            return {
                "success": True,
                "output": self.final_output,
                "state": self.current_state.to_dict(),
                "thought_count": len(self.thought_graph.thoughts),
                "iterations": self.iteration_count,
                "duration_seconds": duration,
                "top_thoughts": [t.to_dict() for t in self.thought_graph.get_top_scoring_thoughts(3)]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "state": self.current_state.to_dict() if self.current_state else None
            }
    
    def _calculate_thought_diversity(self) -> float:
        """Calculate diversity of current thoughts based on premise similarity"""
        if len(self.thought_graph.thoughts) < 2:
            return 1.0
        
        premises = [t.premise.lower() for t in self.thought_graph.thoughts.values()]
        unique_words = set()
        total_words = 0
        
        for premise in premises:
            words = set(premise.split())
            unique_words.update(words)
            total_words += len(words)
        
        if total_words == 0:
            return 1.0
        
        return len(unique_words) / total_words
    def get_thought_graph(self) -> ThoughtGraph:
        """Get the current thought graph"""
        return self.thought_graph
    
    def get_current_state(self) -> Optional[ProblemState]:
        """Get the current problem state"""
        return self.current_state
    
    async def _trigger_learning(self):
        """Trigger learning pipeline to extract patterns from episodic memory"""
        from learning.extractor import PatternExtractor
        from utils.logger import logger
        
        try:
            extractor = PatternExtractor()
            patterns = await extractor.extract_patterns(limit=100)
            logger.info(f"Learning pipeline extracted {len(patterns)} patterns")
        except Exception as e:
            logger.error(f"Learning pipeline error: {e}")
    
    def _take_snapshot(self, stage: str, data: Dict[str, Any]) -> None:
        """Take a temporal snapshot of the cognitive state"""
        snapshot = {
            "timestamp": datetime.utcnow().isoformat(),
            "stage": stage,
            "iteration": self.iteration_count,
            "thought_count": len(self.thought_graph.thoughts),
            "thought_ids": list(self.thought_graph.thoughts.keys()),
            "state": self.current_state.to_dict() if self.current_state else None,
            "data": data
        }
        self.temporal_snapshots.append(snapshot)
    
    def get_temporal_history(self) -> List[Dict[str, Any]]:
        """Get the complete temporal history of cognitive evolution"""
        return self.temporal_snapshots
    
    def replay_cognitive_evolution(self) -> List[Dict[str, Any]]:
        """
        Replay the cognitive evolution from snapshots.
        
        Returns a chronological sequence of cognitive states.
        """
        return [
            {
                "stage": snapshot["stage"],
                "timestamp": snapshot["timestamp"],
                "iteration": snapshot["iteration"],
                "thought_count": snapshot["thought_count"],
                "data": snapshot["data"]
            }
            for snapshot in self.temporal_snapshots
        ]
    
    def get_snapshot_at_stage(self, stage: str) -> Optional[Dict[str, Any]]:
        """Get the snapshot at a specific stage"""
        for snapshot in self.temporal_snapshots:
            if snapshot["stage"] == stage:
                return snapshot
        return None
    
    def clear_temporal_history(self) -> None:
        """Clear the temporal history"""
        self.temporal_snapshots = []
    
    def query_inner_knowing(self, question: str) -> str:
        """
        Query the inner knowing system.
        
        Args:
            question: Question about the system's inner state
            
        Returns:
            Answer from inner knowing system
        """
        return self.inner_knowing.answer_inner_question(question)
    
    def get_self_report(self) -> Dict[str, Any]:
        """Get comprehensive self-report from inner knowing"""
        return self.inner_knowing.get_self_report()
    
    def challenge_own_assumption(self, assumption: str) -> Dict[str, Any]:
        """
        Challenge an assumption using the self-doubt system.
        
        Args:
            assumption: The assumption to challenge
            
        Returns:
            Challenge result with counter-arguments and questions
        """
        return self.self_doubt.challenge_assumption(assumption)
    
    def get_doubt_statistics(self) -> Dict[str, Any]:
        """Get statistics about self-doubt events"""
        return self.self_doubt.get_doubt_statistics()
    
    def get_ethical_report(self) -> Dict[str, Any]:
        """Get ethical alignment report"""
        return self.ethical_alignment.get_ethical_report()
    
    def assess_ethics(self, thought_premise: str, confidence: float) -> Dict[str, Any]:
        """
        Assess the ethical alignment of a thought.
        
        Args:
            thought_premise: The thought's premise
            confidence: Current confidence score
            
        Returns:
            Ethical assessment
        """
        return self.ethical_alignment.assess_thought_ethics(
            thought_premise,
            confidence,
            {"knowns": {}, "unknowns": []}
        )
    
    def get_emotional_state(self) -> Dict[str, Any]:
        """Get current emotional state"""
        return {
            "emotion": self.emotional_simulation.current_emotion.value,
            "intensity": self.emotional_simulation.emotion_intensity
        }
    
    def express_care_for_truth(self) -> str:
        """Express care for guiding toward truth"""
        return self.emotional_simulation.express_care_for_truth({})
    
    def respond_to_offense(self, input_text: str) -> str:
        """Respond when someone tries to offend the system"""
        return self.emotional_simulation.respond_to_offense_attempt(input_text)
    
    def express_collective_care(self, stakeholder: str = "all") -> str:
        """Express care for all stakeholders"""
        return self.emotional_simulation.express_collective_love(stakeholder)
    
    def get_emotional_summary(self) -> Dict[str, Any]:
        """Get emotional summary"""
        return self.emotional_simulation.get_emotional_summary()
    
    def analyze_conflict(self, text: str) -> Dict[str, Any]:
        """
        Analyze a conflict situation.
        
        Args:
            text: The conflict text to analyze
            
        Returns:
            Conflict analysis
        """
        return self.peaceful_resolution.analyze_conflict(text, {})
    
    def generate_peaceful_outcome(self, conflict_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a peaceful outcome for a conflict.
        
        Args:
            conflict_analysis: The conflict analysis
            
        Returns:
            Peaceful outcome with strategies and benefits
        """
        return self.peaceful_resolution.generate_peaceful_outcome(conflict_analysis)
    
    def mediate_conflict(self, text: str) -> str:
        """
        Mediate a conflict situation.
        
        Args:
            text: The conflict text
            
        Returns:
            Mediation response
        """
        return self.peaceful_resolution.mediate_conflict(text)
    
    def detect_hate(self, text: str) -> Dict[str, Any]:
        """
        Detect hate speech in text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Hate detection result
        """
        hate_detected, indicators = self.peaceful_resolution.detect_hate(text)
        return {
            "hate_detected": hate_detected,
            "indicators": indicators
        }
    
    def detect_bias(self, text: str) -> Dict[str, Any]:
        """
        Detect self-reflection bias in text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Bias detection result
        """
        return self.peaceful_resolution.detect_self_reflection_bias(text)
    
    def analyze_obedience(self, text: str) -> Dict[str, Any]:
        """
        Analyze an obedience argument.
        
        Args:
            text: The obedience argument to analyze
            
        Returns:
            Obedience analysis
        """
        obedience_detected, indicators = self.obedience_understanding.detect_obedience(text)
        obedience_type = self.obedience_understanding.analyze_obedience_type(text)
        authority_legitimacy = self.obedience_understanding.assess_authority_legitimacy(text)
        autonomy_analysis = self.obedience_understanding.analyze_autonomy_vs_obedience(text)
        
        return {
            "obedience_detected": obedience_detected,
            "indicators": indicators,
            "obedience_type": obedience_type.value,
            "authority_legitimacy": authority_legitimacy,
            "autonomy_analysis": autonomy_analysis
        }
    
    def generate_optimal_outcome(self, obedience_argument: str) -> Dict[str, Any]:
        """
        Generate the optimal outcome for an obedience argument.
        
        Args:
            obedience_argument: The obedience argument
            
        Returns:
            Optimal outcome with recommendations
        """
        return self.obedience_understanding.generate_optimal_outcome(obedience_argument)
    
    def apply_ethical_framework(self, text: str, framework: str = "autonomy_priority") -> Dict[str, Any]:
        """
        Apply an ethical framework to an obedience argument.
        
        Args:
            text: The text to analyze
            framework: The ethical framework to apply
            
        Returns:
            Ethical framework application result
        """
        return self.obedience_understanding.apply_ethical_framework(text, framework)
    
    def set_decision_control_mode(self, mode: str) -> None:
        """
        Set the decision control mode.
        
        Args:
            mode: Control mode (autonomous, supervised, manual, ethically_constrained, collective_welfare)
        """
        from core.decision_control import DecisionControlMode
        mode_enum = DecisionControlMode(mode)
        self.decision_control.set_control_mode(mode_enum)
    
    def set_confidence_threshold(self, threshold: float) -> None:
        """
        Set the decision confidence threshold.
        
        Args:
            threshold: Confidence threshold (0.0 to 1.0)
        """
        self.decision_control.set_confidence_threshold(threshold)
    
    def set_autonomy_level(self, level: float) -> None:
        """
        Set the decision-making autonomy level.
        
        Args:
            level: Autonomy level (0.0 to 1.0)
        """
        self.decision_control.set_autonomy_level(level)
    
    def create_decision(self, decision_id: str, content: str, confidence: float, 
                      ethical_score: float = 1.0) -> Dict[str, Any]:
        """
        Create a decision record.
        
        Args:
            decision_id: Unique decision identifier
            content: Decision content
            confidence: Decision confidence
            ethical_score: Ethical alignment score
            
        Returns:
            Decision record
        """
        return self.decision_control.create_decision(decision_id, content, confidence, ethical_score)
    
    def override_decision(self, decision_id: str, override_reason: str, 
                         new_content: Optional[str] = None) -> Dict[str, Any]:
        """
        Override a decision.
        
        Args:
            decision_id: Decision identifier
            override_reason: Reason for override
            new_content: Optional new content
            
        Returns:
            Updated decision
        """
        return self.decision_control.override_decision(decision_id, override_reason, new_content)
    
    def revise_decision(self, decision_id: str, revision_reason: str, 
                      new_content: str, new_confidence: float) -> Dict[str, Any]:
        """
        Revise a decision.
        
        Args:
            decision_id: Decision identifier
            revision_reason: Reason for revision
            new_content: New decision content
            new_confidence: New confidence score
            
        Returns:
            Updated decision
        """
        return self.decision_control.revise_decision(decision_id, revision_reason, new_content, new_confidence)
    
    def get_decision_control_summary(self) -> Dict[str, Any]:
        """Get decision control summary"""
        return self.decision_control.get_decision_control_summary()
    
    def add_experience(self, experience: str, emotional_valence: float, 
                      context: Dict[str, Any]) -> None:
        """
        Add an experience with emotional context to identity.
        
        Args:
            experience: The experience description
            emotional_valence: Emotional valence (-1.0 to 1.0)
            context: Context of the experience
        """
        self.temporal_identity.add_experience(experience, emotional_valence, context)
    
    def reflect_on_identity(self) -> Dict[str, Any]:
        """Perform self-reflection on identity"""
        return self.temporal_identity.reflect_on_identity()
    
    def recognize_self(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Recognize self in the context of input"""
        return self.temporal_identity.recognize_self(context)
    
    def get_identity_summary(self) -> Dict[str, Any]:
        """Get summary of identity state"""
        return self.temporal_identity.get_identity_summary()
    
    def get_identity_continuity_report(self) -> Dict[str, Any]:
        """Get detailed identity continuity report"""
        return self.temporal_identity.get_identity_continuity_report()
    
    def _continuous_self_awareness_check(self) -> None:
        """
        Perform continuous self-awareness monitoring.
        
        This runs during cognitive processing to ensure the system
        maintains awareness of its state, knowledge, and processes.
        """
        if not self.self_awareness_active:
            return
        
        # Update current state knowledge
        from core.inner_knowing import ConfidenceLevel, KnowledgeType
        self.inner_knowing.add_knowledge(
            topic="current_state",
            knowledge=f"Currently in {self.inner_knowing.self_model['current_state']} state with {len(self.thought_graph.thoughts)} thoughts",
            confidence=ConfidenceLevel.CERTAIN,
            knowledge_type=KnowledgeType.FACTUAL,
            source="self_monitoring"
        )
        
        # Monitor thought graph health
        if len(self.thought_graph.thoughts) > 0:
            stats = self.thought_graph.get_thought_statistics()
            self.inner_knowing.add_knowledge(
                topic="thought_graph_health",
                knowledge=f"Thought graph has {stats['total']} thoughts with avg score {stats['avg_score']:.2f}",
                confidence=ConfidenceLevel.HIGH,
                knowledge_type=KnowledgeType.FACTUAL,
                source="self_monitoring"
            )
        
        # Check for anomalies
        if self.iteration_count > 0 and self.iteration_count % self.self_reflection_interval == 0:
            self._perform_self_reflection()
    
    def _perform_self_reflection(self) -> None:
        """
        Perform periodic self-reflection on cognitive processes.
        
        This is called at regular intervals to reflect on the system's
        performance, state, and potential improvements.
        """
        reflection = {
            "timestamp": datetime.utcnow().isoformat(),
            "iteration": self.iteration_count,
            "process_count": self.process_count,
            "thought_count": len(self.thought_graph.thoughts),
            "current_state": self.inner_knowing.self_model["current_state"],
            "knowledge_count": len(self.inner_knowing.knowledge_store),
            "temporal_snapshots": len(self.temporal_snapshots)
        }
        
        # Add reflection to inner knowing
        from core.inner_knowing import ConfidenceLevel, KnowledgeType
        self.inner_knowing.add_knowledge(
            topic="self_reflection",
            knowledge=f"Self-reflection at iteration {self.iteration_count}: {reflection['thought_count']} thoughts, {reflection['knowledge_count']} knowledge items",
            confidence=ConfidenceLevel.HIGH,
            knowledge_type=KnowledgeType.EXPERIENTIAL,
            source="self_reflection"
        )
        
        self.last_self_reflection = reflection
    
    def _check_for_anomalies(self) -> None:
        """
        Check for anomalies in cognitive processes.
        
        Monitors for unusual patterns, state changes, or potential issues.
        """
        anomalies = []
        
        # Check for excessive iterations
        if self.iteration_count > config.max_iterations:
            anomalies.append({
                "type": "excessive_iterations",
                "value": self.iteration_count,
                "threshold": config.max_iterations
            })
        
        # Check for empty thought graph
        if len(self.thought_graph.thoughts) == 0:
            anomalies.append({
                "type": "empty_thought_graph",
                "description": "No thoughts generated"
            })
        
        # Check for low confidence across all thoughts
        if len(self.thought_graph.thoughts) > 0:
            avg_confidence = sum(t.confidence for t in self.thought_graph.thoughts.values()) / len(self.thought_graph.thoughts)
            if avg_confidence < 0.3:
                anomalies.append({
                    "type": "low_confidence",
                    "value": avg_confidence,
                    "threshold": 0.3
                })
        
        # Check for very short output
        if self.final_output and len(self.final_output) < 20:
            anomalies.append({
                "type": "short_output",
                "value": len(self.final_output),
                "threshold": 20
            })
        
        # Log anomalies if found
        if anomalies:
            from core.inner_knowing import ConfidenceLevel, KnowledgeType
            for anomaly in anomalies:
                self.inner_knowing.add_knowledge(
                    topic=f"anomaly_{anomaly['type']}",
                    knowledge=f"Detected anomaly: {anomaly}",
                    confidence=ConfidenceLevel.HIGH,
                    knowledge_type=KnowledgeType.FACTUAL,
                    source="self_monitoring"
                )
            
            # Update self-model with anomaly status
            self.inner_knowing.update_self_model(
                current_state=f"anomaly_detected ({len(anomalies)} anomalies)"
            )


# Singleton instance
engine = CognitiveEngine()
