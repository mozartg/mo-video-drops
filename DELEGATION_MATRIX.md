# SIX-SURFACE DELEGATION MATRIX — v2
**Issued 2026-08-09 · Owner: Mozart Guerrier · Director: Claude (Cowork, Opus 5)**
**v2 corrects a material error in v1: Claude Chat was described as having no tools. It has connectors,
skills, web search, file uploads, vision, artifacts, and Projects. That error under-assigned the
second-most-capable surface in the fleet.**

---

## 0. Model policy — corrected

v1 recommended dropping Cowork to Sonnet. **Mozart's pushback is correct and supersedes it:**
*while running Opus 5 High, make architectural decisions.*

The distinction v1 missed: the question is not "is Opus expensive" but **"is this turn producing
architecture or typing?"** Opus on lane design, failure diagnosis, and routing decisions is the
correct spend — those decisions propagate across five other surfaces and get executed for free.
Opus running `git push` is waste.

| Turn produces | Model | Rationale |
|---|---|---|
| Architecture, routing, root-cause, contradiction-hunting | **Opus 5 High** | One decision here directs hours of free execution elsewhere |
| Pipeline runs, file ops, publishing, batch execution | Sonnet | Identical output |
| Bulk mechanical passes | Haiku | Volume |
| Anything a free surface can do | **Delegate — not Claude at all** | Free parallel capacity |

**Rule:** Opus decides *what* and *why*. Cheaper surfaces do *how*.

---

## 1. Six surfaces — accurate capabilities

| # | Surface | Has | **Cannot** |
|---|---|---|---|
| 1 | **Claude Chat** (claude.ai) | **Connectors (MCP), skills, web search, file upload, vision, artifacts, Projects w/ persistent knowledge base**, extended thinking | No local filesystem. No local shell. No persistent local repo state |
| 2 | **Cowork (Claude)** | All of the above **plus** local file tools, sandboxed Linux shell, local machine control | Chat-shaped; not built for long unattended refactors. **Metered against the premium budget** |
| 3 | **Claude Code** | Terminal-native, local repo, long builds, git, filesystem | No connector graph. **BLOCKED — OAuth token expired** |
| 4 | **ChatGPT Chat** | Sustained autonomy (4–8 h observed with tooling open), browsing, files | No repo write |
| 5 | **ChatGPT Work** | Live web, connectors, vision, Agent Mode, cross-app | No repo. No terminal |
| 6 | **Codex** | Repo clone/edit, run tests, open PRs, git worktrees, local or cloud | **No internet during agent phase. No image input.** `AGENTS.md` truncates past 32 KiB |

### What changes because of the correction

**Claude Chat is the second-most-capable surface, not the least.** It can:
- Run **Asana and GitHub connector work** directly — the reconciliation and triage tasks I routed to
  Codex could run here instead, with better judgment and no sandbox blindness
- **Build the Drive Out page as an artifact** — no repo needed to produce and iterate the HTML
- **Hold persistent context in a Project** — the Drive Out knowledge base, the ledger, the fact sheet
  all live there permanently instead of being re-pasted each session

**The real dividing line is not "tools vs no tools." It is *local machine access*.**
Only Cowork and Claude Code touch Mozart's filesystem. Everything else is cloud-side.
That single axis explains the whole fleet.

### Two structural blind spots that dictate routing
- **Codex cannot browse mid-task** → fact-finding never goes to Codex; it fabricates citations.
- **Codex cannot see images** → no visual judgment in a media operation. Structural, not stylistic.

### The autonomy multiplier (Mozart's finding)
ChatGPT Chat sustains 4–8 h autonomously with tooling open. **Claude Chat Projects is the analogous
pattern on this side** — persistent knowledge base, connectors live. Both should carry long-duration
work. Neither costs the premium budget.

---

## 2. Corrected lane assignments

| Surface | Owns | Why this surface |
|---|---|---|
| **Cowork (Opus)** | Architecture, routing, gate calibration, ledger | Only surface with local machine + judgment premium |
| **Claude Chat + Project** | **Asana reconciliation** (connector), **Drive Out page as artifact**, script production, red-teaming | Connectors + artifacts + persistent context, no premium burn |
| **Claude Code** | Caption overlay system, batch runner, long local renders | *(blocked — needs `claude` login)* |
| **ChatGPT Chat** | Overnight: free-stock source ledger, licence enumeration, monitoring | Cheapest sustained autonomy |
| **ChatGPT Work** | NY/WA pay-floor citations, captions, scheduler selection, visual QA | Live web + vision + Agent Mode |
| **Codex** | Repo build-out of the approved page, PR triage, Core Flow spec | Only surface that edits repos and opens PRs |

**Notable re-route from v1:** Asana reconciliation moves **Codex → Claude Chat**. Codex would need the
Asana API blind, with no ability to check docs mid-task. Claude Chat has the connector natively.
**Codex should receive the page as an approved artifact and commit it**, rather than designing it —
design needs sight, commit does not.

---

## 3. Blocking items

1. **Claude Code — OAuth expired.** `claude.exe` v2.1.187 runs; returns `401 access token has expired`.
   **Fix: run `claude` in a terminal, complete login.** Only Mozart can do this.
2. **GitHub Actions billing-blocked** — no CI on private repos; absent checks ≠ passing.
3. **Social accounts don't exist** — scheduler can be selected, not activated.
4. **Long-form hosting unsolved** — GitHub caps 100 MB; 10-min video is 150–400 MB.

---

## 4. Standing rule for the director

Two questions before Cowork acts:
1. **Is this architecture or typing?** Typing gets delegated.
2. **Does this need the local machine?** If no, it belongs on a cloud surface — free capacity.

---

## 5. CORRECTION LOG — 2026-08-10

Mozart corrected three errors directly:
1. **Gate threshold was wrong by 15x.** His reference folder (`C:\Users\mozar\Desktop\High Quality
   Media Folder`, read-only) measures lap 1,800-6,300. Gate was set to 120. Fixed.
2. **AVG was killed at 31% out of impatience, not a real failure.** Re-run unattended reached 100% and
   produced a real 1.8MB video with zero intervention. Published: assets/driveout-mileage-log-AVG.mp4
3. **ComfyUI was declared dead from checking the wrong directory.** Real install found under
   `...\ComfyUI\repo\` with a working SD1.5 checkpoint. Needed `--cpu` flag (no NVIDIA GPU on this
   machine -- venv PyTorch build is CUDA-only, --cpu forces the fallback path). Booted clean, first
   generation job queued with zero node errors.

**Standing lesson:** two of three "dead lane" verdicts this session were investigation failures, not
tool failures. Before declaring anything dead: check the actual install path exhaustively, and give
long-running local jobs realistic completion time before killing them.
