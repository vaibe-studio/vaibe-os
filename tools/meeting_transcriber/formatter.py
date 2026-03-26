"""Format transcript with speaker diarization (for local Whisper + pyannote)."""

from .diarizer import DiarizationSegment
from .transcriber_whisper import TranscriptSegment


def format_timestamp(seconds: float) -> str:
    """Format seconds as [HH:MM:SS]."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"[{hours:02d}:{minutes:02d}:{secs:02d}]"


def find_speaker(time: float, diarization: list[DiarizationSegment]) -> str:
    """Find speaker for a given timestamp."""
    for seg in diarization:
        if seg.start <= time <= seg.end:
            return seg.speaker
    return "Unknown"


def normalize_speaker_names(diarization: list[DiarizationSegment]) -> dict[str, str]:
    """Create mapping from speaker IDs to numbered names."""
    unique_speakers = []
    for seg in diarization:
        if seg.speaker not in unique_speakers:
            unique_speakers.append(seg.speaker)
    return {speaker: f"Speaker {i + 1}" for i, speaker in enumerate(unique_speakers)}


def format_transcript(
    segments: list[TranscriptSegment],
    diarization: list[DiarizationSegment],
) -> str:
    """
    Combine transcription segments with speaker diarization.

    Output format (no header, no metadata):
    [HH:MM:SS] Speaker N: Text...
    """
    speaker_names = normalize_speaker_names(diarization)

    lines = []
    for seg in segments:
        timestamp = format_timestamp(seg.start)
        speaker_id = find_speaker(seg.start, diarization)
        speaker_name = speaker_names.get(speaker_id, "Unknown")
        lines.append(f"{timestamp} {speaker_name}: {seg.text}")

    return "\n".join(lines) + "\n"
