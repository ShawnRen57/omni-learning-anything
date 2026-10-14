# Omni Learning Anything implementation plan

> Execution: implement and verify in this session, following the user-approved eight-part scope. The user approved execution on 2026-10-08; do not add another design approval gate.

Goal: portable Agent Skills package, source-grounded learning PDFs, persistent course progress, six four-document examples, bilingual documentation and GitHub release.
Architecture: agent-owned research and teaching; Python-owned rendering and state; host-owned scheduling and notification. Keep the distributable skill self-contained under skills/omni-learning-anything.
Stack: Python 3.10+, XeLaTeX, pypdf, pypdfium2, Pillow. No cloud API credentials required by the package itself.

## Scope and acceptance
- Ask for topic, objective/baseline, duration, daily minutes, execution time/timezone/weekdays, language/output directory. Defaults are proposals, not user facts.
- Render plan first, obtain explicit approval of its current hash, then create a host schedule. Never create schedules during sample batch runs.
- Each document: XeLaTeX PDF, explanatory figure, >=5 unique expansion links, inline evidence, Chinese FangSong/English Times New Roman with detected fallbacks.
- Each course: earliest undelivered day, no advance on failure, immutable accepted plan unless reapproved, separate render/review/delivery states, repeat-safe handling, completion stops future work.
- Six samples: technology, economics, music, Agent product, Western architecture, Ming history; 30-day plans and days 1-3; 24 PDFs with source data and previews.
- Validation covers the Skill workflow, state and document output; host scheduling reliability is outside the test scope.

## Tasks
- [x] 1. Core skill and reference contracts: SKILL.md, content.md, platforms.md; check trigger and approval flow.
- [x] 2. Python CLI: doctor, init, approve, next, render, review, delivered, pause/resume, schedule record; unittest state and validation including concurrent access, changed plan and notification retry.
- [x] 3. Portable XeLaTeX rendering: fonts, escaping, links, source files, page extraction/render; compile multilingual and adversarial text fixtures.
- [x] 4. Research and author six full sample courses; open sources, create explanatory images, preserve evidence and original prompts.
- [x] 5. Render 24 PDFs, inspect every page, publish screenshots, validate link/font counts and course alignment.
- [x] 6. Independent fresh-context behavioral review; fix material issues and rerun relevant checks.
- [x] 7. Bilingual README, license, changelog, package zip and install smoke check. GitHub publication tracked separately below.

## Review focus
Unsafe TeX/paths; stale approved plan; duplicate concurrent runs; delivering unreviewed or changed PDF; schedule capability overstated.

## Decisions
The skill identifier is omni-learning-anything.
Sample runs simulate plan approval and consecutive delivery in an isolated sample mode; they do not prove real timed delivery or learner mastery.

## Publication
- [x] Public repository created under ShawnRen57/omni-learning-anything.
- [x] Upload all deliverables and verify remote files. All 279 Git blob hashes matched on 2026-10-09.
