"""
Score Manager.
"""


class ScoreManager:
    """
    Provides Exponential Moving Average (EMA) scoring.
    """

    def __init__(self, alpha: float = 0.3):
        self.alpha = alpha

    def update_score(self, historical_score: float, new_score: float) -> float:
        """
        Updates a score using EMA. Higher alpha weights new score more heavily.
        """
        return (self.alpha * new_score) + ((1 - self.alpha) * historical_score)
