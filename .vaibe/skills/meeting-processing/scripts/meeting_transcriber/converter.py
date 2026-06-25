"""Audio conversion using ffmpeg."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


def convert_to_wav(input_path: Path) -> tuple[Path, Path | None]:
    """
    Convert input file to WAV 16kHz mono for pyannote.audio / Whisper compatibility.

    Returns:
        tuple: (audio_path_to_use, temp_file_path or None)
        If input is already .wav with correct format, returns (input_path, None).
        Otherwise creates temp file and returns (temp_path, temp_path) for cleanup.
    """
    input_path = Path(input_path)
    suffix = input_path.suffix.lower()

    # Prefer creating temp WAV for consistency
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_path = Path(temp_file.name)
    temp_file.close()

    try:
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                str(input_path),
                "-ar",
                "16000",
                "-ac",
                "1",
                "-y",
                str(temp_path),
            ],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        temp_path.unlink(missing_ok=True)
        raise RuntimeError(
            f"ffmpeg conversion failed: {e.stderr.decode()}"
        ) from e
    except FileNotFoundError:
        temp_path.unlink(missing_ok=True)
        raise RuntimeError("ffmpeg not found. Please install ffmpeg.")

    return temp_path, temp_path
