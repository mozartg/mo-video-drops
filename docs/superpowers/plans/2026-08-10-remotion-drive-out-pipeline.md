# Remotion Drive Out Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a deterministic JSON-driven Remotion pipeline that renders a 15-second proof and can render a ten-minute vertical long-form composition, while keeping the existing static campaign surface deployable without CI.

**Architecture:** Keep the existing GitHub Pages site at the repository root. Add an isolated `remotion/` package with a typed input contract, a single composition that maps timed scenes and captions onto supplied local image assets, and PowerShell verification scripts that do not invoke `ffmpeg`. The public page will remain plain HTML/CSS and will use only supplied or already-published facts; missing sourced pay-floor figures stay visibly marked as placeholders.

**Tech Stack:** Remotion, React, TypeScript, Zod, PowerShell, static HTML/CSS, SHA-256 file hashing.

## Global Constraints

- Do not modify `LEDGER.md`.
- Do not invoke `ffmpeg`, Pexels, Pollinations, Asana, or GitHub APIs during this agent phase.
- Do not generate AI media; only use existing local image fixtures and programmatic Remotion markup.
- Do not make visual-quality claims because this agent cannot see images.
- Do not invent pay-floor figures, citations, PR state, or Asana state.
- Do not rely on GitHub Actions; verification runs locally.
- Treat `C:\Users\mozar\Desktop\High Quality Media Folder` as read-only.

---

### Task 1: Establish the Remotion package and input contract

**Files:**
- Create: `remotion/package.json`
- Create: `remotion/tsconfig.json`
- Create: `remotion/src/types.ts`
- Create: `remotion/src/input.ts`
- Create: `remotion/src/index.ts`
- Create: `remotion/src/Root.tsx`
- Create: `remotion/src/DriveOutComposition.tsx`
- Create: `remotion/inputs/trial.json`
- Create: `remotion/inputs/long-form.json`

**Interfaces:**
- `VideoInput`: `{ title: string; imagePaths: string[]; captions: Caption[]; durationInFrames?: number }`.
- `Caption`: `{ text: string; startFrame: number; endFrame: number }`.
- `DriveOutComposition`: a Remotion composition receiving `VideoInput` props and rendering `1080x1920` at `30fps`.

- [ ] **Step 1: Add the package manifest and TypeScript configuration.**

Use Remotion's CLI and renderer packages at the versions installed by the current scaffold command, with scripts for `render:trial`, `render:long-form`, and `verify:trial`.

- [ ] **Step 2: Add the Zod-backed JSON contract.**

Reject fewer than three image paths, captions with negative frames, captions whose end precedes their start, and non-positive durations. Keep `durationInFrames` optional so the composition can default to 15 seconds for the trial and accept 10 minutes for long-form.

- [ ] **Step 3: Add the composition entrypoint.**

Register `DriveOutTrial` with 450 frames and `DriveOutLongForm` with 18,000 frames. Both use the same component and receive props from `--props` JSON at render time.

- [ ] **Step 4: Add the two JSON fixtures.**

The trial fixture contains three local image paths and a caption track spanning the 15-second timeline. The long-form fixture uses the same schema with repeated scene timing and no uncited economic figures.

- [ ] **Step 5: Run TypeScript validation.**

Run `npm run typecheck` from `remotion/`. Expected result: exit code 0 with no diagnostics.

### Task 2: Implement deterministic image scenes and captions

**Files:**
- Modify: `remotion/src/DriveOutComposition.tsx`
- Create: `remotion/src/styles.ts`

**Interfaces:**
- Consumes: `VideoInput` from `src/types.ts`.
- Produces: deterministic frame output with no CSS animation or browser transition dependency.

- [ ] **Step 1: Add the timed scene layout.**

Split the timeline into equal image scenes, use `staticFile()` for repository-relative assets, and use Remotion `Sequence` boundaries so frame ownership is deterministic.

- [ ] **Step 2: Add frame-driven movement and caption visibility.**

Drive opacity, scale, and translation through `useCurrentFrame()` and `interpolate()`. Render the active caption from the JSON track with a high-contrast panel and no external font or network dependency.

- [ ] **Step 3: Add non-visual input errors.**

Throw a clear error if an input path escapes the public asset root or if a caption is outside the declared duration. Do not silently substitute missing media.

- [ ] **Step 4: Run the composition listing check.**

Run `npx remotion compositions src/index.ts`. Expected result: both composition IDs appear with 1080x1920 dimensions and the expected frame counts.

### Task 3: Copy read-only fixtures and pass the 15-second render gate

**Files:**
- Create: `remotion/public/trial-assets/drive-out-poster.png`
- Create: `remotion/public/trial-assets/drive-out-poster-2.png`
- Create: `remotion/public/trial-assets/sample-shots.png`
- Create: `remotion/scripts/verify-trial.ps1`
- Create: `remotion/out/.gitkeep`
- Modify: `remotion/.gitignore`

**Interfaces:**
- Consumes: three existing PNG files from the read-only benchmark folder.
- Produces: `remotion/out/trial.mp4` and a machine-readable verification receipt.

- [ ] **Step 1: Copy the three existing PNG fixtures without changing the benchmark folder.**

Use `Copy-Item -LiteralPath` from the benchmark folder into `remotion/public/trial-assets/`; do not open, edit, resize, or visually inspect them.

- [ ] **Step 2: Render the trial.**

Run `npm run render:trial` from `remotion/`. Expected result: Remotion exits 0 and creates a non-empty MP4 at `remotion/out/trial.mp4`.

- [ ] **Step 3: Verify the artifact without ffmpeg.**

The PowerShell verifier checks that the file exists, is larger than zero bytes, hashes it with SHA-256, and records the requested composition dimensions, FPS, and frame count from the known render contract. It writes `remotion/out/trial-receipt.json`.

- [x] **Step 4: Stop or promote based on evidence.**

If the Remotion render exits nonzero, stop the broader build and report the exact error. If it passes, continue to the long-form and public-surface tasks.

### Task 4: Promote the proof into the ten-minute long-form lane

**Files:**
- Modify: `remotion/src/Root.tsx`
- Modify: `remotion/src/DriveOutComposition.tsx`
- Modify: `remotion/inputs/long-form.json`
- Create: `remotion/scripts/verify-long-form.ps1`
- Modify: `README.md`

**Interfaces:**
- Consumes: the same `VideoInput` contract as the trial.
- Produces: a render command for `18,000` frames at `30fps`, plus a non-visual contract receipt.

- [ ] **Step 1: Make long-form duration explicit.**

Use `18,000` frames exactly for ten minutes and keep the image/caption sequence deterministic across the full timeline.

- [ ] **Step 2: Add the long-form render command.**

Expose `npm run render:long-form` with a local output path under `remotion/out/`; do not commit the large video artifact to GitHub.

- [ ] **Step 3: Verify the long-form composition contract.**

Run the composition listing and metadata verifier. If a full ten-minute render is practical within the execution window, run it; otherwise record the exact reason and keep the render command reproducible rather than claiming a completed video.

- [x] **Step 4: Document the local build path.**

Add concise commands to `README.md` for installing dependencies, rendering the trial, verifying it, and rendering the ten-minute composition.

### Task 5: Build the static Drive Out destination surface

**Files:**
- Modify: `index.html`
- Create: `docs/EXTERNAL_DATA_BLOCKERS.md`

**Interfaces:**
- Consumes: already-published MP4 links and facts directly present in the repository.
- Produces: a mobile-first static landing surface with a non-sending email capture form and a clearly marked pay-floor placeholder.

- [ ] **Step 1: Add the Drive Out landing section.**

Explain the audience as NY/WA rideshare drivers using the supplied brief, link to the existing clips, and preserve the existing media-drop catalog.

- [ ] **Step 2: Add a draft-only email capture.**

Use a form with an explicit `mailto:` fallback and a clear note that no submission backend is configured in this repository. Do not send or store email.

- [ ] **Step 3: Add the sourced-figure placeholder.**

Show `PAY-FLOOR FIGURE PENDING SOURCED INPUT` instead of a number, with a short note that ChatGPT Work must supply current citations before publication.

- [ ] **Step 4: Record blocked external work.**

Document that current Asana state, the 27-PR inventory, and source citations were not verified in this agent phase because internet and connector access are unavailable. Do not manufacture a triage table.

- [ ] **Step 5: Run static checks.**

Use a local HTML parse or targeted text assertions to verify the page contains the Drive Out section, all three existing media links, the placeholder, and the form; do not claim GitHub Pages deployment without a fresh external receipt.

### Task 6: Final verification and handoff

**Files:**
- Modify: `docs/superpowers/plans/2026-08-10-remotion-drive-out-pipeline.md`
- Create: `docs/BUILD_RECEIPT.md`

- [ ] **Step 1: Run all local checks.**

Run typecheck, composition listing, trial render verification, long-form contract verification, and static assertions.

- [ ] **Step 2: Check repository boundaries.**

Confirm `LEDGER.md` is unchanged, the benchmark folder has no modified files, no `ffmpeg` command was invoked, and no output MP4 larger than the repository limit is staged.

- [ ] **Step 3: Write the evidence receipt.**

Record exact commands, exit statuses, output paths, hashes, and blocked claims. Separate local artifacts from published, deployed, or externally verified states.

- [ ] **Step 4: Commit the implementation.**

Commit only source, fixtures, docs, and receipts; exclude rendered MP4s and dependency directories. Use commit message `feat: add deterministic remotion drive out pipeline`.

## Execution Outcome

- Tasks 1 through 3 completed and verified.
- Task 4 contract and command completed; the full ten-minute render remains blocked by the host-level orphaned-renderer condition recorded in `docs/BUILD_RECEIPT.md`.
- Task 5 completed locally; deployment, citations, capture backend, Asana state, and PR state remain externally unverified.
- Task 6 local verification completed; the implementation is ready for a local commit, with no long-form MP4 staged.
