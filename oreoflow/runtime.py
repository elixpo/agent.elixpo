"""Adapter protocols and one policy-bound local coordinator."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field

from oreoflow.cards import AgentCard
from oreoflow.ids import new_id
from oreoflow.messages import A2AMessage
from oreoflow.policy import PolicyGrant
from oreoflow.registry import AgentRegistry
from oreoflow.tasks import Task, TaskState


class MessageStore(Protocol):
    async def put_if_absent(self, message: A2AMessage) -> bool: ...


class Transport(Protocol):
    async def send(self, message: A2AMessage) -> None: ...


AgentHandler = Callable[[Task, A2AMessage], Awaitable[Task]]


class Room(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    room_id: str = Field(default_factory=lambda: new_id("room"))
    floor: str = Field(min_length=1, max_length=80)
    objective: str = Field(min_length=1, max_length=1_000)
    participants: tuple[str, ...] = ()
    token_budget: int = Field(default=0, ge=0)
    timeout_seconds: int = Field(default=900, ge=1, le=86_400)


class LocalCoordinator:
    """Small embeddable runtime; durable stores/transports remain adapters."""

    def __init__(self, registry: AgentRegistry):
        self.registry = registry
        self._handlers: dict[str, AgentHandler] = {}

    def bind(self, card: AgentCard, handler: AgentHandler) -> None:
        registered = self.registry.get(card.name)
        if registered != card:
            raise ValueError("handler card does not match the registered card")
        self._handlers[card.name] = handler

    async def dispatch(self, task: Task, message: A2AMessage, grant: PolicyGrant | None = None) -> Task:
        if not message.verify():
            raise ValueError("message is not sealed or failed integrity verification")
        if message.task_id != task.task_id or message.capability != task.capability:
            raise ValueError("task and message identity do not match")
        card = self.registry.route(task.capability, grant or message.policy)
        handler = self._handlers.get(card.name)
        if handler is None:
            raise RuntimeError(f"agent {card.name} has no bound handler")
        accepted = task if task.state == TaskState.ACCEPTED else task.transition(TaskState.ACCEPTED)
        return await handler(accepted, message)
