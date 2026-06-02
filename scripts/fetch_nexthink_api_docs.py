"""Fetch a versioned snapshot of the official Nexthink API documentation."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL = "https://docs.nexthink.com/api"
OUTPUT_DIR = Path("specs/vendor/nexthink-api-docs/current")
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
)

DOCS = {
    "sitemap.md": f"{BASE_URL}/sitemap.md",
    "llms-full.txt": f"{BASE_URL}/llms-full.txt",
    "readme.md": f"{BASE_URL}/readme.md",
    "authentication-token.md": f"{BASE_URL}/getting-authentication-token.md",
    "campaigns.md": f"{BASE_URL}/campaigns.md",
    "campaigns-models.md": f"{BASE_URL}/campaigns/models.md",
    "data-management.md": f"{BASE_URL}/data-management.md",
    "data-management-models.md": f"{BASE_URL}/data-management/models.md",
    "enrichment.md": f"{BASE_URL}/enrichment.md",
    "enrichment-models.md": f"{BASE_URL}/enrichment/models.md",
    "nql.md": f"{BASE_URL}/nql.md",
    "nql-models.md": f"{BASE_URL}/nql/models.md",
    "remote-actions.md": f"{BASE_URL}/remote-actions.md",
    "remote-actions-models.md": f"{BASE_URL}/remote-actions/models.md",
    "workflows.md": f"{BASE_URL}/workflows.md",
    "workflows-models.md": f"{BASE_URL}/workflows/models.md",
    "spark.md": f"{BASE_URL}/spark.md",
    "spark-handoff-api.md": f"{BASE_URL}/spark/handoff-api.md",
    "spark-models.md": f"{BASE_URL}/spark/models.md",
}


def fetch(url: str) -> str:
    """Fetch a documentation URL as text."""
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:  # noqa: S310 - trusted official docs URL list
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset)


def main() -> int:
    """Fetch all configured documentation pages."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {
        "base_url": BASE_URL,
        "user_agent": USER_AGENT,
        "documents": [],
    }

    failures: list[str] = []
    for filename, url in DOCS.items():
        target = OUTPUT_DIR / filename
        try:
            content = fetch(url)
        except (HTTPError, URLError, TimeoutError) as error:
            failures.append(f"{url}: {error}")
            continue

        target.write_text(content, encoding="utf-8")
        manifest["documents"].append(
            {
                "filename": filename,
                "url": url,
                "bytes": len(content.encode("utf-8")),
            }
        )
        print(f"fetched {url} -> {target}")

    (OUTPUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    if failures:
        print("Failures:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
