"""Transcription and speaker diarization via AssemblyAI REST API."""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import requests

# Retry upload/transcription on server errors (502, 503, 504, etc.)
UPLOAD_RETRIES = 3
UPLOAD_RETRY_DELAY_SEC = 5
POLL_DELAY_SEC = 3
# Large uploads need longer timeouts than the requests default.
UPLOAD_HTTP_TIMEOUT_SEC = 600
API_BASE_URL = "https://api.assemblyai.com/v2"


def _create_session() -> requests.Session:
    """Create a requests session that ignores ambient proxy variables."""
    session = requests.Session()
    session.trust_env = False
    return session


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
    timeout_sec = int(os.getenv("ASSEMBLYAI_HTTP_TIMEOUT", str(UPLOAD_HTTP_TIMEOUT_SEC)))
    headers = {"Authorization": api_key}
    session = _create_session()

    upload_url = _upload_file(session, audio_path, headers, timeout_sec)
    transcript_id = _submit_transcript(
        session, upload_url, headers, language_code, timeout_sec
    )
    transcript = _poll_transcript(session, transcript_id, headers, timeout_sec)

    segments: list[UtteranceSegment] = []
    for u in transcript.get("utterances") or []:
        segments.append(
            UtteranceSegment(
                start_ms=int(u.get("start", 0)),
                end_ms=int(u.get("end", 0)),
                speaker=str(u.get("speaker") or "A"),
                text=str(u.get("text") or "").strip(),
            )
        )

    return segments


def _upload_file(
    session: requests.Session, audio_path: Path, headers: dict[str, str], timeout_sec: int
) -> str:
    last_error: Optional[Exception] = None
    upload_headers = {
        **headers,
        "Content-Type": "application/octet-stream",
    }

    for attempt in range(1, UPLOAD_RETRIES + 1):
        try:
            with audio_path.open("rb") as f:
                response = session.post(
                    f"{API_BASE_URL}/upload",
                    headers=upload_headers,
                    data=f,
                    timeout=timeout_sec,
                )
            _raise_for_status(response, "upload file to AssemblyAI")
            upload_url = response.json().get("upload_url")
            if not upload_url:
                raise RuntimeError("AssemblyAI upload response does not contain upload_url.")
            return str(upload_url)
        except Exception as e:
            last_error = e
            if attempt < UPLOAD_RETRIES:
                time.sleep(UPLOAD_RETRY_DELAY_SEC)
                continue
            raise last_error

    raise RuntimeError("AssemblyAI upload failed for an unknown reason.")


def _submit_transcript(
    session: requests.Session,
    upload_url: str,
    headers: dict[str, str],
    language_code: Optional[str],
    timeout_sec: int,
) -> str:
    payload: dict[str, object] = {
        "audio_url": upload_url,
        "speaker_labels": True,
        "speech_models": ["universal-2"],
    }
    if language_code:
        payload["language_code"] = language_code

    response = session.post(
        f"{API_BASE_URL}/transcript",
        headers={**headers, "Content-Type": "application/json"},
        json=payload,
        timeout=timeout_sec,
    )
    _raise_for_status(response, "create AssemblyAI transcript")

    transcript_id = response.json().get("id")
    if not transcript_id:
        raise RuntimeError("AssemblyAI transcript response does not contain id.")
    return str(transcript_id)


def _poll_transcript(
    session: requests.Session,
    transcript_id: str,
    headers: dict[str, str],
    timeout_sec: int,
) -> dict:
    while True:
        response = session.get(
            f"{API_BASE_URL}/transcript/{transcript_id}",
            headers=headers,
            timeout=timeout_sec,
        )
        _raise_for_status(response, "poll AssemblyAI transcript")

        data = response.json()
        status = data.get("status")
        if status == "completed":
            return data
        if status == "error":
            raise RuntimeError(
                f"AssemblyAI transcription failed: {data.get('error', 'unknown error')}"
            )
        time.sleep(POLL_DELAY_SEC)


def _raise_for_status(response: requests.Response, action: str) -> None:
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        body = response.text.strip()
        message = f"Failed to {action}: HTTP {response.status_code}"
        if body:
            message = f"{message} - {body}"
        raise RuntimeError(message) from e


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
