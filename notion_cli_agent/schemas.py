NOTION_CLI_HELP = {
    "name": "notion_cli_help",
    "description": "Return Notion CLI capability summary, install/auth facts, and environment diagnostics for ntn.",
    "parameters": {
        "type": "object",
        "properties": {
            "include_catalog": {"type": "boolean", "description": "Include documented command catalog", "default": True},
        },
    },
}

NOTION_CLI_RUN = {
    "name": "notion_cli_run",
    "description": "Run a documented ntn command through a safety wrapper. Use for arbitrary Notion CLI tasks that are not covered by more specific helper tools.",
    "parameters": {
        "type": "object",
        "properties": {
            "argv": {"type": "array", "items": {"type": "string"}, "description": "Arguments after 'ntn'"},
            "stdin": {"type": "string", "description": "Optional stdin passed to ntn"},
            "timeout": {"type": "integer", "default": 180},
            "confirm_destructive": {"type": "boolean", "default": False},
        },
        "required": ["argv"],
    },
}

NOTION_PAGES_MARKDOWN = {
    "name": "notion_pages_markdown",
    "description": "Read or write Notion pages using documented ntn pages commands. Supports get, create, edit, and trash.",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["get", "create", "edit", "trash"]},
            "page_id": {"type": "string"},
            "parent": {"type": "string", "description": "Parent ref like page:<id>, database:<id>, or data-source:<id>"},
            "content": {"type": "string", "description": "Markdown content"},
            "json_output": {"type": "boolean", "default": False},
            "allow_deleting_content": {"type": "boolean", "default": False},
            "confirm_destructive": {"type": "boolean", "default": False},
        },
        "required": ["action"],
    },
}

NOTION_DATASOURCES = {
    "name": "notion_datasources",
    "description": "Work with Notion data sources via documented ntn datasources and ntn api patterns. Supports resolve, retrieve, query, create, and update.",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["resolve", "retrieve", "query", "create", "update"]},
            "target_id": {"type": "string", "description": "Database id or data source id depending on action"},
            "limit": {"type": "integer", "default": 25},
            "start_cursor": {"type": "string"},
            "filter_json": {"type": "string", "description": "Raw JSON string for --filter or API body"},
            "sorts": {"type": "array", "items": {"type": "string"}, "description": "Repeated <property> [asc|desc] sorts"},
            "filter_properties": {"type": "array", "items": {"type": "string"}},
            "inline_args": {"type": "array", "items": {"type": "string"}, "description": "Extra inline ntn api args for create/update"},
            "json_output": {"type": "boolean", "default": True},
        },
        "required": ["action", "target_id"],
    },
}

NOTION_FILES = {
    "name": "notion_files",
    "description": "Upload or inspect Notion File Upload objects with documented ntn files commands. Supports text uploads, base64 uploads, external URL imports, get, and list.",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["create", "get", "list"]},
            "upload_id": {"type": "string"},
            "file_path": {"type": "string"},
            "file_base64": {"type": "string", "description": "Optional base64-encoded file payload for create"},
            "external_url": {"type": "string"},
            "filename": {"type": "string"},
            "content_type": {"type": "string"},
            "json_output": {"type": "boolean", "default": True},
            "plain_output": {"type": "boolean", "default": False},
        },
        "required": ["action"],
    },
}

NOTION_WORKERS = {
    "name": "notion_workers",
    "description": "Run documented Notion Workers CLI subcommands such as list, get, deploy, exec, sync, env, oauth, runs, and webhooks.",
    "parameters": {
        "type": "object",
        "properties": {
            "argv": {"type": "array", "items": {"type": "string"}, "description": "Arguments after 'workers'"},
            "stdin": {"type": "string"},
            "timeout": {"type": "integer", "default": 180},
            "confirm_destructive": {"type": "boolean", "default": False},
        },
        "required": ["argv"],
    },
}
