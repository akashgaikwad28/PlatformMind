"""
Gap Detector.
"""

from dataclasses import dataclass


@dataclass
class CapabilityGap:
    instruction: str
    missing_workflow: bool
    missing_tools: list[str]


class GapDetector:
    """
    Identifies missing capabilities when planner fails.
    """

    def detect_gap(self, instruction: str, planner_error: str) -> CapabilityGap:
        """
        Analyzes a planner failure to determine the gap.
        """
        missing_tools = []
        missing_workflow = False

        if "unknown_tool" in planner_error:
            missing_workflow = True

        return CapabilityGap(
            instruction=instruction,
            missing_workflow=missing_workflow,
            missing_tools=missing_tools,
        )
