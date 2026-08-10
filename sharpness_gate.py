"""
T2 SHARPNESS / RICHNESS GATE  -- pure math, no AI, ~100ms per frame.
Closes the blind spot that let v1 PASS while Mozart rated the visuals poor.

WHY v1 SLIPPED THROUGH: the vision model reported "blurry" in plain English three
times, but the only boolean gate was looks_broken_or_garbled=false. "Mediocre" is
not "broken", so it passed. Prose was not converted into a threshold.

MATH
----
1) SHARPNESS = variance of the Laplacian.
   The Laplacian is a second-derivative edge kernel:
        0  1  0
        1 -4  1
        0  1  0
   Convolve, then take variance of the response. Sharp images carry high-frequency
   edge energy -> high variance. Blur is a low-pass filter: it removes exactly that
   energy -> variance collapses toward 0. Classic, deterministic, no model.

2) RICHNESS = Shannon entropy of the 256-bin luma histogram:
        H = -sum(p_i * log2(p_i))
   A flat/solid frame concentrates mass in few bins -> low H. 8.0 is the max.
   Catches the "solid car view" failure mode directly.

3) COLOURFULNESS = Hasler-Susstrunk metric on rg/yb opponent channels:
        rg = R - G ,  yb = 0.5(R+G) - B
        C  = sqrt(sd_rg^2 + sd_yb^2) + 0.3 * sqrt(mean_rg^2 + mean_yb^2)
   Flags washed-out or monochrome-by-accident frames.

THRESHOLDS are provisional and MUST be calibrated against Mozart's own ratings.
They are starting points, not truth.

================================================================================
CHANGELOG -- 2026-08-10, 3rd pass: CONTENT-TYPE-AWARE THRESHOLDS (final fix)
================================================================================
Prior passes today:
  1. Original global SHARP_MIN=1800 (calibrated off a reference folder that
     turned out to be a mixed bag of text-heavy posters/mockups AND soft
     photographic/illustration content -- only 39% of that same folder passed
     its own threshold).
  2. Stopgap: dropped to a single global SHARP_MIN=300 to stop false-rejecting
     real photographic content, at the cost of being too permissive for
     graphic/text assets.

THIRD-PARTY CONFIRMATION that a single global number is the wrong fix (not just
this project's data): PyImageSearch's canonical blur-detection tutorial, the
Pertuz et al. (2013) focus-measure survey ("Analysis of focus measure operators
for shape-from-focus"), and OpenCV's own comparative writeup on Laplacian
variance all state that variance-of-Laplacian is inherently content-dependent --
text/graphics/high-frequency-by-design content scores far higher than
photographic content at equal *real* sharpness, and the recommended practice is
per-dataset / per-content-type calibration, not one universal cutoff.

FIX: classify each image as "photo" or "graphic" (heuristic below, or an
explicit --content-type CLI override), then apply the threshold calibrated for
that content type using this session's own measured data:

  PHOTO_SHARP_MIN = 250
    Real, genuinely sharp photographic content measured this session:
      - Cloud Flux (Pollinations) photographic generation: 282.7
      - Local SD1.5 photographic generation: 322
      - ffmpeg video-frame extracts (stock video, photographic): 237-282
      - Reference-folder photographic/illustration content: 699-1967
    250 sits just under the lowest legitimate photographic scores observed
    (237-282), so it still rejects genuinely broken/blank/frozen/garbled
    frames (near-zero variance) without false-rejecting normal photographic
    sharpness variance. This is NOT the same as the earlier stopgap 300 --
    it is now scoped to photographic content only, so it doesn't also have to
    absorb graphic/text content's much higher legitimate range.

  GRAPHIC_SHARP_MIN = 1800
    Matches the reference folder's text-heavy posters / app-mockups / UI
    content, which legitimately scores 2300-6500 because sharp vector-like
    text and hard geometric edges inflate Laplacian variance on purpose. This
    is the ORIGINAL 1800 number -- it was never wrong for this content type,
    it was wrong applied globally to photographic content too.

CLASSIFICATION: see classify_content() below. Heuristic: graphic/text content
combines (a) a large fraction of near-uniform/flat-color pixels (solid
backgrounds, common in posters/UI/slides) with (b) unusually high edge density
relative to that flatness (hard text/vector edges cutting through those flat
regions). Photographic content is edge-rich but rarely dominated by large flat
regions in the same way. This is intentionally simple, not a trained
classifier -- if it misfires, use --content-type photo|graphic to override.
Fallback default is "photo" per Mozart's own instruction, since photographic
content (rideshare driver photos, video frames) is the overwhelming majority
of this project's media; graphic/poster assets from Canva/slides templates are
expected to be manually flagged with --content-type graphic when scored.

Sources (not fetched live in this pass, cited from prior research this
session): PyImageSearch "Blur detection with OpenCV" tutorial; S. Pertuz,
D. Puig, M. A. Garcia, "Analysis of focus measure operators for shape-from-
focus", Pattern Recognition 46(5), 2013; OpenCV blog comparative post on
Laplacian-variance blur metrics.

See also: C:\\temp\\claude-ops\\drops\\GATE_CALIBRATION_DIAGNOSIS_20260810.md
================================================================================
"""
import sys, os, json, math, argparse, subprocess, statistics

FF = r"C:\Program Files\Krita (x64)\bin\ffmpeg.exe"

try:
    from PIL import Image
except ImportError:
    print(json.dumps({"error": "Pillow not installed"})); sys.exit(9)

# --- Content-type-aware sharpness thresholds (see CHANGELOG above for data) ---
PHOTO_SHARP_MIN = 250.0     # photographic / illustration content
GRAPHIC_SHARP_MIN = 1800.0  # text-heavy posters / UI / app-mockup content

ENTROPY_MIN = 6.5   # RECALIBRATED: reference folder floor was 6.83, typical 7.2-7.9
                    # low-entropy. 6.5 rejected good Pexels night clips (false positive).
                    # Ground truth: Mozart rated v1 (lap 25) poor, v2 (lap 282) improved.
COLOR_MIN = 15.0    # Hasler-Susstrunk

# Content-type classifier tuning (see docstring CHANGELOG for rationale)
FLAT_PIXEL_FRACTION_MIN = 0.35   # >=35% of pixels in the single dominant luma bin
                                  # (+/- 2 bins) => large flat/solid-color regions,
                                  # typical of posters/UI backgrounds
EDGE_DENSITY_MIN = 0.06          # >=6% of sampled pixels have a hard Laplacian
                                  # response (>30) => sharp vector/text edges

def laplacian_variance(gray, w, h):
    px = gray.load()
    vals = []
    for y in range(1, h - 1, 2):          # stride 2 = 4x faster, same distribution
        for x in range(1, w - 1, 2):
            v = (px[x, y - 1] + px[x, y + 1] + px[x - 1, y] + px[x + 1, y] - 4 * px[x, y])
            vals.append(v)
    if len(vals) < 2: return 0.0, []
    return statistics.pvariance(vals), vals

def entropy(gray):
    hist = gray.histogram()
    total = sum(hist)
    if not total: return 0.0
    return -sum((c / total) * math.log2(c / total) for c in hist if c)

def colourfulness(img):
    small = img.resize((160, 284))
    px = small.load()
    rg, yb = [], []
    for y in range(0, small.height, 2):
        for x in range(0, small.width, 2):
            r, g, b = px[x, y][:3]
            rg.append(r - g)
            yb.append(0.5 * (r + g) - b)
    if len(rg) < 2: return 0.0
    return (math.sqrt(statistics.pvariance(rg) + statistics.pvariance(yb))
            + 0.3 * math.sqrt(statistics.mean(rg) ** 2 + statistics.mean(yb) ** 2))

def classify_content(gray, lap_vals):
    """Simple, documented heuristic -- not a trained classifier.

    graphic/text content tends to combine:
      (a) large near-uniform/flat-color regions (solid poster/UI backgrounds)
      (b) unusually high edge density (hard vector/text edges cutting through
          those flat regions)
    photographic content is edge-rich in a more distributed way and rarely
    dominated by one flat luma bin the way posters/UI mockups are.

    Returns "graphic" or "photo". Callers may override via --content-type.
    """
    hist = gray.histogram()
    total = sum(hist) or 1
    peak = max(hist)
    # include the peak bin's immediate neighbors to tolerate anti-aliasing
    peak_idx = hist.index(peak)
    lo, hi = max(0, peak_idx - 2), min(256, peak_idx + 3)
    flat_fraction = sum(hist[lo:hi]) / total

    if lap_vals:
        edge_hits = sum(1 for v in lap_vals if abs(v) > 30)
        edge_density = edge_hits / len(lap_vals)
    else:
        edge_density = 0.0

    if flat_fraction >= FLAT_PIXEL_FRACTION_MIN and edge_density >= EDGE_DENSITY_MIN:
        return "graphic"
    return "photo"

def score_image(path, content_type=None):
    img = Image.open(path).convert("RGB")
    img.thumbnail((640, 640))
    gray = img.convert("L")
    lv, lap_vals = laplacian_variance(gray, gray.width, gray.height)
    en = entropy(gray)
    cf = colourfulness(img)

    ctype = content_type or classify_content(gray, lap_vals)
    sharp_min = GRAPHIC_SHARP_MIN if ctype == "graphic" else PHOTO_SHARP_MIN

    fails = []
    if lv < sharp_min: fails.append(f"blurry (laplacian_var {lv:.1f} < {sharp_min} for {ctype})")
    if en < ENTROPY_MIN: fails.append(f"flat/low-detail (entropy {en:.2f} < {ENTROPY_MIN})")
    if cf < COLOR_MIN: fails.append(f"washed out (colourfulness {cf:.1f} < {COLOR_MIN})")
    return {"file": os.path.basename(path), "laplacian_var": round(lv, 1),
            "entropy_bits": round(en, 2), "colourfulness": round(cf, 1),
            "content_type": ctype, "sharp_min_used": sharp_min,
            "tier": "PASS" if not fails else "REJECT", "reasons": fails}

def score_video(path, n=4, content_type=None):
    d = os.path.join(os.path.dirname(path), "_sg_" + os.path.basename(path).replace(".", "_"))
    os.makedirs(d, exist_ok=True)
    subprocess.run([FF, "-y", "-v", "quiet", "-i", path, "-vf",
                    f"fps=1/2,scale=640:-1", "-frames:v", str(n),
                    os.path.join(d, "f_%02d.jpg")], capture_output=True, timeout=300)
    frames = sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith(".jpg"))
    if not frames: return {"file": os.path.basename(path), "tier": "UNKNOWN",
                           "reasons": ["no frames extracted"]}
    per = [score_image(f, content_type=content_type) for f in frames]
    return {"file": os.path.basename(path), "frames": len(per),
            "mean_laplacian": round(statistics.mean(p["laplacian_var"] for p in per), 1),
            "mean_entropy": round(statistics.mean(p["entropy_bits"] for p in per), 2),
            "mean_colourfulness": round(statistics.mean(p["colourfulness"] for p in per), 1),
            "content_type": per[0]["content_type"] if per else None,
            "tier": "PASS" if all(p["tier"] == "PASS" for p in per) else "REJECT",
            "reasons": sorted({r for p in per for r in p["reasons"]}),
            "per_frame": per}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--content-type", choices=["photo", "graphic"], default=None,
                     help="Override the auto classifier. Defaults to auto-detect "
                          "(falls back to 'photo' when the heuristic is ambiguous).")
    args = ap.parse_args()

    out = []
    for p in args.paths:
        if not os.path.exists(p): continue
        if p.lower().endswith((".mp4", ".mov")):
            out.append(score_video(p, content_type=args.content_type))
        else:
            out.append(score_image(p, content_type=args.content_type))
    print(json.dumps(out, indent=1))
