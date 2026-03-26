"""Speaker diarization using pyannote.audio (local)."""

from dataclasses import dataclass
from pathlib import Path

import torch
from pyannote.audio import Pipeline


@dataclass
class DiarizationSegment:
    """A segment with speaker identification."""

    start: float
    end: float
    speaker: str


def diarize(audio_path: Path, huggingface_token: str) -> list[DiarizationSegment]:
    """
    Perform speaker diarization on audio file.

    Args:
        audio_path: Path to audio file
        huggingface_token: HuggingFace API token

    Returns:
        List of diarization segments with speaker IDs (start/end in seconds).
    """
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-community-1",
        token=huggingface_token,
    )
    pipeline.to(torch.device("cuda"))

    diarization = pipeline(str(audio_path))

    segments = []
    for turn, speaker in diarization.speaker_diarization:
        segments.append(
            DiarizationSegment(
                start=turn.start,
                end=turn.end,
                speaker=speaker,
            )
        )

    del pipeline
    torch.cuda.empty_cache()

    return segments
