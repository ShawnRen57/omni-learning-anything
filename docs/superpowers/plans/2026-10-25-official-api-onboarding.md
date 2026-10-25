# Official API onboarding implementation plan

> **For agentic workers:** Execute inline with superpowers:executing-plans and TDD. One fresh whole-branch review at the end.

**Goal:** Make official-API delivery and low-friction first connection part of the self-contained skill.
**Architecture:** Official CLI transports reuse upstream credential management; metadata-only saved connections feed existing immutable delivery configs and receipts. No OAuth server or home-grown secret store.
**Tech Stack:** Python 3.10+, unittest, official ntn and lark-cli, existing DOCX/Markdown exporters.
**Spec:** ../specs/2026-10-25-official-api-onboarding-design.md

## Task 1: Authenticated official CLI transports
Files: new `scripts/omni_official_cli.py` under the skill; modify `omni_notion.py`, `omni_feishu.py`, `omni_delivery.py`; tests `tests/test_official_cli.py`.
- [x] Write failing cases: `ntn api` uses stdin JSON and pinned version; binary upload uses reviewed file; errors never disclose raw provider output; Feishu always uses user identity, saves ticket before readback, and resumes without another import; destination/account mismatches never verify.
- [x] Run `python -m unittest discover -s tests -p test_official_cli.py -v`; confirm failures demonstrate missing behavior.
- [x] Implement argv-array subprocesses, official-host restriction, sanitized errors, profile/account/workspace binding, CLI dispatch and readback with pagination. Use official CLI raw media/import/document APIs in the existing Feishu adapter so upload tokens and import tickets are saved immediately and uncertain-write recovery is retained. This ledgered implementation ruling replaces the opaque import helper shortcut.
- [x] Run targeted tests, full suite, and commit Task 1.

## Task 2: Connection discovery and reusable metadata
Files: new `omni_connections.py`; modify `omni_learning.py`, delivery validation; tests `tests/test_connections.py`.
- [x] Tests first: selected-platform URL parsing, missing CLI/auth actionable state, secret-free identity summary, target read access, metadata-only profile reuse, no silent replacement, and course snapshot independent of profile edits.
- [x] Add `connect --platform notion|feishu|obsidian --location LOCATION [--save-as NAME]`, `connection-show --name NAME`, `connection-list`. CLI routes use read-only identity/parent/folder checks; Obsidian validates Vault path. Return `ready`, `delivery`, `next_action`, `guide`; only explicit save writes profile metadata under user config with owner-only permissions. No secrets accepted by profile schema.
- [x] Run red-green targeted tests and commit Task 2.

## Task 3: Skill workflow, platform guides and real-account checks
Files: `SKILL.md`, `references/onboarding.md`, provider guides, commands/setup/delivery, README, dated validation report.
- [x] Document normal dialogue: choose destination; complete official login only if needed; Agent validates and saves metadata then publishes actual plan. Agent—not user—handles IDs/config/scripts. Existing authorized API tools are reused; no silent UI downgrade.
- [x] Read installed official command help, initiate authorization only with reviewable official scope/URL, ask user to complete it, then test isolated actual API plan and Day01 creation/readback and receipt reuse. Preserve pending outcomes while dependent on user.
- [x] Record UI/API/local results separately; do not claim account passes without actual evidence. Inspect full cloud rendering where tools permit.

## Task 4: Review, package and publication
Files: version metadata/tests/validator/package and release docs.
- [x] Set 2.1.0 consistently; run full unittest suite, Skill validator, syntax/whitespace, package exclusion and isolated extracted runtime checks.
- [x] Dispatch a fresh whole-branch review (required by executing-plans), fix Important/Critical findings with red-green regressions, keep full suite green.
- [x] Publish only after truthful verification; previous user authorization covers repository publication, not new security grants. Push normal fast-forward, create immutable new tag/release, download and compare asset bytes/checksums.

Completed 2026-10-25. Actual official API account acceptance, native visual checks, all105 tests, final independent review fixes, ZIP validation and downloaded release assets passed. See [final validation](../../release-validation-v2.1.0.md) for exact scope and design rulings.
