# Core Flow Ship Gate

Date: 2026-08-10
Source task: https://app.asana.com/1/15960956269365/project/1217010827283807/task/1217207674221772
Task: CORE FLOW SHIP GATE - Complete the remaining release-candidate feature set

## Live task state

- Asana task: incomplete, upcoming, no due date, no assignee.
- The task is in `Pelvic Health Application` and `411`.
- The task notes require an openable release candidate, a complete user path, observable guidance behavior, and recorded failures.
- The task notes explicitly reserve shipping or public release for Mo's approval.

This document is a development-ready acceptance contract. It does not claim that the product is implemented, tested, or approved for release.

## Release packages

### 1. Interaction loop

Acceptance evidence:

- A fresh release-candidate build opens from a clean start.
- The primary user path is executable from entry through completion without a dead end.
- Every interactive state has a visible state change or a recorded failure.
- Completion feedback is observable and occurs once for a completed path.
- A reset or restart path is defined and verified so a second run does not inherit stale state.

Required receipt fields:

- Build identifier and environment.
- Start state and end state.
- Ordered interaction trace.
- Completion evidence.
- Failure ID, reproduction step, and severity for each failed path.

### 2. Guidance and progression

Acceptance evidence:

- Vibration timing is defined in the product contract and observable during the relevant interaction.
- Vibration-disabled behavior is defined and does not make the path unusable.
- Optional voice or tone behavior is separately switchable and does not block the core flow.
- Progress-screen behavior is verified for initial, in-progress, complete, and reset states.
- Training logic has explicit input, transition, and output examples, including a boundary case.

Required receipt fields:

- Guidance event name and expected timing.
- Observed timing or instrumentation result.
- Device or emulator capability state.
- Voice/tone setting and result.
- Progress and training state before and after each tested transition.

### 3. Ship readiness

Acceptance evidence:

- End-to-end verification covers a clean open, the complete path, guidance, progression, completion, and restart.
- The failure register is attached and distinguishes fixed, known, and release-blocking failures.
- A development-ready MVP specification names the supported path, exclusions, interfaces, and evidence requirements.
- No release or public announcement occurs until Mo supplies explicit approval.

## Minimum verification matrix

| Case | Expected result | Evidence |
|---|---|---|
| Clean open | Release candidate opens at the defined entry state | Build/open receipt |
| Primary path | User reaches completion without an unhandled state | Interaction trace |
| Guidance on | Timing and feedback are observable | Guidance receipt |
| Guidance unavailable | Core path remains usable | Capability-state receipt |
| Optional voice/tone on | Behavior is present without changing core completion | Setting/result receipt |
| Progress start | Initial progress is correct | State snapshot |
| Progress in progress | Progress reflects the defined transition | State snapshot |
| Progress complete | Completion state is stable and visible | Completion receipt |
| Reset/restart | New run begins without stale state | Two-run trace |
| Failure path | Failure is recorded with a stable ID | Failure register |

## Ship decision

Current decision: **NOT SHIP-CERTIFIED**.

Reason: the live task is incomplete, no implementation or fresh end-to-end receipt was supplied by the current task surface, and the task itself requires Mo's explicit approval before shipping. This is a clear gate, not a blocker to preparing the spec.
