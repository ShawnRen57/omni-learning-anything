# v2.3.0 validation

Date: 2026-10-31. Baseline: published v2.2.1 at `32e268d`. This upgrade adds optional learner-started light checks; it creates no quiz timers, quiz reminders or scheduled quiz conversations. Existing lesson schedules remain separate.

## Runtime tests and review

Baseline: 149 tests passed in 59.625 seconds. Initial 19 assessment tests were observed failing because the runtime was absent; actual CLI coverage then failed before command implementation. After implementation the first complete suite passed 169 tests in 60.481 seconds.

Independent read-only review found two material defects: replaying a resume request could undo a subsequent pause, and a raw letter could ambiguously refer to an option label or literal option text. Both were reproduced as failing regressions, then fixed. Start/resume deduplication now binds the complete request payload; raw ambiguous selections require clarification/canonical IDs. The final focused assessment/CLI set passed 22 tests. Final whole-suite and package evidence is recorded below.

Covered behaviors: immutable source-bound revisions; approved/reviewed/delivered lesson requirements; no private keys/rubrics/hints in public pre-answer payloads; stable IDs and Unicode choice replies; persistence before model grading; stale/failed grading recovery; short follow-up answers; explicit response revision after feedback; hints/solutions/skip/pause/retake; source/rubric validation and uncertainty; append-only correction history; heavy-action declarations and explicit practical-request exceptions; extra-time consent; private guarded atomic storage; JSON/CSV export; confirmed assessment deletion; unchanged config/plan/delivery/receipts/schedules/mastery.

The host authors and judges meaning. Schema checks cannot prove that a prompt is semantically light or that an attested practical request genuinely came from the learner. Review actual prompts, source support and feedback; do not infer calibrated mastery or a numerical learning gain.

## Independent behavior observations

The reviewer exercised runtime plus documented host rendering in an isolated synthetic course:

- Explicit start returned one public choice question and controls. Skip then reveal ended with zero answers and zero independent correct responses, while recording skip/reveal separately.
- A retake, wrong choice and dispute produced a retained correction marked for review.
- Supplied-code reading with selection was accepted. Declared code writing without a practical request was rejected. An actual explicit writing/running training request permitted a declared practical check with time disclosure.

These are model-based/document-guided and synthetic runtime observations. No real learner effectiveness study or native-card UI was tested. Native cards remain conditional on an actual suitable host tool and explicit returned submission; normal conversation uses the same backend. No separate interactive HTML or website is required; offline HTML stays static.

## Account and scheduling scope

No new cloud API transport or account authorization is introduced. Historical account acceptance remains in the prior releases; this upgrade does not claim another real cloud write/readback/visual cycle. No live task was created and no unattended quiz/background learning was tested or advertised. A scheduled lesson job may prepare a check and deliver an invitation, then ends; only a real learner request starts an assessment.

## Release evidence

Final whole-suite result: **171/171 tests passed in 61.722 seconds**. Skill Creator validation and isolated ZIP runtime/provider/checksum validation passed. All **50 packaged entries** match the Skill source. The extracted ZIP completed actual CLI prepare/start/public question/hint/choice answer/open answer/pause/resume/feedback/JSON+CSV export/confirmed forget operations; course delivery state remained unchanged. This is synthetic transport/state QA, not source-researched teaching acceptance.

The six earlier release ZIPs remain byte-identical. Ten README badges/navigation/local targets were checked. Private learning records are excluded from packaging. README defaults to English with nine translated alternatives.

Package: `omni-learning-anything-skill-v2.3.0.zip`, 124,428 bytes. SHA256: `c1553b6716fcacdf6b319888eb7a707b67d4f44a837e8c4a0aeaa26f70ee75dc`. Remote publication was independently verified as recorded below.


## GitHub publication

Published 2026-10-31: [v2.3.0](https://github.com/ShawnRen57/omni-learning-anything/releases/tag/v2.3.0), latest stable release. The default branch and annotated tag resolved to `b6a2472b33542319768495f50e2401cb5ec76744` at publication. GitHub README and Skill metadata show v2.3.0. Both release assets were downloaded and compared byte-for-byte with the local ZIP and SHA256SUMS; both match. This publication record is a documentation-only follow-up; the tested tag and package remain unchanged.
