"""
Instruction Normalizer.
"""

import re


class InstructionNormalizer:
    def normalize(self, instruction: str) -> str:
        # Lowercase, strip whitespace
        normalized = instruction.strip().lower()
        # Remove multiple spaces
        normalized = re.sub(r"\s+", " ", normalized)
        # Handle common abbreviations
        normalized = normalized.replace("repo", "repository")
        normalized = normalized.replace("lbl", "label")
        normalized = normalized.replace("msg", "message")
        return normalized
