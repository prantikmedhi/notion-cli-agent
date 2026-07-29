from __future__ import annotations

import shutil
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "notion_cli_agent"
DST = Path.home() / ".hermes" / "plugins" / "notion-cli-agent"

if DST.exists():
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)
print(f"Installed directory plugin to {DST}")
print("Next: hermes plugins enable notion-cli-agent")
