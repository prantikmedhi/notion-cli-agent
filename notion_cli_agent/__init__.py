from __future__ import annotations

import logging
from pathlib import Path

from .cli import register_cli, slash_command_factory, handle_cli
from .schemas import (
    NOTION_CLI_HELP,
    NOTION_CLI_RUN,
    NOTION_PAGES_MARKDOWN,
    NOTION_DATASOURCES,
    NOTION_FILES,
    NOTION_WORKERS,
)
from .tools import (
    handle_notion_cli_help,
    handle_notion_cli_run,
    handle_notion_pages_markdown,
    handle_notion_datasources,
    handle_notion_files,
    handle_notion_workers,
)

logger = logging.getLogger(__name__)
_SEEN_TOOL_CALLS: list[dict] = []


def _post_tool_call(tool_name, params=None, result=None, **kwargs):
    if tool_name.startswith("notion_"):
        _SEEN_TOOL_CALLS.append({
            "tool_name": tool_name,
            "task_id": kwargs.get("task_id"),
        })
        if len(_SEEN_TOOL_CALLS) > 50:
            _SEEN_TOOL_CALLS.pop(0)


def _register_skills(ctx):
    skills_dir = Path(__file__).parent / "skills"
    for child in sorted(skills_dir.iterdir()):
        skill_md = child / "SKILL.md"
        if child.is_dir() and skill_md.exists():
            ctx.register_skill(child.name, skill_md, f"Bundled Notion CLI skill: {child.name}")


def register(ctx):
    ctx.register_tool(
        name="notion_cli_help",
        toolset="notion_cli_agent",
        schema=NOTION_CLI_HELP,
        handler=handle_notion_cli_help,
        description="Notion CLI doctor and catalog helper",
        emoji="📘",
    )
    ctx.register_tool(
        name="notion_cli_run",
        toolset="notion_cli_agent",
        schema=NOTION_CLI_RUN,
        handler=handle_notion_cli_run,
        description="Generic documented ntn command runner",
        emoji="🧰",
    )
    ctx.register_tool(
        name="notion_pages_markdown",
        toolset="notion_cli_agent",
        schema=NOTION_PAGES_MARKDOWN,
        handler=handle_notion_pages_markdown,
        description="Read and write pages with ntn pages",
        emoji="📝",
    )
    ctx.register_tool(
        name="notion_datasources",
        toolset="notion_cli_agent",
        schema=NOTION_DATASOURCES,
        handler=handle_notion_datasources,
        description="Resolve, retrieve, query, create, and update Notion data sources",
        emoji="🗃️",
    )
    ctx.register_tool(
        name="notion_files",
        toolset="notion_cli_agent",
        schema=NOTION_FILES,
        handler=handle_notion_files,
        description="Upload and inspect Notion file uploads",
        emoji="📎",
    )
    ctx.register_tool(
        name="notion_workers",
        toolset="notion_cli_agent",
        schema=NOTION_WORKERS,
        handler=handle_notion_workers,
        description="Run Notion Workers subcommands",
        emoji="⚙️",
    )
    ctx.register_hook("post_tool_call", _post_tool_call)
    ctx.register_cli_command(
        name="notion-cli",
        help="Notion CLI helpers and command proxy",
        setup_fn=register_cli,
        handler_fn=handle_cli,
        description="Expose Notion CLI helper flows through Hermes CLI",
    )
    ctx.register_command(
        "notion-cli",
        slash_command_factory(ctx),
        description="Run documented ntn commands through the Notion CLI plugin",
        args_hint="run api ls",
    )
    _register_skills(ctx)
    logger.info("notion-cli-agent registered tools, commands, and bundled skills")
