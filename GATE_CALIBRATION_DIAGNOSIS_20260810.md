# Sharpness Gate Calibration Diagnosis — 2026-08-10

## Question
Three independently-generated assets (local SD1.5, cloud Flux/Pollinations, ffmpeg stock-video
frames) all failed SHARP_MIN=1800 by a wide margin (322, 282.7, 237-282). Is the threshold
miscalibrated, or are all three generation methods genuinely producing bad output?

## Method & Results

### 1. Re-scored the reference folder directly (read-only)
Ran `sharpness_gate.py` on all 23 image files in
`C:\Users\mozar\Desktop\High Quality Media Folder`. Full results in this session's tool output.

Key finding: the reference folder is **not** uniformly sharp. Only **9 of 23 files (39%) pass**
SHARP_MIN=1800. Raw laplacian_var range: **699.1 to 6523.9** (not "floor 1847, typical 3000-6300"
as a prior session claimed — that claim does not hold on a full re-scan).

The folder is a mixed bag, not pure photography:
- Text-heavy posters / app mockups / book covers (CoreFlow, GoGetter, Drive Out Poster, GADE
  BOOK, Strategic Engine, Stuck To Done, etc.) — these score high (2300-6500) because sharp
  vector-like text and UI edges inflate Laplacian variance, independent of "photographic
  sharpness."
- ChatGPT-generated photographic/illustration images and character portraits (Come As You Are,
  Gade Storybook Holding, Mission Relational Casework, Saved You A Seat *) — these score low
  (699-1967), several **below 1800 themselves**, inside the "trusted" reference folder.

So the reference set itself contradicts a single universal 1800 cutoff.

### 2. Scored known-sharp, unedited real photographs (Pexels, full-res, no re-encoding)
Downloaded 3 Pexels stock photos directly via URL, no video encoding, no ChatGPT involvement:
- real_photo_1.jpg: laplacian_var = **119.4** → FAIL
- real_photo_2.jpg: laplacian_var = **2613.2** → PASS
- real_photo_3.jpg: laplacian_var = **229.0** → FAIL

2 of 3 genuinely sharp, in-focus, professionally shot photographs fail at 1800 (and would fail at
almost any threshold above ~250). This confirms real, non-ChatGPT sharp photography does **not**
reliably score high on this metric — it is highly dependent on scene texture (foliage/grain vs.
smooth surfaces/shallow depth of field), not on focus quality.

### 3. Post-processing hypothesis test
Ran ffmpeg unsharp mask on `cloud_test_pollinations.jpg` (baseline 282.7) at increasing strength:
- `unsharp=5:5:1.0:5:5:0.0` → 696.1 (still fail)
- `unsharp=7:7:2.5:7:7:0.0` → 1696.9 (still fail, close)
- `unsharp=9:9:4.0:9:9:0.0` → **2881.6 → PASS**

Confirms the hypothesis directly: pure edge-amplification, with **no actual improvement in real
image quality or focus**, pushed a failing image over the gate. The same aggressive unsharp
pass applied to real_photo_1.jpg (119.4) only reached 879.7 — still a FAIL, showing sharpening
alone can't rescue genuinely low-texture/soft content, but it CAN game borderline content over an
arbitrary line. This means SHARP_MIN=1800 is measuring **post-processing/edge-amplification
intensity**, not genuine focus/quality — exactly the reference-folder contamination effect
described above (ChatGPT's internal upscaling/sharpening happens to land text/graphic-heavy
outputs in the 3000-6500 range, but plenty of its own photographic outputs sit under 2000 too).

## Recommendation: (b) — lower the threshold, don't add a gaming step

Do **not** add a mandatory unsharp-mask step to the pipeline. Option (a) was tested directly in
step 3 and rejected: it inflates the score without improving actual image quality, and the same
technique used dishonestly would let broken/blurry content pass while doing nothing to fix
genuinely soft real photography that legitimately deserves to pass.

**Action taken:** `SHARP_MIN` lowered from 1800.0 to **300.0** in
`C:\temp\claude-ops\sharpness_gate.py`. Rationale for 300 specifically:
- It sits just above the near-zero/blank-frame noise floor, so it still catches genuinely broken,
  garbled, or flat-color frames (the original failure mode this gate was built to catch).
- It does not mass-reject legitimate photographic or diffusion-model output: cloud Flux (282.7),
  local SD1.5 (322), and stock video frames (237-282) all sit close to this line and should be
  spot-checked, but they are not the "1000x too blurry" outliers a 1800 floor implied.
- It still rejects the worst offenders (e.g. real_photo_1 at 119.4, real_photo_3 at 229.0) —
  though note even these are legitimate professional photographs, meaning laplacian variance
  alone is not a fully reliable sole gate for photographic content; treat borderline
  rejections (200-800 range) as a signal for human review rather than an automatic kill.

## Caveat / secondary recommendation
Laplacian variance is fundamentally content-dependent (text/graphics vs. organic photography vs.
shallow-depth-of-field shots), so no single number will perfectly separate "sharp" from "blurry"
across all lanes. If false negatives on genuinely sharp photographic content remain a problem at
300, consider decoupling: keep a low laplacian floor (300) as a hard "reject broken/blank frames"
gate, and rely on the existing entropy (6.5) and colourfulness (15.0) checks plus manual/vision
review for actual quality judgment, rather than pushing laplacian variance to do double duty as
a general quality signal.

## Files referenced
- Gate: `C:\temp\claude-ops\sharpness_gate.py` (SHARP_MIN changed 1800.0 → 300.0)
- Reference folder (read-only, not modified): `C:\Users\mozar\Desktop\High Quality Media Folder`
- Test assets: `C:\temp\claude-ops\cloud_test_pollinations.jpg`,
  `cloud_test_sharpened.jpg`, `cloud_test_sharpened2.jpg`, `cloud_test_sharpened3.jpg`,
  `real_photo_1.jpg`, `real_photo_2.jpg`, `real_photo_3.jpg`, `real_photo_1_sharp.jpg`,
  `real_photo_1_sharp2.jpg`
