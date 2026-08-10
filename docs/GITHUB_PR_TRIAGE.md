# GitHub PR and Branch Triage

Date: 2026-08-10
Repository: https://github.com/mozartg/mo-video-drops

## Current remote inventory

These values were read from the live GitHub connector on 2026-08-10. They replace the historical counts in the brief for this repository only.

| Surface | Current evidence | Decision |
|---|---|---|
| Open pull requests | 1: PR #2 | No merge or close executed |
| Branches | 3: `main`, `agent/verified-drive-out-media-batch`, `chatgpt/prompt3-media-research-20260810` | No branch deleted |
| GitHub checks on PR #2 head | Combined status returned no statuses | Untested; absence is not passing |
| PR #2 mergeability after latest push | GitHub reports `mergeable=false`; base `main` is at `65fe6e8`, evidence head is `2da53c3` | REBASE candidate; do not merge until the branch is reconciled and rechecked |
| Repository | Public, default branch `main`, merge permissions available | Keep review gate explicit |

The brief's `27 open PRs / 19 branches` count and the five-repository MCLP-001 statement remain user-reported historical scope. They were not reproduced by the current search scoped to `mozartg/mo-video-drops`.

## PR table

| PR | Head | State | Recommendation | One-line justification |
|---|---|---|---|---|
| #2 | `agent/verified-drive-out-media-batch` | Open, draft, `mergeable=false`, 10 commits, 60 files | REBASE candidate after human review; keep draft now | The branch contains the verified media batch but is not currently mergeable against the newer `main`; checks are absent and deployment is not verified. |

PR #2: https://github.com/mozartg/mo-video-drops/pull/2

The branch's local merge base is `cf19181`. Remote `main` contains newer Prompt 3 commits through `65fe6e8`, so the PR is not up to date with its base. GitHub did not expose a conflict explanation in the returned metadata; no rebase was attempted. This table is an evidence snapshot for head `2da53c3`; later commits require a fresh readback.

## Branch table

| Branch | Observed state | Recommendation | Reason |
|---|---|---|---|
| `main` | Default branch | KEEP | Repository authority and PR base. |
| `agent/verified-drive-out-media-batch` | PR #2 head | KEEP until PR decision | Contains the verified Remotion and Drive Out batch deliverables. |
| `chatgpt/prompt3-media-research-20260810` | Present; no open PR appeared in the current scoped search | HOLD for ownership review, then CLOSE or open a scoped PR | Current inventory does not establish whether its work is still needed or duplicated. |

## MCLP-001 proposal

The brief describes a media consumer pack duplicated across five repositories. No five-repository inventory was available in the current scoped GitHub result, so no copies or cross-repository decisions were fabricated. The safe proposal is one manifest and one acceptance decision, then five repository-local adapters only after each repository and branch is identified.

Required evidence before a cross-repository MERGE/CLOSE/REBASE table:

1. Exact five repository names and PR numbers.
2. Head and base commit for each PR.
3. File overlap and unique diff per PR.
4. Local verification result for each consumer.
5. Explicit disposition for any branch with no surviving consumer.

## Non-actions

- No pull request was merged, closed, rebased, or made ready for review.
- No branch was deleted.
- No GitHub Actions result was treated as passing.
- The table is a proposal and certification record, not an authorization to perform destructive operations.
