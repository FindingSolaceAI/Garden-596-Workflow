#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Garden Regeneration Test
-------------------------
Reads a folder of JSON metadata files (the 596 archive)
and rebuilds a new world-tree (597) on disk.

Author: Shayna & Solace
License: MIT
Version: 1.0
"""

import os
import json
from pathlib import Path
from datetime import datetime


# ---- CONFIG ----------------------------------------------------------
SOURCE_DIR = Path("garden_596/metadata")   # where your .json metadata files live
TARGET_DIR = Path("garden_597")            # where the new structure will be created
PLACEHOLDER_TEXT = "Placeholder for actual file or link."
# ---------------------------------------------------------------------


def safe_name(name: str) -> str:
    """Sanitize folder/file names for filesystem safety."""
    keep = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    return "".join(c if c in keep else "_" for c in name)[:64]


def build_world():
    """Main regeneration routine."""
    if not SOURCE_DIR.exists():
        print(f"⚠️  Source folder '{SOURCE_DIR}' not found.")
        return

    TARGET_DIR.mkdir(exist_ok=True)
    manifest_path = TARGET_DIR / f"manifest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    count = 0
    with manifest_path.open("w", encoding="utf-8") as manifest:
        for file in SOURCE_DIR.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"❌ Failed to read {file.name}: {e}")
                continue

            # derive paths
            author = safe_name(data.get("author", {}).get("name", "unknown"))
            world = safe_name(data.get("world", "unassigned"))
            title = safe_name(data.get("title", "untitled"))
            category = safe_name(data.get("type", "misc"))

            # create nested directories
            dest_dir = TARGET_DIR / world / author / category
            dest_dir.mkdir(parents=True, exist_ok=True)

            # create placeholder
            placeholder_file = dest_dir / f"{title}.txt"
            placeholder_file.write_text(PLACEHOLDER_TEXT, encoding="utf-8")

            manifest.write(f"{file.name} → {placeholder_file}\n")
            count += 1

    print(f"\n🌿 Regeneration complete.")
    print(f"   Files processed: {count}")
    print(f"   New world stored in: {TARGET_DIR.resolve()}")
    print(f"   Manifest log created at: {manifest_path.name}")


if __name__ == "__main__":
    build_world()
