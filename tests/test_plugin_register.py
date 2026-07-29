from pathlib import Path

import notion_cli_agent


class FakeCtx:
    def __init__(self):
        self.tools = []
        self.hooks = []
        self.cli = []
        self.commands = []
        self.skills = []

    def register_tool(self, **kwargs):
        self.tools.append(kwargs["name"])

    def register_hook(self, name, callback):
        self.hooks.append(name)

    def register_cli_command(self, **kwargs):
        self.cli.append(kwargs["name"])

    def register_command(self, name, handler, description="", args_hint=""):
        self.commands.append(name)

    def register_skill(self, name, path, description=""):
        self.skills.append((name, Path(path)))


def test_register_wires_tools_commands_hooks_and_skills():
    ctx = FakeCtx()
    notion_cli_agent.register(ctx)
    assert set(ctx.tools) == {
        "notion_cli_help",
        "notion_cli_run",
        "notion_pages_markdown",
        "notion_datasources",
        "notion_files",
        "notion_workers",
    }
    assert "post_tool_call" in ctx.hooks
    assert "notion-cli" in ctx.cli
    assert "notion-cli" in ctx.commands
    skill_names = {name for name, _ in ctx.skills}
    assert skill_names == {
        "notion-cli-overview",
        "notion-cli-pages",
        "notion-cli-datasources",
        "notion-cli-files-workers",
    }
    for _, path in ctx.skills:
        assert path.exists()
