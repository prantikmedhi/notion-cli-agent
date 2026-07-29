from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any

from .helpers import CATALOG, doctor, run_ntn


def _dump(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False)


def handle_notion_cli_help(args: dict[str, Any], **kwargs) -> str:
    del kwargs
    payload = doctor()
    if args.get("include_catalog", True):
        payload["catalog"] = CATALOG
    return _dump(payload)


def handle_notion_cli_run(args: dict[str, Any], **kwargs) -> str:
    del kwargs
    result = run_ntn(
        list(args.get("argv") or []),
        stdin_text=args.get("stdin"),
        timeout=int(args.get("timeout", 180)),
        confirm_destructive=bool(args.get("confirm_destructive", False)),
    )
    return _dump(result.to_dict())


def handle_notion_pages_markdown(args: dict[str, Any], **kwargs) -> str:
    del kwargs
    action = args.get("action")
    json_output = bool(args.get("json_output", False))
    argv: list[str] = ["pages", str(action)]
    stdin_text = None
    if action == "get":
        if not args.get("page_id"):
            return _dump({"ok": False, "reason": "page_id is required for pages get"})
        argv.append(str(args["page_id"]))
        if json_output:
            argv.append("--json")
    elif action == "create":
        if not args.get("parent"):
            return _dump({"ok": False, "reason": "parent is required for pages create"})
        argv.extend(["--parent", str(args["parent"])])
        content = args.get("content")
        if content:
            argv.extend(["--content", str(content)])
        else:
            stdin_text = ""
    elif action == "edit":
        if not args.get("page_id"):
            return _dump({"ok": False, "reason": "page_id is required for pages edit"})
        argv.append(str(args["page_id"]))
        content = args.get("content")
        if content:
            argv.extend(["--content", str(content)])
        else:
            stdin_text = ""
        if args.get("allow_deleting_content"):
            argv.append("--allow-deleting-content")
    elif action == "trash":
        if not args.get("page_id"):
            return _dump({"ok": False, "reason": "page_id is required for pages trash"})
        argv.append(str(args["page_id"]))
        argv.append("--yes")
    else:
        return _dump({"ok": False, "reason": f"Unsupported pages action: {action}"})
    result = run_ntn(
        argv,
        stdin_text=stdin_text,
        confirm_destructive=bool(args.get("confirm_destructive", False)),
    )
    return _dump(result.to_dict())


def handle_notion_datasources(args: dict[str, Any], **kwargs) -> str:
    del kwargs
    action = args.get("action")
    target_id = str(args.get("target_id") or "")
    if not target_id:
        return _dump({"ok": False, "reason": "target_id is required"})
    if action == "resolve":
        argv = ["datasources", "resolve", target_id]
        if args.get("json_output", True):
            argv.append("--json")
    elif action == "retrieve":
        argv = ["api", f"v1/data_sources/{target_id}"]
    elif action == "query":
        argv = ["datasources", "query", target_id, "--limit", str(int(args.get("limit", 25)))]
        if args.get("start_cursor"):
            argv.extend(["--start-cursor", str(args["start_cursor"])])
        for spec in args.get("sorts") or []:
            argv.extend(["--sort", str(spec)])
        if args.get("filter_json"):
            argv.extend(["--filter", str(args["filter_json"])])
        if args.get("json_output", True):
            argv.append("--json")
    elif action == "create":
        argv = ["api", "v1/data_sources", "-X", "POST", *list(args.get("inline_args") or [])]
    elif action == "update":
        argv = ["api", f"v1/data_sources/{target_id}", "-X", "PATCH", *list(args.get("inline_args") or [])]
    else:
        return _dump({"ok": False, "reason": f"Unsupported datasource action: {action}"})
    result = run_ntn(argv)
    return _dump(result.to_dict())


def handle_notion_files(args: dict[str, Any], **kwargs) -> str:
    del kwargs
    action = args.get("action")
    json_output = bool(args.get("json_output", True))
    plain_output = bool(args.get("plain_output", False))
    stdin_text = None
    stdin_bytes = None
    argv: list[str] = ["files", str(action)]
    if action == "create":
        if args.get("external_url"):
            argv.extend(["--external-url", str(args["external_url"])])
        else:
            file_base64 = args.get("file_base64")
            file_path = args.get("file_path")
            if file_base64:
                try:
                    stdin_bytes = base64.b64decode(str(file_base64), validate=True)
                except Exception as exc:
                    return _dump({"ok": False, "reason": f"Invalid file_base64 payload: {exc}"})
                if not args.get("filename"):
                    return _dump({"ok": False, "reason": "filename is required when using file_base64"})
            elif file_path:
                stdin_bytes = Path(str(file_path)).read_bytes()
            else:
                return _dump({"ok": False, "reason": "file_path, file_base64, or external_url is required for files create"})
        if args.get("filename"):
            argv.extend(["--filename", str(args["filename"])])
        if args.get("content_type"):
            argv.extend(["--content-type", str(args["content_type"])])
        if plain_output:
            argv.append("--plain")
        elif json_output:
            argv.append("--json")
    elif action == "get":
        upload_id = args.get("upload_id")
        if not upload_id:
            return _dump({"ok": False, "reason": "upload_id is required for files get"})
        argv.append(str(upload_id))
    elif action == "list":
        pass
    else:
        return _dump({"ok": False, "reason": f"Unsupported files action: {action}"})
    result = run_ntn(argv, stdin_text=stdin_text, stdin_bytes=stdin_bytes)
    return _dump(result.to_dict())


def handle_notion_workers(args: dict[str, Any], **kwargs) -> str:
    del kwargs
    argv = ["workers", *list(args.get("argv") or [])]
    result = run_ntn(
        argv,
        stdin_text=args.get("stdin"),
        timeout=int(args.get("timeout", 180)),
        confirm_destructive=bool(args.get("confirm_destructive", False)),
    )
    return _dump(result.to_dict())
