# Assessment schema and agent commands

`OMNI` means the installed `python .../scripts/omni_learning.py --project /absolute/course`. These are agent operations. Data stays under course/learning, never the installed bundle. No quiz command schedules jobs, sends notifications or changes delivery state.

## Definition

```json
{
  "schema_version": 2, "key": "Day01", "revision": 1, "estimated_minutes": 2,
  "questions": [{
    "id": "q1", "kind": "choice",
    "prompt": "A rectangular garden is 9 m long and 4 m wide. A student says it needs 13 m of fencing all the way around. Which length is correct?",
    "objective": "Apply the rectangle perimeter rule to a new situation",
    "response_hint": "Choose one length.",
    "actions": ["select"],
    "source_refs": [{
      "source_id": "S1", "section_index": 0,
      "quote": "A full perimeter includes two lengths and two widths.",
      "original_quote": "The perimeter of a rectangle is the sum of its four sides.",
      "locator": "Perimeter section"
    }],
    "review": {
      "mode": "error_analysis",
      "scope": "The garden and dimensions are supplied examples. The only rule needed is summing the four sides [S1].",
      "solution": "The sides are 9, 4, 9 and 4 m. Their sum is 26 m.",
      "answer_check": "13 m covers only two sides. 26 m covers all four sides and is the only correct option."
    },
    "hints": ["Trace the four sides before adding."],
    "explanation": "Add both lengths and both widths to get 26 m [S1].",
    "options": [
      {"id":"half","text":"13 m","feedback":"That adds one length and one width."},
      {"id":"full","text":"26 m","feedback":"That includes all four sides."}
    ], "answer_id":"full"
  }]
}
```

Replace illustrative text with actual authored content. Use 1–3 questions per round. Default estimated time is 1–5 minutes. `kind` is `choice`, `short` or `open`; short/open replace `options` and `answer_id` with `expected_answer` text and `rubric:[{"id":"criterion1","description":"Observable required point"}]`. Empty hints are valid. Question/option/criterion IDs are stable, letter-led and use letters/digits/underscore/hyphen/dot. Choice options have unique normalized text and IDs; answer_id is an option ID, never a displayed letter.

Light actions: `select`, `brief_text`, `conversation`. Heavy actions: `long_writing`, `operate_device`, `write_code`, `experiment`, `project`. Heavy/longer checks require the top-level nonempty `practice_request` quoting the learner's actual explicit practical-training request. This is a recorded host attestation, not automatic permission verification. Accurate semantic effort classification is required.

Each source anchor names a reviewed lesson source, a zero-based section index and a verbatim lesson quote from that section alongside its citation. Add a short `original_quote` from the inspected original and its `locator` (section, page, chapter, slide or timestamp). When the lesson cites selected materials, each question anchor must use one of those sources, with the excerpt inside its exact cited unit and the locator returned by the material reader. The excerpt may expand on the lesson's citation within that unit, provided it supports the same taught outcome. With a web/course source, the host checks the original excerpt and location.

`review.mode` is `application`, `error_analysis`, `original` or `recall`. For `original`, quote enough original text to contain the exact prompt. For application and error analysis, use a genuinely new stem. `scope`, `solution` and `answer_check` summarize the checks performed before freezing. They are private. The tool validates bindings and the structure of the review. Correctness, fit, ambiguity, answer cues and the reasoning in the review require host judgment.

The frozen definition binds config, plan, reviewed manifest and lesson input hashes. `prepare` may precede publication. `start` requires verified lesson delivery. Identical preparation is idempotent and changes require a higher revision. Previously frozen legacy definitions still open and resume. Newly prepared revisions require `schema_version: 2`. Source/config changes block assessment actions, preserving old records for export/recovery.

## Commands

```sh
OMNI quiz prepare --input /private/Day01-quiz.json
# Only on the learner's actual request; --extra-time only after disclosed extra-time consent:
OMNI quiz start --key Day01 --request-id user-message-1 --consent 'Finished reading; test me'
OMNI quiz next --attempt ACTUAL_ATTEMPT_ID
OMNI quiz answer --attempt ACTUAL_ATTEMPT_ID --question q1 --event-id user-message-2 --input /private/answer.json
OMNI quiz hint --attempt ACTUAL_ATTEMPT_ID --question q1 --event-id hint-request
OMNI quiz reveal --attempt ACTUAL_ATTEMPT_ID --question q1 --event-id solution-request
OMNI quiz skip --attempt ACTUAL_ATTEMPT_ID --question q1 --event-id skip-request
OMNI quiz pause --attempt ACTUAL_ATTEMPT_ID --event-id later-request
# Resume through start with a new actual request ID; it keeps the active attempt.
OMNI quiz status
OMNI quiz export --output /private/my-answers.json --format json
OMNI quiz export --output /private/my-answers.csv --format csv
# Only when the learner explicitly requests removal:
OMNI quiz forget --confirm --scope attempts
```

Answers: `{"choice_id":"evidence"}` or `{"text":"A"}` for choice, `{"text":"My original response"}` for text/dialogue. Full-width letters and exact normalized option text are supported. Prefer canonical IDs for card submissions. Do not infer an ambiguous free-form selection; ask. Keep original explanation in `text` alongside choice_id if supplied. A further explicit answer after grading uses `quiz answer ... --revise`; earlier text remains. A finished retake uses `quiz start ... --new-attempt` and a new stable request ID.

For short/open pending answers, the host receives private grading context and writes:

```json
{
 "criteria":[{"id":"criterion1","result":"met","note":"Explain the correspondence to the actual answer."}],
 "strengths":["An observed strength"], "gaps":[],
 "explanation":"Grounded feedback [S1]", "source_ids":["S1"],
 "next_step":"One small review or follow-up suggestion"
}
```

```sh
OMNI quiz feedback --attempt ACTUAL_ATTEMPT_ID --question q1 --event-id grade-event --answer-id ACTUAL_LATEST_ANSWER_ID --input /private/feedback.json
OMNI quiz correct --attempt ACTUAL_ATTEMPT_ID --question q1 --event-id correction-event --replaces ACTUAL_LATEST_GRADE_ID --reason-file /private/dispute.txt --input /private/corrected-feedback.json
```

Every frozen criterion is covered once: `met`, `partly_met`, `not_met` or `uncertain`. Verdict derives from those judgments: all met → correct; all not_met → incorrect; any uncertain → needs_review; otherwise partial. Strengths/gaps may be empty; source_ids must reference the question's anchors. No `score` field. A choice correction instead supplies `verdict: "withdrawn"` or `"needs_review"` and the same explanation/strengths/gaps/source_ids/next_step fields, without criteria. A choice's original automatic grade ID is its answer event ID.

Use stable IDs on retry; conflicting reuse is rejected. Missing/failed feedback never discards a raw answer. Pause and skip produce no failure grade. `next` returns only the current public question before response; private grading context appears only after an actual answer. Do not copy private tool output wholesale into a learner card.
