# v2.1.0 validation — official API onboarding

Updated 2026-10-25. This release adds official-API-first onboarding and named connection reuse. Development base `bf4369b`; historical immutable v2.0.0/v2.0.1 tags/assets remain unchanged.

## Automated verification

- **105/105 tests passed**, including real XeLaTeX integration where available, legacy course/receipt integrity, format isolation, transport contracts and the live-account regressions below.
- Official CLI transports: 8/8 focused tests; connection onboarding: 9/9; provider contracts: 25/25; delivery lifecycle: 16/16 (included in the full total).
- Official tools inspected and used: Notion `ntn 0.23.25`, Feishu `lark-cli 1.0.98`. Installed from official distributions in a dedicated task cache; Feishu release checksum verified. No global defaults changed, tokens exported or private credential stores read.
- Fresh whole-branch review completed. Feishu brand/user verification, selected-profile recovery and malformed connection fields were reproduced and fixed with failing-then-passing regressions. No deferred review findings remain.
- ZIP extraction/runtime/Skill metadata/checksum and whitespace checks are repeated for the final package before publication. No private profiles, test documents, device codes or account identifiers are included.

## Real-account acceptance

| Platform | Actual write method | Acceptance on 2026-10-25 |
|---|---|---|
| Notion | Official `ntn` calling Notion APIs | Plan and Day01 created under a dedicated private API QA parent; PNG upload/image block, title/parent/full text/five source links, native browser full visual inspection, connection reuse and receipt reuse passed |
| Feishu | Official `lark-cli`, explicit verified **user** identity | Embedded DOCX uploaded/imported into two editable documents in a dedicated private API QA folder; task resume, title/folder/full text/image/five actual hrefs, native browser full visual inspection, connection reuse and receipt reuse passed |
| Obsidian | Existing local Vault Markdown + copied images | Historical native/readback acceptance retained; new read-only connection check passed against the actual Vault. No cloud API or cross-device sync claim |
| Tencent Docs | Existing official API adapter / authorized API connector | Real-account document delivery not accepted; prior deferral retained |
| DingTalk | Existing official `dws` | Historical login/organization gate/private folder passed; OSS upload failed. Editable document delivery not accepted; prior deferral retained |

Notion and Feishu writes were performed entirely through official API transports. Browser UI was used to inspect actual cloud rendering, not to paste/import the test documents. Prior Notion Word browser import (2026-10-18) and Feishu Word browser import (2026-10-25) remain separate historical results.

Both new API courses use `sample_mode: true`, synthetic bilingual content, an explicitly disclosed reused code-drawn QA figure, simulated approval and accelerated Day01. Five official source URLs were reopened on 2026-10-25 solely for hyperlink-preservation checks; this is not a newly researched learner curriculum. Full local output was inspected before publication (Notion HTML; Feishu two-page plan and one-page Day01 DOCX conversions), then full actual cloud documents were inspected.

After plan/Day01 acceptance, each publisher ran twice again: IDs and receipt bytes stayed identical. An independent provider readback checked existing objects, and folder/parent listings contained **exactly two documents**, matching the receipts. Saved named connections were rechecked live without retargeting course snapshots. Both isolated sample courses reached `complete`; schedules remained null. Existing historical QA documents and course archives were preserved. Private evidence is retained locally outside the installable bundle; private account/page IDs are not published here.

## Live contract fixes

Each fix was first reproduced by a failing regression, then verified against the same actual cloud objects:

- Accept the official `app.notion.com` URLs returned by Notion, while rejecting lookalike hosts and credential-bearing URLs.
- Normalize Notion's escaped Markdown punctuation during text checks; resume the same page/image upload rather than creating another page.
- Include Feishu import-media `extra` metadata declaring source extension and target native document type. The initial 1061004 response was resolved by this request correction with the existing authorization; no broader grant was requested.
- Treat Feishu task states1/2 and state0 without a materialized token as pending; reuse the stored ticket.
- Decode Feishu's percent-encoded link URLs and verify actual hrefs exactly. URLs appearing only in body text cannot satisfy hyperlink acceptance.
- Remove a prior error when a subsequent publication successfully verifies. Historical already-verified receipts remain immutable.

Feishu payload/status behavior was checked against the [official v1.0.98 import implementation](https://github.com/larksuite/cli/blob/v1.0.98/shortcuts/drive/drive_import_common.go).

## Scope and design decisions

1. Credentials stay with official CLIs' secure storage/renewal; connection files contain metadata only. This avoids a second OAuth/secret backend and depends on the host's credential-store availability.
2. Feishu uses official CLI raw API calls for DOCX endpoints lacking typed commands, retaining per-step upload/import checkpoints. Upstream CLI JSON contract changes require adaptation.
3. The read-only reviewer deferred live accounts/rendering and unattended credentials. This run completed actual account/rendering acceptance independently; unattended scheduler/credential availability remains untested and is not claimed.
4. Unchanged Tencent/DingTalk/historical UI routes retain their dated validation scope and the user's prior deferral. Their live document-write reliability remains unaccepted.

A successful `connect` is read-only and does not prove write permission; the actual plan publication closes that check. Timed login URLs can expire; tool setup precedes URL generation and fresh links are handed to the learner immediately. Feishu app configuration and user authorization are separate official steps. No universal two-dialogue OAuth promise is made when platform membership or administrator approval is required.

## Publication

Final package validation and downloaded-asset SHA256 will be recorded after publication. No live learning schedule or cross-device synchronization was tested.
