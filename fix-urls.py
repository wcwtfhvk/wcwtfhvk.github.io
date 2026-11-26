#!/usr/bin/env python3
"""Fix Gridea's hardcoded absolute URLs that break CSS on the custom domain.

Run this from anywhere inside the blog repo after regenerating with Gridea:

    python fix-urls.py

What it does:
  1. In every .html file, replace "https://wcwtfhvk.github.io" with "" so
     links become root-relative (e.g. /styles/main.css). Root-relative paths
     work on both the github.io domain and any custom domain, over http/https.
  2. In atom.xml, replace it with "https://blog.404520.xyz" because feed
     readers require absolute URLs.

Then commit and push manually:
    git add -A
    git commit -m "Fix CSS: use root-relative URLs"
    git push origin master
"""

from pathlib import Path

OLD = "https://wcwtfhvk.github.io"
FEED_DOMAIN = "https://blog.404520.xyz"

ROOT = Path(__file__).resolve().parent


def main() -> None:
    html_files = changed = replacements = 0
    for path in ROOT.rglob("*.html"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        count = text.count(OLD)
        if count:
            path.write_text(text.replace(OLD, ""), encoding="utf-8", newline="")
            html_files += 1
            replacements += count
            print(f"  {path.relative_to(ROOT)}: {count}")

    feed = ROOT / "atom.xml"
    feed_count = 0
    if feed.is_file():
        text = feed.read_text(encoding="utf-8")
        feed_count = text.count(OLD)
        if feed_count:
            feed.write_text(
                text.replace(OLD, FEED_DOMAIN), encoding="utf-8", newline=""
            )
            print(f"  atom.xml: {feed_count}")

    print(f"\nDone: {replacements} replacements in {html_files} HTML files, "
          f"{feed_count} in atom.xml.")
    if not replacements and not feed_count:
        print("Nothing to fix - URLs were already correct.")
    else:
        print("\nNext: git add -A && git commit -m 'Fix URLs' && git push origin master")


if __name__ == "__main__":
    main()
