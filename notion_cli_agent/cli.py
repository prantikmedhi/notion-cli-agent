from __future__ import annotations

import json
from typing import Any

from .helpers import CATALOG, run_ntn, shell_split, doctor


def register_cli(subparsers) -> None:
    parser = subparsers.add_parser("notion-cli", help="Notion CLI helpers and command proxy")
    subs = parser.add_subparsers(dest="notion_cli_cmd")

    doctor_p = subs.add_parser("doctor", help="Check ntn installation and auth hints")
    doctor_p.add_argument("--json", action="store_true")
    doctor_p.set_defaults(func=handle_cli)

    catalog_p = subs.add_parser("catalog", help="Show documented ntn command catalog")
    catalog_p.add_argument("--json", action="store_true")
    catalog_p.set_defaults(func=handle_cli)

    run_p = subs.add_parser("run", help="Run ntn argv through the plugin safety wrapper")
    run_p.add_argument("argv", nargs="+")
    run_p.add_argument("--stdin")
    run_p.add_argument("--confirm-destructive", action="store_true")
    run_p.set_defaults(func=handle_cli)


def handle_cli(args) -> int:
    cmd = getattr(args, "notion_cli_cmd", None)
    if cmd == "doctor":
        payload = doctor()
        print(json.dumps(payload, indent=2) if getattr(args, "json", False) else payload)
        return 0
    if cmd == "catalog":
        if getattr(args, "json", False):
            print(json.dumps(CATALOG, indent=2))
        else:
            for group, items in CATALOG.items():
                print(f"[{group}]")
                if isinstance(items, dict):
                    for k, v in items.items():
                        print(f"  {k}: {v}")
                else:
                    for item in items:
                        print(f"  - {item}")
        return 0
    if cmd == "run":
        result = run_ntn(list(args.argv), stdin_text=getattr(args, "stdin", None), confirm_destructive=bool(getattr(args, "confirm_destructive", False)))
        print(json.dumps(result.to_dict(), indent=2))
        return 0 if result.ok else result.exit_code or 1
    print("Choose one of: doctor, catalog, run")
    return 2


def slash_command_factory(ctx):
    def _handler(raw_args: str) -> str:
        raw_args = (raw_args or "").strip()
        if not raw_args:
            return json.dumps({
                "ok": True,
                "usage": "/notion-cli run api ls",
                "catalog_groups": sorted(CATALOG.keys()),
            }, indent=2)
        argv = shell_split(raw_args)
        if argv and argv[0] == "run":
            argv = argv[1:]
        result = run_ntn(argv)
        return json.dumps(result.to_dict(), indent=2)
    return _handler
