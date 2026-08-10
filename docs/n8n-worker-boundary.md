# n8n Media Worker Boundary

## Objective

Keep orchestration separate from media correctness.

## Worker contract

Every production lane must work without n8n first:

`job -> artifact -> QA -> receipt`

The direct worker is promoted only after it repeatedly produces a valid receipt for a real artifact.

## n8n may own

- schedules and triggers
- dispatch
- branching and provider routing
- bounded retry policy
- approval handoffs
- notifications
- status synchronization

## n8n must not be source of truth for

- model inference correctness
- FFmpeg or Remotion rendering internals
- existence or integrity of an artifact
- media licensing decisions
- QA pass/fail truth
- platform permissions or publishing authorization

## Binary handling

Pass artifact paths, URLs and receipt IDs through orchestration whenever possible instead of moving large media binaries node-to-node.

## Promotion test

Run the same known-good job through two paths:

A. direct worker
B. n8n -> same worker

Compare completion, duplicates, retry correctness, recovery after a forced worker failure, elapsed time and operator visibility. n8n earns a lane only when it adds operational value without changing the media contract.
