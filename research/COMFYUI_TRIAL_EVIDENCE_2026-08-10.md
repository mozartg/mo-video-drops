# ComfyUI Trial Evidence — 2026-08-10

The trial requirement is intentionally stricter than “find people saying ComfyUI works.” A qualifying operator demo must establish successful execution and distinguish what is visibly demonstrated from what is merely asserted.

| Evidence | 2026? | Windows? | What is demonstrated / reported | Install method | Model evidence | Qualification |
|---|---|---|---|---|---|---|
| AMD ROCm native-Windows ComfyUI walkthrough | Yes, July 14 | Yes | Reproducible native Windows setup and measured SDXL / FLUX.1-dev / WAN 2.2 execution on Ryzen AI Max+ / Radeon 8060S | Manual Python/ROCm/PyTorch + ComfyUI | SDXL, FLUX.1-dev, WAN 2.2 named; full model families and measured runtimes reported | **Strong technical demonstration, but vendor/operator documentation rather than YouTube/TikTok/Reddit**. https://rocm.blogs.amd.com/artificial-intelligence/comfyui-windows/README.html |
| DripPanDan Reddit AMD/ROCm operator record | Yes | Yes / Windows portable attempts, later Ubuntu/WSL stable path | Operator supplies exact ROCm/PyTorch wheel filenames, launcher settings, reports image generation ~1 minute and 2-second video tests ~5–7 minutes; later reports reliable images and 5-second video generation under stable setup | Windows Portable ROCm attempts plus later Ubuntu/WSL stable environment | Z-Image Turbo named; exact generation checkpoint filename not exposed in retrieved post | **Operator-reported execution and concrete install details; does not satisfy exact checkpoint-filename requirement**. Reddit user history retrieved 2026-08-10. |
| SCAIL-2 Reddit Show & Tell | Yes, July 6 | OS not supplied | Actual video result is posted. Operator explains chunking due VRAM and use of SCAIL autoextend + SAM3. Commenters explicitly criticize missing workflow/system specs | Not supplied | SCAIL-2 + SAM3 named; exact model files absent | **Output demonstrated; installation and exact files not demonstrated**. https://www.reddit.com/r/comfyui/comments/1uoxjqd/scail_2_is_actually_amazing/ |

## Trial conclusion

The available 2026 evidence establishes that ComfyUI is actively producing real image/video output on current Windows/AMD systems and in operator workflows. It **does not yet satisfy the original demand for three independent YouTube/TikTok/Reddit Windows demos each exposing exact model filenames**. TikTok retrieval was blocked by robots during this research pass, and current search did not return qualifying YouTube pages.

Therefore the correct state is:

- **ComfyUI viability as a platform:** demonstrated.
- **ComfyUI viability on Mozart's exact Ryzen 7 5700U machine:** unresolved until the existing local install produces a captured artifact.
- **Three-demo exact-filename trial:** partial, not complete.

Do not substitute model-family names for exact checkpoint filenames in future receipts.
