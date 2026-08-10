# PROMPT 3 — Research Summary

Date: 2026-08-10

## ComfyUI

**Correction after live-ledger read-back:** the earlier empty-shell finding inspected the wrong level/path. The current ledger records a real install at `C:\Users\mozar\TriggerCMD-Scripts\Tools\ComfyUI\repo\` with full ComfyUI source, a Python virtual environment, and an SD1.5 checkpoint of about 2 GB. The ledger also records that ComfyUI was launched on 2026-08-10. Generation success is still pending until a real output artifact and receipt are captured.

Do not reinstall before inspecting and exercising that existing `repo` install.

First proof on the Ryzen 7 5700U system:
1. read back the exact installed checkpoint filename from the filesystem;
2. start the existing ComfyUI install;
3. submit one 512x512, batch-1 SD1.5 generation;
4. retain workflow JSON, seed, output image, console log, runtime and SHA-256;
5. write a media receipt conforming to `contracts/media-receipt.schema.json`.

The ledger displays the checkpoint name with a corrupted leading character before `1-5-pruned-emaonly-fp16.safetensors`; do not hard-code a guessed filename until local readback confirms it.

Hardware verdict: the laptop is now an **active canary candidate**, not a hypothetical reinstall target. Production-throughput suitability remains unproven until measured generation succeeds.

## Free-media ingestion

Every downloaded asset must carry item-level rights metadata, especially for mixed-license sources such as Openverse, Wikimedia Commons, Library of Congress, NASA, Mixkit and Videvo.

Required fields:
- provider
- provider_asset_id
- source_url
- creator
- license_code
- license_url
- commercial_use_status
- attribution_required
- attribution_text
- retrieved_at
- sha256

## n8n post-mortem

The internal record confirms approximately three weeks / ~100 hours of failed media automation work, but that history alone does not prove n8n is intrinsically the wrong orchestration tool. External GitHub implementations show active n8n↔ComfyUI patterns. The narrower working hypothesis is that the previous implementation mixed unproven generation, rendering, auth, platform permissions and orchestration into one debugging surface.

Promote only workers that satisfy:

job -> artifact -> QA -> receipt

Then test the same known-good worker both directly and through n8n. Keep or reject n8n per lane based on measured duplicate handling, retry correctness, recovery, elapsed time and operator burden.

## Build artifacts in this branch

- contracts/media-job.schema.json
- contracts/media-receipt.schema.json
- docs/free-media-rights-policy.md
- docs/n8n-worker-boundary.md
- examples/comfyui-sd15-canary-spec.json

## Current next action

Exercise the existing ComfyUI install and capture a real SD1.5 artifact. No reinstall and no n8n promotion before that direct proof.
