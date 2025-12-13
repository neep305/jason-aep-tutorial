import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    gateway_url: str
    ims_token_url: str
    client_id: str
    client_secret: str
    scopes: str
    org_id: str
    sandbox_name: str
    api_key: str
    container: str = "tenant"


def _required(name: str, value: Optional[str]) -> str:
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def load_config() -> Config:
    """Load all environment-based configuration for OAuth and Schema Registry."""
    gateway_url = os.environ.get("PLATFORM_GATEWAY_URL", "https://platform.adobe.io").rstrip("/")
    ims_token_url = os.environ.get("IMS_TOKEN_URL", "https://ims-na1.adobelogin.com/ims/token/v3")

    client_id = os.environ.get("CLIENT_ID") or os.environ.get("API_KEY")
    client_secret = os.environ.get("CLIENT_SECRET")
    scopes = os.environ.get(
        "SCOPES",
        "openid,AdobeID,read_organizations,additional_info.projectedProductContext,session",
    )
    org_id = os.environ.get("IMS_ORG_ID") or os.environ.get("ORG_ID")
    sandbox_name = os.environ.get("SANDBOX_NAME") or os.environ.get("SANDBOX") or "prod"
    api_key = os.environ.get("API_KEY") or client_id
    container = os.environ.get("SCHEMA_CONTAINER", "tenant")

    clean_scopes = ",".join(scope.strip() for scope in scopes.split(",") if scope.strip())

    return Config(
        gateway_url=gateway_url,
        ims_token_url=ims_token_url,
        client_id=_required("CLIENT_ID or API_KEY", client_id),
        client_secret=_required("CLIENT_SECRET", client_secret),
        scopes=_required("SCOPES", clean_scopes),
        org_id=_required("IMS_ORG_ID or ORG_ID", org_id),
        sandbox_name=_required("SANDBOX_NAME or SANDBOX", sandbox_name),
        api_key=_required("API_KEY or CLIENT_ID", api_key),
        container=container,
    )
