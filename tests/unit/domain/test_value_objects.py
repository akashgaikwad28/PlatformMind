import pytest
from pydantic import ValidationError

from platformmind.domain.value_objects import (
    BranchName,
    ConfidenceScore,
    IssueNumber,
    RepositoryName,
    SimilarityScore,
)


def test_repository_name_valid() -> None:
    repo = RepositoryName(owner="octocat", name="Hello-World")
    assert repo.full_name == "octocat/Hello-World"


def test_repository_name_invalid() -> None:
    with pytest.raises(ValidationError):
        RepositoryName(owner="", name="Hello-World")


def test_branch_name_valid() -> None:
    branch = BranchName(value="feature/new-feature")
    assert branch.value == "feature/new-feature"


def test_branch_name_invalid_spaces() -> None:
    with pytest.raises(ValidationError):
        BranchName(value="invalid branch name")


def test_issue_number_valid() -> None:
    issue = IssueNumber(value=1)
    assert issue.value == 1


def test_issue_number_invalid() -> None:
    with pytest.raises(ValidationError):
        IssueNumber(value=0)


def test_confidence_score_valid() -> None:
    score = ConfidenceScore(value=0.5)
    assert score.value == 0.5


def test_confidence_score_invalid() -> None:
    with pytest.raises(ValidationError):
        ConfidenceScore(value=1.5)


def test_similarity_score_valid() -> None:
    score = SimilarityScore(value=-0.5)
    assert score.value == -0.5


def test_value_object_immutability() -> None:
    repo = RepositoryName(owner="octocat", name="Hello-World")
    with pytest.raises(ValidationError):
        repo.owner = "new-owner"  # type: ignore
