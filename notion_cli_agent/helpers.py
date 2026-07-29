from __future__ import annotations

import base64
import json
import os
import shlex
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

PLUGIN_NAME = "notion-cli-agent"

CATALOG: dict[str, Any] = {
    "install": [
        "curl -fsSL https://ntn.dev | bash",
        "ntn --version",
    ],
    "auth": {
        "commands": ["ntn login", "ntn logout"],
        "env": [
            "NOTION_API_TOKEN",
            "NOTION_KEYRING",
            "NOTION_WORKSPACE_ID",
            "NOTION_WORKERS_CONFIG_FILE",
            "NOTION_API_VERSION",
        ],
    },
    "api": ["ntn api <path>", "ntn api ls"],
    "datasources": [
        "ntn datasources resolve <database-id>",
        "ntn datasources query <data-source-id>",
    ],
    "pages": [
        "ntn pages get <page-id>",
        "ntn pages create --parent <ref>",
        "ntn pages edit <page-id>",
        "ntn pages trash <page-id>",
    ],
    "files": [
        "ntn files create",
        "ntn files get <upload-id>",
        "ntn files list",
    ],
    "workers": [
        "ntn workers new [directory]",
        "ntn workers deploy",
        "ntn workers list",
        "ntn workers get [worker-id]",
        "ntn workers create",
        "ntn workers delete [worker-id]",
        "ntn workers exec <key>",
        "ntn workers capabilities list",
        "ntn workers tui",
        "ntn workers sync status|trigger|pause|resume|state get|state reset",
        "ntn workers env set|list|unset|pull|push",
        "ntn workers oauth start|token|show-redirect-url",
        "ntn workers runs list|logs",
        "ntn workers webhooks list",
    ],
}

ALLOWED_TOP_LEVEL = {
    "api",
    "datasources",
    "pages",
    "files",
    "workers",
    "doctor",
    "login",
    "logout",
    "update",
    "--version",
    "-V",
    "--help",
    "-h",
}

DESTRUCTIVE_PATTERNS = {
    ("pages", "trash"),
    ("workers", "delete"),
    ("workers", "env", "unset"),
    ("workers", "sync", "state", "reset"),
    ("logout",),
}

@dataclass
class RunResult:
    ok: bool
    command: list[str]
    exit_code: int
    stdout: str
    stderr: str
    parsed_json: Any = None
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "command": self.command,
            "exit_code": self.exit_code,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "parsed_json": self.parsed_json,
            "reason": self.reason,
        }


def package_root() -> Path:
    return Path(__file__).resolve().parent


def skills_root() -> Path:
    return package_root() / "skills"


def find_ntn() -> str | None:
    override = os.getenv("NOTION_CLI_BIN")
    if override:
        return override
    return shutil.which("ntn")


def cli_installed() -> bool:
    return find_ntn() is not None


def shell_split(raw: str) -> list[str]:
    return shlex.split(raw, posix=(os.name != "nt"))


def ensure_allowed(argv: Iterable[str]) -> tuple[bool, str]:
    items = [str(x) for x in argv if str(x).strip()]
    if not items:
        return False, "No Notion CLI command provided"
    top = items[0]
    if top not in ALLOWED_TOP_LEVEL:
        return False, f"Top-level ntn command '{top}' is not in the documented allow-list"
    return True, ""


def is_destructive(argv: Iterable[str]) -> bool:
    items = tuple(str(x) for x in argv if str(x).strip())
    return any(items[:len(pattern)] == pattern for pattern in DESTRUCTIVE_PATTERNS)


def maybe_json(text: str) -> Any:
    text = (text or "").strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        return None


def doctor() -> dict[str, Any]:
    ntn = find_ntn()
    env = {k: bool(os.getenv(k)) for k in [
        "NOTION_API_TOKEN",
        "NOTION_KEYRING",
        "NOTION_WORKSPACE_ID",
        "NOTION_WORKERS_CONFIG_FILE",
        "NOTION_API_VERSION",
    ]}
    auth_file = Path.home() / ".config" / "notion" / "auth.json"
    return {
        "plugin": PLUGIN_NAME,
        "ntn_found": bool(ntn),
        "ntn_path": ntn,
        "auth_file_exists": auth_file.exists(),
        "env": env,
        "catalog_groups": sorted(CATALOG.keys()),
    }


def run_ntn(
    argv: list[str],
    *,
    stdin_text: str | None = None,
    stdin_bytes: bytes | None = None,
    timeout: int = 180,
    confirm_destructive: bool = False,
    extra_env: dict[str, str] | None = None,
) -> RunResult:
    allowed, reason = ensure_allowed(argv)
    if not allowed:
        return RunResult(False, ["ntn", *argv], 2, "", "", reason=reason)
    if is_destructive(argv) and not confirm_destructive:
        return RunResult(
            False,
            ["ntn", *argv],
            2,
            "",
            "",
            reason="Destructive Notion CLI command blocked unless confirm_destructive=true",
        )
    ntn = find_ntn()
    if not ntn:
        return RunResult(
            False,
            ["ntn", *argv],
            127,
            "",
            "ntn executable not found",
            reason="Install Notion CLI first: curl -fsSL https://ntn.dev | bash",
        )
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    use_text = stdin_bytes is None
    proc = subprocess.run(
        [ntn, *argv],
        input=stdin_text if use_text else stdin_bytes,
        text=use_text,
        capture_output=True,
        timeout=timeout,
        env=env,
    )
    stdout = proc.stdout or ""
    stderr = proc.stderr or ""
    parsed = maybe_json(stdout)
    return RunResult(
        ok=(proc.returncode == 0),
        command=[ntn, *argv],
        exit_code=proc.returncode,
        stdout=stdout,
        stderr=stderr,
        parsed_json=parsed,
        reason="",
    )
