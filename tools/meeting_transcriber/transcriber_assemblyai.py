"""Transcription and speaker diarization via AssemblyAI API."""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# Retry upload/transcription on server errors (502, 503, 504, etc.)
UPLOAD_RETRIES = 3
UPLOAD_RETRY_DELAY_SEC = 5
# HTTP timeout for upload (large files need long write timeout; default 30s is too short)
UPLOAD_HTTP_TIMEOUT_SEC = 600


def _format_timestamp(seconds: float) -> str:
    """Format seconds as [HH:MM:SS] (same as formatter.format_timestamp)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"[{hours:02d}:{minutes:02d}:{secs:02d}]"


@dataclass
class UtteranceSegment:
    """Single utterance with speaker and timing (from AssemblyAI)."""

    start_ms: int
    end_ms: int
    speaker: str
    text: str


def transcribe_with_diarization(
    audio_path: Path,
    api_key: str,
    language_code: Optional[str] = "ru",
) -> list[UtteranceSegment]:
    """
    Transcribe audio and get speaker diarization via AssemblyAI.

    Args:
        audio_path: Path to audio/video file (local path; API accepts file upload).
        api_key: AssemblyAI API key.
        language_code: Language code (e.g. 'ru', 'en') or None for auto-detect.

    Returns:
        List of utterance segments with start/end in milliseconds and speaker label.
    """
    import assemblyai as aai

    aai.settings.api_key = api_key
    # Large file uploads need a longer write timeout (default 30s causes WriteTimeout)
    aai.settings.http_timeout = UPLOAD_HTTP_TIMEOUT_SEC
    try:
        aai.client.Client._default = None
    except Exception:
        pass

    config = aai.TranscriptionConfig(
        speaker_labels=True,
        language_code=language_code or None,
    )
    transcriber = aai.Transcriber(config=config)
    last_error: Optional[Exception] = None
    for attempt in range(1, UPLOAD_RETRIES + 1):
        try:
            transcript = transcriber.transcribe(str(audio_path))
            break
        except Exception as e:
            last_error = e
            if attempt < UPLOAD_RETRIES:
                time.sleep(UPLOAD_RETRY_DELAY_SEC)
                continue
            raise last_error from e

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"AssemblyAI transcription failed: {transcript.error}")

    segments: list[UtteranceSegment] = []
    for u in transcript.utterances or []:
        segments.append(
            UtteranceSegment(
                start_ms=u.start,
                end_ms=u.end,
                speaker=u.speaker or "A",
                text=(u.text or "").strip(),
            )
        )

    return segments


def format_assemblyai_transcript(segments: list[UtteranceSegment]) -> str:
    """
    Format AssemblyAI utterances to the same style as local output:
    [HH:MM:SS] Speaker N: text
    """
    if not segments:
        return ""

    unique_speakers = []
    for s in segments:
        if s.speaker not in unique_speakers:
            unique_speakers.append(s.speaker)
    speaker_to_label = {s: f"Speaker {i + 1}" for i, s in enumerate(unique_speakers)}

    lines = []
    for seg in segments:
        ts = _format_timestamp(seg.start_ms / 1000.0)
        label = speaker_to_label.get(seg.speaker, "Unknown")
        lines.append(f"{ts} {label}: {seg.text}")

    return "\n".join(lines) + "\n"
