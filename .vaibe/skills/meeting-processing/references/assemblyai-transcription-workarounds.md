# AssemblyAI: transcription problems and workarounds

> Purpose: operational memory for failures that actually occurred during
> transcription via AssemblyAI and the local backend (Whisper + pyannote) in the
> 2026-05-17 session. The goal is that the next agent or user does not
> re-diagnose already-known environment failures and external-API drift, but
> applies the fix right away.
>
> Related code: `meeting_transcriber/transcriber_assemblyai.py`,
> `config.py`, `converter.py`, `__main__.py`, `README.md` (under
> `.vaibe/skills/meeting-processing/scripts/meeting_transcriber/`).
> Related material: `.vaibe/skills/meeting-processing/SKILL.md`.
>
> Status as of 2026-05-17: fixes 1-5 are already applied in the code/material.
> This file explains the cause and how to diagnose if it recurs.

---

## 1. local-first is blocked without HUGGINGFACE_TOKEN

- **Symptom**: running the tool with the default backend `local`
  (`uv run --project <meeting_transcriber dir> --extra local <…>/main.py <file>`)
  fails with `Error: HUGGINGFACE_TOKEN not set...` even before models load.
- **Likely cause**: the local backend uses `pyannote/speaker-diarization-community-1`,
  which requires a HuggingFace token and accepting the model's terms. `config.py`
  (`load_config("local")`) requires the `HUGGINGFACE_TOKEN` variable and raises
  `ValueError` if it's missing.
- **Minimal workaround**: set `HUGGINGFACE_TOKEN` in the root `.env`
  (present in `.env.example`), get a token at
  https://huggingface.co/settings/tokens and accept the model terms at
  https://huggingface.co/pyannote/speaker-diarization-community-1. If there is no
  token/GPU — that's the normal condition for falling back to `--backend assemblyai`
  (needs `ASSEMBLYAI_API_KEY`).
- **Where it should live**: a rule for skills (local-first policy + fallback
  condition already in `meeting-processing` SKILL.md, Step 2) + a hint for the user
  (where to get the token — in `README.md` and the `config.py` error text).

## 2. The environment forces SOCKS/proxy, requests hits the proxy

- **Symptom**: HTTP requests to `api.assemblyai.com` hang/fail with proxy or
  connection errors, even though the key and network are fine (observed when the
  environment had `HTTP_PROXY`/`HTTPS_PROXY`/`ALL_PROXY`/SOCKS set).
- **Likely cause**: `requests` reads proxy environment variables by default
  (`trust_env=True`). The user's/IDE's environment forces a SOCKS or corporate
  proxy through which the AssemblyAI request does not pass.
- **Minimal workaround**: **already implemented in code** —
  `transcriber_assemblyai.py`, `_create_session()` creates a session with
  `session.trust_env = False`, forcing it to ignore the environment's proxy
  variables. For manual calls outside this module, repeat the same trick.
- **Where it should live**: the agent's operational knowledge (if the transcriber
  is replaced or an ad-hoc REST call is made — don't forget `trust_env=False`).
  The user doesn't need this detail.

## 3. AssemblyAI requires an up-to-date payload (speech_models)

- **Symptom**: creating a transcript (`POST /v2/transcript`) returns an error about
  needing to specify `speech_models` (API drift: the model used to be set differently).
- **Likely cause**: AssemblyAI changed the `POST /transcript` contract — the
  recognition model must be passed explicitly in the `speech_models` field.
- **Minimal workaround**: **already implemented** — `_submit_transcript()`
  sends the payload:
  `{"audio_url": <upload_url>, "speaker_labels": True, "speech_models": ["universal-2"]}`
  plus `"language_code"` when a language is set. Base URL — `API_BASE_URL =
  "https://api.assemblyai.com/v2"`. Auth header — `Authorization: <api_key>`
  (no `Bearer` prefix). On new API drift, check the request body against the current
  AssemblyAI docs and change only the `speech_models` value.
- **Where it should live**: the agent's operational knowledge (the exact current
  payload and the fact that the external API drifts — diagnose from the HTTP error
  body, which is propagated into the exception text via `_raise_for_status`).

## 4. Discovery and commands must account for .ogg and .m4a

- **Symptom**: voice recordings (`.ogg` from messengers, `.m4a` from a recorder)
  previously weren't found when searching `Инбокс/` or were rejected as an
  "unsupported format".
- **Likely cause**: the input-format list was narrower than the real set of
  voice files.
- **Minimal workaround**: **already covered** — supported formats in
  `__main__.py`: `SUPPORTED_FORMATS = {".mp4", ".webm", ".wav", ".mp3", ".ogg", ".m4a"}`;
  the same extensions are listed in `README.md`, in `meeting-processing` SKILL.md (Step 1),
  and in the command (§1). Conversion to WAV 16 kHz mono is done via ffmpeg
  (`converter.py`) for the local backend; AssemblyAI accepts the file as is.
- **Where it should live**: a rule for skills (the format list in the
  meeting-processing discovery step — already synced with the code).

## 5. Not every audio file is a "meeting" (single voice briefing)

- **Symptom**: the transcribed material is a long monologue by one speaker
  (a personal brief, note, case description), but the pipeline tries to format it as
  a classic meeting (`Встречи/`, participants, decisions).
- **Likely cause**: meeting-processing historically assumed a multi-party dialogue;
  a single voice briefing is a separate class of input.
- **Minimal workaround**: **already covered** by the edge-case detector in
  `meeting-processing` SKILL.md (Step 3, the "Single voice briefing" row) and in the
  command (§3): on the signal "one speaker, long monologue, no interaction" —
  stop and offer to save to `Исходные материалы/`, `База знаний/`,
  link to a task, or import as a meeting only on the user's explicit decision.
- **Where it should live**: a rule for skills (edge case in the procedure) + a hint
  for the user (offer alternative storage locations, don't force the meeting format).

---

## Summary map "where the knowledge lives"

| # | Problem | Agent operational knowledge | Rule for skills | Hint for the user |
|---|----------|:---:|:---:|:---:|
| 1 | HUGGINGFACE_TOKEN | | yes (local-first/fallback) | yes (where to get the token) |
| 2 | SOCKS/proxy | yes (`trust_env=False`) | | |
| 3 | speech_models / API drift | yes (current payload) | | |
| 4 | .ogg / .m4a | | yes (format list) | |
| 5 | voice briefing | | yes (edge case) | yes (storage location choice) |

## Known gaps (explicitly noted)

- The code has **no** auto-detection of "meeting vs single brief" — that is entirely
  on the skill procedure side (Step 3); the agent decides from the transcript content.
- The code has **no** option to disable diarization/`speaker_labels` for a known
  single-speaker recording — AssemblyAI returns one speaker anyway, so no extra action
  is needed, but it isn't optimized.
- The proxy bypass (`trust_env=False`) is wired only into the AssemblyAI module; the
  local backend (HuggingFace model downloads) is not protected against proxy forcing
  in the code — an untested scenario.
