#!/usr/bin/env python3
from collections.abc import Mapping, MutableMapping
import os
import pathlib


LOCAL_ENV_PATH = pathlib.Path("~/.config/gpt-image-2-studio/env").expanduser()

AUTH_ENV_KEYS = (
    "GPT_IMAGE_2_AUTH_KEY",
    "OPENAI_API_KEY",
    "GPT_IMAGE_API_AUTH_KEY",
    "AUTH_KEY",
)

BASE_URL_ENV_KEYS = (
    "GPT_IMAGE_2_BASE_URL",
    "OPENAI_BASE_URL",
    "GPT_IMAGE_API_BASE",
)

MANAGED_ENV_GROUPS = (AUTH_ENV_KEYS, BASE_URL_ENV_KEYS)


def read_local_env(env_path: pathlib.Path = LOCAL_ENV_PATH) -> dict[str, str]:
    if not env_path.exists():
        return {}

    values: dict[str, str] = {}
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            continue
        values[key] = value.strip().strip('"').strip("'")
    return values


def first_env_key(env: Mapping[str, str], keys: tuple[str, ...]) -> str:
    return next((key for key in keys if env.get(key)), "")


def first_env_value(env: Mapping[str, str], keys: tuple[str, ...]) -> str:
    key = first_env_key(env, keys)
    return env.get(key, "")


def merge_local_env(
    env: Mapping[str, str], env_path: pathlib.Path = LOCAL_ENV_PATH
) -> dict[str, str]:
    local_values = read_local_env(env_path)
    merged = dict(env)

    # A configured credential or base URL group is authoritative as a whole.
    # This prevents a stale inherited alias from winning over a fresh local one.
    for group in MANAGED_ENV_GROUPS:
        if any(key in local_values for key in group):
            for key in group:
                merged.pop(key, None)

    merged.update(local_values)
    return merged


def apply_local_env(
    env: MutableMapping[str, str] = os.environ,
    env_path: pathlib.Path = LOCAL_ENV_PATH,
) -> None:
    merged = merge_local_env(env, env_path)
    for group in MANAGED_ENV_GROUPS:
        for key in group:
            env.pop(key, None)
    env.update(merged)
