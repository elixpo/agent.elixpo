"""Deterministic capability and delegation policy."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from oreoflow.cards import AgentCard, Capability


class PolicyDenied(RuntimeError):
    pass


class PolicyGrant(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    public_action: bool = False
    approved: bool = False
    delegation_depth: int = Field(default=0, ge=0, le=16)
    scopes: frozenset[str] = Field(default_factory=frozenset)


def authorize(card: AgentCard, capability: Capability, grant: PolicyGrant) -> None:
    if capability.name not in {item.name for item in card.capabilities}:
        raise PolicyDenied(f"{card.name} does not declare capability {capability.name}")
    if capability.public_action and not (grant.public_action and grant.approved):
        raise PolicyDenied("public action requires an explicit approved grant")
    missing = set(capability.required_scopes) - set(grant.scopes)
    if missing:
        raise PolicyDenied(f"missing capability scopes: {sorted(missing)}")
    if grant.delegation_depth > card.max_delegation_depth:
        raise PolicyDenied("delegation depth exceeds the agent card limit")
