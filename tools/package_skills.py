#!/usr/bin/env python3
"""
package_skills.py - build standalone skill zips for platforms that install
skills one at a time (for example claude.ai chat custom skills).

When the plugin is installed whole, setup, tailor and follow-up reach the
tracker at ../job-hunt/scripts/tracker.py. A standalone upload has no sibling
folders, so this script copies tracker.py into each skill that needs it.

Usage (from the repository root):
  python tools/package_skills.py            # writes dist/<skill>.zip
  python tools/package_skills.py --out DIR

Uses only the Python standard library.
"""
import argparse
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
TRACKER = SKILLS / "job-hunt" / "scripts" / "tracker.py"
NEEDS_TRACKER = {"setup", "tailor", "follow-up"}
SKIP = {"__pycache__", ".DS_Store"}


def build(skill_dir: Path, out_dir: Path) -> Path:
    name = skill_dir.name
    target = out_dir / f"{name}.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(skill_dir.rglob("*")):
            if f.is_file() and not (set(f.parts) & SKIP) and f.suffix != ".pyc":
                z.write(f, Path(name) / f.relative_to(skill_dir))
        if name in NEEDS_TRACKER:
            z.write(TRACKER, Path(name) / "scripts" / "tracker.py")
    return target


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "dist"))
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    if not TRACKER.exists():
        sys.exit(f"tracker.py not found at {TRACKER}")
    for d in sorted(p for p in SKILLS.iterdir() if (p / "SKILL.md").exists()):
        print(build(d, out))


if __name__ == "__main__":
    main()
