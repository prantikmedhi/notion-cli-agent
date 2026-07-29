import json
print(json.dumps({
    "property": "Status",
    "select": {"equals": "Active"}
}, indent=2))
