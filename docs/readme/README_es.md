<div align="center">

<img src="../../docs/assets/omni-wordmark-transparent.png" alt="Omni Learning Anything brush wordmark" width="520">

# Omni Learning Anything

[![Release](https://img.shields.io/github/v/release/ShawnRen57/omni-learning-anything?style=flat-square&color=237768&label=release)](https://github.com/ShawnRen57/omni-learning-anything/releases/latest)
[![Agent Skill](https://img.shields.io/badge/Agent-Skill-7c3aed?style=flat-square)](../../skills/omni-learning-anything/SKILL.md)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](../../skills/omni-learning-anything/references/setup.md)
[![Course languages](https://img.shields.io/badge/languages-10-0284c7?style=flat-square)](../../README.md#choose-your-learning-language)
[![Output formats](https://img.shields.io/badge/formats-4-0f766e?style=flat-square)](../../skills/omni-learning-anything/references/setup.md)
[![MIT License](https://img.shields.io/badge/license-MIT-2563eb?style=flat-square)](../../LICENSE)
[![Release downloads](https://img.shields.io/github/downloads/ShawnRen57/omni-learning-anything/total?style=flat-square&color=0891b2&label=downloads)](https://github.com/ShawnRen57/omni-learning-anything/releases)
[![GitHub stars](https://img.shields.io/github/stars/ShawnRen57/omni-learning-anything?style=flat-square&color=b7791f)](https://github.com/ShawnRen57/omni-learning-anything/stargazers)

[English](../../README.md) · [简体中文](README_zh.md) · [日本語](README_ja.md) · [한국어](README_ko.md) · [Español](README_es.md) · [Français](README_fr.md) · [Deutsch](README_de.md) · [Português](README_pt.md) · [Русский](README_ru.md) · [العربية](README_ar.md)

**[Descargar Skill ZIP](https://github.com/ShawnRen57/omni-learning-anything/releases/latest/download/omni-learning-anything-skill-v2.6.0.zip)**

[skills.sh](https://skills.sh/shawnren57/omni-learning-anything/omni-learning-anything) · [Tencent SkillHub](https://skillhub.cn/skills/user_4c4c4339/omni-learning-anything) · [Notas de instalación](../distribution-channels.md)

</div>

**Convierte «quiero aprender…» en un curso que puedas seguir cada día.**

Cuéntale a tu agente tu objetivo, tus conocimientos y el tiempo disponible. Omni prepara un plan y lecciones diarias con ilustraciones, fuentes, ejercicios y autoevaluación.

## Guía de versiones

| Versión | Qué puedes hacer |
| --- | --- |
| **v1** | Tener un curso personal en PDF: aprueba el plan y recibe lecciones ilustradas con ejercicios y lecturas complementarias. |
| **v2** | Guardar el curso en archivos locales, Notion, Obsidian, Feishu, DingTalk o Tencent Docs. El agente guía la conexión y recuerda el destino elegido. |
| **v2.2.0** | Leer HTML sin conexión, generar cursos en 10 idiomas y autorizar DingTalk o Tencent Docs con la ayuda del agente. |
| **v2.2.1** | Empieza con una idea general: el agente aclara el enfoque, organiza los conocimientos previos, propone un curso estructurado y comprueba las capacidades del entorno. |
| **v2.3.0** | Comprueba lo aprendido cuando quieras con preguntas breves y comentarios fundamentados; puedes pedir pistas, saltar y continuar. Sin recordatorios ni tareas programadas de cuestionarios. |
| **v2.4.0** | Aprende con tus libros, artículos y materiales de curso: elige páginas o capítulos, consulta el origen de las explicaciones y decide si permites fuentes externas. |
| **v2.5.0** | Al volver, repasa un poco dentro de tu tiempo diario, consulta lo que muestran tus respuestas, corrige valoraciones, aprueba cambios en futuras lecciones y exporta tarjetas a Anki. |
| **v2.6.0** | Instala desde el chat, con un comando o con el instalador de tu agente. Comprueba solo lo necesario y actualiza conservando cursos y conexiones. |

Basta con decir «Quiero aprender algo de economía». Omni propone enfoques y una secuencia coherente, señala los supuestos y pregunta solo lo que cambia el curso. Si el objetivo ya es concreto, pasa a planificar.

## Aprende a tu ritmo

- Diseña una ruta para viajar, trabajar, preparar una entrevista o explorar una afición.
- Ajusta el tiempo diario para explicaciones, ilustraciones, práctica y orientación sobre las respuestas.
- Consulta las citas del texto y al menos cinco enlaces comentados en cada documento.
- Revisa el plan antes de empezar y retoma la primera lección pendiente después de una interrupción.

## Idiomas del curso

**English · 简体中文 · 日本語 · 한국어 · Español · Français · Deutsch · Português · Русский · العربية**

Tanto los planes como las lecciones pueden redactarse en estos idiomas. El idioma del curso es independiente del tema, las fuentes y este README. El árabe admite escritura de derecha a izquierda.

## Elige dónde guardar el curso

| Destino | Qué indicar al agente |
| --- | --- |
| PDF · HTML · DOCX · Markdown | Carpeta del curso y formato. HTML incluye la imagen en un solo archivo sin conexión; los enlaces externos necesitan Internet. |
| Notion | Enlace a la página principal y espacio de trabajo. |
| Obsidian | Vault local existente y subcarpeta. No necesita una clave API. |
| Feishu | Enlace a la carpeta; configura la aplicación oficial y autoriza tu usuario si hace falta. |
| DingTalk | Carpeta de documentos y organización. El administrador puede tener que habilitar el acceso CLI. |
| Tencent Docs | Raíz de inicio o carpeta personal; inicia sesión y revisa los permisos en la página oficial. |

El agente comprueba los accesos existentes, pregunta solo por lo que falta y explica los pasos. No tienes que buscar identificadores ni escribir archivos de configuración. No pegues contraseñas ni tokens en el chat. Las aprobaciones de la organización pueden requerir más pasos.

## Elige cómo instalar

Pide al agente que instale la última versión, conserve tus cursos y conexiones y confirme que el cliente puede detectar y usar la habilidad.

Con Node.js, ejecuta este comando y elige tu agente. Omite `-g` para instalar solo en el proyecto.

```sh
npx skills@latest add ShawnRen57/omni-learning-anything --skill omni-learning-anything -g
```

En Claude Code:

```text
/plugin install omni-learning-anything --marketplace ShawnRen57/omni-learning-anything
```

Sin Node.js, descarga el Skill ZIP de arriba y súbelo a tu cliente, o pide al agente que lo instale. [Instalación, primer uso y actualizaciones seguras](../../skills/omni-learning-anything/references/install.md)

## Empieza conversando

```text
Instala el Skill ZIP de la última Release de https://github.com/ShawnRen57/omni-learning-anything.
Conserva la carpeta completa y comprueba que el agente puede descubrir la habilidad.
```

```text
Usa omni-learning-anything para enseñarme historia de la arquitectura para viajar.
Soy principiante. Quiero 30 días, 15 minutos diarios, en español.
Guarda el curso como HTML sin conexión en mi carpeta. Muéstrame primero el plan.
```

Revisa y aprueba el plan. Si tu agente permite programar tareas, acuerda la hora y la zona horaria; si no, pide continuar cuando estés listo. La generación comienza a la hora indicada y la entrega sigue a la investigación y revisión.

```text
Continúa desde la primera lección que aún no se haya entregado.
Pausa este curso y su programación.
Conserva el curso anterior y propón un plan para mi nuevo objetivo.
```

## Explora los ejemplos

Consulta planes y PDF diarios de tecnología, economía, música, diseño de productos Agent, arquitectura e historia Ming. Los archivos conservan sus fechas originales de comprobación de fuentes.

| Technology | Economics | Music |
| :---: | :---: | :---: |
| [![Technology](../../docs/screenshots/technology.png)](../../examples/technology/) | [![Economics](../../docs/screenshots/economics.png)](../../examples/economics/) | [![Music](../../docs/screenshots/music.png)](../../examples/music/) |

| Agent products | Architecture | Ming history |
| :---: | :---: | :---: |
| [![Agent products](../../docs/screenshots/agent-product.png)](../../examples/agent-product/) | [![Architecture](../../docs/screenshots/architecture.png)](../../examples/architecture/) | [![Ming history](../../docs/screenshots/ming-history.png)](../../examples/ming-history/) |

## Instalación y guías

[Instalar en tu agente](../../skills/omni-learning-anything/references/install.md) · [Formatos y fuentes](../../skills/omni-learning-anything/references/setup.md) · [Conectar documentos](../../skills/omni-learning-anything/references/onboarding.md) · [Validación de la versión](../../docs/release-validation-v2.6.0.md)

Es una Agent Skill que utiliza las herramientas de investigación, documentos y programación de tu agente. Solo PDF necesita XeLaTeX. La nube usa API/CLI oficiales; Obsidian escribe en el Vault local. La sincronización y la ejecución desatendida dependen del agente y la cuenta.

[MIT](../../LICENSE) · [Changelog](../../CHANGELOG.md)
