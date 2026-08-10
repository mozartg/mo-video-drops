# MEDIA PIPELINE LEDGER
**Owner:** Mozart Guerrier · **Maintained by:** Claude (media lane) · **Readable by:** ChatGPT, Codex, TRIGGERcmd, CatDesk
**Last updated:** 2026-08-10 · **Repo:** `mozartg/mo-video-drops` · **Live:** https://mozartg.github.io/mo-video-drops/

> **2026-08-10 RESCORE:** All published video assets were re-run through the corrected sharpness gate (SHARP_MIN 1800 / ENTROPY_MIN 6.5). All 4 assets (driveout-mileage-log-01, driveout-pay-floor-01, driveout-pay-floor-longer, driveout-mileage-cloudgen-EXPERIMENTAL) now score REJECT. Full scorecard: `SCORECARD_RESCORED_20260810.md` in this same folder. None deleted -- human review needed before treating any of them as still publishable.


> **2026-08-10 GATE UPDATE (3rd pass, final):** The sharpness gate is now content-type-aware, not a single global threshold. It evolved twice today: global SHARP_MIN=1800 (miscalibrated, only 39% of the reference folder passed) -> stopgap global SHARP_MIN=300 -> final fix: PHOTO_SHARP_MIN=250 / GRAPHIC_SHARP_MIN=1800 selected automatically via a simple flat-region+edge-density heuristic, or forced with `--content-type photo|graphic`. Per PyImageSearch, Pertuz et al. 2013, and OpenCV's own blog, Laplacian-variance blur detection is inherently content-dependent and should never use one global number. See GATE_CALIBRATION_DIAGNOSIS_20260810.md ADDENDUM for full detail. Gate script: sharpness_gate.py.
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

---

## 7. CORRECTION — 2026-08-10: quality gate was miscalibrated, three lanes were wrongly written off

**Root cause of every "PASS" video that Mozart rejected on sight:** the sharpness gate threshold was
set to 120 based on my own bad output, never against Mozart's actual standard. He maintains a
READ-ONLY reference folder: `C:\Users\mozar\Desktop\High Quality Media Folder`. Measured directly:

| Reference file | Laplacian variance | Entropy |
|---|---|---|
| village_celebration.png | 6,341 | 7.82 |
| triumphant_goal.png | 6,277 | 7.53 |
| Drive Out Poster.png | 5,458 | 6.83 |
| stadium_crowd.png | 4,772 | 7.48 |
| Sample Shots.png (floor) | 1,847 | 7.21 |

**Corrected thresholds: SHARP_MIN = 1800, ENTROPY_MIN = 6.5** (was 120 / 5.2). Applied in
`C:\temp\claude-ops\sharpness_gate.py`. Every prior "PASS" video in this ledger scored 25-471 on
this scale and would REJECT under the real standard. Pexels stock was previously called "the quality
lane" at lap 471 -- that is 4x below the corrected floor and WRONG.

**ChatGPT image generation matches the standard.** Mozart's reference files are literally named
ChatGPT Image ....png and score 1,500-6,300. This is the image lane, not Pollinations.

**Three lanes I wrote off too early, corrected:**
- **AVG (Automated-Video-Generator):** NOT dead. Prior session killed a job at 31% out of impatience.
  Re-run 2026-08-10 reached 62%+ unattended. Verdict pending completion, but "underestimated" per
  Mozart's direct correction and the tool's own documentation.
- **ComfyUI:** NOT an empty shell. Prior check inspected the wrong path. Real install found at
  `C:\Users\mozar\TriggerCMD-Scripts\Tools\ComfyUI\repo\` -- full ComfyUI source, .venv with
  Python, and a working checkpoint (1-5-pruned-emaonly-fp16.safetensors, 2GB, SD1.5). Launched
  2026-08-10, verdict pending.
- **n8n:** Confirmed genuinely failed -- Mozart reports ~3 weeks / ~100 hours sunk with no working
  media output. This one stands as written off.

**Runway / HeyGen / BlitzReels / Apixel:** Mozart reports ChatGPT already tested these at scale and
found them a "trap door" -- fine for one asset, collapses under volume. Not being pursued further.

**Cloudinary:** works intermittently per Mozart. Cloudflare available as a second host option, untested.


---

## 8. VSRR 2.0 TRACE — 2026-08-10

**Protocol:** Diagnose -> Plan -> Fix -> Verify. The requested outcome is the mission; a blocked vendor route is not the same as an impossible outcome.

### Verified conclusions

- **Image batch:** 50 final PNGs are in Drive: 17 Drive Out, 17 Core Flow, 16 Stuck To Done. The authoritative score table was refreshed after strict prompt-gate review: every final row has Laplacian variance >= 1800 and entropy >= 6.8. Native ChatGPT image output measured 1.572-1.573 MP, below the requested 1.6 MP floor; this platform limitation is recorded rather than hidden.
- **Replacement repair:** The original Stuck To Done rows 11, 13, and 14 were moved to a Drive rejection folder. Replacements were measured at Lap/entropy 3659.96/7.109912, 5244.47/7.332216, and 3733.19/7.373141.
- **Cloudinary:** current connected-account usage receipt exposes a 100 MB video maximum. Cloudinary's official documentation describes chunked uploads for files over 100 MB, but the connected tool exposed no chunked local-file path. The 213,876,372-byte MP4 fixture was rejected on the local-path route, so no public 200 MB Cloudinary URL was claimed and the chunked route remains unverified here.
- **Cloudflare:** authenticated API call to list R2 buckets returned error 10042: R2 must be enabled in the Cloudflare Dashboard. No bucket or upload was created. This is a feature-enablement blocker, not an auth failure.
- **Alternative route:** the existing GitHub Pages site is live for the published page, but GitHub's 100 MB file cap and the connected Drive uploader's 100 MB transfer cap prevent treating it as a verified 200 MB video host. The tested boundary is therefore "no verified free 200 MB public host under the currently enabled routes," not universal impossibility.
- **Drive Out fact sheet:** the existing Source Ledger was extended in-place with dated NY and WA rows. WA L&I's 2026 rates and July 1, 2026 record/receipt changes are verified. NYC TLC's March 1, 2026 rates are verified. NY non-NYC current operator pages publish $28.41/hour while the NY AG settlement page remains stale on historical dollar examples; the discrepancy is explicitly preserved.

### Durable receipts

- Image folder: https://drive.google.com/drive/folders/18cbODWTdc_6_bNHwe6w5Py92AouTQLHB
- Score table: https://drive.google.com/file/d/18wdkXBZXWzWDDKgYI_ZBsxM1Y31U3HDJ/view?usp=drivesdk
- Hosting test folder: https://drive.google.com/drive/folders/1yDOnC5u4YgAYC3gEYSYyB_mbyi14Z7jP
- Source ledger workbook: https://docs.google.com/spreadsheets/d/1bdodhv6ou36Tvl--BVVELzJIueEijjXR5ErzB6sRqqo/edit
- Cloudflare API receipt: R2 bucket listing error 10042 on 2026-08-10

### Next route

1. Use Cloudinary for assets <=100 MB or split/segment longer media; do not call it a verified 200 MB host.
2. Enable R2 in the dashboard only if Mozart chooses that free-tier route, then rerun the same fixture through multipart upload and public delivery verification.
3. Continue the campaign with the verified image and fact-sheet deliverables without waiting on hosting.


---

## 9. SEMANTIC MEDIA REBUILD CANARY — 2026-08-10

**Truth correction:** The 50-image batch above passed its recorded numeric gate but is now **NUMERIC_PASS_SEMANTICALLY_SUPERSEDED**. It is not the accepted brand baseline. The production prompt required ChatGPT for the initial three-image trial; it did not require an exclusively ChatGPT-generated 50-image batch.

**Corrected briefs:**
- **Core Power:** discreet, fully clothed men's pelvic and hip wellness, including private support around frequent urination, erectile dysfunction, and erection quality. No sexualized imagery or outcome guarantees.
- **Drive Out:** rideshare-driver trip, mileage, cost, and working-condition evidence. No uncited statement about what a driver is owed.
- **Stuck To Done:** ADHD and neurodivergent movement from chaos or shutdown toward regulation, grounding, and realistic completion without shame.

**Verified canary deliverable:** Nine 1080x1920 images, three per lane, passed both semantic review and the calibrated numeric gate. Sharpness range: **1805.79-2752.91**. Entropy range: **6.817881-7.209373**. Every image is **2.0736 MP**. Synthetic figures visible in Drive Out 03 were blurred before promotion.

**Working route:** ChatGPT or licensed-stock source scene -> local composition, typography, factual cleanup, hashing, and calibrated QA. Two Pexels-derived assets retain source URLs in the provenance receipt.

**Local-only route:** ComfyUI was tested twice at the real install with the real SD1.5 checkpoint. Default CPU attention and split CPU attention both ended in Windows fatal access violations. Persistent blocker: `LOCAL-COMFY-CPU-ACCESS-001`. Status: **PARKED_NO_VERIFIED_PATH_UNDER_CURRENT_CPU_RUNTIME**. Do not repeat unchanged.

**Durable receipts:**
- Rebuild folder: https://drive.google.com/drive/folders/1TepkRjhzFIklsTBXxJsVB7AaNoFN2AQE
- Numeric scorecard: https://drive.google.com/file/d/1Pnzn10llt9xkH43-4d4qS_P43ccIqZYk/view?usp=drivesdk
- Semantic/provenance scorecard: https://drive.google.com/file/d/1STNEt-aDEO73PnnV1a5XDGyrRjugIr9l/view?usp=drivesdk
- Red-team report: https://drive.google.com/file/d/1TznEhjpdM1K4rsvDo_zLngG8C29N1IW1/view?usp=drivesdk
- Local blocker receipt: https://drive.google.com/file/d/1O6G2XDYCK-J3CGMLYLLycTBuVak7CMxm/view?usp=drivesdk

**Scale state:** The corrected nine-image canary pack is **VERIFIED_PASS**. A replacement 50-image portfolio is **NOT_YET_PRODUCED** and may scale only through the dual numeric-semantic promotion rule.

---

## 10. TURNKEY REVENUE MEDIA RELEASE FACTORY — 2026-08-10

**Delivered:** A tested local state machine now converts the nine approved Core Power, Drive Out, and Stuck To Done canaries into dated revenue-facing release packages with captions, direct-message CTAs, alt text, hashes, provenance, calibrated QA, semantic review, copy red-team decisions, VSRR state, scenario planning, a calendar, and a visual review dashboard.

**Verified production job:** `revenue-release-20260811-v4`

- 9 planned / 9 promoted / 0 rejected
- 9 unique hashes / 9 provenance receipts / 9 copy red-team passes
- 0 missing packaged assets
- 0 external publish flags
- Schedule runs 2026-08-11 through 2026-08-19 across all three products

**Scheduled execution:** Windows task `MoMediaRevenueReleaseFactory` is Ready. Canary result was 0; a second invocation skipped the completed job rather than duplicating it. Next run: 2026-08-16 at 06:10 America/New_York. Output lands in synced `G:\My Drive\Mo Media Factory\Ready to Post`.

**Publisher truth boundary:** No authenticated social publisher was found after two distinct checks. Blocker `SOCIAL-PUBLISH-AUTH-001` is **PARKED**. The system continues creating `READY_TO_POST` packages and labels every external state `NOT_PUBLISHED`. Automatic publication requires a materially different route: connect one publisher and pass one canary post with a public URL receipt.

**Receipts:**

- Production release: https://drive.google.com/drive/folders/11cc3-wdCqQA-x4l13jvj-UYylsi7GQiO
- System receipts: https://drive.google.com/drive/folders/1wV-KdxA6-o0zeoLGuzA-599v0BG7XTck
- Turnkey receipt: https://drive.google.com/file/d/1HhuhsBlGKrwMJUsRFUgPwjf0VSonv5Bb/view?usp=drivesdk
- Dashboard visual QA: https://drive.google.com/file/d/1kjzbp6CI9mAPJFVB6sI0J-gR2aU3FRHf/view?usp=drivesdk
- Source: `media-ops/` in this repository

**Verification:** 7 Python tests passed, PowerShell parser passed, Task Scheduler returned 0, dashboard rendered in headless Edge and passed visual inspection. The read-only High Quality Media Folder was not modified.
