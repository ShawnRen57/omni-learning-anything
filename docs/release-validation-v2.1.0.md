# v2.1.0 validation — official API onboarding

Updated 2026-10-25. This report distinguishes implementation/contract verification from actual account writes. Development branch: `feat/api-onboarding`; base `bf4369b`.

## Current evidence

- Official tools inspected: Notion `ntn 0.23.25`, Feishu `lark-cli 1.0.98`. Official distribution sources and Feishu release checksum verified; installed in a dedicated task cache without changing global defaults.
- Official CLI transport tests: 8/8, including stdin JSON, reviewed file upload, sanitized failures, user identity, account mismatch before write, async ticket reuse and folder readback rejection.
- Connection tests: 9/9, including selected official destination URLs, actionable missing tool/auth states, read-only identity/target checks before saving, metadata profile permissions/no replacement, course snapshot independence, and malformed-profile isolation. Tests observed failing before implementation/fix and then passing.
- Full suite after review fixes: **99/99 passed**, including the malformed-profile regression and real XeLaTeX integration when available.
- Candidate ZIP: isolated extraction, all Python syntax, CLI version/doctor/connect invocation, provider/onboarding resources and SHA256 passed. Official Skill validator passed. `git diff --check` passed. Fresh whole-branch review completed; its three findings have focused passing regressions (brand/verified user, named profile recovery, malformed profile fields). Final full-suite/package recheck passed, including isolated extraction/runtime, Skill validation, checksum and whitespace checks. Publication remains pending actual account API acceptance.

## Real accounts

| Platform | Historical actual acceptance | New default route | New real-account status |
|---|---|---|---|
| Notion | 2026-10-18 Word browser import, plan and Day01 | Official `ntn` API transport | Authorization required; no API-created plan/Day01 accepted yet |
| Obsidian | Local Vault write/readback plus 2026-10-18 native reading | Local Vault exception | Historical route unchanged; no official cloud API or sync claim |
| Feishu | 2026-10-25 Word browser import, plan and Day01 | Official `lark-cli`, explicit user identity | Application setup/user grant required; no API-created plan/Day01 accepted yet |
| Tencent Docs | Incomplete; browser entry timed out | Existing official API adapter/authorized API connector | Not accepted on a real account |
| DingTalk | Login/organization CLI gate/personal folder passed; OSS import upload failed | Existing official `dws` | Editable document delivery not accepted |

Official authorization is completed by the learner, not inferred from browser login or historical organization settings. Generated URLs/device codes expire and are not published in this report. No raw secret/CLI credential store is read, and no private account identifiers or QA document links are packaged.

A successful `connect` is read-only and does not prove write/import access. API acceptance requires isolated actual plan and Day01 publication to the confirmed account/location; native visual inspection of all content/figure/links; recorded provider readback and repeat publish reusing the same object/task. Until completed, the above API account rows remain pending. No real learning schedule is created for QA.

## Design decisions

Credentials stay with the official CLIs' secure storage and renewal; connection profiles store only metadata outside course/skill files. Hosts without a usable credential store need a specifically configured private API alternative rather than silent plaintext fallback. Feishu DOCX endpoints use the official CLI raw API transport, reusing existing per-step upload/import checkpoints because the installed CLI lacks typed DOCX commands. Upstream JSON contract changes must be checked against current help before acceptance.

Historical immutable v2.0.0/v2.0.1 tags and assets are preserved. Release checks and downloaded-asset digests will be appended when publication is complete.
