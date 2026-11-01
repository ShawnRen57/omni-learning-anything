# v3.0.0 validation

Validation began 2026-11-01; publication work continued 2026-11-02 (Asia/Shanghai). Baseline: main `77549ad`. Scope: named university course pathways, undecided first-use discovery, immutable source/edition mapping, registry inspection compatibility, refreshed multilingual examples and ten READMEs. The user approved the [design](superpowers/specs/2026-11-01-v300-design.md) and GitHub publication.

## Catalog and course behavior

The self-contained catalog contains **12 courses and 105 editorial groups of original sessions**. Primary sources, editions, workload, original locators and retrieval limitations are recorded in the [catalog ledger](course-catalog-sources.md). These groups are not advertised as individual original lectures. Harvard PSY 1504 uses the original Spring 2006 syllabus hosted by Penn's Positive Psychology Center; it is not a claim to verified lecture transcripts or a substitute Harvard happiness course. CS50's year-specific redirect, MIT's package/recording year distinction, and Yale music's inaccessible homepage/accessibility of individual lectures are disclosed.

Offline CLI list/search/detail/bind/welcome/check were exercised. “我想学习哈佛积极心理学” matches its course, “幸福课” and a conflicting 2008 edition require clarification, and “哈佛机器学习”/unknown names are not forced into Stanford or another included course. Welcome is an instruction for the current host conversation only, not an autonomous installation callback or new chat.

Course bindings retain a full snapshot, canonical SHA256, selected groups, pacing and practice. Tests verify snapshot mutation rejection, old snapshots independent of catalog updates, ordered day mapping/selected coverage, explicit partial scope, original-source URL/snapshot/group-anchor correspondence, visible context in HTML/Markdown, and legacy courses without a pathway. Actual source access, substantive claim support, within-group progression and appropriate workload remain agent judgments, not proven by a schema or catalog match. Default assessments remain light and learner-started; original assignments require explicit choice. No new timer, account grant or course migration was introduced.

## Independent reviews and regressions

A separate spec/behavior review found no confirmed material gap in the completed runtime/catalog/instructions/README scope and independently spot-checked primary course sources. A following code-quality review found one Important/P2 issue: normalized substring matching interpreted “limited” as MIT, so “CS50x with limited time” failed. A regression reproduced it before the Latin-word-boundary fix; the targeted suite then passed and the reviewer approved the fix. Legacy v2.6.0 bundle validation also passed.

A separate six-language teaching review checked course correspondence, source scope, math, loop traces, cashflow examples, Arabic argument distinctions, exercise answers and native-language clarity. It requested explicit Japanese/Spanish original prerequisites, consistent Japanese inline-vector wording and a more precise Arabic possibility/actuality distinction. All three were corrected, re-rendered and accepted on re-review. The review did not claim university endorsement, completion equivalence or original lecture reproduction.

## Installation, compatibility and full regression

**255/255 unittest tests passed in 70.769 seconds.** This includes 11 course-pathway tests and 17 installation boundary tests. The duplicate-ZIP-entry warning is from an intentional archive rejection fixture. Existing document, material, assessment, review, connection and delivery regressions remain covered; this release does not claim new live cloud-account write acceptance.

Read-only native-registry inspection now recognizes bounded, matching-version `_meta.json` metadata and a `LICENSE.txt` alias. The actual official SkillHub 2.6.0 installation now returns `complete: true`, `integrity_verified: false`, native discovery unknown and update through its original manager; its files were not changed. Tests retain strict refusal of registry metadata in managed archives, managed updates and ZIP adoption, version mismatch, local changes and symlinks. Recognition is not authentication or registry signature verification.

## Actual samples and presentation

[Six example sets](../examples/university/README.md) contain **12 PDFs (36 pages total)** and 12 offline HTML documents: Chinese psychology, English computing, Japanese linear algebra, French music, Spanish finance and Arabic philosophy. Each PDF page was rendered and visually inspected for legibility, complete text/figures/citations, page flow and clipping; embedded-font/missing-glyph checks passed. Japanese vector geometry and Arabic shaping/RTL were inspected. All approvals are explicitly simulated QA for public samples; no live schedule or learner result was created.

Teaching diagrams are original reproducible code-drawn explanations, not AI image-generation claims, measured data or university slides. The 2400×2300 README collage is assembled from actual full first-lesson page renders, checked at full size and 900-pixel README width. It is the first image in all ten READMEs, followed by the existing transparent wordmark. [Sample source/provenance notes](v300-sample-sources.md) retain the research and teaching boundaries.

HTML static checks cover embedded images, source links, language/direction attributes and no external script/style/font dependencies. An actual Chrome `file://` opening of the Arabic Day01 confirmed its rendered RTL text and accessible complete content. Subsequent browser checks were interrupted by the Mac locking again; further actual browser results are recorded here when available, without treating static checks as visual proof.

## Packaging and GitHub publication

Package: `omni-learning-anything-skill-v3.0.0.zip`, **191056 bytes**, **68 files**, SHA256 `10637a3c31d30e087fdf555a2036d77c5862f5f4934b66886b31d5dfd315b046`. Every archive file matched source. Extraction/runtime syntax/version/provider resources/checksum validation passed; extracted `courses list/search/bind` and completeness inspection worked under Python `-S` without site packages. Actual historical v2.6.0 ZIP installation upgraded to v3.0.0 through the managed updater, retained a backup and kept five external synthetic learner/connection files byte-identical. No actual user installation or private course was replaced.

Core Skill Creator validation passed on a normalized temporary frontmatter copy; public registry extension fields remain in the source. Official Claude Code plugin/marketplace validation passed, with its existing optional square-icon directory advisory. All ten README first-image/language links and the sample gallery's local targets passed checks. All 12 HTML files have correct language/direction attributes and an embedded PNG, with no external scripts, style links, imports or private local paths. Prior release archives and unrelated untracked research remain preserved.

Registry versions are separate from GitHub: the earlier SkillHub listing remains 2.6.0, and ClawHub's previously observed platform write-capacity failure is not called a v3.0.0 publication.

## Verified GitHub release

Published [v3.0.0](https://github.com/ShawnRen57/omni-learning-anything/releases/tag/v3.0.0) on **2026-11-02 at 00:12:58 Asia/Shanghai**, as the latest stable release (not draft or prerelease). Main and the annotated tag resolved to tested source commit `9d00cedfc424d7b3fbc4582f911980759c01d178` at publication. Both release assets were downloaded from GitHub: the ZIP and SHA256SUMS were byte-identical to local files, and all 68 extracted runtime files matched source. The downloaded CLI worked under Python `-S`, reported 3.0.0, and listed 12 courses. Thirteen remote README/Skill/plugin/marketplace files matched local content at the tag. This publication record is a documentation-only follow-up; the tested tag and archive bytes remain unchanged.
