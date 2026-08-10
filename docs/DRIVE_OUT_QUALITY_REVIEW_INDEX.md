# Drive Out Quality Review Index

Date: 2026-08-10
Review status: **TECHNICAL RECEIPT PASS / VISUAL REVIEW REQUIRED**

This index is the handoff surface for a visual-capable reviewer. The Google Drive links below are authenticated Drive file links returned by the upload connector. They are not public-web publication receipts; Drive sharing remains unchanged.

## Review folders

- Technical Remotion batch: https://drive.google.com/drive/folders/1DF9GugaCegNB8UVEVRb9fXdmAlMHSELG
- Legacy published clips: https://drive.google.com/drive/folders/1VNlTtmtPPPl_pjT-XKYB6InGm526MC-l
- Experimental, do not approve: https://drive.google.com/drive/folders/1WIGyY7LgiF-itZSjgwpYi4XJo2WDj2Kv
- Supporting documentation and tool chain: https://drive.google.com/drive/folders/1pgQ1FfJRQ0ILjme0Q40gZV5Ek4YBl2uf

## Current Remotion videos

| Review ID | Video | Drive link | Technical evidence | Visual decision |
|---|---|---|---|---|
| R-001 | 15-second trial | https://drive.google.com/file/d/1jWtVp3IXlr_swek9MBdU5u0rBiJGOZeR/view?usp=drivesdk | 450 frames, 1080x1920, 30 fps; SHA-256 `31921F00246EAB3561BE4227E4F1319BEF005F4179E12CEE6B5DB58C2D14C44D` | REVIEW REQUIRED |
| R-002 | 10-minute long form | https://drive.google.com/file/d/1X1LYB7MFpORB3pQjs15dpL4C1RPJWv16/view?usp=drivesdk | 18,000 frames, 1080x1920, 30 fps, 96,524,686 bytes; SHA-256 `D01A1323D95A0C95915EDFEDE69F142E81CC2DDC138BF3F06F3A7649158F52A1` | REVIEW REQUIRED |
| R-003 | Drop 001 - source the number | https://drive.google.com/file/d/1T_Nf5g7qXk_bfZ5Fe39J5EbtS6rJrADP/view?usp=drivesdk | 7,652,426 bytes; SHA-256 `21372714565609F41F3F6E923A3E2A4BCA9AA1F220AB4D5B54364DF375CAC26F` | REVIEW REQUIRED |
| R-004 | Drop 002 - keep the mileage log | https://drive.google.com/file/d/1S9gp2DLO52-fJlYLGjH1JW9Pn0WqIR8t/view?usp=drivesdk | 25,614,385 bytes; SHA-256 `C66BEF636A44AA975169667D845FE2C014CD347AD80A8266E70C12047E820BF7` | REVIEW REQUIRED |
| R-005 | Drop 003 - start with what you own | https://drive.google.com/file/d/1kpdH9mddK3DVwObjQuqH3hnCGBjpVT6h/view?usp=drivesdk | 15,678,508 bytes; SHA-256 `701F477373B5FA69C794A4CE6DD229EF101A2AEA35EB3F6AC5766D1431341639` | REVIEW REQUIRED |
| R-006 | Drop 004 - work behind the wheel | https://drive.google.com/file/d/1vj8mDbmeiEN3Vtfi7zoYilugWjMrWGtL/view?usp=drivesdk | 18,806,304 bytes; SHA-256 `833570E69AB237DB49A91D5F3C376C89B48DA1E042E46682D8CE9870447D7DD2` | REVIEW REQUIRED |
| R-007 | Drop 005 - keep the signal close | https://drive.google.com/file/d/1bKLrCuRb1SoaUAEKP6KpznSc9hFcmpyy/view?usp=drivesdk | 22,255,655 bytes; SHA-256 `8FFC09105C84DBF6BBE9884B071EB92EF183C6694BC69E1A52FF80146ED44FC1` | REVIEW REQUIRED |

The long-form retry render was byte-identical to R-002 and was not uploaded as a redundant review copy.

## Legacy and experimental links

| Review ID | Video | Drive link | Status |
|---|---|---|---|
| L-001 | Legacy mileage log | https://drive.google.com/file/d/13enEvjFXenvEjEYQTQbm3zT1iWRkKMm4/view?usp=drivesdk | Visual review required; outside current Remotion receipt set |
| L-002 | Legacy pay-floor clip | https://drive.google.com/file/d/1GBMIG4IDvTsVpdHKunoa7LcDzC84Qz96/view?usp=drivesdk | Visual review required; pay-floor citation still absent |
| L-003 | Legacy pay-floor longer clip | https://drive.google.com/file/d/1vhV1LrWpGT3ZRDruriACvIoXQOidArCD/view?usp=drivesdk | Visual review required; pay-floor citation still absent |
| X-001 | Cloudgen experimental mileage clip | https://drive.google.com/file/d/1aRkJ9GVpYGIUCc56ZKMguZxmJuX5sBDn/view?usp=drivesdk | Experimental; do not approve or publish |

## Tool-by-tool development chain

| Step | Tool or surface | Contribution | Evidence |
|---|---|---|---|
| 1 | Read-only benchmark folder | Supplied reference PNG inputs; folder was not modified | `C:\Users\mozar\Desktop\High Quality Media Folder` |
| 2 | Remotion JSON contract | Validated title, image paths, captions, durations, and safe paths | `remotion/src/input.ts`; 2 tests passed |
| 3 | Remotion renderer | Produced deterministic 15-second and 10-minute programmatic video | `remotion/src/Root.tsx`; local MP4 outputs |
| 4 | PowerShell receipt verifiers | Recomputed bytes and SHA-256 without visual or ffmpeg claims | `remotion/scripts/verify-trial.ps1`; `verify-long-form-artifact.ps1` |
| 5 | Static-site verifier | Checked Drive Out destination markers and media links | `scripts/verify-site.ps1` |
| 6 | Red-team readback verifier | Cross-checked 8 artifacts, receipts, docs, ledger boundary, and clean tree | `scripts/verify-readback.ps1`; PASS |
| 7 | Google Drive | Uploaded review artifacts and supporting docs outside the local-only delivery path | Links in this index |
| 8 | GitHub | Stores source, receipts, certification, triage, ship-gate, and PR state | https://github.com/mozartg/mo-video-drops/pull/2 |
| 9 | Asana | Receives actionable delivery context and Drive review links on the media work items | Autonomous Media Factory task `1217091707277470`; Media Factory task `1217086443336042` |

## Visual review gate

Codex did not visually inspect or side-by-side judge these videos. A visual-capable reviewer should compare each current Remotion video against the standing benchmark folder and record:

- composition and legibility;
- image quality and artifacting;
- caption timing and readability;
- motion quality and scene continuity;
- audio presence or absence;
- whether the piece meets the benchmark standard for approval.

Until that review is recorded, these are technically receipt-verified review candidates, not quality-certified media.
