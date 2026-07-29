import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_python_doctor_script_json():
    out = subprocess.check_output([sys.executable, str(ROOT / 'scripts' / 'notion_doctor.py'), '--json'], text=True)
    payload = json.loads(out)
    assert payload['plugin'] == 'notion-cli-agent'


def test_node_catalog_script_json():
    out = subprocess.check_output(['node', str(ROOT / 'scripts' / 'notion_command_catalog.mjs'), '--json'], text=True)
    payload = json.loads(out)
    assert 'pages' in payload
    assert 'workers' in payload


def test_node_json_to_markdown():
    sample = json.dumps({"id": "abc", "object": "page"})
    proc = subprocess.run(
        ['node', str(ROOT / 'scripts' / 'notion_json_to_markdown.js')],
        input=sample,
        text=True,
        capture_output=True,
        check=True,
    )
    assert '# Notion JSON Summary' in proc.stdout
    assert '"id": "abc"' in proc.stdout
