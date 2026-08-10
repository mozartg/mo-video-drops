# Asana Media Project Merge and Close Map

Date: 2026-08-10
Scope: proposal only. No Asana task or project was modified.

## Current project state

| Project | Live counts | Current status | Proposed role |
|---|---:|---|---|
| [Autonomous Media Factory - 45 Images + 10 Videos](https://app.asana.com/1/15960956269365/project/1217091707294069) | 29 total, 4 complete, 25 incomplete | Connection repair in progress; benchmark outputs and final review package remain incomplete | Keep as the campaign execution queue |
| [Media Factory](https://app.asana.com/1/15960956269365/project/1217086398796730) | 26 total, 1 complete, 25 incomplete | Canonical architecture and adapter surface; CatDesk availability was verified once, result transport remains defective | Keep as the canonical media control-plane queue |
| [Media Generation Audit and Recovery - 2026-07-31](https://app.asana.com/1/15960956269365/project/1217082622710492) | 20 total, 2 complete, 18 incomplete | Red; recovery scope paused for harvest and minimum-path selection | Harvest evidence, then retire or archive; do not reactivate wholesale |

## Disposition map

| Work family | Destination | Proposed action | Why |
|---|---|---|---|
| 45 image and 10 video benchmark candidates | Autonomous Media Factory | KEEP there | The project is explicitly accountable for benchmark candidates, scoring, receipts, and final unpublished review. |
| Connection repair, adapters, custody, receipts, and result transport | Media Factory | KEEP there and make it canonical | These tasks define reusable worker/control-plane behavior rather than one campaign's candidate set. |
| Cloudinary/local reconciliation and human review of historical assets | Audit and Recovery | RETAIN as evidence, then CLOSE or ARCHIVE after harvest | The project contains historical evidence and unresolved audit work, but its current status says not to resume the full recovery scope. |
| Superseded repair tasks | Audit and Recovery | CLOSE only after confirming the replacement receipt is linked | Two tasks are already marked superseded and complete; the remaining historical repair work should not be silently treated as active production work. |
| MCLP-001 consumer pack | Named consumer repositories, not an Asana project | One cross-repository decision record, then scoped execution tasks | Prevents five copies from becoming five competing authorities. |

## Proposed consolidation sequence

1. Keep Media Factory as the technical authority for adapters, transport, manifests, run IDs, artifacts, hashes, and result receipts.
2. Keep Autonomous Media Factory as the delivery queue for the current 45-image/10-video benchmark and final review package.
3. Harvest reusable controls and direct evidence from Audit and Recovery into the two live projects.
4. Mark only superseded or fully harvested audit tasks for closure; archive the project after its evidence index is durable.
5. Do not merge project tasks solely because their names overlap. Preserve one owner, one destination, and one receipt per surviving work item.

## Why this is not a blind merge

All three projects are still incomplete and contain different evidence responsibilities. A destructive merge now would erase distinctions between active campaign delivery, reusable infrastructure, and historical recovery evidence. The correct action is role separation plus evidence-linked retirement, not mass deletion.
