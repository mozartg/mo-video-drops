# ComfyUI Local-Gen Lane Result — 2026-08-10

## Summary
The lane is **partially viable**: CPU-mode ComfyUI generation on this AMD-integrated-graphics machine CAN
complete and produce a real PNG, but it is (a) extremely slow, (b) currently below the sharpness gate at the
step counts tested, and (c) prone to a non-deterministic native crash in PyTorch's CPU attention kernels that
makes fast iteration unreliable.

## Setup
- ComfyUI: `C:\Users\mozar\TriggerCMD-Scripts\Tools\ComfyUI\repo\`
- Checkpoint: `v1-5-pruned-emaonly-fp16.safetensors` (SD1.5, 2034MB)
- Launch: `.venv\Scripts\python.exe main.py --listen 127.0.0.1 --port 8188 --cpu` (no NVIDIA GPU on this box)
- Prompt: "sharp cinematic photo, rideshare driver hands on steering wheel, city lights at night, high detail, in focus, professional photography"
- Negative: "blurry, out of focus, low quality, deformed"
- Gate thresholds (authoritative): SHARP_MIN=1800.0 (laplacian variance), ENTROPY_MIN=6.5

## Run 1 — 768x1152, 20 steps (prior session's queued job)
- Accepted by server, node_errors empty.
- Prior polling window (10 min) timed out with no output — but the job was in fact still working, not stalled.
- Confirmed via `/history/<prompt_id>`: execution_start to execution_success spanned **~70 minutes** (1786335221184 → 1786339440887 ms).
- Output: `comfy_test_00001_.png` (1,217,512 bytes), file-size stable.
- Gate result: **REJECT** — laplacian_var=322.5 (need ≥1800.0), entropy_bits=7.67 (passes, need ≥6.5), colourfulness=70.5.
  - Reason: "blurry (laplacian_var 322.5 < 1800.0)"
- Conclusion: SD1.5 CPU output at 20 steps/768x1152 is real but too soft to pass the gate as-is.

## Run 2 — 512x512, 15 steps (default sub-quadratic attention)
- Queued successfully, ran to step 10/15 (~5.5 min elapsed) then the ComfyUI server process **crashed** with:
  `Windows fatal exception: access violation` inside `comfy/ldm/modules/sub_quadratic_attention.py` /
  `_get_attention_scores_no_kv_chunking`. This is a native-level PyTorch CPU crash, not a Python exception or OOM —
  the whole process died silently (no output file, empty `/history`).
- Diagnosis: not a timeout/slowness issue — a torch CPU-attention kernel instability on this machine.

## Run 3 — 512x512, 15 steps, relaunched with `--use-split-cross-attention`
- Intended to route around the buggy sub-quadratic attention path.
- Crashed again, this time at step 1/15 (~29s in), same signature: `Windows fatal exception: access violation`,
  now inside the split-cross-attention path instead.
- The crash is **non-deterministic in location** (step 1 vs step 10, different attention backends) which points to
  a lower-level instability (likely a torch/CPU build issue — possibly an unsupported instruction path, thread-safety
  bug, or memory corruption in the AMD CPU inference path) rather than a resolution- or step-count-driven problem.
- The ComfyUI HTTP server itself did not always notice the worker thread died — the `/queue` endpoint kept
  reporting `queue_running` with no progress, which will hang naive polling loops.

## Verdict
- **The lane is not yet production-ready.** CPU generation can complete (proven once, at 768x1152/20 steps,
  ~70 minutes) but the output failed the sharpness gate, and two follow-up attempts at a faster 512x512/15-step
  setting both crashed with the same native access-violation bug before completing.
- To move this forward, next steps would be: (1) reproduce/isolate the access-violation crash — likely needs a
  different torch CPU build or disabling multi-threaded attention entirely (`--use-pytorch-cross-attention` was
  not yet tried); (2) if/when a stable config is found, increase steps toward 25-30 to try to clear the 1800.0
  sharpness bar, since 20 steps at 322.5 is far below threshold; (3) accept that CPU generation times (tens of
  minutes per image) make this lane usable only for occasional/background generation, not fast iteration.
- No PASS-tier image was produced this session, so no asset was published to `assets/`.

## Gate scores this session
| Run | Size | Steps | Result | laplacian_var | entropy_bits | Time |
|---|---|---|---|---|---|---|
| 1 | 768x1152 | 20 | REJECT | 322.5 | 7.67 | ~70 min |
| 2 | 512x512 | 15 | CRASH (no output) | n/a | n/a | crashed ~5.5 min in |
| 3 | 512x512 | 15 | CRASH (no output) | n/a | n/a | crashed ~29s in |
