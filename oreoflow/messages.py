"""Integrity-checked OreoFlow A2A-style message envelope."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from oreoflow.artifacts import ArtifactRef
from oreoflow.ids import new_id
from oreoflow.policy import PolicyGrant

MessageKind = Literal[
    "task.request", "task.accepted", "task.rejected", "task.status", "task.completed",
    "task.failed", "task.canceled", "artifact.available", "artifact.revoked", "control.pause",
    "control.resume", "control.terminate", "security.challenge", "security.denied",
    "security.approved", "carrier.received", "carrier.delivered", "carrier.dead_lettered",
]


class Endpoint(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    floor: str = Field(min_length=1, max_length=80)
    room: str = Field(min_length=1, max_length=120)
    agent: str = Field(min_length=1, max_length=80)


class BudgetGrant(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    tokens: int = Field(default=0, ge=0)
    seconds: int = Field(default=300, ge=1, le=86_400)


class Integrity(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    digest: str = Field(pattern=r"^sha256:[0-9a-f]{64}$")


class A2AMessage(BaseModel):
    """Portable envelope inspired by A2A Task/Message/Artifact semantics.

    This is the OreoFlow profile and does not claim official A2A conformance.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_id: Literal["oreoflow.a2a/v1"] = "oreoflow.a2a/v1"
    message_id: str = Field(default_factory=lambda: new_id("message"))
    correlation_id: str = Field(default_factory=lambda: new_id("correlation"))
    causation_id: str | None = None
    building_id: str = Field(min_length=1, max_length=120)
    source: Endpoint
    destination: Endpoint
    kind: MessageKind
    task_id: str | None = None
    capability: str | None = Field(default=None, max_length=80)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deadline: datetime | None = None
    budget: BudgetGrant = Field(default_factory=BudgetGrant)
    artifact_refs: tuple[ArtifactRef, ...] = Field(default=(), max_length=32)
    payload: dict[str, Any] = Field(default_factory=dict)
    policy: PolicyGrant = Field(default_factory=PolicyGrant)
    integrity: Integrity | None = None

    @model_validator(mode="after")
    def validate_request(self) -> A2AMessage:
        if self.kind == "task.request" and (not self.task_id or not self.capability):
            raise ValueError("task.request requires task_id and capability")
        if self.deadline and self.deadline <= self.created_at:
            raise ValueError("message deadline must be after creation")
        if len(json.dumps(self.payload, sort_keys=True, separators=(",", ":")).encode()) > 65_536:
            raise ValueError("message payload exceeds 64 KiB; use an artifact reference")
        return self

    def canonical_bytes(self) -> bytes:
        data = self.model_dump(mode="json", exclude={"integrity"})
        return json.dumps(data, sort_keys=True, separators=(",", ":")).encode()

    def seal(self) -> A2AMessage:
        digest = hashlib.sha256(self.canonical_bytes()).hexdigest()
        return self.model_copy(update={"integrity": Integrity(digest=f"sha256:{digest}")})

    def verify(self) -> bool:
        return bool(self.integrity and self.seal().integrity == self.integrity)
