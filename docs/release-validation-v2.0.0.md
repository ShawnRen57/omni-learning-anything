# v2.0.0 implementation and validation

Development started 2026-10-14 and validation continued 2026-10-15 (Asia/Shanghai). Base: `e82f3e8`; development branch: `feat/cloud-documents-v2`. The skill metadata and CLI report **2.0.0**. This record separates working implementation/local validation from uncompleted cloud-account acceptance. The original validation preceded publication.

## Publication update — 2026-10-18

The user authorized publication. Code was fast-forwarded to `main`; annotated tag `v2.0.0` resolves to `d2966dd2ec7a4a0d2a2948a42771a8c8c41ba367`. The [v2.0.0 GitHub Release](https://github.com/ShawnRen57/omni-learning-anything/releases/tag/v2.0.0) is published with the skill ZIP and `SHA256SUMS`. Both assets were downloaded from the release and matched the local files byte for byte. ZIP SHA256: `4de70072c0193d756707fe72b017a2d48e0d9ebc997b297e3981f87acb99c3a9`.

Before publication, all 77 automated tests passed again, as did the isolated ZIP validation. Publication does not change the real-account acceptance limits described below.

## Implemented

- Focused multi-round intake for platform, location and only the selected route's missing authorization; reuse confirmed preferences and existing writable connectors.
- Independent Markdown and embedded-image DOCX; retained PDF and combined PDF/DOCX exports. No PDF imports in Markdown generation or doctor.
- Direct Notion, Obsidian Vault, Feishu, Tencent Docs and official DingTalk dws routes; host/verified-import routes for the same platforms and generic DOCX/Markdown-compatible services.
- Separate stable destination receipts with saved task/document identifiers; incomplete/ambiguous delivery cannot advance lessons or blindly create a second document.
- Compatibility with unchanged historical PDF courses, approved settings, daily limits, pause and immutable delivered manifests/receipts.
- Selected-format dependency setup, provider-specific references, version reporting and runtime-resource allowlisting in the ZIP.

## Automated results

The final library/CLI suite passed **77 tests, 0 failures**. Commands:

```sh
python -m unittest discover -s tests -v
python tools/validate_artifacts.py
python tools/validate_release_samples.py
python tools/package_skill.py
python tools/validate_v2.py
python -m compileall -q skills/omni-learning-anything/scripts tools/validate_v2.py
python /path/to/skill-creator/scripts/quick_validate.py skills/omni-learning-anything
git diff --check
```

The tests cover real PDF compile/failure recovery, Unicode/figure/hyperlink preservation, independent document imports, course lifecycle, missing configuration, incorrect receipt bindings, pending and ambiguous writes, saved-task retries, Vault collisions/symlink escapes, malformed successful API responses, package credential exclusion and an isolated extracted-package CLI check.

Historical validation passed read-only: six original example curricula contain **24 PDFs / 55 pages**; the v1.0.0 bilingual acceptance archive contains **6 PDFs / 20 pages**. Their source dates, configs and manifests were not reset or relabeled as fresh v2 research.

## Independent review and fixes

A separate read-only reviewer assessed `e82f3e8..9e10b3d` and found four Important issues, with no Critical findings. Each was reproduced and corrected with regression tests:

1. Empty/null task/page IDs in successful responses could allow duplicate creates. Validate identifiers before leaving `creating`; malformed success now requires reconciliation. Fixtures cover null, empty and whitespace IDs for all three API create routes.
2. Tencent readback incorrectly compared raw relationship XML to URLs containing `&`. Parse relationship targets to handle XML escaping.
3. Equivalent compact/canonical Notion parent UUIDs were rejected. Normalize for comparison without changing approved configuration.
4. Combined PDF/cloud export omitted figure/input metadata. Include canonical input and figure path so cloud publication can use the same reviewed artifact set.

Additional visual QA found an unavailable CJK font alias and a bundled LibreOffice font-discovery issue. The writer selects actual available font families and removes inherited title rules. A temporary read-only host-font configuration resolved preview rendering without modifying system or runtime settings. [Upstream context](https://github.com/openai/codex/issues/32968) matches the locally reproduced issue; the local probe, not the issue report alone, verified the fix.

## Rendered documents and local Vault

Synthetic QA courses were generated under ignored `tmp/v2-qa/`. Simulated plan approval and accelerated execution are explicit; these are storage/format fixtures, not source-grounded learning examples. No real schedule was registered. Figure is a code-drawn QA diagram, not an AI illustration or research evidence; `example.com` links are synthetic hyperlink fixtures.

Chinese-mode and English-mode plans and Day01 documents were rendered through bundled LibreOffice and every resulting page inspected (four main DOCX pages, plus the independent Vault-course plan page). Chinese and English text, reading/practice labels, figure, credit, self-check and all five links are present, with no clipping or inherited title rule. DOCX relationship checks preserve links and embedded image; Markdown retains the same content and resolves copied assets. All synthetic local-course Day01 workflows completed only after reviewed, verified file publication.

The actual currently configured Obsidian Vault received a separate **Omni v2 QA** course subfolder containing `plan.md`, `Day01.md` and a content-hashed figure. Actual filesystem publication/readback and repeated publication passed. Existing notes and `.obsidian` settings were not changed. Native Obsidian display and cross-device sync have **not** been verified.

## Platform validation scope

| Platform | Verified in this run | Not yet verified |
| --- | --- | --- |
| PDF | Real XeLaTeX compile, multilingual text/image/link checks and recovery | No new live learner course |
| Markdown/DOCX | Actual independent exports, bilingual visual inspection and lifecycle | Rendering in every third-party client |
| Obsidian | Real selected-Vault file/asset writes, byte readback, collision protection and idempotent repeat | Native client display after lock; sync completion |
| Notion | Official-contract fixtures: Markdown page, media upload/attachment, UUIDs, content readback, uncertain-write recovery | Real API credentials or successful account UI import |
| Feishu | Official-contract fixtures: DOCX upload/import ticket, pending resume and block/text/image/link readback; native client was observed logged in | Actual API/UI document creation and learner access |
| Tencent Docs | Official-contract fixtures: pre-import, COS route selection, async conversion, export readback, query URL escaping | Actual OAuth/COS upload and native account import |
| DingTalk | CLI contract fixtures: conversion detection and Markdown/image readback | Installed/authorized dws and real document creation |
| Generic services | Document export and verified-host/import workflow | Native APIs or account acceptance on unnamed platforms |

The user authorized local/account testing. App/UI access initially recovered, then the Mac locked and the tool reported that automatic unlock failed. The user was asked once to unlock. No unlock response or selected cloud destination/private credential references arrived before packaging, and available plugin discovery found Notion installable but not connected. No secrets were searched for in browser/app private storage and no new integrations/scopes were granted. Cloud contracts therefore are **not** labeled real-account passes.

## Package and handoff

`dist/omni-learning-anything-skill-v2.0.0.zip` is a lightweight self-contained skill bundle; `dist/SHA256SUMS` records its current digest. Isolation checks extract the ZIP, compile scripts, run packaged `--version`/`doctor` and verify provider references. Packaging excludes private config, hidden files, credential JSON, test/course artifacts and symlinks. The ZIP test intentionally planted private sentinel files and confirmed their absence.

Code and bundle were retained on the local development branch at the original validation handoff; the later authorized publication is recorded above. The user can resume real cloud-account acceptance after unlocking and selecting authorized QA locations, without repeating completed development. Remaining runtime limits include permission/credential expiry, remote Markdown normalization, viewer fonts, provider API/CLI changes and interactive import availability; failures retain the same lesson and existing remote identifiers.
