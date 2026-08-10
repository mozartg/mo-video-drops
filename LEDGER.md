# MEDIA PIPELINE LEDGER
**Owner:** Mozart Guerrier · **Maintained by:** Claude (media lane) · **Readable by:** ChatGPT, Codex, TRIGGERcmd, CatDesk
**Last updated:** 2026-08-09 · **Repo:** `mozartg/mo-video-drops` · **Live:** https://mozartg.github.io/mo-video-drops/

> Any agent picking up this work: read this file first. It is the state of truth.
> Do not reconstruct history from conversation. Resume from `NEXT ACTIONS`.

---

## 1. LANE STATUS — measured, not asserted

| Lane | Status | Evidence | Verdict |
|---|---|---|---|
| **HYBRID-STOCK** (Pexels video + edge-tts + ffmpeg) | **WORKS — SELF-TESTED** | 2/2 samples built and gate-passed. Sharpness lap **471** | **THIS IS THE QUALITY LANE** |
| **CLOUD-GEN** (Pollinations image + edge-tts) | **PARTIAL** | 1/2 samples. Images score lap **29.5–46.4** vs threshold 120 | Fails clarity bar ~50% of the time |
| **LOCAL-ONLY** (ComfyUI) | **DEAD — CONFIRMED** | No `main.py`, no `python_embeded`, 0 checkpoints in `C:\Users\mozar\TriggerCMD-Scripts\Tools\ComfyUI` | Not installed. Empty shell |
| **AVG image generation** | **DOES NOT EXIST** | `src/lib/media-downloader.ts` has only stock search/download + `generateOfflineVisual` placeholder | AVG is an assembler, not a generator |

**Decisive finding:** Pexels stock footage is **10–16× sharper** than Pollinations output on the same
Laplacian-variance measure. For Mozart's stated standard ("clear picture looking out from a car",
≤15% blur tolerance), **AI-generated stills do not meet the bar and stock footage does.**

---

## 2. QUALITY GATES (calibrated against Mozart's own ratings)

| Gate | Threshold | Rejects | Cost |
|---|---|---|---|
| Sharpness — Laplacian variance | **≥ 120** | photographic blur, soft focus | ~100 ms |
| Detail — histogram entropy | **≥ 5.2** | flat/solid frames | ~50 ms |
| Colourfulness — Hasler-Susstrunk | **≥ 15** | washed out | ~50 ms |
| Audio present — RMS dBFS | **> −50** | silence | ~1 s |
| Speech — modulation index / spectral flatness | **M ≥ 0.18**, `0.02 ≤ SF ≤ 0.6` | tones, non-speech | ~2 s |
| Vision semantic — `minicpm-v` | flags only | garbled text, wrong subject | **138 s** — finalists only |

**Calibration record:** entropy was originally 6.5 and produced false rejects on legitimate night
footage. Recalibrated to 5.2 using Mozart's v1-poor / v2-good ratings as ground truth.
**Ground-truth anchors:** v1 (rejected by Mozart) = lap 25.1 · v2 (accepted) = lap 282.1.

---

## 3. WORKING TOOLCHAIN — verified live

| Component | Path / endpoint | State |
|---|---|---|
| ffmpeg / ffprobe | `C:\Program Files\Krita (x64)\bin\` | LIVE. **No `drawtext`** — captions need PNG overlay |
| edge-tts | `...\Python312\Scripts\edge-tts.exe` | LIVE. Use `--rate=-14%` **with equals sign** |
| Pexels API | `api.pexels.com` | LIVE. **Requires `User-Agent` header from Python** |
| Pollinations | `image.pollinations.ai` | LIVE, no auth. **Requires `User-Agent` from Python** |
| Ollama | `127.0.0.1:11434` | LIVE — llama3.2, minicpm-v, qwen3, qwen2.5-coder |
| n8n | `127.0.0.1:5678` | LIVE, API authenticated, **0 workflows** (old ones deleted as trash) |
| AVG portal | `npx tsx src/server.ts`, PORT=3021 | WORKS. Desktop shortcut "Video Studio" |
| GitHub Pages | `mozartg.github.io/mo-video-drops` | **LIVE, HTTP 200** |

### Known traps — do not rediscover these
1. **Silent `except` blocks cost two wrong conclusions this session.** Always log the exception.
2. **Python `urllib` default User-Agent is blocked** by both Pexels and Pollinations. PowerShell is not.
3. **This network returns HTTP 200 from `api.pexels.com` for a garbage API key.** HTTP status cannot
   validate Pexels auth here — only whether real footage returns.
4. **AVG's `.env` keys did not persist from the setup UI.** Write keys to `.env` directly.
5. **AVG form requires `defaultVideo`**; sending `""` fails validation, omitting the field works.
6. **Krita's ffmpeg lacks `drawtext`** (no libfreetype). Use PNG overlay for captions.
7. **GitHub caps files at 100 MB.** 10-minute video will exceed this — needs alternate hosting.

---

## 4. PUBLISHED ASSETS

| Asset | URL | Gate |
|---|---|---|
| Drive Out — pay floor (short) | `/assets/driveout-pay-floor-01.mp4` | PASS |
| Drive Out — mileage log (short) | `/assets/driveout-mileage-log-01.mp4` | PASS |
| Drive Out — pay floor extended (31s) | `/assets/driveout-pay-floor-longer.mp4` | PASS |

All under https://mozartg.github.io/mo-video-drops/

**Licensing position:** Pexels License (free commercial use, no attribution) for all published footage.
edge-tts for voice. **Pollinations output is EXCLUDED from published work** — its commercial terms are
unresolved upstream (pollinations/pollinations issue #8741). Prototyping only.

---

## 5. BLOCKERS REQUIRING MOZART

1. **GitHub Actions is billing-blocked** — *"recent account payments have failed or your spending limit
   needs to be increased."* All private-repo scheduled workflows fail in 2–3 s with zero steps. This is
   money, not engineering. Verified on runs `31325495770` (mo-stack) and `31325124058` (test-vercel-deploy).
2. **Social accounts** — not yet created. Scheduler selection blocked until they exist.
3. **Long-form hosting** — 10-minute videos exceed GitHub's 100 MB limit.

---

## 6. NEXT ACTIONS (resume here)

**Media lane (Claude):**
1. Scale HYBRID-STOCK to 5–10 ten-second vertical shorts — the lane is proven, gate is calibrated.
2. Build PNG-overlay caption system (works around missing `drawtext`).
3. Brand-context image batch — source from Pexels/Pixabay/Unsplash (rights-clean), **not** Pollinations.
4. Solve long-form hosting before building 10-minute videos.
5. Build n8n workflows as a *work tunnel*, not just delivery — templates over brute force.

**Do not redo:** lane validation (done), gate calibration (done), ComfyUI (dead), AVG image gen (nonexistent).
