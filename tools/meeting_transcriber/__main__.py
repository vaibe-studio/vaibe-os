"""CLI entry point for meeting transcription (local or AssemblyAI)."""

import argparse
import sys
from pathlib import Path

from .config import load_config
from .converter import convert_to_wav
from .transcriber_assemblyai import (
    format_assemblyai_transcript,
    transcribe_with_diarization as assemblyai_transcribe,
)

SUPPORTED_FORMATS = {".mp4", ".webm", ".wav", ".mp3", ".ogg", ".m4a"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transcribe audio/video meeting recordings with speaker diarization (local or AssemblyAI)"
    )
    parser.add_argument("file", type=Path, help="Input audio/video file")
    parser.add_argument(
        "--lang",
        default="ru",
        help="Transcription language code (default: ru). For AssemblyAI use 'ru', 'en', etc.",
    )
    parser.add_argument(
        "--backend",
        choices=["local", "assemblyai"],
        default="local",
        help="Backend: local (Whisper + pyannote.audio) or assemblyai (API). Default: local",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output .md file path (default: next to input with .md extension)",
    )
    return parser.parse_args()


def validate_input(input_path: Path) -> Path:
    """Validate input file; return path to use for output .md if not overridden."""
    input_path = input_path.resolve()
    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    if input_path.suffix.lower() not in SUPPORTED_FORMATS:
        print(f"Error: Unsupported format: {input_path.suffix}", file=sys.stderr)
        print(f"Supported: {', '.join(sorted(SUPPORTED_FORMATS))}", file=sys.stderr)
        sys.exit(1)

    return input_path


def run_local(input_path: Path, output_path: Path, lang: str, config: dict) -> None:
    """Run transcription and diarization locally (Whisper + pyannote)."""
    from .diarizer import diarize
    from .formatter import format_transcript
    from .transcriber_whisper import transcribe as whisper_transcribe

    audio_path, temp_audio = convert_to_wav(input_path)
    try:
        diarization = diarize(audio_path, config["huggingface_token"])
        segments = whisper_transcribe(audio_path, language=lang)
        result = format_transcript(segments, diarization)
        output_path.write_text(result, encoding="utf-8")
    finally:
        if temp_audio and temp_audio.exists():
            temp_audio.unlink(missing_ok=True)


def run_assemblyai(
    input_path: Path, output_path: Path, lang: str, config: dict
) -> None:
    """Run transcription and diarization via AssemblyAI API."""
    segments = assemblyai_transcribe(
        input_path,
        api_key=config["assemblyai_api_key"],
        language_code=lang or None,
    )
    result = format_assemblyai_transcript(segments)
    output_path.write_text(result, encoding="utf-8")


def main() -> None:
    args = parse_args()
    input_path = validate_input(args.file)
    output_path = args.output or input_path.with_suffix(".md")
    output_path = output_path.resolve()

    if output_path.exists():
        print(f"Warning: Output already exists: {output_path}", file=sys.stderr)
        sys.exit(1)

    try:
        config = load_config(args.backend)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        if args.backend == "local":
            run_local(input_path, output_path, args.lang, config)
        else:
            run_assemblyai(input_path, output_path, args.lang, config)
        print(f"Transcript saved: {output_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if output_path.exists():
            output_path.unlink(missing_ok=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
