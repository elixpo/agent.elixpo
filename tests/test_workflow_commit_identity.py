"""Elixpoo v1 workflows never create repository commits."""

from pathlib import Path


def test_v1_callers_have_no_commit_or_push_path():
    root = Path(".github/workflows")
    for name in (
        "elixpoo-triage.yml",
        "elixpoo-mentions.yml",
        "elixpoo-review.yml",
        "elixpoo-merge-memory.yml",
    ):
        workflow = (root / name).read_text(encoding="utf-8")
        assert "contents: write" not in workflow
        assert "git commit" not in workflow
        assert "git push" not in workflow


def test_legacy_repository_agent_is_inactive():
    workflow = Path(".github/workflows/elixpo-agent.yml").read_text(encoding="utf-8")
    assert "workflow_dispatch" in workflow
    assert "python -m agents.repository_agent" not in workflow
    assert "contents: write" not in workflow
