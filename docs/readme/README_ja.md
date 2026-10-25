<div align="center">

![Omni Learning Anything](../../docs/assets/omni-banner.svg)

# Omni Learning Anything

[![Release](https://img.shields.io/badge/version-2.2.0-237768)](https://github.com/ShawnRen57/omni-learning-anything/releases) [![License](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

[English](../../README.md) · [简体中文](README_zh.md) · [日本語](README_ja.md) · [한국어](README_ko.md) · [Español](README_es.md) · [Français](README_fr.md) · [Deutsch](README_de.md) · [Português](README_pt.md) · [Русский](README_ru.md) · [العربية](README_ar.md)

**[Skill ZIP をダウンロード](https://github.com/ShawnRen57/omni-learning-anything/releases/latest/download/omni-learning-anything-skill-v2.2.0.zip)**

</div>

**「学びたい」を、毎日続けられる学習コースに。**

目標、経験、使える時間を Agent に伝えると、Omni が学習計画を作り、図解、出典、練習、自己確認を含む毎日の教材で学習を支えます。

## バージョン案内

| バージョン | できること |
| --- | --- |
| **v1** | 自分専用の PDF コース。計画を確認してから、図解、練習、参考資料付きの教材を受け取れます。 |
| **v2** | ローカルファイル、Notion、Obsidian、Feishu、DingTalk、Tencent Docs から保存先を選べます。Agent が接続を案内し、選んだ場所を再利用します。 |
| **v2.2.0** | オフラインで読める単一 HTML ファイル、10 言語のコース、DingTalk と Tencent Docs の公式認証案内を追加しました。 |

## 自分に合った学び方

- 旅行、仕事、面接、趣味など、目的に合わせて学びます。
- 1 日の学習時間を決め、説明、図、練習と回答のヒントを読み進めます。
- 文中の引用と、各教材に最低 5 件ある説明付きの参考リンクから、根拠を確認できます。
- 最初に計画を承認し、中断したら未配信の最初の授業から再開できます。

## 学習言語

**English · 简体中文 · 日本語 · 한국어 · Español · Français · Deutsch · Português · Русский · العربية**

計画も毎日の教材も、上記の言語で作成できます。教材の言語は、テーマ、出典、README の言語とは別に選べます。アラビア語は右から左への組版に対応します。

## 保存先を選ぶ

| 保存先 | Agent に伝える情報 |
| --- | --- |
| PDF · HTML · DOCX · Markdown | コース用フォルダーと形式。HTML は画像を内蔵した単一ファイルで、外部の参考リンク以外はオフラインで読めます。 |
| Notion | 親ページのリンクと使用するワークスペース。 |
| Obsidian | 既存のローカル Vault とコースのサブフォルダー。API キーは不要です。 |
| Feishu | コース用フォルダーのリンク。必要に応じて公式アプリの設定とユーザー認証を行います。 |
| DingTalk | 文書フォルダーのリンクと組織。管理者による CLI アクセスの有効化が必要な場合があります。 |
| Tencent Docs | ホームのルート、または個人フォルダーのリンク。公式ページでログインして権限を確認します。 |

Agent は既存の認証を確認し、不足情報だけを尋ね、設定手順を案内します。ID の調査や設定ファイルの手書きは不要です。パスワードや Token をチャットに貼り付けないでください。組織の承認には追加の手順が必要な場合があります。

## チャットから始める

Agent に次のように依頼します。

```text
https://github.com/ShawnRen57/omni-learning-anything の最新 Release から Skill ZIP をインストールしてください。
フォルダー全体を保持し、スキルを利用できることを確認してください。
```

```text
omni-learning-anything で旅行のための建築史を学びたいです。
初心者向けに 30 日、1 日 15 分、日本語で計画してください。
教材はコース用フォルダーにオフライン HTML で保存してください。まず計画を見せてください。
```

計画を確認して承認します。スケジュール対応の Agent では実行時刻とタイムゾーンも決められます。それ以外は準備ができたときに続きを依頼します。指定時刻に生成を開始し、調査と確認後に配信します。

```text
未配信の最初の授業から再開してください。
このコースとスケジュールを一時停止してください。
以前のコースを残して、新しい目標の計画を提案してください。
```

## コースの実例

科学技術、経済学、音楽、Agent 製品設計、建築史、明代史の計画と毎日の PDF をご覧ください。アーカイブには当初の出典確認日が残っています。

| Technology | Economics | Music |
| :---: | :---: | :---: |
| [![Technology](../../docs/screenshots/technology.png)](../../examples/technology/) | [![Economics](../../docs/screenshots/economics.png)](../../examples/economics/) | [![Music](../../docs/screenshots/music.png)](../../examples/music/) |

| Agent products | Architecture | Ming history |
| :---: | :---: | :---: |
| [![Agent products](../../docs/screenshots/agent-product.png)](../../examples/agent-product/) | [![Architecture](../../docs/screenshots/architecture.png)](../../examples/architecture/) | [![Ming history](../../docs/screenshots/ming-history.png)](../../examples/ming-history/) |

## インストールとガイド

[Agent へのインストール](../../skills/omni-learning-anything/references/install.md) · [形式とフォントの設定](../../skills/omni-learning-anything/references/setup.md) · [文書の接続](../../skills/omni-learning-anything/references/onboarding.md) · [リリース検証](../../docs/release-validation-v2.2.0.md)

これは Agent の調査・文書・スケジュール機能を使う Agent Skill です。XeLaTeX が必要なのは PDF のみです。クラウド文書は公式 API/CLI を使用し、Obsidian はローカル Vault に書き込みます。端末間の同期と無人実行はホストとアカウントの条件に依存します。

[MIT](../../LICENSE) · [Changelog](../../CHANGELOG.md)
