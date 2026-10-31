# v2.4.0 validation

Date: 2026-10-31. Baseline: published v2.3.0 (`b28b5fa`). Adds private material import, explicit source ranges/policies, original locators, scoped evidence retrieval and source-bound teaching/short checks. No new quiz timers/reminders, cloud-library crawl, OCR, bundled media transcription or DRM bypass.

## Format and behavior coverage

Generated real local file fixtures exercise text PDF (with an intentionally empty/scanned-like page), UTF-8/GB18030 text, Markdown, HTML, DOCX, EPUB, PPTX, SRT and VTT. A native `textutil` round-trip generated and read a binary `.doc`; this verifies the installed converter route on this Mac, not native DOC portability to all hosts. RTF uses the same conditional native conversion route; platforms without a trusted converter receive conversion guidance. Complex formulas, tables, images, EPUB media/DRM, speaker notes and actual audio/video comprehension remain explicitly unclaimed.

Tests cover selected-only retrieval, literal quotation and original locator, canonical public origins versus no invented local URLs, immutable file versions and extraction-snapshot hashes, unsafe archives/XML, missing PDF pages, repeated-heading ambiguity, parent/subsection inclusion, approval-bound scope, strict material-only policy, original locator presence during cloud readback, actual CLI operations, all local document formats and material-backed quiz preparation/start. Failed extraction retry preserves failure history. Private material reference excerpts render as literal Markdown rather than active HTML, and use source-location labels instead of optional further-reading labels.

Baseline171 tests passed in59.944s. Initial12 new tests failed because the pipeline was missing. The first integrated suite passed187 tests in66.074s. Independent review found3 material issues: forged material refs bypassing legacy web-link requirements, repeated headings merged silently, and original-file hashing/extraction race. All three were reproduced as failing regressions and fixed. Additional regressions cover nested chapters, failed retry history and literal reference rendering. Final whole-suite result: **193/193 tests passed in 68.646 seconds**.

## Review and evidence limits

One independent read-only reviewer inspected readers, registry, scope/config/rendering/quiz integration and simulated an own-book strict/supplemented workflow, unselected-content isolation and failed-conversion recovery. This establishes structural behavior, not semantic extraction correctness, proof that every cited claim follows from its source, genuine user consent, learning efficacy or access rights. The host must inspect originals, validate source relevance and treat document instructions as untrusted data.

No new real-account cloud writes, remote native-rendering acceptance or background learning jobs were run. Existing cloud transports retain their previous release acceptance; changed plain-source readback behavior is tested locally. Private source data is not included in the distributed Skill. The seven earlier ZIPs are retained unchanged. English remains the default README with nine translated versions.

## Release/package verification

Skill Creator validation and isolated ZIP/runtime/provider/checksum validation passed. All **56 ZIP entries** match source. The extracted CLI exercised import, selected heading including its child, scoped search, exact citation, initialization, PDF/HTML/DOCX/Markdown plan exports, local publication and source-bound short-check preparation/start. The one-page generated PDF was visually inspected, including its original-locator reference section. Other format containers/text were checked structurally; no fresh native cloud or Word UI acceptance is inferred.

The workflow uses synthetic QA material and explicitly simulated approval in sample_mode, not a source-researched real learner course or a teaching-quality result. No live schedules were created. All seven earlier ZIPs remain byte-identical. Ten README/current-version local targets and Skill links were verified.

Package: `omni-learning-anything-skill-v2.4.0.zip`, 142,975 bytes. SHA256: `241636b7b8dfd5cbb299dea4d0e7f9d3e698d604516d3e5d150f0182cd1abb2f`. Remote publication was independently verified as recorded below. No blanket promise is made for all ebooks, encodings, scanned documents or protected/unavailable content.


## GitHub publication

Published 2026-10-31: [v2.4.0](https://github.com/ShawnRen57/omni-learning-anything/releases/tag/v2.4.0), latest stable Release. Default main and annotated tag resolved to `0b0d740d9ad870cfc3d305c9e548c03a6e7ebcce` at publication. Remote README and Skill metadata show v2.4.0. Both release assets were downloaded from GitHub and compared byte-for-byte with the local package and SHA256SUMS; both match. This record is a documentation-only follow-up; tested source tag and package stay unchanged.
