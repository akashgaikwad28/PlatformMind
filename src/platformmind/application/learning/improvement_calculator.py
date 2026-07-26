"""
Improvement Calculator.
"""


class ImprovementCalculator:
    """
    Calculates percentage improvement between historical average and current run.
    """

    def calculate_improvement(
        self, historical: float, current: float, invert: bool = False
    ) -> float:
        """
        Calculates % change.
        If invert is True (e.g. for time/calls where lower is better), a reduction is a positive improvement.
        """
        if historical == 0:
            return 0.0

        change = ((historical - current) / historical) * 100
        return change if invert else -change
