"""JSON Schema export for transport and SDK interoperability."""

from __future__ import annotations

from typing import Any

from oreoflow.artifacts import ArtifactRef
from oreoflow.cards import AgentCard, Capability
from oreoflow.messages import A2AMessage, BudgetGrant, Endpoint
from oreoflow.policy import PolicyGrant
from oreoflow.runtime import Room
from oreoflow.tasks import Task


def schema_bundle() -> dict[str, dict[str, Any]]:
    """Return JSON Schemas for every portable OreoFlow control-plane record."""
    models = (AgentCard, Capability, Room, Task, A2AMessage, Endpoint, BudgetGrant, PolicyGrant, ArtifactRef)
    return {model.__name__: model.model_json_schema() for model in models}
