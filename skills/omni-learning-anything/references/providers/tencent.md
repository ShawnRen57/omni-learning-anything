# 腾讯文档 / Tencent Docs

This is docs.qq.com, not Enterprise WeChat docs. Prefer an already authorized writable official API connector; otherwise use the official API route below. See [onboarding](../onboarding.md); the agent handles setup/IDs/private references, the learner completes official grants. API mode needs `destination.folder_id` and private environment references `client_id`, `open_id`, `token`; every API call sends the official `Client-Id`, `Open-Id`, `Access-Token` headers. A personal website login is not these credentials. The application and OAuth grant must expose the required scopes.

Install `scripts/requirements-tencent.txt` only for this API route. The adapter uses Tencent's official `cos-python-sdk-v5` for temporary COS uploads; secrets are Base64-decoded per the official pre-import contract and remain in memory.

Flow: `POST /openapi/drive/v2/files/pre-import` with MD5/name/size; upload to returned COS key unless already present; `POST /files/async-import` with `parent` (folder ID), file information and COS key; persist `progressQueryID`; `GET /files/import-progress`. Progress 100 must return an editable doc ID/type/URL. Pending tasks are resumed without another import. The progress identifier expires after ten minutes, requiring host inspection/reconciliation if a run resumes later.

For readback, `GET /files/{id}/export`, download the DOCX without account headers to an allowlisted HTTPS storage host, and verify section text, embedded image and five hyperlink relationships. Required permissions include create/import plus `scope.drive.exportable` for this readback. If export is unavailable, retain the existing remote ID and pending receipt; inspect with authorized host tools instead of pretending the cloud document is verified. Do not grant permissions automatically. API receipts cannot be replaced with host attestations without an explicit new course/route, so agree on host mode upfront when API readback is unavailable.

UI fallback: import DOCX in the confirmed folder, open the editable result and inspect images/links. Local DOCX is only `awaiting_import` until an actual cloud document is verified.

Official sources checked 2026-10-14:
- https://docs.qq.com/open/document/app/openapi/v2/
- https://docs.qq.com/open/document/app/openapi/v2/file/import/cos_sdk_pre_import_in.html
- https://docs.qq.com/open/document/app/openapi/v2/file/import/async_import.html
- https://docs.qq.com/open/document/app/openapi/v2/file/import/import_progress.html
- https://docs.qq.com/open/document/app/openapi/v2/file/export/export_in.html
- https://github.com/tencentyun/cos-python-sdk-v5
