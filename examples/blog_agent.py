"""Minimal policy-bound blogging agent built with the OreoFlow SDK."""

from __future__ import annotations

import asyncio

from oreoflow import (
    A2AMessage,
    AgentCard,
    AgentRegistry,
    Capability,
    Endpoint,
    LocalCoordinator,
    PolicyGrant,
    Task,
    TaskState,
)

BLOG_WRITER = AgentCard(
    name="blog_writer",
    description="Draft repository-grounded technical posts",
    version="1.0.0",
    floor="publishing",
    capabilities=(
        Capability(
            name="blog.draft",
            description="Create one Markdown blog draft",
            required_scopes=("content:read",),
        ),
    ),
    model_role="prose",
    default_token_budget=8_000,
)


async def draft(task: Task, _message: A2AMessage) -> Task:
    """Replace this deterministic sample with a bounded Router call and tools."""
    running = task.transition(TaskState.RUNNING)
    topic = str(task.input.get("topic") or "OreoFlow")
    return running.transition(
        TaskState.COMPLETED,
        output={"media_type": "text/markdown", "content": f"# {topic}\n\nDraft ready for review.\n"},
    )


async def main() -> None:
    registry = AgentRegistry([BLOG_WRITER])
    coordinator = LocalCoordinator(registry)
    coordinator.bind(BLOG_WRITER, draft)
    grant = PolicyGrant(scopes=frozenset({"content:read"}))
    task = Task(capability="blog.draft", input={"topic": "Building bounded agent workflows"})
    message = A2AMessage(
        building_id="example-building",
        source=Endpoint(floor="intake", room="room-intake", agent="router"),
        destination=Endpoint(floor="publishing", room="room-blog", agent=BLOG_WRITER.name),
        kind="task.request",
        task_id=task.task_id,
        capability=task.capability,
        policy=grant,
        payload=task.input,
    ).seal()
    result = await coordinator.dispatch(task, message)
    print(result.output["content"] if result.output else "")


if __name__ == "__main__":
    asyncio.run(main())
