# Mo Revenue Media Release Factory

This factory turns the nine approved campaign canaries into a dated, quality-gated, revenue-facing release queue for Core Power, Drive Out, and Stuck To Done.

## Run now

```powershell
.\scripts\run-media-release.ps1
```

Default output:

```text
G:\My Drive\Mo Media Factory\Ready to Post\scheduled-revenue-release-YYYYMMDD
```

Each run contains copied platform-ready assets, caption files, alt text, `calendar.csv`, `schedule-plan.json`, `publishing-manifest.json`, `scenario-plan.json`, `state.json`, and `release-receipt.json`.

## Schedule

```powershell
.\scripts\install-media-release-task.ps1
```

The default task runs Sundays at 6:10 AM and starts when available if the computer was asleep. Completed jobs are idempotent and skipped on rerun.

## Truth boundary

The current factory produces `READY_TO_POST` packages. It does not claim that material was externally published. Automatic publication remains disabled until one authenticated social publisher passes a canary post with a public URL receipt.

## Promotion gates

- Laplacian variance at least 1,800
- Entropy at least 6.8
- Resolution at least 1.6 megapixels
- Semantic review pass
- Medical and driver-entitlement copy red team pass
- Source provenance and SHA-256 receipt present

