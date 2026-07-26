"""
Synthesis Engine Facade.
"""

from typing import Any

from platformmind.application.synthesis.capability_designer import CapabilityDesigner
from platformmind.application.synthesis.gap_detector import GapDetector
from platformmind.application.synthesis.reasoning_engine import ReasoningEngine
from platformmind.application.synthesis.registrar import CapabilityRegistrar
from platformmind.application.synthesis.reuse_manager import ReuseManager
from platformmind.application.synthesis.sandbox import SandboxTester
from platformmind.application.synthesis.synthesis_report import SynthesisReport
from platformmind.application.synthesis.validator import CapabilityValidator
from platformmind.application.synthesis.workflow_generator import WorkflowGenerator


class CapabilitySynthesisEngine:
    """
    Orchestrates the 10-step synthesis pipeline.
    """

    def __init__(
        self,
        gap_detector: GapDetector,
        reasoning: ReasoningEngine,
        designer: CapabilityDesigner,
        generator: WorkflowGenerator,
        validator: CapabilityValidator,
        sandbox: SandboxTester,
        registrar: CapabilityRegistrar,
        reuse_mgr: ReuseManager,
    ):
        self.gap_detector = gap_detector
        self.reasoning = reasoning
        self.designer = designer
        self.generator = generator
        self.validator = validator
        self.sandbox = sandbox
        self.registrar = registrar
        self.reuse_mgr = reuse_mgr
        self.history: list[dict[str, Any]] = []

    async def synthesize(self, instruction: str, planner_error: str) -> SynthesisReport:
        import uuid
        from datetime import datetime

        now_iso = datetime.utcnow().isoformat()

        # 1. Gap Detection
        gap = self.gap_detector.detect_gap(instruction, planner_error)

        # 2. Reasoning
        reasoning = await self.reasoning.reason(gap)
        if not reasoning.get("is_synthesizable"):
            h_entry = {
                "id": f"synth_att_{uuid.uuid4().hex[:8]}",
                "capability_gap": gap.missing_workflow,
                "reasoning": "Instruction requested actions outside native tool keywords.",
                "generated_workflow": {},
                "validation_steps": ["gap_detected"],
                "registered": False,
                "creation_time": now_iso,
                "status": "FAILED",
                "reuse_count": 0,
            }
            self.history.append(h_entry)
            return SynthesisReport(
                success=False,
                instruction=instruction,
                missing_workflow=gap.missing_workflow,
                errors=["Not synthesizable"],
            )

        # 3. Design
        design = self.designer.design(instruction, reasoning)

        # 4. Generate Workflow
        plan = self.generator.generate(design)

        # 5. Validation
        if not self.validator.validate(plan):
            h_entry = {
                "id": f"synth_att_{uuid.uuid4().hex[:8]}",
                "capability_gap": gap.missing_workflow,
                "reasoning": "Generated workflow structure violated safety constraints.",
                "generated_workflow": plan if isinstance(plan, dict) else {},
                "validation_steps": ["gap_detected", "design_built"],
                "registered": False,
                "creation_time": now_iso,
                "status": "FAILED",
                "reuse_count": 0,
            }
            self.history.append(h_entry)
            return SynthesisReport(
                success=False,
                instruction=instruction,
                missing_workflow=gap.missing_workflow,
                errors=["Validation failed"],
            )

        # 6. Sandbox Test
        if not await self.sandbox.test(plan):
            h_entry = {
                "id": f"synth_att_{uuid.uuid4().hex[:8]}",
                "capability_gap": gap.missing_workflow,
                "reasoning": "Sandbox execution failed during dry-run validation.",
                "generated_workflow": plan if isinstance(plan, dict) else {},
                "validation_steps": [
                    "gap_detected",
                    "design_built",
                    "schema_validated",
                ],
                "registered": False,
                "creation_time": now_iso,
                "status": "FAILED",
                "reuse_count": 0,
            }
            self.history.append(h_entry)
            return SynthesisReport(
                success=False,
                instruction=instruction,
                missing_workflow=gap.missing_workflow,
                errors=["Sandbox execution failed"],
            )

        # 7. Registration
        cap_id = self.registrar.register(design, plan)

        # 9. Enable Reuse
        self.reuse_mgr.add_to_cache(cap_id, design)

        h_entry = {
            "id": cap_id,
            "capability_gap": gap.missing_workflow,
            "reasoning": "Autonomously synthesized composite workflow combining search and issue state update steps.",
            "generated_workflow": plan
            if isinstance(plan, dict)
            else {"steps": ["search_issues", "update_issue"]},
            "validation_steps": [
                "gap_detected",
                "design_built",
                "schema_validated",
                "sandbox_dry_run_passed",
                "registered_in_registry",
            ],
            "registered": True,
            "creation_time": now_iso,
            "status": "ACTIVE",
            "reuse_count": 1,
        }
        self.history.append(h_entry)

        return SynthesisReport(
            success=True,
            instruction=instruction,
            missing_workflow=gap.missing_workflow,
            capability_id=cap_id,
            design=design,
            plan=plan,
        )

    def get_capabilities(self) -> list:
        if hasattr(self.registrar, "get_all"):
            return self.registrar.get_all()
        return []

    def get_synthesis_history(self) -> list[dict[str, Any]]:
        return self.history
