---
name: notion-cli-datasources
description: "Use when an agent needs database/data-source work in Notion CLI. Covers resolve, retrieve schema, query rows, and API-based create/update flows."
version: 0.1.0
author: notion-cli-agent
license: MIT
platforms: [linux, macos, windows]
---

# Notion CLI Data Sources

## Overview

Use this skill for Notion database-backed data source operations.

## Core flows

1. Resolve database to data source ids: `ntn datasources resolve <database-id>`
2. Retrieve schema: `ntn api v1/data_sources/<data-source-id>`
3. Query rows: `ntn datasources query <data-source-id>`
4. Create/update via `ntn api` for advanced payloads

## Documented query options

- `--limit`
- `--start-cursor`
- `--sort <property> [asc|desc]`
- `--filter <json>`
- `--filter-file <path>`
- `--json`

## References

- `references/datasources.md`
- `scripts/filter_template.py`

## Verification Checklist

- [ ] database id or data source id chosen correctly
- [ ] filters valid JSON before query
- [ ] pagination cursor preserved when needed
