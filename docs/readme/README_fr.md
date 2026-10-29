<div align="center">

<img src="../../docs/assets/omni-wordmark.png" alt="Omni Learning Anything brush wordmark" width="640">

# Omni Learning Anything

[![Release](https://img.shields.io/badge/version-2.2.0-237768)](https://github.com/ShawnRen57/omni-learning-anything/releases) [![License](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

[English](../../README.md) · [简体中文](README_zh.md) · [日本語](README_ja.md) · [한국어](README_ko.md) · [Español](README_es.md) · [Français](README_fr.md) · [Deutsch](README_de.md) · [Português](README_pt.md) · [Русский](README_ru.md) · [العربية](README_ar.md)

**[Télécharger le Skill ZIP](https://github.com/ShawnRen57/omni-learning-anything/releases/latest/download/omni-learning-anything-skill-v2.2.0.zip)**

</div>

**Transformez « je veux apprendre… » en un parcours à suivre chaque jour.**

Indiquez à votre agent votre objectif, votre expérience et le temps disponible. Omni prépare un plan, puis des leçons quotidiennes avec illustrations, sources, exercices et autoévaluation.

## Guide des versions

| Version | Ce que vous pouvez faire |
| --- | --- |
| **v1** | Suivre votre propre cours en PDF : validez le plan, puis recevez des leçons illustrées avec exercices et lectures complémentaires. |
| **v2** | Conserver le cours dans des fichiers locaux, Notion, Obsidian, Feishu, DingTalk ou Tencent Docs. L’agent vous guide et mémorise l’emplacement choisi. |
| **v2.2.0** | Lire un fichier HTML hors ligne, suivre un cours en 10 langues et autoriser DingTalk ou Tencent Docs avec l’aide de l’agent. |

## Apprendre à votre rythme

- Préparez un voyage, un projet professionnel, un entretien ou explorez un centre d’intérêt.
- Réservez un temps quotidien adapté aux explications, illustrations, exercices et pistes de réponse.
- Consultez les citations et au moins cinq liens commentés dans chaque document.
- Validez d’abord le plan et reprenez à la première leçon non remise après une interruption.

## Langues du cours

**English · 简体中文 · 日本語 · 한국어 · Español · Français · Deutsch · Português · Русский · العربية**

Les plans et les leçons peuvent être rédigés dans ces langues. La langue du cours est indépendante du sujet, des sources et du README. L’arabe bénéficie d’une mise en page de droite à gauche.

## Choisir où conserver le cours

| Destination | Informations à donner à l’agent |
| --- | --- |
| PDF · HTML · DOCX · Markdown | Dossier et format du cours. Le HTML contient l’image dans un seul fichier hors ligne ; les liens externes nécessitent Internet. |
| Notion | Lien de la page parente et espace de travail. |
| Obsidian | Vault local existant et sous-dossier. Aucune clé API nécessaire. |
| Feishu | Lien du dossier ; configuration de l’application officielle et autorisation utilisateur si nécessaire. |
| DingTalk | Lien du dossier et organisation. L’administrateur devra parfois activer l’accès CLI. |
| Tencent Docs | Racine de l’accueil ou dossier personnel ; connexion et vérification des droits sur la page officielle. |

L’agent vérifie les accès existants, demande seulement les informations manquantes et explique les démarches. Vous n’avez pas à rechercher des identifiants ni à écrire des fichiers de configuration. Ne collez pas de mots de passe ou de tokens dans la conversation. Les validations de votre organisation peuvent ajouter des étapes.

## Commencer dans la conversation

```text
Installe le Skill ZIP de la dernière Release de https://github.com/ShawnRen57/omni-learning-anything.
Conserve le dossier complet et vérifie que l’agent peut découvrir la compétence.
```

```text
Utilise omni-learning-anything pour m’enseigner l’histoire de l’architecture pour voyager.
Je débute. Prévois 30 jours, 15 minutes par jour, en français.
Enregistre le cours en HTML hors ligne dans mon dossier. Montre-moi d’abord le plan.
```

Relisez et validez le plan. Si votre agent permet la programmation, convenez de l’heure et du fuseau horaire ; sinon, demandez la suite lorsque vous êtes prêt. L’heure prévue lance la génération ; la remise suit la recherche et la vérification.

```text
Reprends à la première leçon qui n’a pas encore été remise.
Mets en pause ce cours et sa programmation.
Conserve l’ancien cours et propose un plan pour mon nouvel objectif.
```

## Découvrir les exemples

Consultez les plans et PDF quotidiens de technologie, économie, musique, conception de produits Agent, architecture et histoire Ming. Les archives conservent leurs dates initiales de vérification des sources.

| Technology | Economics | Music |
| :---: | :---: | :---: |
| [![Technology](../../docs/screenshots/technology.png)](../../examples/technology/) | [![Economics](../../docs/screenshots/economics.png)](../../examples/economics/) | [![Music](../../docs/screenshots/music.png)](../../examples/music/) |

| Agent products | Architecture | Ming history |
| :---: | :---: | :---: |
| [![Agent products](../../docs/screenshots/agent-product.png)](../../examples/agent-product/) | [![Architecture](../../docs/screenshots/architecture.png)](../../examples/architecture/) | [![Ming history](../../docs/screenshots/ming-history.png)](../../examples/ming-history/) |

## Installation et guides

[Installer dans votre agent](../../skills/omni-learning-anything/references/install.md) · [Formats et polices](../../skills/omni-learning-anything/references/setup.md) · [Connecter vos documents](../../skills/omni-learning-anything/references/onboarding.md) · [Validation de la version](../../docs/release-validation-v2.2.0.md)

Cette Agent Skill utilise les outils de recherche, de documents et de programmation de votre agent. Seul le PDF nécessite XeLaTeX. Les documents cloud utilisent les API/CLI officielles ; Obsidian écrit dans le Vault local. La synchronisation et l’exécution sans surveillance dépendent de l’hôte et du compte.

[MIT](../../LICENSE) · [Changelog](../../CHANGELOG.md)
