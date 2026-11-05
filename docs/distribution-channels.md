# Distribution channels

The latest GitHub release is [v4.1.0](https://github.com/ShawnRen57/omni-learning-anything/releases/tag/v4.1.0). The registry records below concern **2.6.0**. Repository-based skills.sh installs follow the repository source. Verify the version offered by the selected channel.

Checked on 2026-11-01 for Skill **2.6.0**. The GitHub release remains the source of truth: [v2.6.0](https://github.com/ShawnRen57/omni-learning-anything/releases/tag/v2.6.0), source commit `319415748fa4b02f1f85f5d0f89ccda59c239df6`.

| Channel | Verified status | Entry point |
| --- | --- | --- |
| skills.sh | Public detail page displays the actual Skill instructions and installation command; an isolated real GitHub installation passed the bundle completeness check at 2.6.0. | [Skill detail](https://skills.sh/shawnren57/omni-learning-anything/omni-learning-anything) |
| Tencent SkillHub | **Published 2.6.0**. The public page and official CLI search identify the correct publisher/version; an isolated official CLI installation returned 2.6.0 and all 64 file contents matched the release. | [Skill detail](https://skillhub.cn/skills/user_4c4c4339/omni-learning-anything) |
| ClawHub | The author approved additional MIT-0 licensing on 2026-11-01. The channel package is ready, but two spaced browser publication attempts failed with platform `CommitterFullError` (write capacity); official CLI device login also failed. **Blocked by the platform; not published.** | [Publishing page](https://clawhub.ai/skills/publish) |

## Install through skills.sh

With Node.js installed, run:

```sh
npx skills@latest add ShawnRen57/omni-learning-anything --skill omni-learning-anything -g
```

Choose your agent; omit `-g` for a project installation. After installation, follow [first use and safe updates](../skills/omni-learning-anything/references/install.md). Installing a Skill does not provide missing host tools or authorize cloud accounts.

The public page initially showed a missing Skill, then displayed its actual content after one real acceptance installation. [skills.sh documents automatic discovery from installation telemetry](https://skills.sh/docs/faq); no repeated installs were made to inflate metrics. Privacy preferences were preserved.

## Install through Tencent SkillHub

With the [official SkillHub CLI](https://skillhub.cn/tutorials) installed, use the publisher-qualified command:

```sh
skillhub install omni-learning-anything --namespace user_4c4c4339
```

Or download the ZIP from the [public detail page](https://skillhub.cn/skills/user_4c4c4339/omni-learning-anything). The namespace identifies this publisher and avoids selecting another author's similarly named Skill. Acceptance used official CLI 2026.8.5 and an isolated installation directory; no existing user Skill was overwritten.

### v2.6.0 registry inspection limitation

The bundled `installation inspect` command is stricter than this registry's packaging: it flags registry-added `_meta.json` and renamed `LICENSE.txt`, then reports `Missing LICENSE`. This is an observed compatibility limitation, not a missing Python module or permission failure. Do not delete registry metadata, discard a license, adopt the registry install as a managed GitHub ZIP, or claim its managed-ZIP integrity is verified.

For this acceptance, all 64 actual downloaded file contents were independently compared with the trusted release, accounting only for the documented license filename change. A separate temporary diagnostic copy, with the license filename normalized and registry metadata omitted, passed the bundled completeness inspection at 2.6.0; the actual registry installation was left unchanged. Native host discovery remains a separate check. Use SkillHub's original updater for this installation.

**Fixed in the v3.0.0 checker:** read-only unmanaged inspection recognizes this bounded public metadata shape, a matching Skill version and the license filename alias. Running the new checker against the unchanged actual SkillHub 2.6.0 installation reports completeness while retaining `integrity_verified: false`, native discovery unknown and update through the original manager. The older 2.6.0 checker's warning remains an historical limitation of that artifact. ZIP adoption and managed updates continue to reject registry extras; no installed file is deleted or rewritten by inspection.

## Package provenance

The original GitHub ZIP contains 64 files, SHA256 `e481ab58ac72fb1594797f08b9a9d584330449a07c7bc2ed8ccaba9a15a80eb7`. Every extracted file was checked against the release source.

SkillHub rejected the extensionless `LICENSE` file. Its channel ZIP renames only that file to `LICENSE.txt`; all 64 file contents remain byte-identical to the original release. Channel ZIP SHA256: `8ba909da37e29fe621e36bf1b166fd1b47f2219e2347b23db94f54d02bb3c133`. After security review, the dashboard showed **published**, and the public page offered 2.6.0. Official CLI installation downloaded the correct publisher-qualified artifact: all 64 contents matched, with only the documented license filename change and registry-added `_meta.json`. [Official publishing instructions](https://skillhub.cn/ai/release.md).

ClawHub's official CLI device authorization and GitHub web import returned server errors. The official folder-upload alternative parsed the 64-file bundle under publisher `shawnren57`, with version explicitly set to 2.6.0. Its [publishing requirements](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md#license) mandate MIT-0. With the author's explicit approval, the separate ClawHub copy changes only `LICENSE` to MIT No Attribution and the `SKILL.md` license field to `MIT-0`; the other 62 files are unchanged. The GitHub source, tag and original ZIP retain MIT and their original bytes. Both spaced browser publication attempts failed with `CommitterFullError: Too many writes in a short period of time`. A read-only public CLI inspection did not find an available Skill before the retry. A later official CLI device request returned a code but immediately failed polling with `Device flow error: unknown error`; no successful login or publication is claimed. No token was exported or copied into chat. Retry publication after the platform recovers, checking for an existing version before resubmitting; the author's MIT-0 approval remains recorded.

## Follow-up verification

After a platform approves a submission, verify the public owner, slug and version, then download/install into an isolated directory and compare the runtime files with the release. Add public install commands only after verifying the actual published artifact. A successful local dry-run, upload or pending-review response is not public availability.

Documentation checks passed for all ten README header links, relative file targets and balanced HTML containers. `git diff --check` passed. The original release ZIP checksum and all 64 file contents still match the unchanged Skill source. No runtime behavior changed in this channel-publication update; the full v2.6.0 test results remain in the [release validation record](release-validation-v2.6.0.md).
