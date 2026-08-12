"""Immutable, content-addressed artifact references."""

from __future__ import annotations

import hashlib
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from oreoflow.ids import new_id


class ArtifactRef(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    artifact_id: str = Field(default_factory=lambda: new_id("artifact"))
    name: str = Field(min_length=1, max_length=200)
    media_type: str = Field(min_length=1, max_length=120)
    uri: str = Field(min_length=1, max_length=2_000)
    digest: str = Field(pattern=r"^sha256:[0-9a-f]{64}$")
    size: int = Field(ge=0)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_bytes(cls, *, name: str, media_type: str, uri: str, content: bytes, **kwargs) -> ArtifactRef:
        digest = hashlib.sha256(content).hexdigest()
        return cls(name=name, media_type=media_type, uri=uri, digest=f"sha256:{digest}", size=len(content), **kwargs)

    def verify(self, content: bytes) -> bool:
        return self.digest == f"sha256:{hashlib.sha256(content).hexdigest()}" and self.size == len(content)
