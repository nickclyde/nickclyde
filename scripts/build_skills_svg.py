#!/usr/bin/env python3
"""Build assets/skills.svg: a skillicons.dev grid plus tiles for icons it lacks.

skillicons.dev renders unknown ids as empty slots, so the missing icons are
drawn from Simple Icons in the same dark rounded tile style and dropped into
those slots. Run from the repo root after editing ICONS.
"""

import re
import urllib.request

ICONS = [
    "arduino", "aws", "azure", "bash", "css", "cypress", "docker", "express",
    "fastapi", "git", "go", "graphql", "html", "huggingface", "hugo", "java",
    "jekyll", "jest", "js", "kubernetes", "linux", "mysql", "nextjs", "nginx",
    "nodejs", "postgres", "py", "pytorch", "rails", "react", "ruby", "sass",
    "spring", "sqlite", "tailwind", "ts",
]

# Icons missing from skillicons.dev, mapped to their Simple Icons slug.
SIMPLE_ICONS = {"huggingface": "huggingface", "hugo": "hugo", "jekyll": "jekyll"}

PER_LINE = 12
TILE_BG = "#242938"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "build-skills-svg"})
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode()


def simple_icon_tile(slug):
    svg = fetch(f"https://cdn.simpleicons.org/{slug}")
    fill = re.search(r'fill="([^"]+)"', svg).group(1)
    path = re.search(r'<path d="([^"]+)"', svg).group(1)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" fill="none" viewBox="0 0 256 256">'
        f'<rect width="256" height="256" fill="{TILE_BG}" rx="60"/>'
        f'<svg x="48" y="48" width="160" height="160" viewBox="0 0 24 24"><path fill="{fill}" d="{path}"/></svg>'
        "</svg>"
    )


def main():
    grid = fetch(f"https://skillicons.dev/icons?i={','.join(ICONS)}&perline={PER_LINE}")
    tiles = iter(simple_icon_tile(SIMPLE_ICONS[i]) for i in ICONS if i in SIMPLE_ICONS)
    grid = re.sub(r"\bundefined\b", lambda _: next(tiles), grid)
    if "undefined" in grid:
        raise SystemExit("skillicons.dev returned an unknown icon not in SIMPLE_ICONS")
    with open("assets/skills.svg", "w") as f:
        f.write(grid.strip() + "\n")


if __name__ == "__main__":
    main()
