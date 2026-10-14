# 钉钉 / DingTalk

Prefer available writable host tools. Otherwise the supported direct route is the official DingTalk Workspace CLI `dws`; the skill does not invent an undocumented REST interface or request arbitrary app keys. Confirm existing authorized login and a course `folder_id` or `workspace_id`.

Install/login through official documented channels when needed. Enterprise/admin authorization may be required; do not claim a personal desktop login grants CLI scopes. Do not materialize tokens in the course or scheduler prompt.

The adapter invokes argument arrays without a shell:

```sh
dws doc import --file /course/sources/Day01.docx --folder CONFIRMED_FOLDER --name LESSON_TITLE --format json
dws doc import get --task-id RETURNED_TASK --format json
dws doc info --node RETURNED_NODE --format json
dws doc read --node RETURNED_NODE --content-format markdown --format json
```

Import returns node/document URL or an async task. Save it immediately. Reject `fallback=upload`/`converted=false`, which denotes a file object rather than an editable document. Metadata must identify ALIDOC/adoc; readback checks lesson text, source URLs and a remote image. CLI output that lacks these fields remains unverified rather than guessing success. Version changes require checking the current leaf command schema and updating the adapter contract.

On timeout with no saved node/task, inspect the target folder/history before another import. UI fallback imports embedded DOCX, then verifies the actual editable document and records a host receipt. Do not send test documents to chats or groups unless separately instructed.

Official sources checked 2026-10-14:
- https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli
- https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/blob/main/skills/mono/references/products/doc/doc-import.md
- https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/blob/main/skills/mono/references/products/doc.md
