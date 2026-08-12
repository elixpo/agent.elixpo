"""Task lifecycle with terminal-state protection."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from oreoflow.artifacts import ArtifactRef
from oreoflow.ids import new_id


class TaskState(StrEnum):
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    REJECTED = "rejected"
    CANCELED = "canceled"


TERMINAL_TASK_STATES = frozenset({TaskState.COMPLETED, TaskState.FAILED, TaskState.REJECTED, TaskState.CANCELED})
_TRANSITIONS = {
    TaskState.SUBMITTED: {TaskState.ACCEPTED, TaskState.REJECTED, TaskState.CANCELED},
    TaskState.ACCEPTED: {TaskState.RUNNING, TaskState.CANCELED, TaskState.FAILED},
    TaskState.RUNNING: {TaskState.PAUSED, TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELED},
    TaskState.PAUSED: {TaskState.RUNNING, TaskState.FAILED, TaskState.CANCELED},
}


class InvalidTaskTransition(RuntimeError):
    pass


class Task(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_id: str = Field(default_factory=lambda: new_id("task"))
    capability: str = Field(min_length=3, max_length=80)
    state: TaskState = TaskState.SUBMITTED
    input: dict[str, Any] = Field(default_factory=dict)
    output: dict[str, Any] | None = None
    artifacts: tuple[ArtifactRef, ...] = ()
    error: str | None = Field(default=None, max_length=2_000)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def transition(
        self,
        state: TaskState,
        *,
        output: dict[str, Any] | None = None,
        artifacts: tuple[ArtifactRef, ...] | None = None,
        error: str | None = None,
    ) -> Task:
        if self.state in TERMINAL_TASK_STATES:
            raise InvalidTaskTransition(f"terminal task {self.task_id} cannot transition from {self.state}")
        if state not in _TRANSITIONS.get(self.state, set()):
            raise InvalidTaskTransition(f"invalid task transition {self.state} -> {state}")
        if state == TaskState.COMPLETED and error:
            raise InvalidTaskTransition("completed task cannot carry an error")
        data = self.model_dump()
        data.update(
            {
                "state": state,
                "updated_at": datetime.now(timezone.utc),
                "output": output if output is not None else self.output,
                "artifacts": artifacts if artifacts is not None else self.artifacts,
                "error": error,
            }
        )
        return Task.model_validate(data)
