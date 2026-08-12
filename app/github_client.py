import os
import requests


GITHUB_API = "https://api.github.com"


def get_headers():
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        raise RuntimeError(
            "GITHUB_TOKEN environment variable is not set."
        )

    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2026-03-10",
    }


def github_get(url, params=None):
    response = requests.get(
        url,
        headers=get_headers(),
        params=params,
        timeout=30,
    )

    if not response.ok:
        raise RuntimeError(
            f"GitHub API error {response.status_code}: "
            f"{response.text}"
        )

    content_type = response.headers.get("content-type", "")

    if "application/json" in content_type:
        return response.json()

    return response.text