import json
import sys
from typing import Any, Optional

import requests

from .config import load_config
from .oauth import fetch_access_token
from .schema_client import SchemaRegistryClient


def prompt(prompt_text: str) -> str:
    return input(prompt_text).strip()


def prompt_int(prompt_text: str, default: Optional[int] = None) -> Optional[int]:
    raw = input(prompt_text).strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        print("Please enter a number.")
        return prompt_int(prompt_text, default)


def load_json_file(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def menu() -> str:
    print("\nSelect an API action:")
    print("1) List schemas")
    print("2) Get schema")
    print("3) Create schema")
    print("4) Replace schema (PUT)")
    print("5) Patch schema")
    print("6) Delete schema")
    print("0) Exit")
    return input("Enter choice: ").strip()


def run() -> int:
    config = load_config()
    print("Requesting access token via OAuth...")
    access_token = fetch_access_token(config)
    print("Access token acquired.")
    client = SchemaRegistryClient(config, access_token)

    try:
        while True:
            choice = menu()
            if choice == "1":
                result = client.list_schemas()
                print(json.dumps(result, indent=2))
            elif choice == "2":
                schema_id = prompt("Schema ID (meta:altId or URL-encoded ID): ")
                version = prompt_int("Accept version (blank for latest): ", default=None)
                result = client.get_schema(schema_id, version=version)
                print(json.dumps(result, indent=2))
            elif choice == "3":
                file_path = prompt("Path to schema JSON: ")
                version = prompt_int("Accept version (default 1): ", default=1)
                payload = load_json_file(file_path)
                result = client.create_schema(payload, version=version or 1)
                print(json.dumps(result, indent=2))
            elif choice == "4":
                schema_id = prompt("Schema ID to replace: ")
                file_path = prompt("Path to schema JSON: ")
                version = prompt_int("Accept version (required): ")
                payload = load_json_file(file_path)
                result = client.update_schema(schema_id, payload, version=version)
                print(json.dumps(result, indent=2))
            elif choice == "5":
                schema_id = prompt("Schema ID to patch: ")
                file_path = prompt("Path to JSON Patch file: ")
                version = prompt_int("Accept version (required): ")
                payload = load_json_file(file_path)
                result = client.patch_schema(schema_id, payload, version=version)
                print(json.dumps(result, indent=2))
            elif choice == "6":
                schema_id = prompt("Schema ID to delete: ")
                client.delete_schema(schema_id)
                print(f"Deleted schema {schema_id}")
            elif choice == "0":
                return 0
            else:
                print("Invalid selection, try again.")
    except requests.HTTPError as exc:
        print(f"Request failed: {exc.response.status_code} {exc.response.text}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(run())
