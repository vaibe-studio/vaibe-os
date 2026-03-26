# Meeting Transcriber

Транскрибация аудио/видео записей встреч с разделением по спикерам. Два бэкенда:

- **local** (по умолчанию) — Whisper + pyannote.audio на своей машине. Нужен GPU (CUDA), ffmpeg и `HUGGINGFACE_TOKEN` в `.env`.
- **assemblyai** — облачный API, не требует GPU. Нужен `ASSEMBLYAI_API_KEY` в `.env`.

## Требования

- Python 3.10+
- **AssemblyAI**: ffmpeg не обязателен (API принимает файл); ключ в `.env`.
- **Local**: NVIDIA GPU с CUDA (рекомендуется 8GB+ VRAM), ffmpeg, токен HuggingFace (принять условия модели pyannote/speaker-diarization-community-1).

## Установка

```bash
# Из корня репозитория
pip install -r tools/meeting_transcriber/requirements.txt
```

Только AssemblyAI (минимальный набор):

```bash
pip install python-dotenv assemblyai
```

## Настройка

Скопировать `.env.example` в `.env` в корне репозитория.

- **AssemblyAI**: задать `ASSEMBLYAI_API_KEY` (https://www.assemblyai.com/app/account).
- **Local**: задать `HUGGINGFACE_TOKEN`, принять условия: https://huggingface.co/pyannote/speaker-diarization-community-1.

### Ограничения AssemblyAI

- **Размер загружаемого файла**: не более **2.2 ГБ**. Видео большего размера нужно предварительно конвертировать в аудио (например, `ffmpeg -i video.mp4 -vn -acodec libmp3lame -ab 128k audio.mp3`).
- **Таймаут загрузки**: по умолчанию в коде установлен 600 с. При медленном канале можно задать `ASSEMBLYAI_HTTP_TIMEOUT` в `.env` (в секундах).

## Использование

```bash
python -m tools.meeting_transcriber <файл> [--lang CODE] [--backend assemblyai|local] [-o output.md]
```

### Аргументы

- `file` — путь к аудио/видео файлу
- `--lang` — язык (по умолчанию `ru`)
- `--backend` — `assemblyai` (по умолчанию) или `local`
- `-o`, `--output` — путь к выходному .md (по умолчанию рядом с входным файлом, расширение .md)

### Поддерживаемые форматы

mp4, webm, wav, mp3, ogg, m4a

### Примеры

```bash
# Транскрибация локально (русский, по умолчанию)
python -m tools.meeting_transcriber meeting.mp4

# Через AssemblyAI (облако)
python -m tools.meeting_transcriber meeting.mp4 --backend assemblyai

# Локально, английский
python -m tools.meeting_transcriber call.webm --lang en

# Указать выходной файл
python -m tools.meeting_transcriber meeting.mp4 -o Проекты/ПРОЕКТ/Встречи/transcript.md
```

Через единый CLI:

```bash
python -m tools meeting-transcriber meeting.mp4 --backend assemblyai
```

## Формат вывода

Один и тот же для обоих бэкендов (без заголовка, только строки):

```
[00:00:15] Speaker 1: Привет, начинаем митинг.
[00:00:22] Speaker 2: Да, давайте обсудим...
```

Используется в команде `/meeting-processing` и далее в `/summarize-meeting`.
