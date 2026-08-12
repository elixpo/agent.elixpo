"""Human admission boundary tests."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest
from agents.admission.core import (
    APPROVAL_LABEL,
    REQUEST_LABEL,
    AdmissionRejected,
    approve,
    parse_approval,
    propose,
)
from agents.solve.core import SolveRejected, resolve_target
from lib.state.store import StateStore

NOW = datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc)
URL = "https://github.com/example/project/issues/7"
KEY = "example/project#7"
RUN_ID = "pick-run-7"


class FakeRouter:
    def __init__(self):
        self.calls = 0

    async def call(self, *_args, **_kwargs):
        self.calls += 1
        message = SimpleNamespace(content="SAFE")
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])


class FakeAPI:
    def __init__(self):
        self.labels: list[str] = []
        self.created: list[dict] = []

    async def ensure_label(self, _owner, _repo, name, _color, _description=""):
        self.labels.append(name)

    async def create_issue(self, owner, repo, title, body, *, labels=None):
        issue = {
            "number": 41,
            "html_url": f"https://github.com/{owner}/{repo}/issues/41",
            "title": title,
            "body": body,
            "labels": [{"name": name} for name in labels or []],
        }
        self.created.append(issue)
        return issue


def _candidate_store(tmp_path) -> StateStore:
    store = StateStore(tmp_path)
    pick = {
        "status": "picked",
        "picked": True,
        "run_id": RUN_ID,
        "key": KEY,
        "url": URL,
        "source": "autonomous_scout",
    }
    vet = {
        "status": "approved",
        "suitable": True,
        "test_mode": False,
        "run_id": RUN_ID,
        "key": KEY,
        "url": URL,
        "issue_updated_at": "2026-08-12T10:00:00Z",
        "estimated_files": 2,
        "estimated_minutes": 8,
        "confidence": 0.91,
        "summary": "Bounded display fix",
    }
    store.write_state(
        "pick.json", pick, producer="vet", run_id=RUN_ID, key=KEY, ttl=timedelta(hours=24), now=NOW
    )
    store.write_state(
        "vet.json", vet, producer="vet", run_id=RUN_ID, key=KEY, ttl=timedelta(hours=24), now=NOW
    )
    return store


@pytest.mark.asyncio
async def test_proposal_is_safe_revision_bound_and_idempotent(tmp_path):
    store = _candidate_store(tmp_path)
    api = FakeAPI()
    router = FakeRouter()

    first = await propose(store, api, router, "elixpo/agent.elixpo")
    second = await propose(store, api, router, "elixpo/agent.elixpo")

    assert first == second
    assert first["status"] == "approval_required"
    assert first["run_id"] == RUN_ID
    assert api.labels == [REQUEST_LABEL, APPROVAL_LABEL]
    assert len(api.created) == 1
    assert router.calls == 1
    marker = parse_approval(api.created[0]["body"])
    assert marker["fingerprint"] == first["fingerprint"]
    assert "summary" not in marker


@pytest.mark.asyncio
async def test_approval_requires_both_labels_and_exact_control_issue(tmp_path):
    store = _candidate_store(tmp_path)
    api = FakeAPI()
    receipt = await propose(store, api, FakeRouter(), "elixpo/agent.elixpo")
    issue = {
        **api.created[0],
        "labels": [{"name": REQUEST_LABEL}, {"name": APPROVAL_LABEL}],
    }

    approved = approve(store, issue)

    assert approved["status"] == "approved"
    assert approved["fingerprint"] == receipt["fingerprint"]

    wrong_issue = {**issue, "number": 99}
    with pytest.raises(AdmissionRejected, match="different control issue"):
        approve(store, wrong_issue)


def test_production_solve_requires_matching_admission(tmp_path):
    store = _candidate_store(tmp_path)

    with pytest.raises(SolveRejected, match="no matching maintainer admission"):
        resolve_target(store, None, False)

    admission = {
        "status": "approved",
        "run_id": RUN_ID,
        "key": KEY,
        "issue_url": URL,
        "fingerprint": "exact-revision",
    }
    store.write_state(
        "admission.json",
        admission,
        producer="admission",
        run_id=RUN_ID,
        key=KEY,
        ttl=timedelta(days=7),
        now=NOW,
    )

    assert resolve_target(store, None, False) == URL


def test_admission_workflow_is_the_only_automatic_solve_entry():
    admission = Path(".github/workflows/admission.yml").read_text(encoding="utf-8")
    solve = Path(".github/workflows/solve.yml").read_text(encoding="utf-8")

    assert "workflows: [vet]" in admission
    assert "types: [doctor_retry, oreoflow_approved]" in solve
    assert "workflows: [vet]" not in solve
    assert "python -m agents.admission approve" in admission
    assert "event_type=oreoflow_approved" in admission
