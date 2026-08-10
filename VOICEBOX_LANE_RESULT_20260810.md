# Voicebox TTS Lane — Result (2026-08-10)

## Status: BLOCKED (no usable audio clip produced)

Voicebox (`C:\Users\mozar\Desktop\Voicebox`) was actually launched and exercised via its REST
API for the first time — prior sessions only inventoried the binaries. `voicebox-server.exe`
starts cleanly and serves a full OpenAPI surface, but every TTS engine tried either failed the
individual generation or crashed the whole server process. No known documented issue (torch.xpu
#582, chatterbox tag misuse) was hit — these are new, previously unreported failures on this
machine.

## What worked

- **Server startup**: `voicebox-server.exe` from its own directory (no args needed) binds to
  `http://127.0.0.1:8000` in ~20-25s. Log confirms `Backend: PYTORCH`, `GPU: None (CPU only)`,
  `Ready`. No install/setup friction — binary just runs.
- **API discovery**: `GET /openapi.json` lists the full REST surface (`/speak`, `/generate`,
  `/profiles`, `/models/status`, etc.) — no separate docs needed, self-documenting.
- **Model inventory** (`GET /models/status`): confirmed Chatterbox (both variants) are **not
  downloaded** on this machine, so issue #582 (`torch.xpu` AttributeError) was structurally
  avoided — it can't fire if the model was never fetched. Already-downloaded, CPU-viable engines:
  `luxtts` (1.1 GB, "Fast, CPU-friendly"), `qwen-tts-1.7B` (4.3 GB), `qwen-tts-0.6B` (2.4 GB).
- One existing voice profile was present from a prior session ("SwarmTest VSL-Explainer-MG",
  cloned voice type, 1 sample) — reused as the `profile` param for generation attempts.

## What failed

**Attempt 1 — engine=`luxtts`, existing profile, text: "Your mileage log is your evidence. Track
every trip, every time."**
Generation request accepted (`status: generating`), model loaded successfully
(`LuxTTS loaded successfully`), but generation itself threw and the job status flipped to
`failed`. Server stayed alive. Exact error from `/generate/{id}/status`:

```
Calculated padded input size per channel: (6). Kernel size: (7). Kernel size can't be greater than actual input size
```

Traceback shows this originates inside `zipvoice/onnx_modeling.py` → `vocos.py` conv1d decode —
a vocoder-side shape mismatch, almost certainly because the cloned voice sample attached to the
profile is too short/incompatible for LuxTTS's voice-cloning input requirements (that sample was
presumably recorded for a different engine, e.g. qwen). LuxTTS has no built-in preset voices
(`GET /profiles/presets/luxtts` returns an empty voice list), so cloning is mandatory and no
fallback default voice exists.

**Attempt 2 — engine=`qwen` (1.7B), same profile, same text.**
Model began loading (`Loading TTS model 1.7B on cpu...`, talker/code_predictor config init logged),
then the **entire voicebox-server.exe process silently vanished** — no exception, no traceback, no
OOM message in stderr, `Get-Process` simply stopped finding it. Server was restarted and the exact
same sequence reproduced on a second, independent attempt (confirmed via process memory dropping
from ~340 MB back to ~75 MB between polls, with the log frozen mid-model-load both times). This
looks like a native crash / resource exhaustion while loading the 1.7B model on CPU without
flash-attn (a `Warning: flash-attn is not installed` was logged on the first attempt) — but the
process gives zero diagnostic output, so root cause is unconfirmed. This is not one of the
documented GitHub issues; it's new and worth filing.

No config file or CLI flag was found in the Voicebox directory to force a smaller model, cap
threads, or disable flash-attn checks — `voicebox-server.exe` only exposes `host`/`port`/`data_dir`
args per its startup log.

**qwen-tts-0.6B was not independently tested** — the `/speak` request's `model_size` param was
silently ignored (response still showed `"model_size":"1.7B"`), so it's unclear how to force the
smaller variant via this API without further engine-specific config digging, and time was spent
confirming the crash was reproducible instead.

## Output audio

**None produced.** Zero clips were generated across two engines and two independent server
sessions. No file was copied to `assets/` because none exists.

## Comparison to edge-tts (honest, factual only)

| Axis | edge-tts | Voicebox (this session) |
|---|---|---|
| Setup friction | Already working, proven in a published video | Binary launches cleanly with zero config, but every attempted engine failed to produce output |
| Latency to first clip | Fast (cloud API, seconds) | N/A — never reached a completed generation; ~20-25s just for server boot, engine model loads took 45s-2min+ before failing/crashing |
| Reliability | Stable, used in production | 2/2 engine attempts failed; one crashed the whole server process, reproducibly |
| Audio quality (objective) | N/A here, not re-measured this session | N/A — no file to measure sample rate/bitrate/RMS on |
| Paralinguistic tags | N/A | Not tested — correctly avoided per instructions since Chatterbox Turbo (the only engine where tags work) isn't downloaded |

No audio RMS/speech-detection gate script was found in `C:\temp\claude-ops` — `LEDGER.md`
references only the image-quality `sharpness_gate.py` (Laplacian variance / entropy thresholds
for images), which is not applicable to audio. No audio-specific gate exists in this project yet.

## Verdict

**Not a viable second TTS lane in its current state on this machine.** Both CPU-viable engines
that were tried failed outright — one with a reproducible vocoder shape-mismatch on the existing
voice profile's sample, the other with a reproducible silent process crash during model load. A
human listen-test is moot because no audio was ever generated to listen to. Before this lane can
be reconsidered: (1) re-record or re-check the profile's voice sample for LuxTTS compatibility,
or create a fresh profile with a longer/cleaner sample, (2) investigate the qwen 1.7B crash with a
debugger/verbose logging or try qwen-0.6B via whatever mechanism actually selects the smaller
model (not the ignored `model_size` field on `/speak`), and (3) consider that CPU-only inference
for these transformer-based TTS engines may simply be under-resourced on this hardware regardless
of which specific engine is chosen.
