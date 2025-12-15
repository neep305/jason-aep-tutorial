import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import Mock, patch

from app.config import Config, load_config
from app.oauth import fetch_access_token

from dotenv import load_dotenv

load_dotenv()

class ConfigTests(unittest.TestCase):
    def test_load_config_reads_env_file(self) -> None:
        with TemporaryDirectory() as tmpdir, patch.dict(os.environ, {}, clear=True):
            env_path = Path(tmpdir) / ".env"
            env_path.write_text(
                "\n".join(
                    [
                        "CLIENT_ID=test-client",
                        "CLIENT_SECRET=test-secret",
                        "SCOPES=scope1, scope2",
                        "IMS_ORG_ID=org@test",
                        "SANDBOX_NAME=dev",
                        "API_KEY=test-client",
                        "PLATFORM_GATEWAY_URL=https://example.test",
                        "IMS_TOKEN_URL=https://ims.test/token",
                        "SCHEMA_CONTAINER=global",
                    ]
                ),
                encoding="utf-8",
            )

            config = load_config(env_path)

            self.assertEqual(config.client_id, "test-client")
            self.assertEqual(config.client_secret, "test-secret")
            self.assertEqual(config.scopes, "scope1,scope2")
            self.assertEqual(config.org_id, "org@test")
            self.assertEqual(config.sandbox_name, "dev")
            self.assertEqual(config.api_key, "test-client")
            self.assertEqual(config.gateway_url, "https://example.test")
            self.assertEqual(config.ims_token_url, "https://ims.test/token")
            self.assertEqual(config.container, "global")


class OAuthTests(unittest.TestCase):
    def test_fetch_access_token_posts_and_returns_token(self) -> None:
        config = Config(
            gateway_url="https://example.test",
            ims_token_url="https://ims.test/token",
            client_id="client",
            client_secret="secret",
            scopes="scope1,scope2",
            org_id="org@test",
            sandbox_name="dev",
            api_key="client",
            container="tenant",
        )

        fake_response = Mock()
        fake_response.json.return_value = {"access_token": "token-123"}
        fake_response.raise_for_status = Mock()

        post_mock = Mock(return_value=fake_response)

        with patch("app.oauth.requests.post", post_mock):
            token = fetch_access_token(config)

        self.assertEqual(token, "token-123")
        post_mock.assert_called_once_with(
            config.ims_token_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "client_credentials",
                "client_id": "client",
                "client_secret": "secret",
                "scope": "scope1,scope2",
            },
        )


class OAuthWithEnvTests(unittest.TestCase):
    def test_fetch_access_token_with_env_config(self) -> None:
        config = load_config(Path(__file__).parent.parent / ".env")

        token = fetch_access_token(config)
        print("Fetched token:", token)
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 0)

if __name__ == "__main__":
    unittest.main()
