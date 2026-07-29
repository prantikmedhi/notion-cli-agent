---
name: notion-cli-pages
description: "Use when an agent needs Markdown page read/write via Notion CLI. Covers ntn pages get, create, edit, and trash with safe defaults."
version: 0.1.0
author: notion-cli-agent
license: MIT
platforms: [linux, macos, windows]
---

# Notion CLI Pages

## Overview

Use this skill for page content work. Notion CLI pages commands are Markdown-native.

## Documented commands

- `ntn pages get <page-id>`
- `ntn pages create --parent <ref> --content <markdown>`
- `ntn pages edit <page-id> --content <markdown>`
- `ntn pages trash <page-id>`

## Rules

- Prefer `get` for agent-readable Markdown
- Prefer `create` and `edit` when user wants content changes
- Treat `trash` as destructive; require explicit confirmation

## References

- `references/pages.md`
- `scripts/pages_markdown_examples.js`

## Verification Checklist

- [ ] page id or parent ref present
- [ ] Markdown content supplied for create/edit
- [ ] destructive action explicitly confirmed before trash
