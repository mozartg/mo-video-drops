# SIX-SURFACE DELEGATION MATRIX
**Issued 2026-08-09 · Owner: Mozart Guerrier · Director: Claude (Cowork)**
**Constraint driving this document: weekly usage at 75%, session at 52%, on Opus 5 — the most
expensive model in the fleet.**

---

## 0. The resource problem, stated plainly

Mozart's standing global instruction: *"Always default to the cheapest model every time. If a model is
not the cheapest, present a clear notice until it is changed."*

That instruction has been violated for this entire session. Opus 5 has been running **executor** work —
shell commands, file patches, git pushes, ffmpeg invocations — that a cheaper model performs
identically. Opus earns its cost on **architecture, diagnosis, and judgment**, not on typing commands.

**Corrective policy, effective immediately:**

| Work type | Model | Why |
|---|---|---|
| Architecture, lane design, root-cause diagnosis, contradiction-hunting | **Opus** | Judgment is the product |
| Pipeline execution, batch runs, file ops, publishing, gate runs | **Sonnet** | Identical output, fraction of cost |
| Bulk mechanical passes, log triage, format conversion | **Haiku** | Volume work |
| Anything ChatGPT/Codex can do in parallel | **Not Claude at all** | Free parallel capacity |

**The strategic error to avoid:** spending a scarce premium budget on work that a free or cheap surface
would have absorbed. Delegation is a *cost* decision before it is a *capability* decision.

---

## 1. Six surfaces, non-overlapping

| # | Surface | Cost | Uniquely can | Uniquely cannot | Assignment |
|---|---|---|---|---|---|
| 1 | **Claude Chat** | Cheap | Long-form reasoning, writing, critique | No tools, no files, no repo | Scripts, narratives, red-teaming, spec review |
| 2 | **Cowork (Claude)** | **Expensive** | MCP connectors + local files + shell + vision | Not built for long unattended refactors | **Direction + orchestration only** |
| 3 | **Claude Code** | Metered separately | Terminal-native, long local builds, repo | No connector graph | **BLOCKED — token expired** |
| 4 | **ChatGPT Chat** | Free/cheap | Sustained autonomous runs (4–8 h observed) with tooling open | No repo write | Long research runs, monitoring, drafting |
| 5 | **ChatGPT Work** | Included | Live web, connectors, **vision**, Agent Mode | No repo, no terminal | Research, sourcing, captions, visual QA |
| 6 | **Codex** | Included | Repo edit, run tests, open PRs | **No internet mid-task. No image input.** | Build, triage, specs |

### The two structural blind spots that dictate routing
- **Codex cannot browse while working** → all fact-finding goes to Work or ChatGPT Chat. Codex given
  a research task fabricates citations with confidence.
- **Codex cannot see images** → every visual judgment in a *media* company is off-limits to it.

### The autonomy tactic (Mozart's finding, worth templating)
ChatGPT Chat sustains 4–8 hours of autonomous work when prompted well **and the tooling stays open**.
That is the cheapest continuous capacity in the fleet. It should carry long-running, low-judgment,
high-duration work: monitoring, enumeration, drafting, research sweeps. **Do not spend Opus on
anything ChatGPT Chat can run overnight for free.**

---

## 2. Current lane assignments

| Surface | Owns now | Deliverable |
|---|---|---|
| **Cowork (Claude)** | Direction, lane architecture, gate calibration | This matrix; ledger upkeep |
| **Claude Chat** | Video scripts for 10 shorts; red-team of the published clips | 10 scripts, ≤10s spoken each |
| **Claude Code** | *(blocked)* Caption overlay system + batch runner | Needs `claude` login first |
| **ChatGPT Chat** | Long autonomous run: enumerate free stock sources with commercial licences; build the rotation ledger | Source table w/ limits + licences |
| **ChatGPT Work** | NY/WA pay-floor fact sheet w/ citations; captions; scheduler selection; visual QA | See `PROMPT_CHATGPT_WORK.md` |
| **Codex** | Drive Out public surface; PR triage; Core Flow spec; Asana reconciliation | See `PROMPT_CODEX.md` |

---

## 3. Blocking items

1. **Claude Code — token expired.** `claude.exe` v2.1.187 installed and runs; returns
   `401 OAuth access token has expired`. **Fix: run `claude` in a terminal, complete login.**
   Until then surface 3 is dead and its work sits unassigned.
2. **GitHub Actions billing-blocked** — no CI on any private repo.
3. **Social accounts do not exist** — scheduler selection can proceed, activation cannot.
4. **Long-form hosting unsolved** — GitHub caps at 100 MB; 10-min video runs 150–400 MB.

---

## 4. Standing rule for the director role

Before Cowork executes anything, answer: **"Can a cheaper or free surface do this?"**
If yes, write the prompt and hand it off. Executing it here is the expensive mistake.
