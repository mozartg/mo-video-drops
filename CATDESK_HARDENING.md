# CATDESK HARDENING
**Owner:** Mozart Guerrier · **Maintained by:** Claude (Cowork, ops lane) · **Readable by:** ChatGPT, Codex, TRIGGERcmd, CatDesk
**Last updated:** 2026-08-10 · **Repo:** `mozartg/mo-video-drops`

> Any agent picking up this work: read this file first. Do not re-run the discovery steps below —
> the root cause is confirmed and reproducible. Resume from `WHAT REMAINS OPEN`.

---

## 1. STATUS — measured, not asserted

| Item | Status | Evidence |
|---|---|---|
| **Root cause of "catdesk.cmd won't bind port 3200"** | **FOUND — CONFIRMED** | catdesk.exe is a Rust TUI that blocks on an interactive mode-select menu on every launch, regardless of saved config |
| catdesk.cmd → catdesk.js → catdesk.exe argument/env/cwd chain | **NOT the bug — verified correct** | binaryPath resolves correctly, env and cwd both inherit correctly, identical to a direct launch |
| SendKeys automation of the menu (foreground console) | **WORKS when the process owns a real, foregrounded console window** | Confirmed twice: `Get-NetTCPConnection -LocalPort 3200` showed `Listen`, owned by the PID that received the keystroke, within ~5s of sending `"3"` |
| SendKeys automation through the TRIGGERcmd nested launch chain (cmd → powershell → catdesk.exe) | **STILL BROKEN — open item** | `MainWindowHandle` is `0` for catdesk.exe in every nested-launch test (hidden, minimized, and even fully normal outer window style). No window to foreground, so SendKeys has nothing to target |
| `gateway.ps1` null-`$ExtraArgs` bug | **FIXED — verified** | `catdesk_restart` now runs with zero extra args, no dummy-arg workaround needed |
| ngrok public URL external reachability | **STILL UNVERIFIED — network-level failure, cause unclear** | DNS resolves cleanly to real ngrok IPs; TLS handshake fails consistently (`SSL connection could not be established`, `curl` returns `HTTP_000`) both with and without CatDesk actually running locally |
| Reboot/logon persistence mechanism | **NOT IMPLEMENTED — decision point, not silently applied** | See §5 |

---

## 2. ROOT CAUSE

`catdesk.exe` (`C:\Users\mozar\AppData\Roaming\npm\node_modules\catdesk\npm\bin\catdesk.exe`) is
invoked identically whether launched directly or through the npm wrapper chain
(`catdesk.cmd` → `catdesk.js` → `spawn(path.join(__dirname, "bin", "catdesk.exe"), ...)`).
That chain was **not** the bug — env, cwd, and binary resolution are all correct and match a direct
launch exactly (confirmed by reading `catdesk.cmd` and `catdesk.js` and diffing against a live process
tree).

The actual behavior: **on every single launch**, catdesk.exe renders an interactive TUI menu —

```
Select mode:
[1] Control Computer   (local tools)
[2] Control Browser    (chrome-devtools-mcp)
[3] Both
[s] Settings (theme: concise, tool mode: multi-tools)
[q] Quit
```

— and does **not bind port 3200 until a keypress is received**, even though
`~/.catdesk/config.toml` already has `mode = "both"` persisted from a previous session. There is no
documented CLI flag or environment variable to skip this (checked the upstream README quickstart —
only `PORT`, `WORKSPACE_ROOT`, and a macOS-only `CATDESK_SKIP_MACOS_TERMINAL_PROFILE` are
documented). A `--mode both` flag was tested directly; it is not recognized and the app just
re-renders the same menu.

It also does **not** respond to piped/redirected stdin — `Start-Process -RedirectStandardInput` and
writing `"3"` into the pipe never advanced the TUI. The app needs a real console input buffer
(TTY-like), not a byte stream.

**This is why the TRIGGERcmd path always looked like a silent failure.** The process was alive,
correctly resolved, correctly configured — it was just parked at a menu nobody could see or answer,
running hidden/minimized per TRIGGERcmd's launch style.

---

## 3. FIX APPLIED — partial, working component confirmed, full automation still open

### 3a. `gateway.ps1` — fixed and verified

**Bug:** `Set-StrictMode -Version Latest` + `@($ExtraArgs) | ConvertTo-Json -Compress` — piping an
empty array unrolls it to zero pipeline objects, so `ConvertTo-Json` returns `$null` instead of
`"[]"`. `[Text.Encoding]::UTF8.GetBytes($null)` then throws under strict mode, breaking
`catdesk_restart` (and every other async action) whenever no extra positional args are passed.

**Fix**, at `C:\Users\mozar\.TRIGGERcmdData\mo-stack\scripts\gateway.ps1` line ~373:

```powershell
# before
$payload=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes((@($ExtraArgs)|ConvertTo-Json -Compress)))

# after
$safeExtraArgs=@($ExtraArgs)
$payload=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes((ConvertTo-Json -InputObject $safeExtraArgs -Compress)))
```

Using `-InputObject` instead of the pipeline avoids the array-unrolling behavior entirely, so an
empty array correctly serializes to `"[]"`.

**Backup:** `C:\Users\mozar\.TRIGGERcmdData\mo-stack\scripts\gateway.ps1.bak-20260810-050121`
(created before the edit).

**Verified:** `powershell -File gateway.ps1 -Action catdesk_restart` (zero extra args) now returns
`START|catdesk_restart|<run-id>` immediately and the job reaches `running` status — no dummy arg
required.

### 3b. Unattended TUI bypass — proven mechanism, not yet reliable through the launch chain

Built `C:\Users\mozar\TriggerCMD-Scripts\Autonomy\start-catdesk-autopilot.ps1`, which:
1. Checks if port 3200 is already bound; exits cleanly if so (no duplicate launch).
2. Kills orphaned `catdesk.exe` processes that hold no port (these accumulate from failed
   unattended attempts).
3. Launches `catdesk.exe` via `Start-Process`.
4. `SetForegroundWindow` on the new process, then `SendKeys::SendWait("3")` to select "Both" mode
   (matches the saved `config.toml` setting).
5. Retries the foreground+keystroke sequence up to 5 times, polling `Get-NetTCPConnection` for a
   bind.
6. Minimizes the window once bound; logs every step to `C:\Users\mozar\.catdesk\logs\autopilot-*.log`.

`start-catdesk.cmd` was updated to call this script instead of directly re-execing the npm shim.

**Confirmed working:** when `catdesk.exe` is launched directly (not nested inside a hidden/minimized
`cmd.exe → powershell.exe -File` chain), `SetForegroundWindow` + `SendKeys("3")` reliably brings the
TUI past the menu and port 3200 binds within ~5 seconds, owned by the correct PID.

**NOT yet confirmed working through TRIGGERcmd's actual invocation path.** Every test that routed
the launch through the nested `cmd.exe → powershell.exe -File → Start-Process catdesk.exe` chain —
tested with the outer window hidden, minimized, and fully normal — resulted in
`(Get-Process catdesk).MainWindowHandle` reading `0`. No window handle means `SetForegroundWindow`
has nothing to target, so the keystroke sequence has no effect and the process sits at the menu
indefinitely, same as before the fix. This reproduced consistently across five separate test runs.

**Working hypothesis:** the console window for a process spawned this deep in a chain, particularly
when the top of that chain started hidden/minimized, is attributed by Windows to the console-owning
ancestor rather than to `catdesk.exe` itself — so `Process.MainWindowHandle` for catdesk.exe never
populates even though a console technically exists. This needs testing from a real interactive login
session (this investigation ran through a remote automation tool, which may itself not have full
desktop/window-station rights at the point nested child processes are spawned). Forcing a genuinely
new console for the grandchild (e.g. `CREATE_NEW_CONSOLE` via direct P/Invoke to `CreateProcess`
rather than `Start-Process`, or an AutoHotkey-based launcher) is the next thing to try.

---

## 4. RECEIPTS / EVIDENCE

- `catdesk.cmd` content confirmed to resolve `node.exe` fallback correctly to
  `C:\Users\mozar\.catdesk\windows-compat\node\node.exe` (present, on `PATH`).
- `catdesk.js` confirmed: `binaryPath = path.join(__dirname, "bin", "catdesk.exe")`, `spawn(...,
  { cwd: process.cwd(), env: process.env, stdio: "inherit" })` — matches direct-launch behavior
  exactly.
- Direct TUI capture (stdout of a `-RedirectStandardOutput` run) showed the literal boxed menu with
  `[1]/[2]/[3]/[s]/[q]` options and no further output — confirms the block point.
- `Get-NetTCPConnection -LocalPort 3200` before intervention: empty. After `SendKeys("3")` on a
  foregrounded direct launch: `Listen`, `OwningProcess` = the exact PID that received the keystroke.
- `gateway.ps1 -Action catdesk_restart` (no extra args) after the patch: `START|catdesk_restart|<id>`
  → `job_status` → `RESULT|running|catdesk_restart|<id>`. No exception, no dummy arg.
- ngrok: `Invoke-WebRequest https://emphatic-tux-ungodly.ngrok-free.dev/.../mcp` →
  `The SSL connection could not be established`; `curl.exe` → `HTTP_000`. This happened both with
  CatDesk running locally (tunnel API at `127.0.0.1:4040/api/tunnels` showed the tunnel registered,
  `public_url` correct, historical `conns.count: 24`) and with it stopped — the failure mode did not
  change either way, which points at a TLS/network-level block on this network rather than a CatDesk
  or ngrok-account problem. DNS resolution itself was clean (multiple valid ngrok edge IPs, both
  IPv4 and IPv6). **Not resolved — needs a test from a different network (phone hotspot, different
  ISP) to isolate whether this is ISP/router-level SNI filtering of `*.ngrok-free.dev`.**

---

## 5. WHAT REMAINS OPEN

1. **Full unattended bind through the actual TRIGGERcmd launch path is not yet solved.** The
   SendKeys mechanism is proven correct in isolation but doesn't reach catdesk.exe's console when
   nested inside TRIGGERcmd's process chain in this environment. Next step: test
   `start-catdesk.cmd` by having Mozart (or a tool with confirmed interactive-desktop rights) run it
   directly, or replace `Start-Process` in the autopilot script with a raw `CreateProcess` call using
   `CREATE_NEW_CONSOLE` to guarantee catdesk.exe owns its own window regardless of ancestor state.
2. **ngrok external reachability is still not independently confirmed.** TLS handshake fails from
   this execution context regardless of whether the tunnel is live. Needs a test from a genuinely
   different network path (e.g., phone data) to rule out ISP/router-level blocking of
   `*.ngrok-free.dev` domains, which is a known thing some ISPs and consumer routers do.
3. **Persistence-at-logon decision — flagged, not applied.** A Windows Scheduled Task set to
   "run at logon" calling the fixed `start-catdesk.cmd` is the standard answer for "survives reboot
   without a human re-launching it," **but it inherits the exact unattended-TUI problem in §3b above**
   — a Scheduled Task, like TRIGGERcmd, doesn't give the spawned process a genuinely interactive,
   foregroundable console by default either. Setting it up **before** item 1 is solved would just
   relocate the same silent-hang failure to a different trigger. **This is also a standing-autonomy
   choice, not just a technical one** — a scheduled task means a background agent-control server runs
   on Mozart's machine continuously, listening on a public ngrok URL, without a human needing to
   start it each session. That tradeoff (always-on remote control surface vs. manual per-session
   start) should be Mozart's call, not something applied silently. Recommend: solve item 1 first,
   demonstrate a clean unattended bind on demand, then decide together whether "at logon" or
   "manual start, TRIGGERcmd on request" is the right default.

---

## 6. FILES TOUCHED THIS SESSION

| File | Change |
|---|---|
| `C:\Users\mozar\TriggerCMD-Scripts\Autonomy\start-catdesk.cmd` | Now calls `start-catdesk-autopilot.ps1` instead of re-execing the npm shim directly |
| `C:\Users\mozar\TriggerCMD-Scripts\Autonomy\start-catdesk-autopilot.ps1` | **New.** SendKeys-based TUI bypass, orphan-process cleanup, bind-wait loop, logging to `~/.catdesk/logs/` |
| `C:\Users\mozar\.TRIGGERcmdData\mo-stack\scripts\gateway.ps1` | Patched `$ExtraArgs` null/empty-array `ConvertTo-Json` bug at ~line 373 |
| `C:\Users\mozar\.TRIGGERcmdData\mo-stack\scripts\gateway.ps1.bak-20260810-050121` | **New.** Pre-patch backup |
