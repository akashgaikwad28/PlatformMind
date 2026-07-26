"""
Planning Pipeline.
"""

from typing import Any

from platformmind.application.planner.capability_matcher import CapabilityMatcher
from platformmind.application.planner.confidence_estimator import ConfidenceEstimator
from platformmind.application.planner.context_builder import ContextBuilder
from platformmind.application.planner.dependency_resolver import DependencyResolver
from platformmind.application.planner.execution_plan_builder import ExecutionPlanBuilder
from platformmind.application.planner.instruction_normalizer import (
    InstructionNormalizer,
)
from platformmind.application.planner.intent_classifier import IntentClassifier
from platformmind.application.planner.memory_retriever import MemoryRetriever
from platformmind.application.planner.plan_optimizer import PlanOptimizer
from platformmind.application.planner.risk_analyzer import RiskAnalyzer
from platformmind.application.planner.task_decomposer import TaskDecomposer
from platformmind.application.planner.tool_selector import ToolSelector
from platformmind.application.planner.validators.execution_plan_validator import (
    ExecutionPlanValidator,
)
from platformmind.application.planner.validators.guardrails import InputGuardrail
from platformmind.core.telemetry.tracer import trace_step
from platformmind.domain.models.execution import ExecutionPlan
from platformmind.domain.models.instruction import Instruction


class PlanningPipeline:
    def __init__(
        self,
        normalizer: InstructionNormalizer,
        context_builder: ContextBuilder,
        memory_retriever: MemoryRetriever,
        classifier: IntentClassifier,
        decomposer: TaskDecomposer,
        matcher: CapabilityMatcher,
        selector: ToolSelector,
        resolver: DependencyResolver,
        optimizer: PlanOptimizer,
        analyzer: RiskAnalyzer,
        estimator: ConfidenceEstimator,
        builder: ExecutionPlanBuilder,
        validator: ExecutionPlanValidator,
        input_guardrail: InputGuardrail,
    ):
        self.normalizer = normalizer
        self.context_builder = context_builder
        self.memory_retriever = memory_retriever
        self.classifier = classifier
        self.decomposer = decomposer
        self.matcher = matcher
        self.selector = selector
        self.resolver = resolver
        self.optimizer = optimizer
        self.analyzer = analyzer
        self.estimator = estimator
        self.builder = builder
        self.validator = validator
        self.input_guardrail = input_guardrail

    @trace_step("PlanningPipeline.execute")
    async def execute(
        self,
        instruction: Instruction,
        repository: str,
        options: dict[str, Any],
        previous_results: list[dict[str, Any]] = None,
    ) -> ExecutionPlan:
        # Step 1: Normalize instruction
        normalized = self.normalizer.normalize(instruction.original_text)
        instruction = instruction.model_copy(update={"normalized_text": normalized})

        # Step 1.5: Input Guardrail Check (Prompt Injection Protection)
        is_safe = await self.input_guardrail.check_instruction(
            instruction.normalized_text
        )
        if not is_safe:
            raise ValueError(
                "Input Guardrail triggered: Instruction is malicious, destructive, or out-of-scope."
            )

        # Step 2: Build Planning Context
        context = self.context_builder.build(instruction, repository, options)

        # Step 3: Retrieve 4 Independent Memory Sources
        await self.memory_retriever.retrieve_all(context)

        # Step 4: Intent Classification (influenced by memory)
        intent, intent_conf = await self.classifier.classify(
            instruction.normalized_text
        )

        # Step 5: Task Decomposition (influenced by memory and previous results)
        tasks = await self.decomposer.decompose(
            instruction.normalized_text, previous_results
        )

        # Step 6: Capability Matching (matches against Capability Memory)
        cap_matches = self.matcher.match(tasks, context)

        # Step 7: Tool Ranking & Selection (Multi-factor Ranking)
        tool_selection = self.selector.select_tools(
            tasks,
            intent=intent,
            memory_context=context.execution_memory.previous_executions
            if context.execution_memory
            else [],
        )

        # Step 8: Dependency Resolution
        resolved_tasks = self.resolver.resolve(tasks)

        # Step 9: Plan Optimization (improves execution based on Learning Memory)
        optimized_tasks = self.optimizer.optimize(resolved_tasks, context)

        # Step 10: Risk Analysis (checks Constraint Memory)
        risk_score = self.analyzer.analyze(optimized_tasks, context)

        # Step 11: Confidence Estimation
        confidence = self.estimator.estimate(
            intent_conf,
            context.execution_memory.previous_executions
            if context.execution_memory
            else [],
            cap_matches,
            optimized_tasks,
            tool_selection,
        )

        # Step 12: Execution Plan Builder (Builds rich explainable plan)
        plan = self.builder.build(
            instruction.original_text,
            instruction.normalized_text,
            intent,
            optimized_tasks,
            tool_selection,
            confidence,
        )

        # Populate new metric fields for explainability
        plan.risk_score = risk_score
        plan.planner_confidence = confidence
        plan.why_this_plan = "Selected tools and optimal sequence based on lowest execution risk and highest capability confidence."

        if context.capability_memory:
            plan.capability_match_percent = round(
                len(cap_matches) / max(len(optimized_tasks), 1) * 100, 2
            )

        if context.constraint_memory:
            plan.constraint_count = len(
                context.constraint_memory.validation_errors
            ) + len(context.constraint_memory.repository_constraints)

        # Step 13: Execution Plan Validator
        if not self.validator.validate(plan):
            raise ValueError("Generated plan violates constraints or is invalid.")

        return plan
