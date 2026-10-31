# v2.2.1 validation

Date: 2026-10-31. Scope: local v2.2.1 release candidate, guided interpretation of vague study requests, selected-route readiness, private onboarding observations and first-use recovery instructions. This record distinguishes automated checks, model-based behavioral observations and real account access. It does not certify new remote publication or unattended learning delivery.

## Runtime and compatibility

- The unchanged v2.2.0 baseline passed **134/134** tests in 53.627 seconds before runtime edits.
- The initial updated suite passed **147/147** tests in 53.127 seconds. Independent review then identified two material issues: background attestations lacked binding to the registered host/job, and Tencent MCP needed the shared `requests` dependency. Both received failing regression coverage and fixes before final validation.
- New brief tests cover preserving study wording, proposed assumptions, concise requests, malformed fields, optional config compatibility, and existing hash protection after approval.
- New readiness tests cover route-specific requirements, stale/future/wrong-course evidence, expected host/context/config/job matching, active approved non-sample background requirements, missing evidence, cloud credential-context attestations and Tencent MCP dependencies.
- New onboarding tests cover restart/idempotency, conflicting event IDs, authorization waiting, invalid/secret-bearing usage fields, finite real metering, unknown total cost, private atomic storage, symlink escape and approval/config preservation. No outbound telemetry exists.
- CLI dependency errors now return structured selected-dependency guidance rather than a traceback for known missing optional packages. Existing cloud delivery adapters, receipt/daily-limit rules and legacy course records remain in use.

## Independent behavior check

An independent agent reviewed the updated Skill and exercised three text-only intake requests: vague economics with a request for few questions, a concise specific SQL JOIN course, and ambiguous “Agent”. It produced a bounded route with proposals, a focused three-day route preserving settings, and a targeted ambiguity question respectively. Details and limitations: [intake behavior observations](validation/v2.2.1-intake-behavior.md).

This was not an external user test, blinded teaching-quality comparison or learning-effectiveness study. Schema acceptance does not establish semantic understanding, source quality or consent.

## Real account access

Using the previously approved named metadata connections and cached official tools, read-only account/destination checks completed on this Mac:

| Platform | Route | 2026-10-31 result |
| --- | --- | --- |
| Notion | Official `ntn` | Existing account/location check passed. |
| Feishu | Official `lark-cli` | Existing account/location check passed. |
| DingTalk | Official `dws` | Existing account/location check passed. |
| Tencent Docs | Official OAuth/MCP | Existing account/location check passed after providing the documented Python dependencies in a task-local environment. |

No passwords/tokens were printed, copied into course files or added to the package. These were **read-only reconnect checks**: no new write permission or document creation is inferred. Historical real-account plan/Day01 acceptance remains documented in [v2.1.0](release-validation-v2.1.0.md) and [v2.2.0](release-validation-v2.2.0.md), with their original scopes/dates. Obsidian's existing local publisher regression checks remain applicable; no new native-client visual acceptance is claimed here.

## Package and first-use workflow

The extracted v2.2.1 ZIP was exercised in an isolated temporary installation: standalone brief check, HTML staging-config doctor before initialization, private onboarding events, initialization preserving those events, HTML rendering, restart/status and idempotent event reuse. Course state remained `awaiting_approval`; no fabricated review, usable-plan milestone, publish or schedule was recorded. The rendered fixture is synthetic transport/state QA, not source-researched teaching content.

After the review fixes, the final whole suite passed **149/149** tests in **45.984 seconds**. Skill Creator validation and isolated ZIP extraction/runtime/CLI/provider/checksum validation passed. All **43 ZIP entries** match the final Skill source bytes. The final extracted ZIP also passed the actual CLI sequence for pre-init staging checks, brief validation, private event recording, `init`, HTML rendering and idempotent restart, with approval still pending.

Five previous release ZIPs were hashed before this work and remain byte-identical. All ten README variants' current badges/version rows and local navigation targets, plus Skill reference links, were checked. English remains the default README.

Package: `dist/omni-learning-anything-skill-v2.2.1.zip` (105,721 bytes).

SHA256: `11e2f694c6e22c40866678b10980724370b023d2b52eb80337091a7f113b9326`.

## Deliberately unclaimed acceptance

No real new-course activation cohort, expired-login account experiment, fresh four-platform write/readback/visual cycle or live background job was run in this upgrade. There is no new learner-approved non-sample course/schedule on which to establish those results. Foreground reconnects and synthetic host evidence do not establish unattended keychain access. The helper reports attestations and unknowns explicitly; it never schedules or approves a course. Validate the actual chosen host/job after real course approval, and record each future cloud delivery through normal publication/readback/inspection.

No claim is made that vague-goal generation measurably improves learning, or that a seven-day retention target is already met. Those remain real-user evaluation work from the roadmap.
