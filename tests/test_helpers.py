import json
from notion_cli_agent import helpers


def test_catalog_has_core_groups():
    for key in ["install", "auth", "api", "datasources", "pages", "files", "workers"]:
        assert key in helpers.CATALOG


def test_oauth_auth_catalog_present():
    assert "oauth" in helpers.CATALOG["auth"]
    assert "ntn login" in helpers.CATALOG["auth"]["oauth"]


def test_ensure_allowed_rejects_unknown_top_level():
    ok, reason = helpers.ensure_allowed(["rm", "-rf", "/"])
    assert ok is False
    assert "allow-list" in reason


def test_is_destructive_matches_expected_patterns():
    assert helpers.is_destructive(["pages", "trash", "abc"])
    assert helpers.is_destructive(["workers", "delete", "w1"])
    assert not helpers.is_destructive(["pages", "get", "abc"])


def test_maybe_json_parses_valid_json():
    assert helpers.maybe_json('{"ok": true}') == {"ok": True}
    assert helpers.maybe_json('plain text') is None


def test_doctor_shape():
    payload = helpers.doctor()
    assert payload["plugin"] == "notion-cli-agent"
    assert "ntn_found" in payload
    assert "catalog_groups" in payload
    assert "preferred_auth" in payload
    assert "oauth_keychain_possible" in payload
    assert "auth_files" in payload
