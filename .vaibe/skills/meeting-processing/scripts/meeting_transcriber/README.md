# Meeting Transcriber

Транскрибация аудио/видео записей встреч с разделением по спикерам. Два бэкенда:

- **local** (по умолчанию) — Whisper + pyannote.audio на своей машине. Нужен GPU (CUDA), ffmpeg и `HUGGINGFACE_TOKEN` в `.env`.
- **assemblyai** — облачный API, не требует GPU. Нужен `ASSEMBLYAI_API_KEY` в `.env` или в переменной окружения.

## Требования

- Python 3.10+
- **AssemblyAI**: ffmpeg не обязателен (API принимает файл); ключ в `.env`.
- **Local**: NVIDIA GPU с CUDA (рекомендуется 8GB+ VRAM), ffmpeg, токен HuggingFace (принять условия модели pyannote/speaker-diarization-community-1).

## Установка

Это самостоятельный `uv`-проект (`pyproject.toml`). Отдельная установка не требуется —
`uv` при первом запуске создаёт `.venv` и ставит зависимости. Облачный backend
(AssemblyAI) — в базовых зависимостях; локальный (Whisper + pyannote, многогигабайтный) —
в `[project.optional-dependencies] local`, ставится только с флагом `--extra local`.

## Настройка

Скопировать `.env.example` в `.env` в корне репозитория.

- **AssemblyAI**: задать `ASSEMBLYAI_API_KEY` (https://www.assemblyai.com/app/account).
- **Local**: задать `HUGGINGFACE_TOKEN`, принять условия: https://huggingface.co/pyannote/speaker-diarization-community-1.

### Ограничения AssemblyAI

- **Размер загружаемого файла**: не более **2.2 ГБ**. Видео большего размера нужно предварительно конвертировать в аудио (например, `ffmpeg -i video.mp4 -vn -acodec libmp3lame -ab 128k audio.mp3`).
- **Таймаут загрузки**: по умолчанию в коде установлен 600 с. При медленном канале можно задать `ASSEMBLYAI_HTTP_TIMEOUT` в `.env` (в секундах).

## Использование

Запуск из корня репозитория; каталог проекта вынесен в `$P` для краткости:

```bash
P=.vaibe/skills/meeting-processing/scripts/meeting_transcriber
uv run --project $P $P/main.py <файл> [--lang CODE] [--backend local|assemblyai] [-o output.md]
# локальный backend (Whisper+pyannote):
uv run --project $P --extra local $P/main.py <файл> --backend local
```

### Политика бэкендов (агенты и `/meeting-processing`)

1. **Сначала local** — значение по умолчанию для `--backend` в CLI (`local`).
2. **AssemblyAI** — только как **fallback после сбоя** local (нет GPU, ошибка модели, и т.д.), если в `.env` задан `ASSEMBLYAI_API_KEY`. Не выбирать облако первым без явной просьбы пользователя.

### Аргументы

- `file` — путь к аудио/видео файлу
- `--lang` — язык (по умолчанию `ru`)
- `--backend` — `local` (**по умолчанию**) или `assemblyai`
- `-o`, `--output` — путь к выходному .md (по умолчанию рядом с входным файлом, расширение .md)

### Поддерживаемые форматы

mp4, webm, wav, mp3, ogg, m4a

### Примеры

С `P` из раздела «Использование» (`--extra local` добавлять для локального backend):

```bash
# Транскрибация локально (русский, по умолчанию)
uv run --project $P --extra local $P/main.py meeting.mp4

# Через AssemblyAI (облако)
uv run --project $P $P/main.py meeting.mp4 --backend assemblyai

# Локально, английский
uv run --project $P --extra local $P/main.py call.webm --lang en

# Указать выходной файл (облако)
uv run --project $P $P/main.py meeting.mp4 --backend assemblyai -o Проекты/ПРОЕКТ/Встречи/transcript.md
```

## Формат вывода

Один и тот же для обоих бэкендов (без заголовка, только строки):

```
[00:00:15] Speaker 1: Привет, начинаем митинг.
[00:00:22] Speaker 2: Да, давайте обсудим...
```

Используется в команде `/meeting-processing` и далее в `/summarize-meeting`.
