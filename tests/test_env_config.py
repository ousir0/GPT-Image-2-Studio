import argparse
import os
import pathlib
import sys
import tempfile
import unittest
from unittest import mock


SCRIPTS_DIR = pathlib.Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import env_config  # noqa: E402
import gpt_image2_api  # noqa: E402


class EnvConfigTest(unittest.TestCase):
    def write_env(self, directory: str, content: str) -> pathlib.Path:
        env_path = pathlib.Path(directory) / "env"
        env_path.write_text(content, encoding="utf-8")
        return env_path

    def test_local_auth_group_replaces_all_inherited_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            env_path = self.write_env(
                directory,
                "GPT_IMAGE_2_AUTH_KEY=fresh-local-key\n",
            )
            inherited = {
                "OPENAI_API_KEY": "stale-openai-key",
                "GPT_IMAGE_API_AUTH_KEY": "stale-api-key",
                "UNRELATED": "keep-me",
            }

            merged = env_config.merge_local_env(inherited, env_path)

            self.assertEqual(merged["GPT_IMAGE_2_AUTH_KEY"], "fresh-local-key")
            self.assertNotIn("OPENAI_API_KEY", merged)
            self.assertNotIn("GPT_IMAGE_API_AUTH_KEY", merged)
            self.assertEqual(merged["UNRELATED"], "keep-me")

    def test_local_base_url_group_replaces_inherited_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            env_path = self.write_env(
                directory,
                'GPT_IMAGE_2_BASE_URL="https://fresh.example/v1"\n',
            )
            inherited = {
                "OPENAI_BASE_URL": "https://stale.example/v1",
                "GPT_IMAGE_API_BASE": "https://also-stale.example/v1",
            }

            merged = env_config.merge_local_env(inherited, env_path)

            self.assertEqual(
                merged["GPT_IMAGE_2_BASE_URL"], "https://fresh.example/v1"
            )
            self.assertNotIn("OPENAI_BASE_URL", merged)
            self.assertNotIn("GPT_IMAGE_API_BASE", merged)

    def test_process_env_is_used_when_local_group_is_absent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            env_path = self.write_env(directory, "UNRELATED=local-value\n")
            inherited = {"OPENAI_API_KEY": "process-key"}

            merged = env_config.merge_local_env(inherited, env_path)

            self.assertEqual(merged["OPENAI_API_KEY"], "process-key")
            self.assertEqual(merged["UNRELATED"], "local-value")

    def test_gpt_specific_alias_wins_within_local_config(self) -> None:
        values = {
            "OPENAI_API_KEY": "generic-key",
            "GPT_IMAGE_2_AUTH_KEY": "gpt-image-key",
        }

        selected = env_config.first_env_value(values, env_config.AUTH_ENV_KEYS)

        self.assertEqual(selected, "gpt-image-key")

    def test_apply_local_env_removes_stale_managed_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            env_path = self.write_env(
                directory,
                "GPT_IMAGE_2_AUTH_KEY=fresh-local-key\n",
            )
            target = {
                "OPENAI_API_KEY": "stale-openai-key",
                "UNRELATED": "keep-me",
            }

            env_config.apply_local_env(target, env_path)

            self.assertEqual(target["GPT_IMAGE_2_AUTH_KEY"], "fresh-local-key")
            self.assertNotIn("OPENAI_API_KEY", target)
            self.assertEqual(target["UNRELATED"], "keep-me")

    def test_explicit_cli_auth_key_remains_highest_priority(self) -> None:
        args = argparse.Namespace(auth_key="explicit-key")
        with mock.patch.dict(
            os.environ,
            {"GPT_IMAGE_2_AUTH_KEY": "local-key"},
            clear=True,
        ):
            self.assertEqual(gpt_image2_api.get_auth_key(args), "explicit-key")


if __name__ == "__main__":
    unittest.main()
