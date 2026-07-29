# notion-cli-agent

Standalone Notion CLI plugin repository for **Hermes Agent** and other terminal-first AI agents.

This repo packages a reusable Notion CLI integration layer built from the current Notion CLI docs:
- https://developers.notion.com/cli/get-started/overview
- https://www.notion.com/help/use-notion-from-your-terminal-with-notion-cli

It is designed to help AI agents and human operators use the official `ntn` CLI to:
- fetch data from Notion databases / data sources
- query and inspect schemas
- create and update data sources through documented API flows
- create, edit, fetch, and trash pages in Markdown
- upload and inspect files
- run and manage Notion Workers
- diagnose auth / installation state before running commands

## Why this repo exists

Notion CLI is useful for coding agents because it gives a terminal-native way to interact with Notion without inventing undocumented APIs.

This repo turns that capability into a **publishable plugin + skill pack** with:
- a Hermes plugin entry point
- multiple bundled skills
- Python / JS / MJS helper scripts
- references based on the docs
- tests for registration, helper logic, and scripts

## What this repo includes

### 1. Hermes plugin
Path: `notion_cli_agent/`

Provides:
- `plugin.yaml`
- `__init__.py` plugin registration
- tool schemas
- CLI helpers
- safe `ntn` command wrapper logic

Registered Hermes tools:
- `notion_cli_help`
- `notion_cli_run`
- `notion_pages_markdown`
- `notion_datasources`
- `notion_files`
- `notion_workers`

Registered Hermes commands:
- slash command: `/notion-cli`
- CLI command: `hermes notion-cli ...`

### 2. Bundled skills
Each skill has its own:
- `SKILL.md`
- `references/`
- `scripts/`

Bundled skills:
- `notion-cli-overview`
- `notion-cli-pages`
- `notion-cli-datasources`
- `notion-cli-files-workers`

### 3. Generic scripts for any AI agent
Path: `scripts/`

Included:
- `notion_doctor.py` — checks CLI presence, auth hints, and env readiness
- `notion_command_catalog.mjs` — prints documented command families
- `notion_json_to_markdown.js` — converts JSON stdin into Markdown-friendly output
- `install_as_directory_plugin.py` — installs this as a Hermes directory plugin

These scripts can be used by:
- Hermes Agent
- Claude Code
- Codex / OpenAI coding agents
- OpenCode / OpenFlow-style terminal agents
- any AI system that can run shell commands

## Supported Notion CLI capability areas

Based on the docs read for this project, this repo covers these documented `ntn` areas:

### Setup and auth
- `ntn login`
- `ntn logout`
- `ntn doctor`
- `ntn update`
- environment variables:
  - `NOTION_API_TOKEN`
  - `NOTION_KEYRING`
  - `NOTION_WORKSPACE_ID`
  - `NOTION_WORKERS_CONFIG_FILE`
  - `NOTION_API_VERSION`

### API requests
- `ntn api <path>`
- `ntn api ls`

### Data sources / databases
- `ntn datasources resolve <database-id>`
- `ntn datasources query <data-source-id>`
- retrieval via `ntn api v1/data_sources/<id>`
- create / update flows via documented `ntn api` request syntax

### Pages
- `ntn pages get <page-id>`
- `ntn pages create --parent <ref>`
- `ntn pages edit <page-id>`
- `ntn pages trash <page-id>`

### Files
- `ntn files create`
- `ntn files get <upload-id>`
- `ntn files list`
- stdin uploads
- external URL imports
- filename / content-type overrides
- JSON / plain output modes

### Workers
- `ntn workers new`
- `ntn workers deploy`
- `ntn workers list`
- `ntn workers get`
- `ntn workers create`
- `ntn workers delete`
- `ntn workers exec`
- `ntn workers capabilities list`
- `ntn workers tui`
- worker sync / env / oauth / runs / webhooks flows

## Safety model

This repo intentionally adds a guardrail layer around destructive commands.

Blocked by default unless explicit confirmation is passed:
- `ntn pages trash ...`
- `ntn workers delete ...`
- `ntn workers env unset ...`
- `ntn workers sync state reset ...`
- `ntn logout`

That means agents can use the plugin safely for most read/write tasks without casually deleting data or clearing auth state.

## Install and use

## Install as editable Python package
```bash
cd notion_cli_agent_plugin
python3 -m pip install -e .
```

## Enable in Hermes
```bash
hermes plugins enable notion-cli-agent
hermes plugins list
```

## Use as directory plugin instead
```bash
python3 scripts/install_as_directory_plugin.py
hermes plugins enable notion-cli-agent
```

## Run tests
```bash
cd notion_cli_agent_plugin
python3 -m pytest -q
```

## Run helper scripts
```bash
python3 scripts/notion_doctor.py --json
node scripts/notion_command_catalog.mjs --json
node scripts/notion_json_to_markdown.js < sample.json
```

## Repo structure

```text
notion_cli_agent_plugin/
├── README.md
├── pyproject.toml
├── .gitignore
├── scripts/
├── tests/
└── notion_cli_agent/
    ├── __init__.py
    ├── cli.py
    ├── helpers.py
    ├── plugin.yaml
    ├── schemas.py
    ├── tools.py
    └── skills/
        ├── notion-cli-overview/
        ├── notion-cli-pages/
        ├── notion-cli-datasources/
        └── notion-cli-files-workers/
```

## Verification completed locally

Verified in local execution environment:
- `python3 -m pip install -e .` ✅
- `python3 -m pytest -q` ✅
- `python3 scripts/notion_doctor.py --json` ✅
- `node scripts/notion_command_catalog.mjs --json` ✅
- `node scripts/notion_json_to_markdown.js` ✅

Most recent test result during build:
- `16 passed`

## Notes

- The official `ntn` CLI is **not installed** in this machine yet, so runtime calls to live Notion are wrapped and ready, but real Notion operations require the user to install/auth the CLI first.
- This repo is intentionally standalone, so it can live on GitHub as its own integration package instead of being buried inside a larger codebase.

## License

MIT
