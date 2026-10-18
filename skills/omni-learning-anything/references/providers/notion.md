# Notion

Prefer a writable host Notion connector; inspect its creation, media and readback schemas. Search-only connectors cannot deliver documents. Without one use `platform: notion`, `mode: api`, `destination.parent_page_id`, `credential_env.token`. The parent must be a confirmed course page shared with the integration. Extract a page ID from a supplied URL; preserve UUID hyphens consistently.

The bundled adapter pins `Notion-Version: 2026-03-11`, uploads a PNG/JPEG (<=20 MB) through `/v1/file_uploads` and `/send`, creates a Markdown page through `/v1/pages`, and attaches a file-upload image block. It removes local image paths before cloud creation. It reads page parent/title, all root image blocks and Markdown sections/source links before verifying. A page returned from create is not by itself verified.

Grant only the needed insert/read capabilities to the chosen parent. Keep the token outside course/repository in the named environment variable. Published content lives under the course parent; page IDs and upload IDs are saved for recovery. No key is requested when the host connector supplies equivalent access.

If Markdown API rejects a lesson size/format, preserve the existing pending page and use authorized host/block tools to complete it; do not create another page blindly. Uploaded unattached files expire after one hour: if a pending upload expires, reconcile the known page or start a explicitly confirmed new course version; never conceal missing media. Free account upload limits may be lower than the API's 20 MB maximum.

For UI import, `mode: import` now defaults to embedded DOCX plus Markdown; `publish` points to the DOCX. Existing reviewed Markdown-only imports remain resumable and require their referenced image. In the Word importer, explicitly select the confirmed course parent. The importer may use the filename as the page title and omit the Word title: inspect and rename the actual page to the intended plan/lesson title. Reopen it from the parent and inspect the full text, rendered figure/caption and all five exact source URLs before recording a receipt. An import-complete dialog alone does not verify content. Reuse the same page on repeat publish. Login/UI availability cannot guarantee unattended daily delivery.

Real-account acceptance on 2026-10-18: plan and Day01 Word imports, bilingual content, image/credit, five URL destinations per page, parent placement, reopen and verified-receipt reuse passed. This does not validate the direct API route.

Official sources checked 2026-10-14:
- https://developers.notion.com/guides/data-apis/working-with-markdown-content
- https://developers.notion.com/guides/data-apis/uploading-small-files
- https://developers.notion.com/reference/patch-block-children
