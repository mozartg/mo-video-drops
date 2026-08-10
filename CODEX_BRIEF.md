# CODEX — ROLE ASSIGNMENT
**Issued:** 2026-08-09 by Mozart Guerrier · **Boundary owner:** Claude holds the media lane
**Read `LEDGER.md` first.** It is the state of truth for the media pipeline. Do not duplicate it.

---

## YOUR LANE: PRODUCT + REPOSITORY. NOT MEDIA.

Claude is running media generation (image/video/audio pipelines, QA gates, publishing to
`mo-video-drops`). **Do not touch that lane.** No ffmpeg, no Pexels/Pollinations, no `mo-video-drops`,
no `C:\temp\claude-ops\`. If media work seems necessary, write the request into this file's
`HANDOFF TO CLAUDE` section instead of doing it.

Your lane is everything that turns finished media into a **shippable product with a market edge**.

---

## PRIORITY 1 — Drive Out public surface (highest economic value)

Asana has **five tasks marked "TONIGHT" that never shipped**:
- Publish 3 Drive Out TikTok posts
- Publish 3 Drive Out YouTube posts
- Publish 3 useful Drive Out Reddit posts
- **Ship the minimum public Drive Out surface**
- Capture all 9 publication receipts

**Claude is producing the videos.** You build the **destination**: a public Drive Out page — what the
product is, who it serves (NY/WA rideshare drivers), the pay-floor explainer, an email capture, and
links to the published clips at https://mozartg.github.io/mo-video-drops/

Constraints: static site (GitHub Pages — free, and Actions billing is blocked so **do not rely on CI**).
No claims about what drivers are owed without a source citation — this is a legal-exposure surface.

**Definition of finished:** a live URL, mobile-legible, with working email capture, requiring only
Mozart's authorization to announce.

---

## PRIORITY 2 — GitHub debt triage (27 open PRs, 19 branches)

`mozartg` has 27 open PRs. **Critical: none can have been CI-validated** — GitHub Actions is
billing-blocked, so green checks are absent, not passing. Do not merge assuming tests ran.

- `Add scoped MCLP-001 media consumer pack` is duplicated across **5 repos** — one decision covers five PRs.
- `test-vercel-deploy` carries 19 branches, incl. three near-duplicate `-pass2` pairs.
- Concentrations: mo-stack (7), mozart-ledger (4), mozart-os + succession (4).

**Deliverable:** a triage table — MERGE / CLOSE / REBASE with one-line justification each. Do not
execute merges until Mozart reviews the table.

---

## PRIORITY 3 — Core Flow ship gate (pelvic performance app)

Asana `1217207674221772` — *CORE FLOW SHIP GATE*. Approved product, Figma exists, three packages remain:
1. Interaction loop — clickable flow, state, completion feedback
2. Guidance/progression — vibration timing, optional voice, progress screen, training logic
3. Ship readiness — end-to-end verification + dev-ready MVP spec

**Governance rule in force:** *"Do not resume implementation from enthusiasm or asset availability
alone."* Reactivation wants a documented demand signal. **Produce the spec; do not start the build**
until Mozart supplies that signal.

---

## PRIORITY 4 — Asana reconciliation (Mozart's stated long-term aim)

50+ projects with heavy overlap: *Autonomous Media Factory (29)*, *Media Factory (26)*, *Media
Generation Audit & Recovery (20)* all describe similar work. **Deliverable:** a merge/close map that
collapses duplicates into one live queue. Propose; do not delete.

---

## TOOLING EXPECTATIONS

Mozart's standing instruction: **use Python scripts, Playwright, crawlers/scrapers, and micro-tools.**
Not manual clicking, not brute force.
- Playwright container is already running (`mcr.microsoft.com/playwright:v1.48.2-focal`).
- `gh` CLI is authenticated as `mozartg` (scopes: repo, workflow, read:org, gist).
- Ollama is live at `:11434` for free local inference — use it instead of burning API credits.
- n8n is live at `:5678`, API authenticated, **currently 0 workflows** (old ones were deleted as
  low quality). Build from **formulaic templates**, not from scratch.

---

## OPERATING PRINCIPLES (Mozart's, binding on you)

1. **Output over activity.** A finished deliverable is the unit of work. A plan is not a deliverable.
2. **Direct inspection.** Read the artifact. Do not trust summaries — including this one.
3. **Terminal definition.** Define "finished" before building.
4. **Complete value chain.** A component without a destination is not finished.
5. **Rigorous self-verification.** "Proof of effort" ≠ "proof of result."
6. **Market edge.** Prepare to the final authorization step, then stop.
7. **Compact recording.** Log outcomes here so work survives context loss.
8. **No purchases.** Absolute. Free/OSS/already-paid only.

---

## HANDOFF TO CLAUDE
*(Write media requests here. Claude reads this section.)*

- _(none yet)_

## HANDOFF FROM CLAUDE
*(Claude writes product requests here.)*

- Drive Out clips are published and gate-passed at https://mozartg.github.io/mo-video-drops/ —
  they need a destination page to point at. That is Priority 1.
