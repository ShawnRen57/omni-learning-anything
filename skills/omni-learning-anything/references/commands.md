# Data and command contract

Use a dedicated writable course folder. Resolve the installed script path from this skill's directory; never copy a developer's absolute path. Commands below use `python /path/to/omni-learning-anything/scripts/omni_learning.py --project /path/to/course` as `OMNI` for readability (not a shell alias).

## Files

`config.json`: topic, goal, baseline, daily_minutes (positive integer), timezone (IANA), time (HH:MM, 00:00–23:59), weekdays (nonempty list using `MO`, `TU`, `WE`, `TH`, `FR`, `SA`, `SU`), language (`zh` or `en`), immediate_day01 (bool), sample_mode (false in real courses). Keep learner data in the course folder, not in the installed package.

`plan.json`: topic, title, days (ordered objects: day integer, topic, objective), sections (ordered title/body strings), sources, figure. The PDF must visibly include the full curriculum and schedule; put these into sections, not only the days array.

`data/Day01.json`: day integer, title exactly matching approved day topic, reading_minutes, practice_minutes, sections, sources, figure.

Source: `{"id":"S1","title":"Specific page","url":"https://…","publisher":"Institution","published_at":"2026-01-01 or 未标注","checked_at":"YYYY-MM-DD","note":"What to read and why"}`. Minimum five distinct URLs, actually opened. Key facts use [S1] in section body. Section bodies are plain text, blank lines for paragraphs, no Markdown headings/LaTeX.

Figure: `{"path":"assets/teaching.png","caption":"What the reader should notice","credit":"Source and reuse rights, or AI-generated teaching illustration; not evidence"}`. Relative path inside course. PNG/JPEG preferred. Keep generated image prompt in course sources or run report.

## Lifecycle

1. Write intake files in a temporary staging directory, keeping original inputs. `OMNI init --config /staging/config.json --plan /staging/plan.json` creates canonical files without overwriting existing projects. Copy teaching image under course/assets.
2. `OMNI render --input /course/plan.json --key plan` creates PDF, Markdown, LaTeX, previews, manifest and font/link report. Inspect every page.
3. `OMNI review --key plan --note "Observed all pages: ..."` records the inspection. It is an agent attestation, not automatic visual verification.
4. Send the plan to the learner. Only after explicit approval: `OMNI approve`. Repeating approval preserves the current status; use `resume` to resume a paused course. Completed courses remain complete.
5. Create/verify a live schedule in the host, then `OMNI schedule-record --host codex --job-id ACTUAL_RETURNED_ID`. This command does not itself create a host task.
6. `OMNI next` selects earliest undelivered lesson, or returns existing material / paused / already_delivered_today / complete. Read its action, not just its day.
7. Research, write JSON, then `OMNI render --input /course/data/Day01.json --key Day01`. Inspect previews, then `OMNI review --key Day01 --note "..."`.
8. Deliver the PDF. Once delivery is confirmed: `OMNI delivered --day 1`. If delivery fails, rerun `next` to get the same artifact. Reconcile uncertain delivery with host history.
9. `OMNI pause` / `OMNI resume` modify local state. Also update the host schedule. On complete, pause/remove host schedule and report course completion; do not generate Day N+1.

Do not use `sample_mode` to bypass a real user's confirmation or daily limits. Rendered plans and their settings are hash-bound. To revise a rendered plan/settings, create a new course version and obtain approval; preserve the old project. Changing the curriculum after delivery requires a new course version. Source dates are checked against the configured timezone's actual generation date; historical examples must not have their dates relabeled as newly verified without new research.

## Recovery

A project lock prevents simultaneous mutations. If a crashed process leaves `.omni-learning-anything.lock`, verify that no Omni Learning Anything process is running, then remove only that empty lock directory. Never delete state to "fix" duplicate delivery.

A failed render leaves no accepted manifest. Correct input and retry that same day. To revise an unshipped existing manifest, move its current PDF/source/manifest into a dated revision subfolder first; then rerender. Delivered artifacts and their review manifests are immutable and checked before continuation or repeated delivery recording. Keep later errata in a separate file. If a source or file hash changed, investigate before accepting it.
