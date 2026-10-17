"""Public OreoFlow control-plane SDK contracts."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from oreoflow import (
    A2AMessage,
    AgentCard,
    AgentRegistry,
    ArtifactRef,
    BudgetGrant,
    Capability,
    Endpoint,
    InvalidTaskTransition,
    LocalCoordinator,
    PolicyGrant,
    RegistryError,
    Task,
    TaskState,
    schema_bundle,
)


def _card(name="writer", *, public_action=False, weight=1):
    return AgentCard(
        name=name,
        description="Draft a repository-grounded technical article",
        version="1.0.0",
        floor="publishing",
        capabilities=(
            Capability(
                name="blog.draft",
                description="Create one technical draft",
                public_action=public_action,
                required_scopes=("content:read",),
            ),
        ),
        model_role="prose",
        concurrency_weight=weight,
    )


def _message(task: Task, **updates):
    values = {
        "building_id": "example",
        "source": Endpoint(floor="intake", room="room-source", agent="router"),
        "destination": Endpoint(floor="publishing", room="room-blog", agent="writer"),
        "kind": "task.request",
        "task_id": task.task_id,
        "capability": task.capability,
        "deadline": datetime.now(timezone.utc) + timedelta(minutes=5),
        "budget": BudgetGrant(tokens=3_000, seconds=300),
        "policy": PolicyGrant(scopes=frozenset({"content:read"})),
        "payload": {"topic": "bounded agent workflows"},
    }
    values.update(updates)
    return A2AMessage(**values).seal()


def test_message_integrity_detects_payload_changes_and_bounds_payloads():
    task = Task(capability="blog.draft")
    message = _message(task)

    assert message.verify()
    changed = message.model_copy(update={"payload": {"topic": "changed"}})
    assert not changed.verify()

    with pytest.raises(ValueError, match="64 KiB"):
        _message(task, payload={"content": "x" * 66_000})


def test_artifacts_are_content_addressed():
    content = b"# Draft\n"
    artifact = ArtifactRef.from_bytes(
        name="draft.md", media_type="text/markdown", uri="state/artifacts/draft.md", content=content
    )

    assert artifact.verify(content)
    assert not artifact.verify(b"changed")


def test_task_transition_graph_protects_terminal_state():
    task = Task(capability="blog.draft")
    task = task.transition(TaskState.ACCEPTED).transition(TaskState.RUNNING)
    task = task.transition(TaskState.COMPLETED, output={"title": "A bounded agent"})

    with pytest.raises(InvalidTaskTransition, match="terminal task"):
        task.transition(TaskState.RUNNING)

    with pytest.raises(InvalidTaskTransition, match="invalid task transition"):
        Task(capability="blog.draft").transition(TaskState.COMPLETED)


def test_registry_routes_deterministically_and_enforces_public_policy():
    registry = AgentRegistry([_card("writer-small", weight=1), _card("writer-large", weight=3)])
    grant = PolicyGrant(scopes=frozenset({"content:read"}))

    assert registry.route("blog.draft", grant).name == "writer-large"

    public_registry = AgentRegistry([_card("publisher", public_action=True)])
    with pytest.raises(RegistryError, match="explicit approved grant"):
        public_registry.route("blog.draft", grant)

    authorized = PolicyGrant(public_action=True, approved=True, scopes=frozenset({"content:read"}))
    assert public_registry.route("blog.draft", authorized).name == "publisher"


@pytest.mark.asyncio
async def test_local_coordinator_dispatches_one_sealed_policy_bound_task():
    card = _card()
    registry = AgentRegistry([card])
    coordinator = LocalCoordinator(registry)

    async def handler(task, _message):
        return task.transition(TaskState.RUNNING).transition(
            TaskState.COMPLETED, output={"title": "Bounded workflows"}
        )

    coordinator.bind(card, handler)
    task = Task(capability="blog.draft", input={"topic": "agents"})

    completed = await coordinator.dispatch(task, _message(task))

    assert completed.state == TaskState.COMPLETED
    assert completed.output == {"title": "Bounded workflows"}


def test_sdk_exports_transport_json_schemas():
    schemas = schema_bundle()

    assert set(schemas) >= {"AgentCard", "Room", "Task", "A2AMessage", "ArtifactRef"}
    assert schemas["A2AMessage"]["properties"]["schema_id"]["const"] == "oreoflow.a2a/v1"
