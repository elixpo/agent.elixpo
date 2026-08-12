"""Manage the human admission boundary after a successful autonomous Vet."""

from __future__ import annotations

import argparse
import asyncio
import json
import os

import structlog

from agents.admission.core import AdmissionRejected, approve, propose

log = structlog.get_logger()


async def _run(mode: str, issue_number: int | None) -> int:
    from lib.config import settings
    from lib.github.api import GitHubAPI
    from lib.state.store import StateStore
    from rtk import Budget, Router

    control_repo = settings.github.control_repo or os.getenv("GITHUB_REPOSITORY", "")
    if not settings.github.token or "/" not in control_repo:
        log.error("admission.missing_configuration")
        return 1
    store = StateStore(settings.state_dir)
    api = GitHubAPI.from_token(settings.github.token)
    router = None
    try:
        if mode == "propose":
            if not settings.pollinations.api_key:
                raise AdmissionRejected("proposal safety review requires ELIXPO_POLLINATIONS_API_KEY")
            router = Router.from_settings("admission", budget=Budget("admission", limit=500))
            result = await propose(store, api, router, control_repo)
        else:
            if issue_number is None:
                raise AdmissionRejected("approve requires --issue-number")
            owner, repo = control_repo.split("/", 1)
            result = approve(store, await api.get_issue(owner, repo, issue_number))
    except Exception as exc:
        log.error("admission.failed", mode=mode, error=str(exc))
        return 1
    finally:
        await api.close()
        if router is not None:
            await router.aclose()
    log.info("admission.done", mode=mode, status=result["status"], key=result["key"])
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Create or approve one OreoFlow admission")
    parser.add_argument("mode", choices=("propose", "approve"))
    parser.add_argument("--issue-number", type=int)
    args = parser.parse_args()
    raise SystemExit(asyncio.run(_run(args.mode, args.issue_number)))


if __name__ == "__main__":
    main()
