# Cloud-Free-Tier vs. Local-CPU Image Generation: Capacity Test

**Date:** 2026-08-10
**Question:** Does routing image generation to a free cloud GPU service (instead of this
machine's CPU) give enough capacity/quality to clear the sharpness/richness QA gate,
while still running QA and assembly locally?

## Candidates researched

| Service | Free without payment info? | Verdict |
|---|---|---|
| **Pollinations.ai** (`image.pollinations.ai`) | Yes — no auth, no signup, no card | **Tested** (see below) |
| **Hugging Face Inference Providers / Serverless API** | Free tier exists for light/non-commercial use, but requires creating a free HF account + API token first. No card required, but account creation could not be completed in this headless session and no existing HF token was found in `.env` files on this machine. | Viable candidate, **not tested this run** |
| **fal.ai** | No true free tier as of mid-2026 — requires a minimum credit purchase to get a working API key. Some signup promotional credits exist but a payment method is generally required at signup. | **Excluded** — violates "no payment info" requirement |
| **Together.ai / Replicate** | Both typically require card-on-file for API access beyond a small one-time signup credit; no existing keys found in `Automated-Video-Generator\.env` or elsewhere under `C:\Users\mozar`. | Not pursued this run |

Existing `.env` scan (`C:\Users\mozar\Automated-Video-Generator\.env`, plus a home-directory
search for other `.env` files) found only `PEXELS_API_KEY`, `PIXABAY_API_KEY`, and a
placeholder (unset) `GEMINI_API_KEY`. No Hugging Face, Replicate, fal, or Together tokens
exist anywhere on this machine.

Given the constraints, **Pollinations.ai** was the only candidate that could be tested
without any signup step, so it was used as the cloud-GPU stand-in.

## Test run

- Endpoint: `https://image.pollinations.ai/prompt/<url-encoded-prompt>?width=1024&height=1024&model=flux&seed=42`
- Prompt: "sharp cinematic photo, rideshare driver hands on steering wheel, city lights at
  night, high detail, in focus, professional photography"
- Two runs were made (seed 42 plain; seed 99 with `enhance=true` and extra "8k, sharp focus"
  boosters) to see if prompt/param tuning could close the gap.

| Run | Generation time | Laplacian variance | Entropy | Colourfulness | Gate result |
|---|---|---|---|---|---|
| Local CPU (ComfyUI, prior session) | ~70 min | 322 | — | — | **FAIL** (< 1800) |
| Cloud v1 (Pollinations, plain prompt) | **1.29 sec** | **282.7** | 7.33 (pass, ≥6.5) | 41.0 (pass, ≥15) | **FAIL** (< 1800) |
| Cloud v2 (Pollinations, enhanced prompt) | 1.29 sec | 31.2 | 6.78 (pass) | 7.7 (**fail**, <15) | **FAIL** (worse) |

Files: `C:\temp\claude-ops\cloud_test_pollinations.jpg`,
`C:\temp\claude-ops\cloud_test_pollinations_v2.jpg`.

Exact gate command: `python C:\temp\claude-ops\sharpness_gate.py <file>` — thresholds
`SHARP_MIN=1800.0`, `ENTROPY_MIN=6.5`, `COLOR_MIN=15.0`.

## Verdict

**Cloud generation is dramatically faster (1.3 sec vs. ~70 min — over 3,000x), which fully
answers the capacity question: free cloud GPU removes the local-CPU throughput bottleneck.**

**But it does NOT clear the quality gate.** Both cloud runs failed on sharpness
(laplacian variance 282.7 and 31.2, both far below the 1800 threshold), and the
"enhanced" prompt made it worse and also failed colourfulness. The cloud result is
actually in the same failing range as the local-CPU result (322) — neither is remotely
close to 1800.

This means the honest finding is **case (6) from the brief, not case (5)**: the
**sharpness gate itself, not compute location, is the current bottleneck.** SHARP_MIN=1800
was calibrated against a reference folder of professional photography and ChatGPT-generated
images, which appear to sit in a fundamentally different sharpness regime than default
Flux/SD outputs from consumer-facing free APIs (which apply denoising/style choices that
depress raw Laplacian edge energy regardless of where the model runs).

**Recommendation:** Do not route image generation to Pollinations free-tier expecting it to
pass the current gate — it won't, and the ambiguous commercial-licensing status flagged in
GitHub issue #8741 (https://github.com/pollinations/pollinations/issues/8741, which covers
ElevenLabs-via-Pollinations licensing and by extension raises the same "whose license
applies" question for image endpoints) is a separate reason to avoid it for anything
commercial anyway. Instead:
1. Sign up for a free Hugging Face account (email only, no card) and get an Inference
   Providers API token, then re-run this same test against a proper photorealistic
   checkpoint (e.g. FLUX.1-schnell or SDXL) at higher steps — HF's free tier was not
   testable in this headless run purely because account creation needs a human, not
   because it's unsuitable.
2. In parallel, treat SHARP_MIN=1800 as suspect: verify it against a larger sample of
   real-world "acceptable" video-frame stills (not just polished stock photography) before
   concluding no generator can pass it. A threshold calibrated only against professional/
   ChatGPT images may be systematically too strict for any diffusion-model output, cloud or
   local.

No image is being added to `assets/` because neither test run passed the gate.

## Sources
- Pollinations.ai API: https://image.pollinations.ai/prompt/{prompt}
- Pollinations GitHub issue #8741: https://github.com/pollinations/pollinations/issues/8741
- Hugging Face Inference Providers text-to-image docs: https://huggingface.co/docs/inference-providers/tasks/text-to-image
- fal.ai free-plan status (2026): https://costbench.com/software/ai-ml-platforms/fal/free-plan/
