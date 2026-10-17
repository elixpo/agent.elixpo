"""Deterministic capability registry."""

from __future__ import annotations

from oreoflow.cards import AgentCard, Capability
from oreoflow.policy import PolicyGrant, authorize


class RegistryError(RuntimeError):
    pass


class AgentRegistry:
    def __init__(self, cards: tuple[AgentCard, ...] | list[AgentCard] = ()):
        self._cards: dict[str, AgentCard] = {}
        for card in cards:
            self.register(card)

    def register(self, card: AgentCard) -> None:
        if card.name in self._cards:
            raise RegistryError(f"duplicate agent card: {card.name}")
        self._cards[card.name] = card

    def get(self, name: str) -> AgentCard:
        try:
            return self._cards[name]
        except KeyError as exc:
            raise RegistryError(f"unknown agent: {name}") from exc

    def route(self, capability: str, grant: PolicyGrant | None = None) -> AgentCard:
        grant = grant or PolicyGrant()
        candidates: list[tuple[int, str, AgentCard, Capability]] = []
        for card in self._cards.values():
            for declared in card.capabilities:
                if declared.name == capability:
                    candidates.append((card.concurrency_weight, card.name, card, declared))
        if not candidates:
            raise RegistryError(f"no agent declares capability {capability}")
        denied: list[str] = []
        for _weight, _name, card, declared in sorted(candidates, key=lambda item: (-item[0], item[1])):
            try:
                authorize(card, declared, grant)
                return card
            except RuntimeError as exc:
                denied.append(str(exc))
        raise RegistryError(f"no authorized agent for {capability}: {'; '.join(denied)}")

    def cards(self) -> tuple[AgentCard, ...]:
        return tuple(self._cards[name] for name in sorted(self._cards))
