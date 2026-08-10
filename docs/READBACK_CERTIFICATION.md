# Red-Team Readback Certification

Date: 2026-08-10
Repository: https://github.com/mozartg/mo-video-drops
Evidence snapshot: `2da53c310dedec7cf63334539c837c58b015b816`
Independent verifier: `scripts/verify-readback.ps1`
Manifest: `docs/READBACK_MANIFEST.json`

## Purpose

This packet is designed for a separate assistant or reviewer to validate the deliverable without trusting the prior certification message. It binds the claim set to a commit, the local MP4 artifacts to byte counts and SHA-256 hashes, the receipts to those artifacts, the supporting documents to required paths, and the protected-boundary checks to executable commands.

## Completion chain

1. **Source:** the evidence snapshot commit identifies the repository state under review.
2. **Artifact:** every listed MP4 must exist at its declared path and match the manifest byte count and SHA-256.
3. **Receipt:** every artifact receipt must be `PASS` and agree with the recomputed artifact size and hash.
4. **Supporting documentation:** required certification, triage, ship-gate, project-map, build-receipt, and brief files must exist.
5. **Boundary checks:** the static-site verifier must pass, `LEDGER.md` must have no diff, and the working tree must be clean.
6. **Remote readback:** the manifest preserves the PR head, base, state, draft state, mergeability, and zero-status result that must be checked against live GitHub metadata.
7. **Independent affirmation:** a third-party assistant reports PASS, PARTIAL, or FAIL using the manifest and verifier, with no reliance on this response.

## Red-team findings

| ID | Finding | Resolution or remaining limit |
|---|---|---|
| RT-001 | Prior certification named an older commit than the final pushed evidence. | Corrected by binding the readback packet to snapshot `2da53c3`; later commits require a new readback. |
| RT-002 | Prior GitHub triage named an older PR head and stale commit/file counts. | Corrected in `GITHUB_PR_TRIAGE.md` for snapshot `2da53c3`. |
| RT-003 | The build receipt's global “no GitHub writes” statement conflicted with later PR and documentation pushes. | Narrowed to the initial build phase and recorded the later delivery writes. |
| RT-004 | MP4 evidence is local and ignored by Git; a fresh clone cannot verify bytes without the local artifact set. | Explicitly retained as a local-artifact limit in the manifest. |
| RT-005 | Earlier GitHub reads returned no CI statuses and `mergeable=false`, while the latest live reread returned no statuses and `mergeable=true`. | Preserved as time-sensitive remote state; CI remains untested and mergeability must be refreshed immediately before any merge. |
| RT-006 | Codex cannot visually judge the media or certify aesthetic fidelity. | Explicit non-claim; third-party human or visual-capable review remains required. |

## Third-party affirmation protocol

A separate assistant can affirm the package by:

1. Reading `docs/READBACK_MANIFEST.json` and checking out the evidence snapshot or inspecting the same local workspace.
2. Running `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify-readback.ps1`.
3. Running the listed tests and static-site verifier.
4. Reading the supporting documents and comparing their claims to the verifier output and live PR metadata.
5. Returning a signed-style report with the snapshot commit, verifier result, artifact count, documentation count, and any disagreement.

The packet is **READY_FOR_INDEPENDENT_AFFIRMATION**. It is not itself a third-party signature, and no visual-quality affirmation is implied.

## Execution record

- `scripts/verify-readback.ps1` ran on the clean workspace and returned `PASS`: 8 artifacts, 6 documentation files, unchanged `LEDGER.md`, and a clean working tree.
- An independent assistant was dispatched for a separate readback, but it did not return within two bounded 120-second waits and was shut down. No third-party assistant affirmation is claimed.
- Current affirmation state: **PENDING_INDEPENDENT_REVIEW**.
