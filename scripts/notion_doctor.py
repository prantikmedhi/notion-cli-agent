import argparse
import json
import sys
from pathlib import Path

# Allow running from a repo checkout without requiring pip install -e .
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from notion_cli_agent.helpers import doctor  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument('--json', action='store_true')
args = parser.parse_args()

payload = doctor()
if args.json:
    print(json.dumps(payload, indent=2))
else:
    print(f"plugin: {payload['plugin']}")
    print(f"ntn_found: {payload['ntn_found']}")
    print(f"ntn_path: {payload['ntn_path']}")
    print(f"preferred_auth: {payload['preferred_auth']}")
    print(f"oauth_keychain_possible: {payload['oauth_keychain_possible']}")
    print(f"oauth_session_hint: {payload['oauth_session_hint']}")
    print(f"auth_files: {payload['auth_files']}")
    print(f"env: {payload['env']}")
    print(f"catalog_groups: {payload['catalog_groups']}")
