"""Versioned agent cards and capability declarations."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Capability(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(pattern=r"^[a-z][a-z0-9_.-]{2,80}$")
    description: str = Field(min_length=1, max_length=500)
    input_schema: dict[str, Any] = Field(default_factory=dict)
    output_schema: dict[str, Any] = Field(default_factory=dict)
    public_action: bool = False
    required_scopes: tuple[str, ...] = ()


class AgentCard(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(pattern=r"^[a-z][a-z0-9_-]{1,63}$")
    description: str = Field(min_length=1, max_length=500)
    version: str = Field(pattern=r"^\d+\.\d+\.\d+$")
    floor: str = Field(min_length=1, max_length=80)
    capabilities: tuple[Capability, ...] = Field(min_length=1)
    model_role: str | None = Field(default=None, max_length=80)
    default_token_budget: int = Field(default=0, ge=0)
    default_timeout_seconds: int = Field(default=300, ge=1, le=86_400)
    max_delegation_depth: int = Field(default=1, ge=0, le=16)
    concurrency_weight: int = Field(default=1, ge=1, le=100)
    transports: tuple[str, ...] = ("local",)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("capabilities")
    @classmethod
    def unique_capabilities(cls, capabilities: tuple[Capability, ...]) -> tuple[Capability, ...]:
        names = [item.name.casefold() for item in capabilities]
        if len(names) != len(set(names)):
            raise ValueError("agent card contains duplicate capabilities")
        return capabilities
