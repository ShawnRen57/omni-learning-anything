# v2.2.0 validation

Real-account/rendering validation: 2026-10-25; release verification: 2026-10-26. This report separates released features from local rendering, contract tests and real-account acceptance. Private account IDs, authorization material, signed download URLs and course receipts are excluded from the repository/package.

## Real accounts

| Platform | Write path | Actual acceptance |
| --- | --- | --- |
| DingTalk | Official checksum-verified `dws` v1.0.65; DOCX upload/import API and Markdown readback | Plan + Day01 in the confirmed private folder; fixed organization:user; editable document type, title/body, embedded synthetic figure, caption/credit and five exact semantic source hrefs; both complete native pages inspected; repeat receipt bytes unchanged; folder listing contains exactly two course documents. |
| Tencent Docs | Official public OAuth authorization code + PKCE with an ephemeral loopback callback; official MCP API signed upload/import/export | Plan + Day01 in the explicitly confirmed personal home root; fixed official user identity; editable `doc`, exact titles and folder membership; exported text, embedded synthetic image and five semantic hyperlinks; both complete native pages inspected; repeat receipt bytes unchanged. |
| Notion | Official `ntn` API | The plan + Day01 account acceptance from [v2.1.0](release-validation-v2.1.0.md) is retained; no new Notion write is claimed in this upgrade. |
| Feishu | Official `lark-cli` user API | The [v2.1.0](release-validation-v2.1.0.md) plan + Day01 acceptance is retained; no new Feishu write is claimed here. |
| Obsidian | Local Vault Markdown and copied image | Existing local/native acceptance remains the supported exception to cloud APIs; this release does not claim a new cloud synchronization test. |

The two new platform courses used `sample_mode: true`, one simulated approval and one accelerated daily lesson. No live schedule or chat/group message was created. These are synthetic transport/layout fixtures (including a teal QA image and example hrefs), not evidence of fresh research, teaching quality or learner mastery. A successful foreground keychain session does not establish unattended host access.

Tencent home search returned exactly one plan and one Day01 course document, plus a separately named **“Omni v2.2 QA 诊断记录（非课程）”** SmartCanvas probe retained for diagnosis. It is not an extra delivered course lesson. The initial SmartCanvas tool appended content after a default tutorial; the shipped course publisher uses official DOCX import instead. Tencent's DOCX export represents source hyperlinks as complex Word `HYPERLINK` fields; the checker now recognizes complete semantic fields as well as relationship hyperlinks. Plain text URLs are insufficient.

## Local formats and languages

Course language codes: `en zh ja ko es fr de pt ru ar`. Localized labels, language validation, actual authored-text preservation, DOCX image/relationship integrity, Japanese/Korean script fonts and Arabic bidi/complex-script properties are exercised by automated tests. Ten real XeLaTeX plan fixtures compiled with embedded fonts and five PDF URL annotations; every page was inspected. The deliberately mixed Chinese input text is preserved, not translated by the exporter. Arabic uses RTL with Latin identifiers isolated; Japanese/Korean use native fonts with mixed-Chinese fallback. Additional native-text and DOCX viewer inspection records are kept with local QA evidence.

HTML uses one serializer for explicit deliverables and previews, embeds the exact reviewed PNG/JPEG bytes, escapes authored content, includes five semantic source anchors, and has no script, external stylesheet or font dependency. Outbound reference links still need Internet. CLI HTML generation works without TeX on PATH. Mixed PDF/HTML exports retain their reviewed hashes and deliver the selected HTML artifact. Tampering is rejected. Desktop/narrow/RTL visual inspection is part of the release check.

## Recovery and privacy

New cloud connections preserve the learner's account and location in a course snapshot. DingTalk carries the exact organization:user profile on every CLI call. Tencent stores OAuth secrets in an OS keyring and keeps only the authorization name/user ID in course metadata. OAuth host/state/PKCE, secret-free status/errors, import task checkpoints, resume without duplicate creates, official signed upload hosts and expired-export recovery have regression coverage. Legacy Tencent application/COS API mode and historical courses remain supported without automatic migration.

The current official Tencent device endpoint rejected a dynamically registered public client, although device authorization appears in server metadata. The supported guided route is PKCE/local callback. It requires opening the official grant on the same computer; it is not a hosted OAuth service. Export tasks can expire; only exports are recreated, with a bounded retry count, preserving the course document/import.

## Documentation and package

The root README is English, with nine translated READMEs and consistent ten-language navigation. Its near-top version guide explains learner benefits; technical evidence belongs in this report. The page uses an original banner and existing sample gallery, with layout inspiration from [DeepTutor's README](https://github.com/HKUDS/DeepTutor/blob/main/assets/README/README_CN.md); no branding, text or assets were copied.

Final suite, skill validation, package SHA256, independent review and downloaded-release verification are recorded below when performed. A local package alone is not proof of GitHub publication.

Candidate verification: **131/131 tests passed** (including real XeLaTeX integration); Skill Creator validation and extracted ZIP runtime/CLI/provider/SHA256 checks passed. Ten real DOCX fixtures each rendered to one page and were inspected. A separate native Arabic prose fixture was inspected in PDF, DOCX and a 390-pixel HTML viewport; ISO dates remain LTR within RTL text.

## Final review and regressions

One fresh whole-branch review of `cb94ff8..e53a3b1` found no Critical issues and two Important issues. Both were reproduced as failing regressions, then fixed in one pass: Arabic PDF paragraph boundaries remain outside inline direction commands, and DingTalk readback parses HTTP(S) destinations with balanced/escaped parentheses and optional titles. Wrong targets, plain URLs and image-only source destinations are rejected. The new Arabic multi-paragraph PDF was visually inspected; the current DingTalk reader also reverified the two existing real documents without imports or receipt changes.

The final complete suite passed **134/134 tests** in 60.961 seconds. Skill Creator and isolated ZIP extraction/runtime/CLI/provider/checksum validation passed again. All 38 ZIP entries match their source files. No Minor findings were deferred. The prior v2.1.0 archive remains byte-identical.

Implementation decisions and review boundaries, in decision order:

1. Official metadata initially suggested Tencent device authorization plus MCP, conditional on live capability. Actual public-client rejection superseded that tentative selection; metadata alone never counted as account acceptance. The cost would otherwise have been a login path that new users cannot complete.
2. Tencent therefore uses the proven official PKCE loopback flow with read/write scope and OS keyring storage. It needs the grant completed on the same computer; it does not supply a hosted or remote authorization service.
3. The independent reviewer performed no live account actions. Account/native-page conclusions rely on the implementer's recorded real-account inspection and receipts; native viewing was not repeated by a second person.
4. Unattended keyring access, host scheduling and cross-device synchronization remain host-specific acceptance work. A foreground pass does not promise those behaviors.
5. Cloud QA uses synthetic transport/layout fixtures. It does not measure fresh research, teaching quality or mastery; the Skill's normal sourcing and learner review steps remain required.
6. Universal operating-system/viewer font substitution is not claimed. Other hosts may need appropriate fonts and actual output inspection.
7. Legacy generic host/import compatibility remains for existing courses, without a new native-support claim for unspecified platforms. A new platform still needs explicit capability verification.
8. Release integrity is gated on downloading the published assets and comparing exact bytes/SHA256. Until that step is recorded, a local archive is only a candidate.

## Published asset verification

Published on **2026-10-26**: [v2.2.0](https://github.com/ShawnRen57/omni-learning-anything/releases/tag/v2.2.0), non-draft and non-prerelease. The immutable tag points to `494a221`; subsequent documentation commits record the completed publication without changing that tag.

The downloaded ZIP and `SHA256SUMS` each match their local release files byte-for-byte. The downloaded ZIP is **89,593 bytes**, contains 38 source-matching runtime/resource files, and passes isolated extraction/runtime/CLI/provider/checksum validation. Its SHA256, also reported by GitHub, is:

```text
7165a5df79c5de7025f792b14edd1bf836661882dd59022f81c1fc22de0149c1
```

GitHub's published default README rendering was retrieved and confirmed to be English with the near-top version guide and ten-language navigation. English/Chinese/Arabic GitHub-compatible previews were also inspected locally. No remote release-upload verification remains pending.
