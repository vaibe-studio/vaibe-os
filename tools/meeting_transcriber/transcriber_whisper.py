"""Audio transcription using Whisper (local)."""

from dataclasses import dataclass
from pathlib import Path

import whisper


@dataclass
class TranscriptSegment:
    """A segment of transcribed text with timing."""

    start: float
    end: float
    text: str


def transcribe(audio_path: Path, language: str = "ru") -> list[TranscriptSegment]:
    """
    Transcribe audio file using Whisper.

    Args:
        audio_path: Path to audio file
        language: Language code for transcription

    Returns:
        List of transcript segments with timestamps (seconds).
    """
    model = whisper.load_model("medium", device="cuda")

    result = model.transcribe(
        str(audio_path),
        language=language,
        verbose=False,
    )

    segments = []
    for seg in result["segments"]:
        segments.append(
            TranscriptSegment(
                start=seg["start"],
                end=seg["end"],
                text=seg["text"].strip(),
            )
        )

    return segments
