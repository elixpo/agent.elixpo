"""Create and approve idempotent OreoFlow admission requests."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from typing import Any

from lib.state.store import StateStore
from rtk.models import Message

APPROVAL_LABEL = "oreoflow/approved"
REQUEST_LABEL = "oreoflow/approval-required"
_MARKER_RE = re.compile(r"<!-- oreoflow-admission:v1\s*(\{[^\n]*\})\s*-->")


class AdmissionRejected(RuntimeError):
    """The proposed or approved admission does not match durable Vet state."""


def fingerprint(key: str, issue_updated_at: str, run_id: str) -> str:
    material = f"{key.casefold()}|{issue_updated_at}|{run_id}"
    return hashlib.sha256(material.encode()).hexdigest()[:24]


def approval_body(payload: dict[str, Any]) -> str:
    marker_fields = {
        field: payload[field]
        for field in ("fingerprint", "key", "issue_url", "issue_updated_at", "run_id", "source")
    }
    metadata = json.dumps(marker_fields, sort_keys=True, separators=(",", ":"))
    summary = re.sub(r"\s+", " ", str(payload["summary"])).replace("<", "&lt;").replace(">", "&gt;")
    return (
        "OreoFlow found and independently vetted a bounded issue. No repository "
        "mutation or model-heavy Solve run starts until a maintainer approves this admission.\n\n"
        f"- Candidate: {payload['issue_url']}\n"
        f"- Source: `{payload['source']}`\n"
        f"- Estimated scope: `{payload['estimated_files']} files`, "
        f"`{payload['estimated_minutes']} focused minutes`\n"
        f"- Vet confidence: `{payload['confidence']:.0%}`\n"
        f"- Vet summary: {summary}\n\n"
        f"Add `{APPROVAL_LABEL}` to authorize exactly this vetted issue revision. "
        "Closing this issue without approval declines the candidate.\n\n"
        f"<!-- oreoflow-admission:v1\n{metadata}\n-->"
    )


def parse_approval(body: str) -> dict[str, Any]:
    match = _MARKER_RE.search(body or "")
    if not match:
        raise AdmissionRejected("approval issue has no OreoFlow admission marker")
    payload = json.loads(match.group(1))
    required = {"fingerprint", "key", "issue_url", "issue_updated_at", "run_id", "source"}
    if not required.issubset(payload):
        raise AdmissionRejected("approval issue metadata is incomplete")
    return payload


async def _safety_check(router, body: str) -> None:
    response = await router.call(
        "safety",
        [
            Message(
                role="system",
                content=(
                    "Moderate this operational GitHub issue. Reply exactly SAFE if it contains "
                    "no secrets, abuse, unsafe instructions, or deceptive claims; otherwise UNSAFE."
                ),
            ),
            Message(role="user", content=body),
        ],
        effort="low",
        max_tokens=20,
    )
    content = (response.choices[0].message.content or "").strip().casefold()
    if re.search(r"\bunsafe\b", content) or not re.search(r"\bsafe\b", content):
        raise AdmissionRejected("public admission issue failed the safety gate")


def _load_candidate(store: StateStore) -> tuple[dict, dict, dict]:
    vet = store.read_state("vet.json", {}, expected_producer="vet") or {}
    pick = store.read_state(
        "pick.json",
        {},
        expected_producer="vet",
        expected_run_id=str(vet.get("run_id") or "") or None,
        expected_key=str(vet.get("key") or "") or None,
    ) or {}
    if vet.get("status") != "approved" or vet.get("suitable") is not True:
        raise AdmissionRejected("Vet did not approve the current candidate")
    if pick.get("status") != "picked" or pick.get("url") != vet.get("url"):
        raise AdmissionRejected("Pick and Vet do not identify the same approved candidate")
    payload = {
        "fingerprint": fingerprint(
            str(vet.get("key") or ""),
            str(vet.get("issue_updated_at") or ""),
            str(vet.get("run_id") or ""),
        ),
        "key": str(vet["key"]),
        "issue_url": str(vet["url"]),
        "issue_updated_at": str(vet.get("issue_updated_at") or ""),
        "run_id": str(vet.get("run_id") or ""),
        "source": str(pick.get("source") or "autonomous_scout"),
        "estimated_files": int(vet.get("estimated_files") or 0),
        "estimated_minutes": int(vet.get("estimated_minutes") or 0),
        "confidence": float(vet.get("confidence") or 0),
        "summary": str(vet.get("summary") or "Bounded issue approved by Vet")[:500],
    }
    return pick, vet, payload


async def propose(store: StateStore, api, router, control_repo: str) -> dict:
    _pick, _vet, payload = _load_candidate(store)
    existing = store.read_json("admission.json", {}) or {}
    if existing.get("fingerprint") == payload["fingerprint"] and existing.get("status") in {
        "approval_required",
        "approved",
    }:
        return existing
    owner, repo = control_repo.split("/", 1)
    body = approval_body(payload)
    await _safety_check(router, body)
    await api.ensure_label(owner, repo, REQUEST_LABEL, "b60205", "OreoFlow admission needs maintainer approval")
    await api.ensure_label(owner, repo, APPROVAL_LABEL, "0e8a16", "Approve one exact OreoFlow admission")
    issue = await api.create_issue(
        owner,
        repo,
        f"[OreoFlow admission] {payload['key']}",
        body,
        labels=[REQUEST_LABEL],
    )
    now = datetime.now(timezone.utc)
    receipt = {
        "schema_version": 1,
        "status": "approval_required",
        **payload,
        "approval_issue_number": int(issue["number"]),
        "approval_issue_url": str(issue.get("html_url") or ""),
        "proposed_at": now.isoformat(),
    }
    store.write_state(
        "admission.json",
        receipt,
        producer="admission",
        run_id=payload["run_id"],
        key=payload["key"],
        ttl=timedelta(days=7),
        now=now,
    )
    return receipt


def approve(store: StateStore, issue: dict) -> dict:
    labels = {str(item.get("name") or "") for item in issue.get("labels", [])}
    if not {REQUEST_LABEL, APPROVAL_LABEL}.issubset(labels):
        raise AdmissionRejected("approval issue is missing the required labels")
    payload = parse_approval(str(issue.get("body") or ""))
    current = store.read_state(
        "admission.json",
        {},
        expected_producer="admission",
        expected_run_id=str(payload["run_id"]),
        expected_key=str(payload["key"]),
    ) or {}
    if current.get("fingerprint") != payload["fingerprint"]:
        raise AdmissionRejected("approval does not match the current admission fingerprint")
    if int(current.get("approval_issue_number") or 0) != int(issue.get("number") or 0):
        raise AdmissionRejected("approval came from a different control issue")
    if current.get("status") == "approved":
        return current
    if current.get("status") != "approval_required":
        raise AdmissionRejected(f"cannot approve admission in state {current.get('status')!r}")
    approved = {
        **current,
        "status": "approved",
        "approved_at": datetime.now(timezone.utc).isoformat(),
    }
    store.write_state(
        "admission.json",
        approved,
        producer="admission",
        run_id=str(payload["run_id"]),
        key=str(payload["key"]),
        ttl=timedelta(days=7),
    )
    return approved
