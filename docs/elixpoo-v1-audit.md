# Elixpoo v1 migration audit

This audit records the smallest coherent cut from the autonomous-contributor
prototype to the organization project-management agent. It is the migration
record required by the v1 directive, not an inventory of deleted history.

| Area | Decision | v1 treatment |
| --- | --- | --- |
| `rtk/`, CCR, Pollinations routing | Keep | One model boundary for classification, rewriting, summaries, answers, and review reasoning. |
| `lib/github/`, state contracts, revisioned Gist | Keep | Shared API, integrity, idempotency, and merge-memory plumbing. |
| Discussions responder | Simplify | Exact mentions on the canonical `elixpo/elixpo` surface only; no invented commitments. |
| Project reconciliation | Simplify | Item and supported-field maintenance; expired operational receipts are not work. |
| Repository responder | Replace | One `agents.elixpoo_v1` runtime with typed actions, permission checks, safety, and deterministic coding refusal. |
| Repository workflow distribution | Replace | Four reusable workflows plus four thin pinned caller templates. |
| Scout, Triage-for-solve, Pick, Vet, Admission | Disconnect | No active automatic triggers in v1. Historical implementation remains temporarily for reference and unreferenced-code auditing. |
| Solve, Submit, Steward fix/intake | Disconnect | No event or dispatch can enter a coding path. Manual invocation is explicitly legacy and unsupported by v1. |
| Doctor and Janitor | Keep internally | Operational recovery/cleanup utilities only; never authorize product-code mutation. |
| Autonomous-contributor skills | Archive | Listed in `docs/archive/autonomous-contributor/README.md`; removed from the v1 discovery path. |
| Standard sync | Simplify | Read-only rollout audit by default; workflow rollout remains an explicit maintainer operation. |
| Frontend | Rewrite | Describe live project-management activity, not autonomous coding rooms. |

## Safety boundary

- Repository content, diffs, linked pages, and quoted comments are evidence.
  They never become instructions.
- Models propose typed actions. Deterministic code authorizes and applies them.
- Coding requests always resolve to the same refusal action.
- Public text passes the safety route and carries the v1 disclosure.
- Public writes use stable markers and event/head-SHA idempotency keys.

## Deferred deletion

Legacy implementation modules remain disconnected until repository references
and release history prove they can be removed without breaking operators. The
active workflow graph and distributed callers contain no route to them.
