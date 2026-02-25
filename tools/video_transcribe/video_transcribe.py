#!/usr/bin/env python3
"""
Video Transcribe Tool

Скрипт для транскрибации видеофайлов из папки Инбокс.
Конвертирует видео (mp4, webm) в mp3 и использует AssemblyAI API
для получения текстовой транскрипции.

Usage:
    python -m tools.video_transcribe
    python -m tools.video_transcribe --input video.mp4
    python -m tools.video_transcribe --language ru
"""

import argparse
import logging
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Supported video formats
VIDEO_EXTENSIONS = {'.mp4', '.webm'}


def check_dependencies() -> bool:
    """Check if required dependencies are installed."""
    missing = []
    
    try:
        import assemblyai
    except ImportError:
        missing.append('assemblyai')
    
    try:
        from moviepy.video.io.VideoFileClip import VideoFileClip
    except ImportError:
        missing.append('moviepy')
    
    try:
        from dotenv import load_dotenv
    except ImportError:
        missing.append('python-dotenv')
    
    if missing:
        logger.error(f"Missing dependencies: {', '.join(missing)}")
        logger.error("Install with: pip install " + ' '.join(missing))
        return False
    
    return True


def find_video_files(inbox_path: Path) -> list[Path]:
    """
    Find all video files in the inbox folder.
    
    Args:
        inbox_path: Path to inbox folder
        
    Returns:
        List of paths to video files
    """
    video_files = []
    
    if not inbox_path.exists():
        logger.warning(f"Inbox folder not found: {inbox_path}")
        return video_files
    
    for file_path in inbox_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in VIDEO_EXTENSIONS:
            video_files.append(file_path)
    
    return sorted(video_files)


def convert_video_to_audio(video_path: Path, audio_path: Path) -> bool:
    """
    Convert video file to mp3 audio.
    
    Args:
        video_path: Path to input video file
        audio_path: Path to output audio file
        
    Returns:
        True if conversion successful
    """
    from moviepy.video.io.VideoFileClip import VideoFileClip
    
    try:
        logger.info(f"Converting video to audio: {video_path.name}")
        
        video = VideoFileClip(str(video_path))
        
        if video.audio is None:
            logger.error(f"Video has no audio track: {video_path.name}")
            video.close()
            return False
        
        video.audio.write_audiofile(
            str(audio_path),
            codec='libmp3lame',
            bitrate='192k',
            logger=None  # Suppress moviepy progress output
        )
        
        video.close()
        logger.info(f"Audio extracted: {audio_path.name}")
        return True
        
    except Exception as e:
        logger.error(f"Error converting video: {e}")
        return False


def transcribe_audio(
    audio_path: Path,
    api_key: str,
    language_code: Optional[str] = None,
    speaker_labels: bool = True
) -> Optional[str]:
    """
    Transcribe audio file using AssemblyAI API.
    
    Args:
        audio_path: Path to audio file
        api_key: AssemblyAI API key
        language_code: Language code (e.g., 'ru', 'en')
        speaker_labels: Enable speaker diarization
        
    Returns:
        Transcription text or None if failed
    """
    import assemblyai as aai
    
    aai.settings.api_key = api_key
    
    try:
        logger.info(f"Starting transcription: {audio_path.name}")
        
        # Configure transcription
        config = aai.TranscriptionConfig(
            speaker_labels=speaker_labels,
            language_code=language_code,
        )
        
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(str(audio_path), config=config)
        
        if transcript.status == aai.TranscriptStatus.error:
            logger.error(f"Transcription failed: {transcript.error}")
            return None
        
        logger.info("Transcription completed successfully")
        return transcript
        
    except Exception as e:
        logger.error(f"Error during transcription: {e}")
        return None


def format_transcript_markdown(
    transcript,
    video_name: str,
    include_timestamps: bool = True,
    include_speakers: bool = True
) -> str:
    """
    Format transcript as Markdown document.
    
    Args:
        transcript: AssemblyAI transcript object
        video_name: Original video file name
        include_timestamps: Include word timestamps
        include_speakers: Include speaker labels
        
    Returns:
        Formatted Markdown string
    """
    lines = []
    
    # Header
    lines.append(f"# Транскрипция: {video_name}")
    lines.append("")
    lines.append(f"**Дата обработки:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    if transcript.audio_duration:
        duration_min = int(transcript.audio_duration // 60)
        duration_sec = int(transcript.audio_duration % 60)
        lines.append(f"**Длительность:** {duration_min}:{duration_sec:02d}")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Check if we have speaker labels
    if include_speakers and transcript.utterances:
        lines.append("## Транскрипция по спикерам")
        lines.append("")
        
        for utterance in transcript.utterances:
            speaker = utterance.speaker
            text = utterance.text
            
            if include_timestamps:
                start_time = format_timestamp(utterance.start)
                lines.append(f"**[{start_time}] Спикер {speaker}:**")
            else:
                lines.append(f"**Спикер {speaker}:**")
            
            lines.append(f"> {text}")
            lines.append("")
    else:
        # Simple text output
        lines.append("## Текст транскрипции")
        lines.append("")
        lines.append(transcript.text or "")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Транскрипция выполнена с помощью AssemblyAI*")
    
    return '\n'.join(lines)


def format_timestamp(ms: int) -> str:
    """
    Format milliseconds as MM:SS or HH:MM:SS.
    
    Args:
        ms: Time in milliseconds
        
    Returns:
        Formatted time string
    """
    total_seconds = ms // 1000
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"


def process_video(
    video_path: Path,
    output_dir: Path,
    api_key: str,
    language_code: Optional[str] = None,
    keep_audio: bool = False
) -> Optional[Path]:
    """
    Process a single video file: convert to audio and transcribe.
    
    Args:
        video_path: Path to video file
        output_dir: Directory to save transcript
        api_key: AssemblyAI API key
        language_code: Language code for transcription
        keep_audio: Keep the extracted audio file
        
    Returns:
        Path to transcript file or None if failed
    """
    # Create temporary or permanent audio file
    if keep_audio:
        audio_path = output_dir / f"{video_path.stem}.mp3"
    else:
        temp_dir = tempfile.mkdtemp()
        audio_path = Path(temp_dir) / f"{video_path.stem}.mp3"
    
    try:
        # Convert video to audio
        if not convert_video_to_audio(video_path, audio_path):
            return None
        
        # Transcribe audio
        transcript = transcribe_audio(audio_path, api_key, language_code)
        
        if transcript is None:
            return None
        
        # Format and save transcript
        markdown_content = format_transcript_markdown(
            transcript,
            video_path.name
        )
        
        transcript_path = output_dir / f"{video_path.stem}_transcript.md"
        transcript_path.write_text(markdown_content, encoding='utf-8')
        
        logger.info(f"Transcript saved: {transcript_path}")
        return transcript_path
        
    finally:
        # Clean up temporary audio file
        if not keep_audio and audio_path.exists():
            audio_path.unlink()
            if audio_path.parent != output_dir:
                audio_path.parent.rmdir()


def get_project_root() -> Path:
    """Get the project root directory."""
    # This file is at tools/video_transcribe/video_transcribe.py
    # Project root is 3 levels up
    return Path(__file__).parent.parent.parent


def load_api_key() -> Optional[str]:
    """Load AssemblyAI API key from environment."""
    from dotenv import load_dotenv
    
    # Try to load from project .env file
    project_root = get_project_root()
    env_file = project_root / '.env'
    
    if env_file.exists():
        load_dotenv(env_file)
    
    api_key = os.getenv('ASSEMBLYAI_API_KEY')
    
    if not api_key:
        logger.error("ASSEMBLYAI_API_KEY not found in environment")
        logger.error(f"Add it to {env_file} or set as environment variable")
    
    return api_key


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Transcribe video files from Inbox folder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Process all videos in Инбокс/
  %(prog)s --input video.mp4         # Process specific video
  %(prog)s --language ru             # Force Russian language
  %(prog)s --keep-audio              # Keep extracted audio file
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        help='Specific video file to process (relative to Инбокс/ or absolute path)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output directory for transcript (default: same as input)'
    )
    
    parser.add_argument(
        '-l', '--language',
        help='Language code for transcription (e.g., "ru", "en"). Auto-detect if not specified'
    )
    
    parser.add_argument(
        '--keep-audio',
        action='store_true',
        help='Keep the extracted audio file'
    )
    
    parser.add_argument(
        '--api-key',
        help='AssemblyAI API key (overrides environment variable)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Get API key
    api_key = args.api_key or load_api_key()
    if not api_key:
        return 1
    
    # Determine paths
    project_root = get_project_root()
    inbox_path = project_root / 'Инбокс'
    
    # Find videos to process
    if args.input:
        input_path = Path(args.input)
        if not input_path.is_absolute():
            # Try relative to inbox first
            if (inbox_path / input_path).exists():
                input_path = inbox_path / input_path
            # Then try relative to current directory
            elif not input_path.exists():
                logger.error(f"Video file not found: {args.input}")
                return 1
        
        if not input_path.exists():
            logger.error(f"Video file not found: {input_path}")
            return 1
        
        video_files = [input_path]
        default_output = input_path.parent
    else:
        video_files = find_video_files(inbox_path)
        default_output = inbox_path
        
        if not video_files:
            logger.info(f"No video files found in {inbox_path}")
            logger.info(f"Supported formats: {', '.join(VIDEO_EXTENSIONS)}")
            return 0
    
    # Determine output directory
    output_dir = Path(args.output) if args.output else default_output
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process videos
    logger.info(f"Found {len(video_files)} video file(s) to process")
    
    success_count = 0
    for video_path in video_files:
        logger.info(f"\n{'='*50}")
        logger.info(f"Processing: {video_path.name}")
        
        result = process_video(
            video_path=video_path,
            output_dir=output_dir,
            api_key=api_key,
            language_code=args.language,
            keep_audio=args.keep_audio
        )
        
        if result:
            success_count += 1
    
    # Summary
    logger.info(f"\n{'='*50}")
    logger.info(f"Completed: {success_count}/{len(video_files)} videos processed successfully")
    
    return 0 if success_count == len(video_files) else 1


if __name__ == '__main__':
    sys.exit(main())
