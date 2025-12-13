import json
from typing import Any, Dict, Optional

import requests

from .config import Config

BASE_PATH = "/data/foundation/schemaregistry"


class SchemaRegistryClient:
    def __init__(self, config: Config, access_token: str) -> None:
        self.config = config
        self.access_token = access_token
        self.session = requests.Session()

    def _accept(self, version: Optional[int] = None) -> str:
        if version is None:
            return "application/vnd.adobe.xdm+json"
        return f"application/vnd.adobe.xdm+json;version={version}"

    def _headers(self, accept: Optional[str] = None, content_type: Optional[str] = None) -> Dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "x-gw-ims-org-id": self.config.org_id,
            "x-api-key": self.config.api_key,
            "x-sandbox-name": self.config.sandbox_name,
        }
        if accept:
            headers["Accept"] = accept
        if content_type:
            headers["Content-Type"] = content_type
        return headers

    def _url(self, *parts: str) -> str:
        joined = "/".join(part.strip("/") for part in parts)
        return f"{self.config.gateway_url}{BASE_PATH}/{joined}"

    def list_schemas(self, limit: Optional[int] = None, start: Optional[str] = None, orderby: Optional[str] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if start:
            params["start"] = start
        if orderby:
            params["orderby"] = orderby

        url = self._url(self.config.container, "schemas")
        resp = self.session.get(url, headers=self._headers(self._accept()), params=params)
        resp.raise_for_status()
        return resp.json()

    def get_schema(self, schema_id: str, version: Optional[int] = None) -> Dict[str, Any]:
        url = self._url(self.config.container, "schemas", schema_id)
        resp = self.session.get(url, headers=self._headers(self._accept(version)))
        resp.raise_for_status()
        return resp.json()

    def create_schema(self, schema: Dict[str, Any], version: int = 1) -> Dict[str, Any]:
        url = self._url(self.config.container, "schemas")
        headers = self._headers(self._accept(version), "application/json")
        resp = self.session.post(url, headers=headers, json=schema)
        resp.raise_for_status()
        return resp.json()

    def update_schema(self, schema_id: str, schema: Dict[str, Any], version: int) -> Dict[str, Any]:
        url = self._url(self.config.container, "schemas", schema_id)
        headers = self._headers(self._accept(version), "application/json")
        resp = self.session.put(url, headers=headers, json=schema)
        resp.raise_for_status()
        return resp.json()

    def patch_schema(self, schema_id: str, operations: Any, version: int) -> Dict[str, Any]:
        url = self._url(self.config.container, "schemas", schema_id)
        headers = self._headers(self._accept(version), "application/json-patch+json")
        resp = self.session.patch(url, headers=headers, json=operations)
        resp.raise_for_status()
        return resp.json()

    def delete_schema(self, schema_id: str) -> None:
        url = self._url(self.config.container, "schemas", schema_id)
        resp = self.session.delete(url, headers=self._headers(self._accept()))
        resp.raise_for_status()
