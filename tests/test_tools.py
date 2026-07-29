import base64
import json
from unittest.mock import patch

from notion_cli_agent.tools import (
    handle_notion_cli_help,
    handle_notion_cli_run,
    handle_notion_pages_markdown,
    handle_notion_datasources,
    handle_notion_files,
    handle_notion_workers,
)
from notion_cli_agent.helpers import RunResult


def test_help_returns_catalog():
    payload = json.loads(handle_notion_cli_help({"include_catalog": True}))
    assert payload["plugin"] == "notion-cli-agent"
    assert "catalog" in payload


def test_run_delegates_to_helper():
    fake = RunResult(True, ["ntn", "api", "ls"], 0, '{"ok":true}', '', {"ok": True})
    with patch('notion_cli_agent.tools.run_ntn', return_value=fake) as run:
        payload = json.loads(handle_notion_cli_run({"argv": ["api", "ls"]}))
    run.assert_called_once()
    assert payload["ok"] is True


def test_pages_requires_page_id_for_get():
    payload = json.loads(handle_notion_pages_markdown({"action": "get"}))
    assert payload["ok"] is False


def test_datasources_builds_query_command():
    fake = RunResult(True, ["ntn", "datasources", "query"], 0, '', '', None)
    with patch('notion_cli_agent.tools.run_ntn', return_value=fake) as run:
        json.loads(handle_notion_datasources({
            "action": "query",
            "target_id": "ds1",
            "limit": 10,
            "sorts": ["Name asc"],
            "json_output": True,
        }))
    argv = run.call_args.args[0]
    assert argv[:3] == ["datasources", "query", "ds1"]
    assert "--json" in argv


def test_workers_wraps_workers_prefix():
    fake = RunResult(True, ["ntn", "workers", "list"], 0, '', '', None)
    with patch('notion_cli_agent.tools.run_ntn', return_value=fake) as run:
        json.loads(handle_notion_workers({"argv": ["list"]}))
    assert run.call_args.args[0][:2] == ["workers", "list"]


def test_files_requires_filename_for_base64_upload():
    payload = json.loads(handle_notion_files({
        "action": "create",
        "file_base64": base64.b64encode(b'hello').decode('ascii'),
    }))
    assert payload["ok"] is False
    assert "filename is required" in payload["reason"]


def test_files_base64_upload_passes_binary_stdin():
    fake = RunResult(True, ["ntn", "files", "create"], 0, '', '', None)
    with patch('notion_cli_agent.tools.run_ntn', return_value=fake) as run:
        json.loads(handle_notion_files({
            "action": "create",
            "file_base64": base64.b64encode(b'hello world').decode('ascii'),
            "filename": 'note.txt',
            "json_output": True,
        }))
    assert run.call_args.kwargs["stdin_bytes"] == b'hello world'
