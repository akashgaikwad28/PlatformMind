from platformmind.domain.enums import ConfidenceLevel, InstructionPriority
from platformmind.domain.models.execution import ExecutionPlan, ExecutionStep
from platformmind.domain.models.instruction import Instruction
from platformmind.domain.value_objects import InstructionId


def test_instruction_creation() -> None:
    instruction = Instruction(original_text="Create a new issue")
    assert instruction.normalized_text == "create a new issue"
    assert instruction.priority == InstructionPriority.NORMAL
    assert instruction.confidence == ConfidenceLevel.LOW


def test_execution_plan_add_remove_step() -> None:
    plan = ExecutionPlan(instruction_id=InstructionId())
    step = ExecutionStep(
        step_id="step_1",
        name="Test Step",
        description="A test step",
        tool_name="TestTool",
    )
    plan.add_step(step)
    assert plan.total_steps() == 1

    plan.remove_step("step_1")
    assert plan.total_steps() == 0


def test_execution_plan_reorder_steps() -> None:
    plan = ExecutionPlan(instruction_id=InstructionId())
    step1 = ExecutionStep(step_id="step_1", name="Step 1", description="", tool_name="")
    step2 = ExecutionStep(step_id="step_2", name="Step 2", description="", tool_name="")
    plan.add_step(step1)
    plan.add_step(step2)

    plan.reorder_steps(["step_2", "step_1"])
    assert plan.steps[0].step_id == "step_2"
    assert plan.steps[1].step_id == "step_1"


def test_execution_plan_validate_dependencies() -> None:
    plan = ExecutionPlan(instruction_id=InstructionId())
    step1 = ExecutionStep(step_id="step_1", name="Step 1", description="", tool_name="")
    step2 = ExecutionStep(
        step_id="step_2",
        name="Step 2",
        description="",
        tool_name="",
        dependencies=["step_1"],
    )  # noqa: E501
    plan.add_step(step1)
    plan.add_step(step2)

    assert plan.validate_dependencies() is True

    # Invalid dependency (step_3 does not exist)
    step3 = ExecutionStep(
        step_id="step_3",
        name="Step 3",
        description="",
        tool_name="",
        dependencies=["step_missing"],
    )  # noqa: E501
    plan.add_step(step3)
    assert plan.validate_dependencies() is False
