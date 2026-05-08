#!/usr/bin/env python3
import os
from datetime import datetime, timedelta, timezone

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("GitHub Intelligence")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO = os.getenv("GITHUB_REPO", "")


def _headers() -> dict:
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers


def _get(path: str, params: dict | None = None):
    url = f"https://api.github.com{path}"
    r = httpx.get(url, headers=_headers(), params=params, timeout=15)
    r.raise_for_status()
    return r.json()


def _repo(repo: str) -> str:
    resolved = repo or GITHUB_REPO
    if not resolved:
        raise ValueError("No repo specified. Pass repo='owner/name' or set GITHUB_REPO env var.")
    return resolved


@mcp.tool()
def get_repo_overview(repo: str = "") -> dict:
    """Return high-level metadata for a GitHub repository."""
    data = _get(f"/repos/{_repo(repo)}")
    return {
        "name": data["full_name"],
        "description": data.get("description"),
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "open_issues_count": data["open_issues_count"],
        "primary_language": data.get("language"),
        "topics": data.get("topics", []),
        "default_branch": data["default_branch"],
        "created_at": data["created_at"],
        "updated_at": data["updated_at"],
    }


@mcp.tool()
def get_recent_commits(repo: str = "", days: int = 7, limit: int = 30) -> list[dict]:
    """Return commits from the past N days, newest first."""
    since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    data = _get(f"/repos/{_repo(repo)}/commits", {"since": since, "per_page": limit})
    return [
        {
            "sha": c["sha"][:8],
            "message": c["commit"]["message"].split("\n")[0],
            "author": c["commit"]["author"]["name"],
            "date": c["commit"]["author"]["date"],
        }
        for c in data
    ]


@mcp.tool()
def get_open_issues(repo: str = "", limit: int = 30) -> list[dict]:
    """Return open issues (excluding pull requests), sorted by most recently updated."""
    data = _get(
        f"/repos/{_repo(repo)}/issues",
        {"state": "open", "per_page": limit, "sort": "updated"},
    )
    return [
        {
            "number": i["number"],
            "title": i["title"],
            "author": i["user"]["login"],
            "labels": [l["name"] for l in i["labels"]],
            "comments": i["comments"],
            "created_at": i["created_at"],
            "updated_at": i["updated_at"],
        }
        for i in data
        if "pull_request" not in i
    ]


@mcp.tool()
def get_open_pull_requests(repo: str = "", limit: int = 30) -> list[dict]:
    """Return open pull requests with author, draft status, and requested reviewers."""
    data = _get(
        f"/repos/{_repo(repo)}/pulls",
        {"state": "open", "per_page": limit, "sort": "updated"},
    )
    return [
        {
            "number": pr["number"],
            "title": pr["title"],
            "author": pr["user"]["login"],
            "draft": pr.get("draft", False),
            "labels": [l["name"] for l in pr["labels"]],
            "requested_reviewers": [r["login"] for r in pr.get("requested_reviewers", [])],
            "created_at": pr["created_at"],
            "updated_at": pr["updated_at"],
        }
        for pr in data
    ]


if __name__ == "__main__":
    mcp.run()
