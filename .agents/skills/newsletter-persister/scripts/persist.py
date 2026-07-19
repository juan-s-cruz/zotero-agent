#!/usr/bin/env python3
import os
import sys
import re
import json
import urllib.request
import urllib.error

# Ensure markdown library is installed
try:
    import markdown
except ImportError:
    print(
        "Error: The 'markdown' Python library is required. Please install it using: pip install markdown"
    )
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 persist.py <relative_markdown_path>")
        sys.exit(1)

    relative_path = sys.argv[1]

    # 1. Read config from user_config.json (navigate 4 levels up to workspace root)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.abspath(
        os.path.join(script_dir, "../../../../user_config.json")
    )

    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found at {config_path}")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    collection_key = config.get("NEWSLETTERS_COLLECTION_KEY")
    if not collection_key:
        print("Error: NEWSLETTERS_COLLECTION_KEY not found in user_config.json")
        sys.exit(1)

    # 2. Get credentials (prioritize user_config.json, fallback to environment)
    api_key = config.get("ZOTERO_API_KEY") or os.environ.get("ZOTERO_API_KEY")
    user_id = (
        config.get("ZOTERO_LIBRARY_ID")
        or config.get("ZOTERO_USER_ID")
        or os.environ.get("ZOTERO_LIBRARY_ID")
        or os.environ.get("ZOTERO_USER_ID")
    )
    library_type = config.get("ZOTERO_LIBRARY_TYPE") or os.environ.get(
        "ZOTERO_LIBRARY_TYPE", "user"
    )

    if not api_key or not user_id:
        print(
            "Error: ZOTERO_API_KEY and ZOTERO_LIBRARY_ID (or ZOTERO_USER_ID) must be specified in user_config.json or as environment variables."
        )
        print("Please add them to your user_config.json, for example:")
        print("  {")
        print('    "ZOTERO_API_KEY": "your_api_key",')
        print('    "ZOTERO_LIBRARY_ID": "your_library_id"')
        print("  }")
        sys.exit(1)

    # 3. Resolve path, check activity restriction, and read markdown file
    workspace_root = os.path.abspath(os.path.join(script_dir, "../../../.."))
    activity_dir = os.path.join(workspace_root, "activity")
    md_path = os.path.abspath(os.path.join(workspace_root, relative_path))

    if not md_path.startswith(activity_dir + os.sep) and md_path != activity_dir:
        print(
            "Error: The markdown file must be located inside the 'activity' directory."
        )
        sys.exit(1)

    if not os.path.exists(md_path):
        print(f"Error: File not found at {relative_path} (resolved to: {md_path})")
        sys.exit(1)

    if os.path.getsize(md_path) == 0:
        print(f"Error: The markdown file at {relative_path} is empty.")
        sys.exit(1)

    filename = os.path.basename(md_path)

    # 4. Extract date from filename
    date_match = re.search(r"(\d{4})-(\d{2})-(\d{2})", filename)
    if not date_match:
        print(
            "Error: Filename must contain a date in YYYY-MM-DD format (e.g., 2026-07-18-summary.md)"
        )
        sys.exit(1)

    year, month, day = date_match.groups()
    standard_title = f"Summary - {day}-{month}-{year}"
    iso_date = f"{year}-{month}-{day}"

    print(f"Processing '{filename}'...")
    print(f"Standardized Title: {standard_title}")

    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # 5. Convert markdown to simple HTML (UTF-8/Emojis preserved)
    html_content = markdown.markdown(md_content, extensions=["extra"])

    # 6. Build Zotero Base URL
    base_url = f"https://api.zotero.org/{library_type}s/{user_id}/items"

    # 7. Create Parent Report Item
    parent_data = [
        {
            "itemType": "report",
            "title": standard_title,
            "creators": [{"creatorType": "author", "name": "AI RSS Evaluator Agent"}],
            "date": iso_date,
            "collections": [collection_key],
        }
    ]

    print("Creating parent report item in Zotero...")
    req = urllib.request.Request(
        base_url,
        data=json.dumps(parent_data).encode("utf-8"),
        headers={"Zotero-API-Key": api_key, "Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as res:
            res_data = json.loads(res.read().decode("utf-8"))

        successful_items = res_data.get("successful", {})
        if not successful_items:
            print("Error creating parent item. Response details:")
            print(json.dumps(res_data, indent=2))
            sys.exit(1)

        parent_key = list(successful_items.values())[0]["key"]
        print(f"Parent report item created successfully. Key: {parent_key}")

    except urllib.error.HTTPError as e:
        print(f"HTTP Error creating parent item: {e.code} - {e.reason}")
        print(e.read().decode("utf-8"))
        sys.exit(1)
    except Exception as e:
        print(f"Error creating parent item: {e}")
        sys.exit(1)

    # 8. Create Child Note
    note_data = [
        {"itemType": "note", "parentItem": parent_key, "note": html_content, "tags": []}
    ]

    print("Attaching summary content as child note...")
    req = urllib.request.Request(
        base_url,
        data=json.dumps(note_data).encode("utf-8"),
        headers={"Zotero-API-Key": api_key, "Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as res:
            res_data = json.loads(res.read().decode("utf-8"))

        successful_notes = res_data.get("successful", {})
        if not successful_notes:
            print("Error creating child note. Response details:")
            print(json.dumps(res_data, indent=2))
            sys.exit(1)

        note_key = list(successful_notes.values())[0]["key"]
        print(f"Child note created successfully. Key: {note_key}")
        print("\nSuccess! Summary added to Zotero.")

    except urllib.error.HTTPError as e:
        print(f"HTTP Error creating child note: {e.code} - {e.reason}")
        print(e.read().decode("utf-8"))
        sys.exit(1)
    except Exception as e:
        print(f"Error creating child note: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
