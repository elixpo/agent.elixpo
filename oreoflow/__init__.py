"""Stable public framework API for building Pollinations-backed agents.

Application repositories should import from :mod:`oreoflow`, not the internal
``rtk`` modules. Internal modules may evolve while this surface remains stable.
"""

__version__ = "1.3.0"

from rtk.budget import Budget, BudgetExceeded
from rtk.client import LLMClient
from rtk.ledger import TokenLedger
from rtk.models import ChatCompletionChunk, ChatCompletionResponse, Message, ToolDef, Usage
from rtk.router import Effort, RoleNotFound, Router, load_models_config

from oreoflow.artifacts import ArtifactRef
from oreoflow.cards import AgentCard, Capability
from oreoflow.ids import IdKind, new_id
from oreoflow.messages import A2AMessage, BudgetGrant, Endpoint, Integrity, MessageKind
from oreoflow.policy import PolicyDenied, PolicyGrant, authorize
from oreoflow.registry import AgentRegistry, RegistryError
from oreoflow.runtime import AgentHandler, LocalCoordinator, MessageStore, Room, Transport
from oreoflow.schemas import schema_bundle
from oreoflow.tasks import TERMINAL_TASK_STATES, InvalidTaskTransition, Task, TaskState

__all__ = [
    "Budget",
    "BudgetGrant",
    "BudgetExceeded",
    "ChatCompletionChunk",
    "ChatCompletionResponse",
    "A2AMessage",
    "AgentCard",
    "AgentHandler",
    "AgentRegistry",
    "ArtifactRef",
    "Capability",
    "Effort",
    "Endpoint",
    "IdKind",
    "Integrity",
    "InvalidTaskTransition",
    "LLMClient",
    "Message",
    "MessageKind",
    "MessageStore",
    "LocalCoordinator",
    "PolicyDenied",
    "PolicyGrant",
    "RegistryError",
    "RoleNotFound",
    "Router",
    "Room",
    "TERMINAL_TASK_STATES",
    "Task",
    "TaskState",
    "TokenLedger",
    "ToolDef",
    "Transport",
    "Usage",
    "load_models_config",
    "new_id",
    "schema_bundle",
    "authorize",
    "__version__",
]
