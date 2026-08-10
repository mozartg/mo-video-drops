# PROMPT 3 — Research Summary

Date: 2026-08-10

## ComfyUI

The existing local ComfyUI path was an incomplete shell, not a valid failed install. Recommended first proof on the Ryzen 7 5700U system: clean manual ComfyUI install, CPU-first, Stable Diffusion 1.5 at 512x512, batch 1, with workflow JSON, seed, output, console log and runtime captured.

Model canary order:
1. Stable Diffusion 1.5 — v1-5-pruned-emaonly.safetensors
2. SDXL Base 1.0 only after the first canary passes
3. FLUX.1-schnell is commercially permissive but too heavy to use as the first test on this laptop

Hardware verdict: retain ComfyUI as a development/canary/fallback lane until a real local generation proves otherwise; do not treat this laptop as a production GPU.

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

Do not abandon n8n categorically. The failed history is better explained by sequencing and system-boundary problems: generation, rendering, authentication, publishing permissions and orchestration were being debugged together.

Promote only workers that satisfy:

job -> artifact -> QA -> receipt

n8n may then orchestrate scheduling, dispatch, routing, retry, approvals, notifications and status. It should not be the authoritative implementation of model inference, rendering internals, artifact truth, rights decisions or platform permissions.

## Next build artifacts

- contracts/media-job.schema.json
- contracts/media-receipt.schema.json
- docs/free-media-rights-policy.md
- docs/n8n-worker-boundary.md
- examples/comfyui-sd15-canary.json after a real local ComfyUI export exists
