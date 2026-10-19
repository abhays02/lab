"""Assemble the dependency-free website and its public research evidence."""

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "dist" / "site"
EXPERIMENTS = (
    "barren-plateaus",
    "double-descent",
    "colibri-glm",
    "sorting-network-depth",
    "quantum-advantage-boundary",
    "emergence-mirage",
)
PUBLIC_SUFFIXES = {".svg", ".gif", ".png", ".json", ".md", ".py"}


def build():
    if not (ROOT / "site" / "index.html").is_file():
        raise FileNotFoundError("The website source needs site/index.html")
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    shutil.copytree(ROOT / "site", OUTPUT)
    for name in EXPERIMENTS:
        destination = OUTPUT / name
        destination.mkdir()
        for source in (ROOT / name).iterdir():
            if source.is_file() and source.suffix in PUBLIC_SUFFIXES:
                shutil.copy2(source, destination / source.name)
    shutil.copytree(ROOT / "assets", OUTPUT / "assets")
    (OUTPUT / "docs").mkdir()
    shutil.copy2(ROOT / "docs" / "RESEARCH_NOTEBOOK.md", OUTPUT / "docs")
    shutil.copy2(ROOT / "README.md", OUTPUT / "README.md")
    (OUTPUT / ".nojekyll").touch()
    print(f"Built website: {OUTPUT}")


if __name__ == "__main__":
    build()
