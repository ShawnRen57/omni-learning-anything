# v2.0.1 real-account acceptance

Date: 2026-10-18, Asia/Shanghai. Continues the [v2.0.0 implementation validation](release-validation-v2.0.0.md). The user authorized testing with local accounts and later requested stopping unfinished platform tests and publishing completed results. No live learning schedule was created. The published v2.0.0 tag/assets remain unchanged.

## Account results

| Platform / route | Actual result | Remaining limit |
| --- | --- | --- |
| Notion native Word import | **Passed** for a plan and Day01 in a private QA parent: editable pages, bilingual body, practice/self-check, diagram/caption/credit, all five exact source URL destinations, correct parent, reopen and receipt reuse | Direct API still contract-tested only; no unattended scheduling claim |
| Obsidian local Vault + native app | **Passed**: previously delivered plan/Day01 reopened in the selected Vault; full reading views, Chinese/English body/practice, diagram/credit and five hyperlink fixtures per note inspected | No cross-device or cloud-sync acceptance |
| Feishu native Word-to-online import | Private personal QA folder created; upload failed at 0B, and one retry of the existing task also failed; folder remained empty | No editable document or verified delivery receipt; API remains contract-tested only |
| Tencent Docs | Dedicated in-app browser creation timed out | Account import/API acceptance not completed; user stopped further testing |
| DingTalk official dws v1.0.64 | Device OAuth, organization CLI-access enforcement, successful login, personal document-space discovery and isolated folder creation tested | DOCX import failed at OSS upload; folder readback empty. No converted document or content pass |

These are route-specific findings. A desktop login or an API/CLI fixture pass is not an account delivery pass. Incomplete routes remain supported implementations awaiting account acceptance; they are not advertised as fully account-verified.

## Notion evidence and lifecycle

Used the generated embedded-image DOCX through the native Word importer with the private QA parent explicitly selected. Both imports reported completion, then their actual pages were opened. The importer used the filename as the page title and omitted the Word title; pages were renamed to readable QA titles, including a Chinese lesson title.

Inspected the full bilingual body, lesson practice/answer, actual visible three-stage diagram, caption/credit, and all source sections. Each of the five URLs on each page was read from Notion's native link editor and matched the source fixture. Navigated back to the private parent, verified that both child links were present, and reopened each child to check persistence. Copied each actual page URL and retained the observed ID in ignored local evidence.

`receipt-record` bound the observed pages and actual inspection evidence to each reviewed manifest and configured destination. Repeated `publish` returned the same verified document IDs without invoking another import. Day01 advanced only after its verified receipt and completed the isolated one-day sample. Approval was explicitly simulated for QA; no real scheduler was registered.

## Local document and Obsidian evidence

The account sample contains synthetic Chinese/English text and a code-drawn Plan → Lesson → Verify diagram. It is a delivery fixture, not an AI-image or researched learner-course claim. Five official documentation URLs were opened on the test date and used to test hyperlink preservation.

The plan DOCX rendered to two pages and Day01 to one page. Every page was visually inspected with readable CJK/English text, figure/credit and links, without clipping. Notion and DingTalk DOCX exports were compared by every decompressed ZIP entry against these inspected files. Equivalent archive bytes do not establish cloud conversion success.

Obsidian acceptance reopened the existing v2.0.0 QA notes rather than overwriting them. Both notes were inspected from top to bottom in native reading mode. All five `example.com/1` through `/5` hyperlink targets were exposed in the rendered accessibility tree. Those older links are synthetic URL-preservation fixtures, not validated research references. This complements the prior actual Vault file/asset byte readback, collision protection and idempotent repeat checks.

## Diagnosed failures and fixes

- **Notion import artifact:** the old default offered loose Markdown even when an embedded DOCX had been explicitly generated. New `notion/import` courses now render DOCX + Markdown and select DOCX for import. Existing reviewed Markdown-only archives remain resumable; their linked image still needs actual import/inspection. Provider guidance now covers explicit parent selection, filename-derived titles, reopen and exact URL checks.
- **DingTalk poll timeout:** official v1.0.64 import includes up to roughly five minutes of conversion polling. A 60-second subprocess timeout could terminate it before its recoverable task result. Initial import now permits 600 seconds including upload; ordinary queries/reads keep 60 seconds. Structured `success=false`, `timed_out=true`, `status=processing` with a task ID is preserved as pending.
- **DingTalk destination recovery:** resume now includes the original folder/workspace. A `verified=false` placement result retains the document/task and cannot become delivered, including on repeat publication; subsequent attempts query the same saved task instead of creating again. These changes are contract regression-tested, not claimed as a successful real import.
- **Authorization vs upload connectivity:** DingTalk OAuth first succeeded but organization CLI access was denied. After the user saved the organization/member setting and reauthorized, login succeeded. Actual import then failed on the separate OSS upload host. Read-only connectivity probes observed proxy TLS EOF and direct timeout; no system proxy/security settings were changed. Feishu's upload failure had no detailed UI cause, so it is not attributed to that same root cause.

The [official v1.0.64 import implementation](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/blob/v1.0.64/internal/helpers/import_flow.go) and installed leaf-command help were inspected for the DingTalk recovery contract. Raw upload errors can contain signed storage URLs; those errors, credentials, account/organization identifiers and native screenshots of private sidebars are excluded from the repository/release.

## Verification and package

- Full suite: **82 tests passed, 0 failures**. New recovery/default-import regressions were observed failing before fixes, then passing. Existing lifecycle, API fixtures, real PDF compilation, Vault safety and private-file package checks remain covered.
- Skill frontmatter/reference validation, script compilation, whitespace checks and isolated ZIP runtime/doctor/provider-resource/SHA256 validation are run before publication.
- Public package contains the Skill/runtime/references only. Private account evidence stays under ignored local QA staging; no test courses, auth files or private account screenshots are included.

Commands:

```sh
python -m unittest discover -s tests -v
python /path/to/skill-creator/scripts/quick_validate.py skills/omni-learning-anything
python tools/package_skill.py
python tools/validate_v2.py
python -m compileall -q skills/omni-learning-anything/scripts tools/validate_v2.py
git diff --check
```

The release ZIP is `dist/omni-learning-anything-skill-v2.0.1.zip`; `dist/SHA256SUMS` records its checksum. Publication must verify the remote commit/tag and download the release assets for byte/digest comparison. This report does not turn unfinished account routes into passes.
