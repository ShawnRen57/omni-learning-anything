# Distribution channels

Checked on 2026-11-01 for Skill **2.6.0**. The GitHub release remains the source of truth: [v2.6.0](https://github.com/ShawnRen57/omni-learning-anything/releases/tag/v2.6.0), source commit `319415748fa4b02f1f85f5d0f89ccda59c239df6`.

| Channel | Verified status | Entry point |
| --- | --- | --- |
| skills.sh | Public detail page displays the actual Skill instructions and installation command; an isolated real GitHub installation passed the bundle completeness check at 2.6.0. | [Skill detail](https://skills.sh/shawnren57/omni-learning-anything/omni-learning-anything) |
| Tencent SkillHub | Submitted through the official website; publisher dashboard and version history show **2.6.0, security review pending**. Public installation has not yet been verified. | [Publisher dashboard](https://skillhub.cn/dashboard) (owner login required) |
| ClawHub | Local official CLI preflight passed; browser upload prepared. Publication awaits the author's explicit acceptance of ClawHub's MIT-0 license requirement. No published listing or installation is claimed. | [Publishing page](https://clawhub.ai/skills/publish) |

## Install through skills.sh

With Node.js installed, run:

```sh
npx skills@latest add ShawnRen57/omni-learning-anything --skill omni-learning-anything -g
```

Choose your agent; omit `-g` for a project installation. After installation, follow [first use and safe updates](../skills/omni-learning-anything/references/install.md). Installing a Skill does not provide missing host tools or authorize cloud accounts.

The public page initially showed a missing Skill, then displayed its actual content after one real acceptance installation. [skills.sh documents automatic discovery from installation telemetry](https://skills.sh/docs/faq); no repeated installs were made to inflate metrics. Privacy preferences were preserved.

## Package provenance

The original GitHub ZIP contains 64 files, SHA256 `e481ab58ac72fb1594797f08b9a9d584330449a07c7bc2ed8ccaba9a15a80eb7`. Every extracted file was checked against the release source.

SkillHub rejected the extensionless `LICENSE` file. Its channel ZIP renames only that file to `LICENSE.txt`; all 64 file contents remain byte-identical to the original release. Channel ZIP SHA256: `8ba909da37e29fe621e36bf1b166fd1b47f2219e2347b23db94f54d02bb3c133`. The website accepted this package and created the pending 2.6.0 version. This does not mean security review or public download has passed. [Official publishing instructions](https://skillhub.cn/ai/release.md).

ClawHub's official CLI device authorization and GitHub web import returned server errors. The official folder-upload alternative successfully parsed the original 64-file bundle under publisher `shawnren57`, with version explicitly set to 2.6.0. Its [publishing requirements](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md#license) mandate MIT-0, whereas the GitHub source is MIT; that difference requires a separate author decision before submission.

## Follow-up verification

After a platform approves a submission, verify the public owner, slug and version, then download/install into an isolated directory and compare the runtime files with the release. Add public install commands only after verifying the actual published artifact. A successful local dry-run, upload or pending-review response is not public availability.

Documentation checks passed for all ten README header links, relative file targets and balanced HTML containers. `git diff --check` passed. The original release ZIP checksum and all 64 file contents still match the unchanged Skill source. No runtime behavior changed in this channel-publication update; the full v2.6.0 test results remain in the [release validation record](release-validation-v2.6.0.md).
