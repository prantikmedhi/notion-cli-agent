---
name: notion-cli-files-workers
description: "Use when an agent needs file uploads or Workers commands in Notion CLI. Covers ntn files plus deploy, exec, sync, env, oauth, runs, and webhooks."
version: 0.1.0
author: notion-cli-agent
license: MIT
platforms: [linux, macos, windows]
---

# Notion CLI Files and Workers

## Overview

Use this skill for file uploads and operational Workers commands.

## File flows

- local upload: `ntn files create < ./photo.png`
- external import: `ntn files create --external-url https://... --filename photo.png`
- inspect upload: `ntn files get <upload-id>`
- list uploads: `ntn files list`

## Worker flows

- create scaffolding: `ntn workers new`
- deploy: `ntn workers deploy`
- run capability: `ntn workers exec <key>`
- sync operations: `ntn workers sync ...`
- env operations: `ntn workers env ...`
- oauth operations: `ntn workers oauth ...`
- run logs: `ntn workers runs ...`
- webhook URLs: `ntn workers webhooks list`

## References

- `references/files-workers.md`
- `scripts/files_workers_examples.mjs`

## Verification Checklist

- [ ] file upload reached `uploaded` before attachment
- [ ] worker id or workers.json resolved correctly
- [ ] delete/reset/unset actions explicitly confirmed
