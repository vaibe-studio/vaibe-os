"""Configuration loading from environment variables."""

import os
from pathlib import Path

from dotenv import load_dotenv


def get_repo_root() -> Path:
    """Get repository root directory (tools/meeting_transcriber -> repo root)."""
    return Path(__file__).resolve().parent.parent.parent


def load_config(backend: str) -> dict:
    """
    Load configuration from .env file and environment variables.
    backend: 'local' | 'assemblyai'
    """
    env_path = get_repo_root() / ".env"
    load_dotenv(env_path)

    if backend == "local":
        token = os.getenv("HUGGINGFACE_TOKEN")
        if not token:
            raise ValueError(
                "HUGGINGFACE_TOKEN not set. Copy .env.example to .env and set token "
                "(https://huggingface.co/settings/tokens, accept pyannote/speaker-diarization-community-1 terms)."
            )
        return {"huggingface_token": token}

    if backend == "assemblyai":
        api_key = os.getenv("ASSEMBLYAI_API_KEY")
        if not api_key:
            raise ValueError(
                "ASSEMBLYAI_API_KEY not set. Copy .env.example to .env and set key "
                "(https://www.assemblyai.com/app/account)."
            )
        return {"assemblyai_api_key": api_key}

    raise ValueError(f"Unknown backend: {backend}")
