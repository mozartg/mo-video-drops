# SCORECARD — RESCORED 2026-08-10

**Reason:** `sharpness_gate.py` was recalibrated this session against Mozart's real reference
folder (`C:\Users\mozar\Desktop\High Quality Media Folder`, read-only). Corrected thresholds:
`SHARP_MIN = 1800.0` (Laplacian variance), `ENTROPY_MIN = 6.5`. Every prior pass/fail verdict in
`LEDGER.md` predates this correction and is invalid. This scorecard is the current authoritative
read for all published assets.

**Method:** `python sharpness_gate.py <file>.mp4` for each asset in
`C:\temp\claude-ops\drops\assets\`, using the script's `score_video()` path (4 sampled frames per
video, one every ~2s). No missing dependencies encountered — Pillow was already installed, ffmpeg
resolved via the script's hardcoded Krita path. No fixes needed.

## Results

| Asset | Mean Lap Var | Mean Entropy | Mean Colourfulness | Tier | Disposition |
|---|---|---|---|---|---|
| driveout-mileage-log-01.mp4 | 237.3 | 7.48 | 22.1 | **REJECT** | **FAILS CURRENT GATE — human review needed before continuing to treat as PUBLISHABLE.** |
| driveout-pay-floor-01.mp4 | 273.2 | 6.22 | 29.8 | **REJECT** | **FAILS CURRENT GATE — human review needed before continuing to treat as PUBLISHABLE.** |
| driveout-pay-floor-longer.mp4 | 282.1 | 6.22 | 29.7 | **REJECT** | **FAILS CURRENT GATE — human review needed before continuing to treat as PUBLISHABLE.** |
| driveout-mileage-cloudgen-EXPERIMENTAL.mp4 | 144.3 | 7.26 | 27.1 | **REJECT** | Already labeled EXPERIMENTAL / non-published; confirmed still failing. |

**Pass/fail count: 0 PASS / 4 REJECT.**

## Detail — why each failed

- **driveout-mileage-log-01.mp4** — sharpness only failure. Lap var 166–330, all far below the
  1800 floor (roughly 7–11x under threshold). Entropy is fine (7.35–7.56).
- **driveout-pay-floor-01.mp4** — fails both sharpness (187–335 vs 1800) and entropy (5.99–6.40
  vs 6.5) on every sampled frame.
- **driveout-pay-floor-longer.mp4** — same failure pattern as pay-floor-01 (same source content,
  longer cut): sharpness 207–342 vs 1800, entropy 6.00–6.41 vs 6.5.
- **driveout-mileage-cloudgen-EXPERIMENTAL.mp4** — sharpness only failure, and the worst of the
  four: lap var 129–169 vs 1800. Entropy fine (7.24–7.28). Was already flagged EXPERIMENTAL and
  not part of the "published" set proper.

## Net effect on published-asset status

Every asset currently listed under "PUBLISHED ASSETS" in `LEDGER.md`
(`driveout-pay-floor-01.mp4`, `driveout-mileage-log-01.mp4`, `driveout-pay-floor-longer.mp4`) now
fails the corrected gate. None were deleted or pulled by this pass — per instructions, no asset
is removed automatically. All three need explicit human review before continuing to be treated as
publishable under the corrected standard. `driveout-mileage-cloudgen-EXPERIMENTAL.mp4` was never
published and remains non-published, now confirmed failing under the corrected gate too.

## Files scored / located

All four found in `C:\temp\claude-ops\drops\assets\`:
- `driveout-mileage-log-01.mp4`
- `driveout-pay-floor-01.mp4`
- `driveout-pay-floor-longer.mp4`
- `driveout-mileage-cloudgen-EXPERIMENTAL.mp4`

No other published/generated video or image assets were found elsewhere under `C:\temp\claude-ops\`
matching ledger references (other files present under `media-test/` and `qa/` are intermediate
working artifacts, not published deliverables, and were not in scope for this rescore).
