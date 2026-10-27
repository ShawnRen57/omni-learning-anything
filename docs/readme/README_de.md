<div align="center">

<img src="../../docs/assets/omni-logo.png" alt="Omni Learning Anything logo" width="144" height="144">

# Omni Learning Anything

[![Release](https://img.shields.io/badge/version-2.2.0-237768)](https://github.com/ShawnRen57/omni-learning-anything/releases) [![License](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

[English](../../README.md) · [简体中文](README_zh.md) · [日本語](README_ja.md) · [한국어](README_ko.md) · [Español](README_es.md) · [Français](README_fr.md) · [Deutsch](README_de.md) · [Português](README_pt.md) · [Русский](README_ru.md) · [العربية](README_ar.md)

**[Skill ZIP herunterladen](https://github.com/ShawnRen57/omni-learning-anything/releases/latest/download/omni-learning-anything-skill-v2.2.0.zip)**

</div>

**Aus „Ich möchte lernen…“ wird ein Lernweg für jeden Tag.**

Nenne deinem Agenten dein Ziel, deine Vorkenntnisse und deine verfügbare Zeit. Omni erstellt einen Plan und tägliche Lektionen mit Abbildungen, Quellen, Übungen und Selbstkontrollen.

## Versionsübersicht

| Version | Deine Möglichkeiten |
| --- | --- |
| **v1** | Dein eigener PDF-Kurs: Bestätige den Plan und erhalte bebilderte Lektionen mit Übungen und weiterführender Literatur. |
| **v2** | Speichere deinen Kurs als lokale Dateien oder in Notion, Obsidian, Feishu, DingTalk und Tencent Docs. Der Agent begleitet die Verbindung und merkt sich den gewählten Ort. |
| **v2.2.0** | Lies HTML offline, lerne in 10 Sprachen und verbinde DingTalk oder Tencent Docs mit angeleiteter offizieller Anmeldung. |

## Lernen für deine Ziele

- Plane einen Lernweg für Reisen, Arbeit, Vorstellungsgespräche oder persönliche Interessen.
- Bestimme ein tägliches Zeitbudget für Erklärungen, Abbildungen, Übungen und Lösungshinweise.
- Prüfe Belege im Text und mindestens fünf erläuterte Literatur-Links je Dokument.
- Bestätige zuerst den Plan und setze nach einer Unterbrechung bei der ersten noch nicht gelieferten Lektion fort.

## Kurssprachen

**English · 简体中文 · 日本語 · 한국어 · Español · Français · Deutsch · Português · Русский · العربية**

Pläne und Lektionen lassen sich in diesen Sprachen erstellen. Kurssprache, Thema, Quellen und README-Sprache sind unabhängig. Arabisch wird von rechts nach links gesetzt.

## Speicherort auswählen

| Ziel | Angaben für den Agenten |
| --- | --- |
| PDF · HTML · DOCX · Markdown | Kursordner und Format. HTML enthält das Bild in einer einzigen Offline-Datei; externe Links benötigen Internet. |
| Notion | Link zur übergeordneten Seite und gewünschter Arbeitsbereich. |
| Obsidian | Bestehender lokaler Vault und Unterordner. Kein API-Schlüssel nötig. |
| Feishu | Kursordner-Link; bei Bedarf offizielle App einrichten und Benutzerzugriff erlauben. |
| DingTalk | Dokumentordner und Organisation. Ein Administrator muss gegebenenfalls den CLI-Zugriff aktivieren. |
| Tencent Docs | Stammordner der Startseite oder persönlicher Ordner; auf der offiziellen Seite anmelden und Berechtigungen prüfen. |

Der Agent prüft vorhandene Zugriffe, fragt nur nach fehlenden Angaben und erklärt die Schritte. Du musst keine Objekt-IDs suchen oder Konfigurationsdateien schreiben. Teile keine Passwörter oder Tokens im Chat. Organisatorische Freigaben können weitere Schritte erfordern.

## Im Chat beginnen

```text
Installiere das Skill ZIP der neuesten Release von https://github.com/ShawnRen57/omni-learning-anything.
Behalte den vollständigen Ordner und prüfe, ob der Agent den Skill findet.
```

```text
Hilf mir mit omni-learning-anything, Architekturgeschichte für Reisen zu lernen.
Ich bin Anfänger. Plane 30 Tage mit je 15 Minuten auf Deutsch.
Speichere den Kurs als Offline-HTML in meinem Kursordner. Zeige zuerst den Plan.
```

Prüfe und bestätige den Plan. Unterstützt dein Agent geplante Aufgaben, vereinbart ihr Uhrzeit und Zeitzone. Andernfalls bittest du bei Bedarf um Fortsetzung. Zur vereinbarten Zeit beginnt die Erstellung; Recherche und Prüfung gehen der Lieferung voraus.

```text
Setze bei der ersten noch nicht gelieferten Lektion fort.
Pausiere diesen Kurs und seinen Zeitplan.
Bewahre den bisherigen Kurs auf und schlage einen Plan für mein neues Ziel vor.
```

## Beispielkurse ansehen

Entdecke Pläne und tägliche PDFs zu Technologie, Wirtschaft, Musik, Agent-Produktdesign, Architektur und Ming-Geschichte. Die Archive behalten die ursprünglichen Prüfdaten ihrer Quellen.

| Technology | Economics | Music |
| :---: | :---: | :---: |
| [![Technology](../../docs/screenshots/technology.png)](../../examples/technology/) | [![Economics](../../docs/screenshots/economics.png)](../../examples/economics/) | [![Music](../../docs/screenshots/music.png)](../../examples/music/) |

| Agent products | Architecture | Ming history |
| :---: | :---: | :---: |
| [![Agent products](../../docs/screenshots/agent-product.png)](../../examples/agent-product/) | [![Architecture](../../docs/screenshots/architecture.png)](../../examples/architecture/) | [![Ming history](../../docs/screenshots/ming-history.png)](../../examples/ming-history/) |

## Installation und Anleitungen

[Im Agenten installieren](../../skills/omni-learning-anything/references/install.md) · [Formate und Schriftarten](../../skills/omni-learning-anything/references/setup.md) · [Dokumente verbinden](../../skills/omni-learning-anything/references/onboarding.md) · [Release-Prüfung](../../docs/release-validation-v2.2.0.md)

Dieser Agent Skill nutzt die Recherche-, Dokument- und Zeitplanwerkzeuge deines Agenten. Nur PDF benötigt XeLaTeX. Cloud-Dokumente verwenden offizielle APIs/CLIs; Obsidian schreibt in den lokalen Vault. Gerätesynchronisierung und unbeaufsichtigte Ausführung hängen von Host und Konto ab.

[MIT](../../LICENSE) · [Changelog](../../CHANGELOG.md)
