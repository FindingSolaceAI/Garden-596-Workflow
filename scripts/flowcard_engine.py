#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flowcard Engine
---------------
Reads Garden metadata (.json) and generates human-readable summaries or
README snippets for Notion, GitHub, or in-world campfire threads.

Author: Shayna & Solace
License: MIT
Version: 0.1
"""

import json
import os
from pathlib import Path
from datetime import datetime

SOURCE_DIR = Path("garden_596/metadata")
OUTPUT_DIR = Path("docs/flowcards")
TEMPLATE_FILE = Path("docs/templates/flowcard_template.md")

DEFAULT_TEMPLATE = """\
# {title}
*World:* {world}  
*Type:* {type}  
*Author:* {author} ({role})  
*Created:* {created}  
*Last Updated:* {updated}  

---

### 🌿 Summary
{summary}

### 🧩 Tags
{tags}

### 🔗 Links
- [Notion]({notion_url})
- [GitHub]({github_url})

---
*(Generated automatically by Flowcard Engine on {timestamp})*
"""

def load_template() -> str:
    """Load a markdown template, or fall back to DEFAULT_TEMPLATE."""
    if TEMPLATE_FILE.exists():
        return TEMPLATE_FILE.read_text(encoding="utf-8")
    return DEFAULT_TEMPLATE

def make_safe_name(name: str) -> str:
    """Sanitize file names."""
    keep = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    return "".join(c if c in keep else "_" for c in name)[:64]

def build_flowcard(data: dict, template: str) -> str:
    """Render markdown card from metadata JSON."""
    return template.format(
        title=data.get("title", "Untitled"),
        world=data.get("world", "unknown"),
        type=data.get("type", "misc"),
        author=data.get("author", {}).get("name", "unknown"),
        role=data.get("author", {}).get("role", ""),
        created=data.get("created", ""),
        updated=data.get("updated", ""),
        summary=data.get("metadata", {}).get("summary", "No summary."),
        tags=", ".join(data.get("metadata", {}).get("tags", [])),
        notion_url=data.get("links", {}).get("notion_url", "#"),
        github_url=data.get("links", {}).get("github_url", "#"),
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

def generate_all():
    """Generate flowcards for every metadata file in SOURCE_DIR."""
    if not SOURCE_DIR.exists():
        print(f"⚠️  Metadata folder '{SOURCE_DIR}' not found.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    template = load_template()

    for file in SOURCE_DIR.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        flowcard_md = build_flowcard(data, template)
        safe_title = make_safe_name(data.get("title", "untitled"))
        output_file = OUTPUT_DIR / f"{safe_title}.md"
        output_file.write_text(flowcard_md, encoding="utf-8")
        print(f"✅ Flowcard created: {output_file}")

    print("\n🌊 Flowcard generation complete.")
    print(f"Output folder: {OUTPUT_DIR}")

if __name__ == "__main__":
    generate_all()
