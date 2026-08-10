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
"""
import sys, os, json, math, subprocess, statistics

FF = r"C:\Program Files\Krita (x64)\bin\ffmpeg.exe"

try:
    from PIL import Image
except ImportError:
    print(json.dumps({"error": "Pillow not installed"})); sys.exit(9)

SHARP_MIN = 300.0   # RECALIBRATED 2026-08-10 (2nd pass) -- 1800 was set from a
                    # reference folder that mixes text-heavy posters/app-mockups
                    # (laplacian 2300-6500, edge-dense by design) with soft
                    # photographic/illustration content (699-1967). Direct test:
                    # 23 files in reference folder itself only PASS 9/23 at 1800.
                    # 3 known-sharp Pexels stock photos (unedited, full-res) scored
                    # 119 / 229 / 2613 -- 2 of 3 genuinely sharp real photos FAIL at
                    # 1800. Aggressive ffmpeg unsharp masking pushed a failing
                    # Pollinations image (282.7) up to 2881.6 -- gate mostly measures
                    # post-processing/edge-amplification intensity, not focus quality,
                    # so it is content-type dependent and not a safe universal cutoff.
                    # 300 is set just above near-zero/broken-frame noise floor so it
                    # still catches truly blank/garbled frames without mass-rejecting
                    # legitimate soft-focus photography or unsharpened diffusion output.
                    # See C:\temp\claude-ops\drops\GATE_CALIBRATION_DIAGNOSIS_20260810.md
ENTROPY_MIN = 6.5   # RECALIBRATED: reference folder floor was 6.83, typical 7.2-7.9
                    # low-entropy. 6.5 rejected good Pexels night clips (false positive).
                    # Ground truth: Mozart rated v1 (lap 25) poor, v2 (lap 282) improved.
COLOR_MIN = 15.0    # Hasler-Susstrunk

def laplacian_variance(gray, w, h):
    px = gray.load()
    vals = []
    for y in range(1, h - 1, 2):          # stride 2 = 4x faster, same distribution
        for x in range(1, w - 1, 2):
            v = (px[x, y - 1] + px[x, y + 1] + px[x - 1, y] + px[x + 1, y] - 4 * px[x, y])
            vals.append(v)
    if len(vals) < 2: return 0.0
    return statistics.pvariance(vals)

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

def score_image(path):
    img = Image.open(path).convert("RGB")
    img.thumbnail((640, 640))
    gray = img.convert("L")
    lv = laplacian_variance(gray, gray.width, gray.height)
    en = entropy(gray)
    cf = colourfulness(img)
    fails = []
    if lv < SHARP_MIN: fails.append(f"blurry (laplacian_var {lv:.1f} < {SHARP_MIN})")
    if en < ENTROPY_MIN: fails.append(f"flat/low-detail (entropy {en:.2f} < {ENTROPY_MIN})")
    if cf < COLOR_MIN: fails.append(f"washed out (colourfulness {cf:.1f} < {COLOR_MIN})")
    return {"file": os.path.basename(path), "laplacian_var": round(lv, 1),
            "entropy_bits": round(en, 2), "colourfulness": round(cf, 1),
            "tier": "PASS" if not fails else "REJECT", "reasons": fails}

def score_video(path, n=4):
    d = os.path.join(os.path.dirname(path), "_sg_" + os.path.basename(path).replace(".", "_"))
    os.makedirs(d, exist_ok=True)
    subprocess.run([FF, "-y", "-v", "quiet", "-i", path, "-vf",
                    f"fps=1/2,scale=640:-1", "-frames:v", str(n),
                    os.path.join(d, "f_%02d.jpg")], capture_output=True, timeout=300)
    frames = sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith(".jpg"))
    if not frames: return {"file": os.path.basename(path), "tier": "UNKNOWN",
                           "reasons": ["no frames extracted"]}
    per = [score_image(f) for f in frames]
    return {"file": os.path.basename(path), "frames": len(per),
            "mean_laplacian": round(statistics.mean(p["laplacian_var"] for p in per), 1),
            "mean_entropy": round(statistics.mean(p["entropy_bits"] for p in per), 2),
            "mean_colourfulness": round(statistics.mean(p["colourfulness"] for p in per), 1),
            "tier": "PASS" if all(p["tier"] == "PASS" for p in per) else "REJECT",
            "reasons": sorted({r for p in per for r in p["reasons"]}),
            "per_frame": per}

if __name__ == "__main__":
    out = []
    for p in sys.argv[1:]:
        if not os.path.exists(p): continue
        out.append(score_video(p) if p.lower().endswith((".mp4", ".mov")) else score_image(p))
    print(json.dumps(out, indent=1))

