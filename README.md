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

## Quick install

### macOS
```bash
git clone https://github.com/prantikmedhi/notion-cli-agent.git
cd notion-cli-agent
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip
/Users/prantikpratimmedhi/.hermes/hermes-agent/venv/bin/python -m pip install -e .
hermes plugins enable notion-cli-agent
ntn login
```

### Linux
```bash
git clone https://github.com/prantikmedhi/notion-cli-agent.git
cd notion-cli-agent
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip
# use the Hermes Python, not just your shell Python
~/.hermes/hermes-agent/venv/bin/python -m pip install -e .
hermes plugins enable notion-cli-agent
ntn login
```

### Windows (PowerShell)
```powershell
git clone https://github.com/prantikmedhi/notion-cli-agent.git
cd notion-cli-agent
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
# install into the same Python Hermes uses
$env:HERMES_HOME\hermes-agent\venv\Scripts\python.exe -m pip install -e .
hermes plugins enable notion-cli-agent
ntn login
```

Headless OAuth flow:
```bash
ntn login --no-browser
ntn login poll
```

Verify:
```bash
python3 -m pytest -q
python3 scripts/notion_doctor.py --json
```

## Authentication modes

This repo supports **OAuth/keychain mode first** and **env-var token mode second**.

### OAuth / keychain mode
Best for:
- local machine
- interactive usage
- normal developer workflow

Use:
```bash
ntn login
```

Headless / remote browser flow:
```bash
ntn login --no-browser
ntn login poll
```

In this mode, Notion CLI stores workspace credentials in the OS credential store / keychain.
That means you can run normal `ntn` commands **without exporting `NOTION_API_TOKEN`**.

### Env-var token mode
Best for:
- CI/CD
- unattended jobs
- containers
- remote servers without working keychain integration

Use:
```bash
export NOTION_API_TOKEN=...
```

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
- `notion_doctor.py` — checks CLI presence, OAuth/keychain hints, auth files, env readiness
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
- `ntn login --no-browser`
- `ntn login poll`
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

## Install process

### macOS

#### Requirements
- Python 3.10+
- Git
- Hermes Agent installed if you want Hermes plugin usage
- optional: Node.js if you want to run the JS/MJS helper scripts

#### 1. Clone the repo
```bash
git clone https://github.com/prantikmedhi/notion-cli-agent.git
cd notion-cli-agent
```

#### 2. Install the Python package
Best for Hermes entry-point plugin detection:
```bash
/Users/prantikpratimmedhi/.hermes/hermes-agent/venv/bin/python -m pip install -e .
```

If your Python allows direct install and you only want the local package available outside Hermes:
```bash
python3 -m pip install -e .
```

If your Python is externally managed, use a virtualenv for local dev, but still install the plugin into the Hermes Python so `hermes plugins` can see it:
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip
python3 -m pip install -e .
/Users/prantikpratimmedhi/.hermes/hermes-agent/venv/bin/python -m pip install -e .
```

#### 3. Enable in Hermes
```bash
hermes plugins enable notion-cli-agent
hermes plugins list
```

#### 4. Authenticate Notion CLI with OAuth/keychain
```bash
ntn login
```

Headless fallback:
```bash
ntn login --no-browser
ntn login poll
```

#### 5. Verify
```bash
python3 -m pytest -q
python3 scripts/notion_doctor.py --json
node scripts/notion_command_catalog.mjs --json
```

### Linux

#### Requirements
- Python 3.10+
- Git
- Hermes Agent installed if you want Hermes plugin usage
- optional: Node.js if you want JS/MJS helper scripts
- optional: working keychain/secret service if you want pure OAuth/keychain storage

#### 1. Clone the repo
```bash
git clone https://github.com/prantikmedhi/notion-cli-agent.git
cd notion-cli-agent
```

#### 2. Install the Python package
Recommended for Hermes plugin detection:
```bash
~/.hermes/hermes-agent/venv/bin/python -m pip install -e .
```

For local development, you can also keep a project venv:
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip
python3 -m pip install -e .
~/.hermes/hermes-agent/venv/bin/python -m pip install -e .
```

If your system Python allows it, direct install also works for non-Hermes use:
```bash
python3 -m pip install -e .
```

#### 3. Enable in Hermes
```bash
hermes plugins enable notion-cli-agent
hermes plugins list
```

#### 4. Authenticate Notion CLI
Local desktop Linux:
```bash
ntn login
```

Remote/headless Linux:
```bash
ntn login --no-browser
ntn login poll
```

If your Linux machine has no usable keychain, use token mode instead:
```bash
export NOTION_API_TOKEN=...
```

#### 5. Verify
```bash
python3 -m pytest -q
python3 scripts/notion_doctor.py --json
node scripts/notion_command_catalog.mjs --json
```

### Windows

#### Requirements
- Python 3.10+
- Git for Windows
- Hermes Agent installed if you want Hermes plugin usage
- optional: Node.js if you want JS/MJS helper scripts
- PowerShell recommended

#### Important note
This repo installs on Windows, but the official Notion CLI may not have the same native support maturity as macOS/Linux. If native `ntn` usage is unavailable, use:
- WSL for `ntn`
- or install the plugin/scripts on Windows and run Notion CLI from a supported environment

#### 1. Clone the repo
PowerShell:
```powershell
git clone https://github.com/prantikmedhi/notion-cli-agent.git
cd notion-cli-agent
```

#### 2. Create and activate virtualenv
```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -e .
```

#### 3. Install into the same Python Hermes uses
```powershell
$env:HERMES_HOME\hermes-agent\venv\Scripts\python.exe -m pip install -e .
```

#### 4. Enable in Hermes
```powershell
hermes plugins enable notion-cli-agent
hermes plugins list
```

#### 5. Authenticate
If `ntn` works natively:
```powershell
ntn login
```

If you are using WSL or a remote environment:
```bash
ntn login --no-browser
ntn login poll
```

#### 5. Verify
```powershell
python -m pytest -q
python scripts/notion_doctor.py --json
node scripts/notion_command_catalog.mjs --json
```

## Alternative: install as Hermes directory plugin
This works on macOS, Linux, and Windows once Python is available.

```bash
python3 scripts/install_as_directory_plugin.py
hermes plugins enable notion-cli-agent
```

Windows PowerShell:
```powershell
python scripts/install_as_directory_plugin.py
hermes plugins enable notion-cli-agent
```

## Run tests
```bash
python3 -m pytest -q
```

Windows PowerShell:
```powershell
python -m pytest -q
```

## Run helper scripts
```bash
python3 scripts/notion_doctor.py --json
node scripts/notion_command_catalog.mjs --json
node scripts/notion_json_to_markdown.js < sample.json
```

## Repo structure

```text
notion-cli-agent/
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
- `17 passed`

## Notes

- The official `ntn` CLI is **not installed** in this machine yet, so runtime calls to live Notion are wrapped and ready, but real Notion operations require the user to install/auth the CLI first.
- OAuth/keychain mode is supported by design and should be the preferred mode for local interactive use.
- This repo is intentionally standalone, so it can live on GitHub as its own integration package instead of being buried inside a larger codebase.

## License

MIT
