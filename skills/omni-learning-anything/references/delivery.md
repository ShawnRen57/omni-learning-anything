# Destinations, intake and verified delivery

New courses explicitly choose a destination. Reuse known preferences and inspect actual host tools first; do not ask for API credentials when a writable connector is already authorized. Legacy configs without `delivery` remain PDF courses.

## Intake examples

Missing platform: “学习计划和每日材料希望放到哪里：PDF、本地 Markdown/Word，还是 Notion、Obsidian、飞书、腾讯文档或钉钉？”

Platform selected, missing location: “你已选择飞书。请提供课程文件夹链接；已有可写连接器会直接复用，否则再配置应用授权。”

Missing credential reference: “当前没有可写 Notion 连接器。请在本机私有环境中设置令牌，并告诉我环境变量名，以及授权给该连接的课程父页面。不要把令牌发到聊天。”

Actual access failure: explain the missing permission/expired credential, preserve pending material, and offer the smallest correction or an accepted import/local route. Do not treat a long unanswered question as approval to change platforms. Confirmed choices persist for the course; there is no monthly re-confirmation rule.

## Configuration

`config.json` keeps the existing learning settings plus:

```json
{
  "delivery": {
    "platform": "notion",
    "mode": "api",
    "destination": {"parent_page_id": "COURSE_PARENT_PAGE_ID"},
    "credential_env": {"token": "OMNI_NOTION_TOKEN"}
  }
}
```

Environment references are variable names, not secrets. A private env-file can live outside the repository/course; use the host's approved credential loader to populate the subprocess environment. The CLI deliberately does not evaluate/source arbitrary env files. Do not echo environment contents. Automatic OAuth creation, scope expansion or account changes remain subject to the host's permission rules.

| Platform | Modes | Confirmed destination | Default export |
| --- | --- | --- | --- |
| pdf / markdown / docx | local or host | Local course folder; host recipient if relevant | Matching format |
| obsidian | local | Existing `vault_path`, safe relative `subdir` | Markdown + copied image |
| notion | api, host, import | Course `parent_page_id` | Markdown + image upload |
| feishu | api, host, import | Course `folder_token` | DOCX + Markdown |
| tencent | api, host, import | Course `folder_id` | DOCX + Markdown |
| dingtalk | cli, host, import | Course `folder_id` or `workspace_id` | DOCX + Markdown |
| generic | host, import | Actual host-confirmed document location | DOCX + Markdown |

Use API identifiers in API configs; extract them from a supplied URL only after inspecting the platform's documented URL form and access. IDs are not authentication tokens. A cloud course parent/folder is selected or created during intake with authorized host tools; the publisher creates plan/daily documents inside it. Never choose a shared/team space merely because it is visible.

`delivery-check` performs local config/environment validation only. `ready: true` is not remote authorization proof. Only `publish` plus provider readback can verify API/CLI delivery; connector/UI modes use actual tool evidence.

## Provider guides

Read only the chosen route: [Notion](providers/notion.md), [Obsidian](providers/obsidian.md), [Feishu](providers/feishu.md), [Tencent Docs](providers/tencent.md), [DingTalk](providers/dingtalk.md), [generic import](providers/generic.md).

## Artifact and receipt contracts

Rendering saves an immutable hash-bound `manifests/KEY.json` with `artifact`, `artifacts`, `files`, `previews`, `reviewed_at`. Existing PDF manifests remain accepted. Receipts in `receipts/KEY.json` are separate and bind the key, manifest hash and destination hash into a stable `delivery_id`.

States: `prepared` (host work has not been done), `creating` (external write started), `pending` (known task/document needs completion/readback), `needs_reconciliation` (write result uncertain), `awaiting_import` (local file ready), `failed` (known conversion failure), `verified` (content, figure and links checked). Local-file `verified` means the file exists in the agreed local folder; sending its chat notification is a separate host action.

New explicit destinations cannot use `delivered` before their primary receipt is verified. Recording delivery also binds the receipt hash into course state; subsequent edits to delivered receipts/manifests are rejected. Do not revise a review note after publishing; it changes the receipt binding.

For a host connector/browser import, first run `publish --key KEY` to obtain the binding. Use actual host tools, verify the returned remote document and its rendering, then save a private staging JSON with the binding plus:

```json
{
  "key": "Day01",
  "manifest_hash": "ACTUAL_MANIFEST_SHA256",
  "target_hash": "ACTUAL_TARGET_SHA256",
  "delivery_id": "ACTUAL_DELIVERY_ID",
  "status": "verified",
  "remote_id": "ACTUAL_RETURNED_DOCUMENT_ID",
  "url": "https://www.notion.so/ACTUAL_DOCUMENT",
  "evidence": {
    "content_checked": true,
    "image_checked": true,
    "links_checked": true,
    "note": "Describe actual tool readback and visual inspection."
  }
}
```

Run `receipt-record --key KEY --receipt /private/staging/receipt.json`. This is an agent attestation, like `review`; the JSON is not an automatic proof of remote access. Never substitute invented IDs, links, tool success or inspection. Local file creation, reminders and successful API create responses alone do not prove populated cloud documents.

## Recovery

- `delivery-status --key KEY` shows the existing bound receipt.
- `pending`: rerun `publish --key KEY`; known async tasks/pages are reused. It makes one status query per run rather than sleeping/polling indefinitely.
- `needs_reconciliation` or `creating` without IDs: inspect/search the destination and host history. If the existing object is found, run `reconcile --key KEY --remote-id OBSERVED_ID --url OBSERVED_URL` or `reconcile --key KEY --task-id OBSERVED_IMPORT_TASK`, then `publish` to independently read back. `reconcile` does not verify or advance the course.
- If no object can be found, uncertainty remains. Do not delete the receipt to trigger a new create or edit state to advance. Ask the learner to check platform history/support, or explicitly authorize a new course/destination while retaining the old record.
- `failed`: inspect the saved conversion task/document. API adapters will query it rather than create another one. Fix permission/readback problems on the existing object; use a new explicit version for a truly failed conversion needing a fresh create.
- Tencent's import progress credential lasts only ten minutes; after expiration locate the resulting document through the authorized host UI, then reconcile its ID/URL.
- Vault collisions/user edits: never overwrite. Preserve the existing note, choose a confirmed new course subdirectory and start a new approved version.

A paused course can inspect delivery state but cannot publish an undelivered daily lesson. Completion stops the host schedule; API timeouts never skip a day. Remote edits made later by the learner are outside the local archive's immutability contract.
