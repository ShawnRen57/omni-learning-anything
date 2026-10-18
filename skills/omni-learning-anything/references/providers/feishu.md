# 飞书 / Feishu

Prefer authorized writable host tools. API mode needs a confirmed course `destination.folder_token`, and either `credential_env.token` (user/tenant token supplied by a private loader) or `credential_env.app_id` + `credential_env.app_secret`. The app/identity must have access to the folder; a tenant app's document ownership is different from the learner's personal account. Confirm that the learner can actually open the result. The bundled endpoint is Feishu (`open.feishu.cn`), not a silently substituted international Lark tenant.

API flow: upload embedded-image DOCX to `/drive/v1/medias/upload_all` with `parent_type=ccm_import_open`; create `/drive/v1/import_tasks` with `type=docx`, `file_extension=docx`, and confirmed folder mount; persist ticket; query `/drive/v1/import_tasks/{ticket}`. Success is `job_status=0` plus a document token/URL. A processing result remains pending. Read `/docx/v1/documents/{id}/raw_content` and paginated `/blocks` to check sections, image block and all hyperlinks. No local image path is sent to the cloud.

Ask for the minimum documented scopes for media upload, document import/read and the selected folder; verify actual API permissions rather than inferring them from app publication. App credentials stay only in the named environment. Tokens are not persisted. Folder/doc tokens in the receipt are object identifiers, not account credentials.

UI fallback: import the embedded DOCX through the user's confirmed folder and choose conversion into a Feishu document, not a file attachment. Open the result, inspect all content and record the actual document URL/ID. Manual import is not an unattended automation claim. If upload stalls or fails, inspect the existing transfer task and destination before retrying; a file picker selection or upload queue entry is not a cloud document. Preserve the existing course and diagnose the actual failure before creating another upload.

Real-account attempt on 2026-10-18: the personal QA folder was created, but Word-to-online-document upload failed at 0B; retrying the same task once also failed, leaving the folder empty. This route remains unaccepted; the local DOCX was visually checked separately.

Official sources checked 2026-10-14:
- https://open.feishu.cn/document/server-docs/docs/drive-v1/import_task/import-user-guide
- https://open.feishu.cn/document/server-docs/docs/drive-v1/import_task/create
- https://open.feishu.cn/document/server-docs/docs/drive-v1/import_task/get
- https://open.feishu.cn/document/server-docs/docs/drive-v1/media/upload_all
- https://github.com/larksuite/oapi-sdk-python/tree/v2_main/lark_oapi/api/drive/v1/model
- https://www.feishu.cn/hc/en-US/articles/360033241654-upload-or-import-local-files-and-folders
