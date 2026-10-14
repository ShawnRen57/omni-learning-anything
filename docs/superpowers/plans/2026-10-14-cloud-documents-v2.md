# Cloud documents v2 Implementation Plan

> **For agentic workers:** Execute inline with superpowers:executing-plans; use a fresh reviewer for the final branch review. Steps use checkbox syntax for tracking.

**Goal:** Deliver approved learning plans and daily lessons to PDF, Markdown, DOCX, Notion, Obsidian, Feishu, Tencent Docs and DingTalk, with verified recoverable delivery and a v2.0.0 bundle.

**Architecture:** Share format-independent validation and artifact manifests. Export locally before publication; keep mutable destination receipts separate from immutable reviewed artifacts. Prefer installed host connectors, with deterministic official API/CLI adapters and truthful import fallback.

**Tech Stack:** Python 3.10+, unittest, python-docx, requests; existing XeLaTeX/PDF tools remain optional outside PDF mode.

**Spec:** ../specs/2026-10-14-cloud-documents-v2-design.md

## Global constraints and interfaces

- Existing configs without `delivery` retain the PDF workflow and historical manifest hashes.
- `delivery = {platform, mode, destination, credential_env}`; platforms are `pdf`, `markdown`, `docx`, `obsidian`, `notion`, `feishu`, `tencent`, `dingtalk`, `generic`. Modes are `local`, `api`, `cli`, `host`, `import`.
- `render(root, input_path, key, formats=None)` produces `{key, artifact, artifacts, files, reviewed_at, ...}`. All files are project-relative and hash-bound.
- `publish(root, key)` saves a per-key receipt before external writes. Receipt states: `prepared`, `creating`, `pending`, `needs_reconciliation`, `verified`, `awaiting_import`, `failed`. A receipt binds target configuration and manifest digest.
- `delivered` checks verified primary destination for configs with explicit delivery. Legacy PDF workflows keep their existing host-attestation contract.
- No raw credentials in config, errors, manifests, receipts, docs, test artifacts or ZIPs. No blind create retry after ambiguous write failures.
- Local and remote images must be embedded/copied/uploaded; no unresolved local image paths in cloud content.

## Task 1: Shared documents and exports

Files: create `scripts/omni_document.py`, `tests/test_documents.py`; modify `omni_pdf.py`, requirements.

- [ ] RED: tests generate Markdown/DOCX with PDF imports prohibited, preserve Chinese text/image/links, reject malformed input/time/key/paths, and protect reviewed archives.
- [ ] Run `python -m unittest discover -s tests -p test_documents.py -v`; expected missing document module/behavior failures.
- [ ] GREEN: move shared validation/preparation into `omni_document`; add independent Markdown/DOCX generation and local HTML preview. PDF delegates shared validation while keeping existing public functions.
- [ ] Check `Document(root / manifest['artifacts']['docx'])` and source hyperlink/image relationships; rerun focused and legacy tests, then commit.

## Task 2: Destination config, receipts and course progress

Files: create `scripts/omni_delivery.py`, `tests/test_delivery.py`; modify `omni_core.py`, CLI.

- [ ] RED: destination selection/preflight reports only relevant missing fields; reject secrets and unsafe paths; pending/import/ambiguous receipts cannot advance; verified delivery can advance and repeat safely; legacy course remains readable.
- [ ] Run focused delivery tests; expected absent module/receipt gate failures.
- [ ] GREEN: validate explicit destination config, choose default export formats, persist separate receipts under project lock, bind receipts to reviewed manifests, add status/reconciliation commands and generic artifact results.
- [ ] CLI interfaces: `render --format markdown|docx|pdf`, `delivery-check`, `publish --key`, `delivery-status --key`, `receipt-record --key --receipt FILE`. Host receipts require actual document ID/URL and readback evidence.
- [ ] Rerun delivery/core/documents tests and commit.

## Task 3: Official platform adapters

Files: create `scripts/omni_http.py`, `scripts/omni_providers.py`, `tests/test_providers.py`; add provider references.

- [ ] Read current official Notion Markdown/file-upload, Feishu imports, Tencent file import and DingTalk dws docs; record URLs and retrieval date.
- [ ] RED: use a recording fake transport with official response fixtures; assert correct auth/payloads, media upload, task recovery, target validation, readback checks, business errors, unsupported converted=false, timeout ambiguity and no second create.
- [ ] GREEN: implement Notion page/file uploads; Feishu DOCX import; Tencent DOCX pre-import/upload/async import/poll; DingTalk `dws doc import`/info/read via subprocess without shell; Obsidian copied Markdown/assets with collision-safe idempotent writes.
- [ ] Require success identifiers plus readback/contents checks before returning verified. Resume saved asynchronous tasks; unknown create outcomes require reconciliation.
- [ ] Run provider and delivery tests, then commit.

## Task 4: Skill workflow and compatibility docs

Files: SKILL.md, agents/openai.yaml, references/{delivery,providers/*,commands,setup,content,platforms}.md, README, CHANGELOG, .gitignore, packaging.

- [ ] Update progressive intake, confirmed preferences, plan approval and mode-specific review. Explain connectors/API/CLI/UI/import and scheduling limits without claiming fallback files are delivered cloud pages.
- [ ] Add private credential examples using env names, never secret values; ignore local credentials, allowlist installable bundle files.
- [ ] Document unchanged historical course operation and explicit new-course migration for changed delivery settings.
- [ ] Version metadata and UI wording to 2.0.0; keep runtime dependencies format-specific.

## Task 5: End-to-end validation and local accounts

Files: `tests/test_cli.py`, `tools/validate_v2.py`, `docs/release-validation-v2.0.0.md`, isolated `tmp/v2-qa/` artifacts.

- [ ] RED: subprocess CLI workflow tests verify plan render/review/approve, lesson publish and delayed advancement, wrong receipt bindings, interruption and retry behavior.
- [ ] GREEN: complete CLI changes; run entire suite and real PDF compile recovery checks.
- [ ] Create multilingual plan/lesson QA exports; render DOCX with bundled LibreOffice and inspect every page; inspect HTML/Markdown plus real Obsidian client display.
- [ ] Use user-specified account destinations when available; create named QA documents, return verification evidence and record exact limits when credentials/login or tools are missing.
- [ ] Verify original archived samples read-only; do not change historical checked_at dates.

## Task 6: Review and v2 package

- [ ] Run complete tests, skill validation, compileall and whitespace checks.
- [ ] Request one independent code-review subagent against base e82f3e8, spec, plan and current branch; fix important findings with regression tests.
- [ ] Package `omni-learning-anything-skill-v2.0.0.zip`, verify SHA256 and isolated extraction/import/CLI execution with all required resources and no credentials/course files.
- [ ] Commit tested changes; deliver local branch, package and truthful platform validation results. Publish a GitHub Release only on explicit subsequent instruction.

## Review focus

Ambiguous create responses must never duplicate pages; mutable receipts must not rewrite delivered manifests. Readback must distinguish a created empty page/file upload from a populated editable document. Credential handling and redirects must not expose secrets. Vault path traversal/symlinks/collisions must not overwrite user notes. No-XeLaTeX runs must not import PDF packages. Partial image uploads or async conversions must keep the course at the same lesson. Old archived sample configs and hashes must remain unchanged.
