---
name: notion-cli-overview
description: "Use when an agent needs setup, auth, install, or command discovery for Notion CLI. Gives quickest path to ntn install, login, env vars, and command map."
version: 0.1.0
author: notion-cli-agent
license: MIT
platforms: [linux, macos, windows]
---

# Notion CLI Overview

## Overview

Use this skill when an agent first needs to work with Notion CLI. It summarizes current documented install, auth, environment variables, and command families.

## Fast path

1. Install CLI: `curl -fsSL https://ntn.dev | bash`
2. Verify: `ntn --version`
3. Authenticate: `ntn login`
4. Optional env override: `NOTION_API_TOKEN`
5. Inspect commands: `ntn api ls`

## Current documented environment variables

- `NOTION_API_TOKEN`
- `NOTION_KEYRING`
- `NOTION_WORKSPACE_ID`
- `NOTION_WORKERS_CONFIG_FILE`
- `NOTION_API_VERSION`

## Command families

- `ntn api`
- `ntn datasources`
- `ntn pages`
- `ntn files`
- `ntn workers`
- `ntn doctor`

## References

- `references/overview.md`
- `scripts/print_setup.py`

## Verification Checklist

- [ ] `ntn --version` works
- [ ] either `ntn login` succeeded or `NOTION_API_TOKEN` is set
- [ ] `ntn api ls` returns endpoint list
