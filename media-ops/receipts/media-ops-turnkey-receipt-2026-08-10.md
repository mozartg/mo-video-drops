# Turnkey Revenue Media Factory Receipt

Date: 2026-08-10

## Delivered System

The revenue media factory is a tested local state machine that converts approved media into dated, product-specific, ready-to-post packages for Core Power, Drive Out, and Stuck To Done.

One run produces:

- platform-ready 1080 by 1920 assets
- revenue-facing captions and direct-message CTAs
- accessible alt text
- calendar CSV
- source provenance and SHA-256 hashes
- calibrated numeric QA and semantic decisions
- medical and driver-claims copy red-team decisions
- VSRR state and scenario plan
- publishing manifest with exact external truth state
- a visual campaign review dashboard

## Verified Production Run

Job: `revenue-release-20260811-v4`

Shared Drive folder: https://drive.google.com/drive/folders/11cc3-wdCqQA-x4l13jvj-UYylsi7GQiO

Results:

- 9 planned
- 9 promoted
- 0 rejected
- 9 unique hashes
- 9 provenance receipts
- 9 copy red-team passes
- 0 external publish flags
- no missing packaged assets

Schedule:

| Date | Time ET | Product | State |
|---|---:|---|---|
| 2026-08-11 | 09:15 | Core Power | READY_TO_POST |
| 2026-08-12 | 12:10 | Drive Out | READY_TO_POST |
| 2026-08-13 | 18:20 | Stuck To Done | READY_TO_POST |
| 2026-08-14 | 09:15 | Core Power | READY_TO_POST |
| 2026-08-15 | 12:10 | Drive Out | READY_TO_POST |
| 2026-08-16 | 18:20 | Stuck To Done | READY_TO_POST |
| 2026-08-17 | 09:15 | Core Power | READY_TO_POST |
| 2026-08-18 | 12:10 | Drive Out | READY_TO_POST |
| 2026-08-19 | 18:20 | Stuck To Done | READY_TO_POST |

## Scheduler

Windows task: `MoMediaRevenueReleaseFactory`

- State: Ready
- Last canary result: 0
- Idempotency canary: completed run was skipped rather than duplicated
- Next run: 2026-08-16 06:10 America/New_York
- Start-when-available: enabled
- Multiple instances: ignored
- Weekly output destination: `G:\My Drive\Mo Media Factory\Ready to Post`

## VSRR Red Team

Blocker: `SOCIAL-PUBLISH-AUTH-001`

Status: `PARKED`

Route checks:

1. Connected-tool inventory found no authenticated social publishing connector.
2. Bounded local credential scan found no configured Buffer, Metricool, Meta, TikTok, or YouTube publisher.

The system therefore labels every item `NOT_PUBLISHED` and continues producing synced `READY_TO_POST` packages. It does not poll or retry the same unavailable route. A materially different route begins only when one publisher is authenticated, followed by one canary post with a public URL receipt.

## Verification

- Python tests: 7 passed
- PowerShell scripts: parser pass
- Scheduled-task execution: result 0
- Dashboard: rendered in headless Edge and visually inspected
- Reference folder: read only and untouched

## Operating Commands

Manual run:

```powershell
.\scripts\run-media-release.ps1
```

Install or repair scheduler:

```powershell
.\scripts\install-media-release-task.ps1
```

