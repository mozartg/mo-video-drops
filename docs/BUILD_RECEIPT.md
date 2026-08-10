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
| Ten-minute Remotion render | PASS | `remotion/out/long-form.mp4`, 96,524,686 bytes |
| Ten-minute artifact hash | PASS | SHA-256 `D01A1323D95A0C95915EDFEDE69F142E81CC2DDC138BF3F06F3A7649158F52A1` |
| Five local campaign drops | PASS | `remotion/out/drops/drop-001.mp4` through `drop-005.mp4`, each with its own receipt |
| Static site assertions | PASS | `scripts/verify-site.ps1` |

## Execution Notes

The initial foreground render cells did not return promptly, but both final artifacts appeared asynchronously and were later verified by path, size, SHA-256, and the 18,000-frame contract. The retry artifact is byte-identical to `long-form.mp4`.

The required machine-control fallback was also exercised. CatDesk failed its MCP SSE probe with HTTP 404. TRIGGERcmd accepted job `20260810T045416567Z-05804062` for `npm run render:long-form`; a lookup using `id` returned `DONE|job_result|failed|3368281c734c|Invalid run or job ID.`, and a corrected `job_id` lookup returned `session=null`. No remote artifact receipt was returned, so this submission remains accepted-but-unverified.

## Boundaries checked

- `LEDGER.md` was not modified.
- The benchmark media folder was read-only; its files were copied as render inputs and not edited.
- No `ffmpeg` command was invoked.
- During the initial build phase, no AI media generation, purchases, Asana writes, GitHub writes, or email sends were performed. The later delivery-certification phase did update and push the draft PR and commit supporting documentation; those writes are recorded in Git history and the PR link.
- No pay-floor figure or citation was invented.
- No GitHub Pages deployment or external URL verification is claimed.
- CatDesk was attempted first and failed its MCP probe with HTTP 404. TRIGGERcmd was used as the fallback; its job receipt remained unverified, but the local artifact verification independently passed.

## Remaining authorization gates

1. Supply cited pay-floor data and a real capture destination before public announcement.
2. Decide whether to host the 96.5 MB long-form artifact outside GitHub Pages before publishing it.
3. Re-run the independent readback verifier after any branch rewrite, artifact replacement, or documentation change.
