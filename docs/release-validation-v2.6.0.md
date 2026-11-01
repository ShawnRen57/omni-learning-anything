# v2.6.0 validation

Date: 2026-11-01. Baseline: v2.5.0 main `c186f36`. Scope: three install entry points (chat, one-command community CLI, native/ZIP), selected first-use setup, native discovery checks and preservation of external learner data during updates. No separate npm package, new reminder/job, blanket cloud grant or token migration.

## Actual installation checks

- Community `skills` 1.7.4, Node 24.14.0/npm 11.9.0: installed this actual public GitHub repository for Codex and Claude Code into an isolated project; native paths and Claude link were created. `update omni-learning-anything -p -y` checked this repository and reported up to date. Pre-release local-source installation of v2.6.0 passed. Global flags were also exercised with a process-local Node homedir shim; the real user HOME/CODEX_HOME variables and installed global skills were not changed. This is a simulated home, not a claim that the user's global installation was replaced.
- Official Codex GitHub installer: actual v2.5.0 repository/path/tag downloaded into an isolated project `.agents/skills`. The installed Codex app-server's read-only `skills/list` identified it enabled. It also identified the community-installed v2.6.0 Skill enabled, with its actual namespaced name. No model turn/new chat was started. The current app-server schema does not support the extra roots shown by newer official documentation; the test therefore uses actual supported project roots.
- Official Claude Code 2.1.316: actual public GitHub marketplace/plugin install passed. A separate local pre-release marketplace/plugin installation passed, and native `plugin details` lists version 2.6.0 and exactly one Skill. The local-source update command correctly explains there is nothing to copy and reports the current version. Plugin validation passes; an optional directory-listing icon advisory does not affect installation. No marketplace directory submission or client-wide policy change was made.
- ZIP/chat path: the same complete runtime bundle is used by agent-operated instructions and managed installation helpers. No installer can prove an arbitrary host's model invocation or obtain document permissions just from placing files. Client upload UIs from older acceptance records were not all freshly retested.

## First-use and update checks

Bundle inspection checks entry files, local Python imports and linked references. Integrity requires a matching installation receipt; native discovery remains unknown until a real host inventory/enablement check. Current Codex may namespace invocation names, so instructions use the returned name instead of assuming a fixed command.

Setup recipes select only the chosen output/input route. HTML/Markdown/Obsidian need no document libraries; hosts missing an OS IANA timezone database conditionally require tzdata; DOCX selects python-docx/Pillow; PDF selects pypdf/pypdfium2 plus a real TeX/font check; Tencent's official default selects OAuth/keyring rather than legacy COS. Recipes do not execute pip, change settings or claim authorization. Existing official account/destination adapters and authorization recovery retain their previous acceptance and regression coverage; this release does not re-claim new native cloud-account write acceptance.

Managed ZIP updates validate checksum, allowlisted bounded content and actual installed file hashes, reject unknown/modified/symlinked files, stage before replacement, keep an old-version backup and restore it on swap failure. Legacy standalone copies can only be adopted when byte-identical to an exact verified historical release. Native manager caches/links use their original updater. Course creation inside the installed Skill tree is refused. Saved connections and external config/plan/state/learning/receipts remain outside replacement scope; no old course is reinitialized, approved, retargeted or scheduled by updating.

Baseline: 222 tests passed in 69.319 seconds. Initial new tests failed for missing helpers and unsafe boundaries before implementation; regressions reproduce missing linked references, corrupt archives, accidental installation inside a course, missing historical-install receipts and edited-file adoption refusal. One independent review and final suite/package/publication results are recorded below when complete.

## Independent review and regressions

One independent read-only reviewer found two Important/P2 issues and no Critical issues. Both were reproduced with failing regressions: absent system timezone data left an HTML recipe empty while course initialization failed, and Ctrl-C between the old-directory rename and staged replacement left no active installation. Setup now detects unavailable IANA data and recommends tzdata conditionally; replacement restores the old installation on catchable interruption, or retains a complete new target if the atomic swap already finished. Hard kill/power-loss recovery is explicitly documented rather than claimed as automatic.

## Final local verification

Final full suite: **242/242 tests passed in 66.103 seconds**. All 64 Skill ZIP entries match source. The extracted CLI passed fresh managed installation, v2.5.0 historical-copy adoption and upgrade with an old-version backup, idempotent update, continuation of an existing lesson-bound quiz, unchanged external config/plan/state/learning/receipts and saved Obsidian connection reuse. Python `-S` (no site packages) rendered/published HTML and Markdown and correctly identified DOCX libraries as missing. Synthetic fixtures and simulated approval establish workflow behavior, not semantic teaching quality or native cloud-write/UI acceptance.

Core Skill Creator validation passed on a normalized temporary copy. The six pre-existing catalog extension fields are retained and separately validated with matching versions; the strict core validator does not accept those extension keys directly. Claude plugin/marketplace validation and runtime component inventory pass; the optional plugin-directory icon advisory is not marketplace submission approval. All nine previous ZIPs are retained byte-identically.

Package: `omni-learning-anything-skill-v2.6.0.zip`, 168747 bytes, SHA256 `e481ab58ac72fb1594797f08b9a9d584330449a07c7bc2ed8ccaba9a15a80eb7`. Final archive entries match source after documentation updates.

## GitHub publication and actual remote upgrade

Published 2026-11-01: [v2.6.0](https://github.com/ShawnRen57/omni-learning-anything/releases/tag/v2.6.0), latest stable Release. Main and annotated tag resolved to `319415748fa4b02f1f85f5d0f89ccda59c239df6` at publication. GitHub API confirmed the release assets and consistent README, nested/flat Skill, plugin and marketplace versions. Both ZIP and SHA256SUMS were downloaded from GitHub and matched local files byte-for-byte.

After pushing the tested source, the existing real GitHub community-CLI installation was upgraded from v2.5.0 to v2.6.0. Its completeness check passed, and all 16 external synthetic learner/connection files stayed byte-identical. The original remote Claude marketplace was refreshed, its cached plugin upgraded to v2.6.0, and native component inventory again listed exactly one Skill. This validates actual remote upgrade, beyond the earlier local-source/no-op checks. No actual user's global Skill, private account store, course or schedule was replaced. This publication record is a documentation-only follow-up; tested tag/package bytes stay unchanged.
