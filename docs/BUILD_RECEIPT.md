# Build Receipt

Date: 2026-08-10

## Verified

| Check | Result | Evidence |
|---|---|---|
| JSON contract tests | PASS | `remotion/npm test`, 2 tests passed |
| TypeScript | PASS | `remotion/npm run typecheck` |
| Composition discovery | PASS | `DriveOutTrial` 450 frames; `DriveOutLongForm` 18,000 frames; both 1080x1920 at 30 fps |
| 15-second Remotion render | PASS | `remotion/out/trial.mp4`, 7,790,495 bytes |
| Trial artifact hash | PASS | SHA-256 `31921F00246EAB3561BE4227E4F1319BEF005F4179E12CEE6B5DB58C2D14C44D` |
| Trial receipt | PASS | `remotion/out/trial-receipt.json` |
| Long-form input contract | PASS | `remotion/out/long-form-contract-receipt.json`, 600 seconds |
| Static site assertions | PASS | `scripts/verify-site.ps1` |

## Blocked

The first foreground `npm run render:long-form` attempt did not return a process status within the execution cell. A read-only process check later found no originating Node renderer process and no `remotion/out/long-form.mp4`. A second materially different retry used `--concurrency=4 --log=verbose` and a fresh `out/long-form-retry.mp4` path; it likewise produced no artifact or returned status. Both detached waits were terminated to prevent indefinite orphaned commands. This is not a completed ten-minute render and is not reported as one.

The required machine-control fallback was also exercised. CatDesk failed its MCP SSE probe with HTTP 404. TRIGGERcmd accepted job `20260810T045416567Z-05804062` for `npm run render:long-form`; a lookup using `id` returned `DONE|job_result|failed|3368281c734c|Invalid run or job ID.`, and a corrected `job_id` lookup returned `session=null`. No remote artifact receipt was returned, so this submission remains accepted-but-unverified.

## Boundaries checked

- `LEDGER.md` was not modified.
- The benchmark media folder was read-only; its files were copied as render inputs and not edited.
- No `ffmpeg` command was invoked.
- No AI media generation, purchases, Asana writes, GitHub writes, or email sends were performed.
- No pay-floor figure or citation was invented.
- No GitHub Pages deployment or external URL verification is claimed.
- CatDesk was attempted first; TRIGGERcmd was used as the fallback and its accepted job remains unverified.

## Remaining authorization gates

1. Diagnose the long-form host hang and obtain a fresh 600-second artifact receipt.
2. Supply cited pay-floor data and a real capture destination before public announcement.
3. Read live GitHub and Asana state before producing PR or task recommendations.
