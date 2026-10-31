# v2.5.0 validation

Date: 2026-10-31. Baseline: published v2.4.0 source and follow-up publication record (`f19b45f`; upstream catalog additions through `2eff4a2` retained). Adds learner-started review, evidence-based recaps, private self-reports/preferences, one-way Anki CSV and confirmed proposals for separate future courses. No new quiz/review timers, reminders, proactive quiz chats or weekly tasks.

## Behavior and boundaries

Tests cover delivered-versus-observed study, wrong/assisted/independent/pending/disputed outcomes, current corrections, retired quiz versions, time-budget modes, explicit consent, isolated one-question review with normal original-quiz continuation, hint/pause/resume behavior, request idempotency, exact raw evidence, annotations and exclusion, answer deletion, timezone-based windows, source integrity, symlink/overwrite protection, stable literal CSV with source notes, immutable proposals, stale evidence rejection, selected material snapshot continuity and separate awaiting-approval archives. Original config, plan, delivery state, manifests, receipts and schedules remain unchanged throughout the review/proposal workflow.

Initial baseline: 193 tests passed in 72.228 seconds. The first 27 new cases failed because the feature modules were absent; shared fixtures were then separated to avoid duplicate inherited cases. An additional regression reproduced a withdrawn question becoming trusted again after a later retake; unresolved disputes now stay excluded for that frozen question. Full integrated suite: **216 tests passed in 64.107 seconds** before independent review.

## Evidence limits

Review intervals use an explicit 1/3/doubling-to-30-day heuristic, not an optimal memory model or a learning-efficacy measurement. Time budgets are estimates per plan, not a stopwatch or accumulated daily ledger; host instructions require accounting for actual session time and exposing conflicts with existing lesson duration. Source hashes prove identity and integrity, not semantic correctness. Actual source relevance, feedback quality and real learner consent require agent/user judgment. Reading without answering remains unobserved, not failed learning.

Anki output is UTF-8 CSV with official text-import headers, literal fields, sources and first-field stable version identity. Structural and escaping checks do not prove native Anki application import or synchronization; no two-way synchronization is provided. Review deletion preserves raw assessments unless separately requested; answer deletion removes inferred judgments, while exported files and separate future course copies remain independent.

No fresh cloud-account writes or scheduled learning jobs were needed for these local workflow additions. Existing cloud transports retain their earlier release acceptance. Ten README languages describe user benefits; English remains the default. Unrelated local research files are excluded.

## Package and release checks

Skill Creator validation and isolated ZIP syntax/version/doctor/provider/checksum validation passed. All 61 ZIP entries matched source at the first package validation. Extracted CLI exercised actual lesson-bound quiz preparation, answer persistence and grading, a budgeted review, original-quiz resumption, recap, raw-evidence lookup, exclusion, two Anki cards and assessment-based future-course proposal/application. The resulting course was awaiting approval with no delivered lessons or schedule. Original course artifacts and all eight previous ZIPs were byte-identical.

The workflow uses synthetic QA material and simulated plan approval in sample_mode. It is structural behavior validation, not evidence of teaching quality, native Anki UI acceptance or a real learner's progress. One independent read-only reviewer reproduced two Important issues: a revised answer could hide an unresolved historical dispute, and a paused open-answer review awaiting feedback could not resume. Both were reproduced with failing regressions and fixed. Effective judgments now include unresolved grades for prior answers; active review continuation precedes the pending-feedback check for new attempts. A further regression prevents using the revised response to hide disputed evidence in a course proposal. Same-answer resolved grading remains usable. Additional tests verify the course timezone boundary and heavy-task exclusion.

After the runtime fixes, the whole suite passed 220 tests in 73.020 seconds. Two additional edge-case tests were then added; final whole-suite result: **222/222 tests passed in 70.479 seconds**.

The upstream flat catalog fields and marketplace manifest were preserved and versioned together. Skill Creator's strict validator rejects those six existing catalog extension keys; its core contract passed on a normalized temporary copy, and the catalog shapes/version consistency were checked separately. This is not a claim that the strict validator accepts the unmodified catalog-extended file.

Final package: `omni-learning-anything-skill-v2.5.0.zip`, 158288 bytes; SHA256 `605f5bf34bc58941998a836bd4538478fb31dd541a364cbd8147399701713e82`. All 61 entries match source. The extracted final workflow again passed and all 8 older ZIPs remain unchanged.
