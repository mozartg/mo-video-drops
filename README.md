# AGENT SURFACE MAP — who does what, and what each one physically cannot do
**Issued 2026-08-09 · Owner: Mozart Guerrier · Read `LEDGER.md` for pipeline state**

Four agent surfaces are in play. Their limits are **structural, not stylistic** — assigning work to the
wrong surface produces confident failure, not a slower success.

---

## The four surfaces

| Surface | Loop | Has | **Cannot** |
|---|---|---|---|
| **ChatGPT Work** | Conversational, projectless, cross-app | Connectors, Agent Mode (multi-step browsing), file uploads, **vision** | No repo. No terminal. No persistent git state. Cannot run your test suite |
| **ChatGPT Codex** | Project/code-first agent | Clones repo into sandbox, edits across files, runs commands, runs tests, opens PRs, git worktrees, local *or* cloud execution | **Internet blocked by default during the agent phase.** **No image inputs.** `AGENTS.md` silently truncates past 32 KiB |
| **Cowork (Claude)** | Conversational + orchestration | MCP connectors (Asana, GitHub, Drive), local file tools, sandboxed shell, **vision**, web search | Chat-shaped. Not built for long unattended repo refactors |
| **Claude Code** | Terminal-native agent | Local repo, filesystem, long-running builds, git | No connector graph. Not conversational |

**The load-bearing asymmetry:**
- **Codex cannot browse the web while working.** Research → ChatGPT Work. Never Codex.
- **Codex cannot see images.** Anything visual — design matching, thumbnail review, media QA,
  "does this look right" — **cannot go to Codex.** It is structurally blind to this project's core output.
- **ChatGPT Work cannot run code against a repo.** Implementation → Codex. Never Work.

Sources: [Codex vs ChatGPT loop](https://www.morphllm.com/comparisons/chatgpt-vs-codex) ·
[ChatGPT Work vs Codex guide](https://explainx.ai/blog/chatgpt-work-vs-codex-complete-guide-2026) ·
[Codex cloud security / internet defaults](https://www.developersdigest.tech/blog/openai-codex-cloud-security-playbook-2026) ·
[Codex capabilities guide](https://www.innovatrixinfotech.com/blog/openai-codex-2026-what-it-can-do)

---

## Routing rule

```
Needs the live web, a connector, or an eye?      -> ChatGPT Work
Needs a repo edited, tests run, a PR opened?     -> Codex
Needs media generated, gated, published?         -> Claude (this repo)
Needs a long local build or refactor?            -> Claude Code
```

**Corollary that matters here:** Codex must be handed *fully specified* work. It cannot look anything
up mid-task. If a spec is ambiguous, Codex guesses. **ChatGPT Work does the research and writes the
spec; Codex implements it.** That sequencing is not a preference — it is forced by the sandbox.

---

## Current assignments

| Agent | Owns | Explicitly forbidden |
|---|---|---|
| **Claude** | Media pipeline: generation, QA gates, publishing to `mo-video-drops` | — |
| **ChatGPT Work** | Research, sourcing, competitive/legal review, narratives, captions, scheduler selection, visual review of Claude's output | Editing repos. Running code |
| **Codex** | Drive Out public surface, PR triage, Core Flow spec, Asana reconciliation scripts | ffmpeg, Pexels/Pollinations, `mo-video-drops`, `C:\temp\claude-ops\`, anything requiring sight or live web |

Prompts: `PROMPT_CHATGPT_WORK.md` · `PROMPT_CODEX.md`

---

## Why the split is drawn here

Drive Out needs videos (Claude), a legal-safe factual basis about NY/WA pay floors (**Work** — needs
live sources), a public destination page (**Codex** — needs repo + deploy), and captions/narratives
(**Work** — needs judgment and current platform norms).

Handing the legal research to Codex would produce fabricated citations, because it cannot reach the
web to check them. Handing the page build to Work would produce a code block nobody deploys. The
split follows the capability boundary, not a division of labour preference.
