<div align="center">

<img src="../../docs/assets/omni-logo.png" alt="Omni Learning Anything logo" width="144" height="144">

# Omni Learning Anything

[![Release](https://img.shields.io/badge/version-2.2.0-237768)](https://github.com/ShawnRen57/omni-learning-anything/releases) [![License](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

[English](../../README.md) · [简体中文](README_zh.md) · [日本語](README_ja.md) · [한국어](README_ko.md) · [Español](README_es.md) · [Français](README_fr.md) · [Deutsch](README_de.md) · [Português](README_pt.md) · [Русский](README_ru.md) · [العربية](README_ar.md)

**[Descargar Skill ZIP](https://github.com/ShawnRen57/omni-learning-anything/releases/latest/download/omni-learning-anything-skill-v2.2.0.zip)**

</div>

**Convierte «quiero aprender…» en un curso que puedas seguir cada día.**

Cuéntale a tu agente tu objetivo, tus conocimientos y el tiempo disponible. Omni prepara un plan y lecciones diarias con ilustraciones, fuentes, ejercicios y autoevaluación.

## Guía de versiones

| Versión | Qué puedes hacer |
| --- | --- |
| **v1** | Tener un curso personal en PDF: aprueba el plan y recibe lecciones ilustradas con ejercicios y lecturas complementarias. |
| **v2** | Guardar el curso en archivos locales, Notion, Obsidian, Feishu, DingTalk o Tencent Docs. El agente guía la conexión y recuerda el destino elegido. |
| **v2.2.0** | Leer HTML sin conexión, generar cursos en 10 idiomas y autorizar DingTalk o Tencent Docs con la ayuda del agente. |

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

[Instalar en tu agente](../../skills/omni-learning-anything/references/install.md) · [Formatos y fuentes](../../skills/omni-learning-anything/references/setup.md) · [Conectar documentos](../../skills/omni-learning-anything/references/onboarding.md) · [Validación de la versión](../../docs/release-validation-v2.2.0.md)

Es una Agent Skill que utiliza las herramientas de investigación, documentos y programación de tu agente. Solo PDF necesita XeLaTeX. La nube usa API/CLI oficiales; Obsidian escribe en el Vault local. La sincronización y la ejecución desatendida dependen del agente y la cuenta.

[MIT](../../LICENSE) · [Changelog](../../CHANGELOG.md)
