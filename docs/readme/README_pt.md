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

**[Descarregar Skill ZIP](https://github.com/ShawnRen57/omni-learning-anything/releases/latest/download/omni-learning-anything-skill-v2.6.0.zip)**

[skills.sh](https://skills.sh/shawnren57/omni-learning-anything/omni-learning-anything)

</div>

**Transforme «quero aprender…» num percurso para seguir todos os dias.**

Diga ao seu agente qual é o objetivo, a sua experiência e o tempo disponível. O Omni prepara um plano e aulas diárias com ilustrações, fontes, exercícios e autoavaliação.

## Guia de versões

| Versão | O que pode fazer |
| --- | --- |
| **v1** | Ter um curso pessoal em PDF: aprove o plano e receba aulas ilustradas com exercícios e leituras complementares. |
| **v2** | Guardar o curso em ficheiros locais, Notion, Obsidian, Feishu, DingTalk ou Tencent Docs. O agente orienta a ligação e recorda o destino escolhido. |
| **v2.2.0** | Ler HTML offline, criar cursos em 10 idiomas e autorizar DingTalk ou Tencent Docs com orientação do agente. |
| **v2.2.1** | Comece com uma ideia geral: o agente esclarece a direção, organiza os pré-requisitos, propõe um curso estruturado e verifica os recursos disponíveis no ambiente. |
| **v2.3.0** | Confira o que aprendeu quando quiser, com perguntas curtas e feedback fundamentado. Peça dicas, pule e retome. Sem lembretes ou tarefas agendadas de questionários. |
| **v2.4.0** | Aprenda com seus livros, artigos e materiais de curso: selecione páginas ou capítulos, confira os trechos originais e escolha se permite fontes externas. |
| **v2.5.0** | Ao voltar, faça uma pequena revisão dentro do seu tempo diário, veja o que suas respostas mostram, corrija avaliações, aprove mudanças nas próximas aulas e exporte cartões para o Anki. |
| **v2.6.0** | Instale pelo chat, com um comando ou pelo seu agente. Verifique só o necessário e atualize preservando cursos e conexões. |

Você pode dizer apenas “Quero aprender um pouco de economia”. Omni sugere caminhos e uma sequência coerente, explicita suposições e pergunta apenas o que muda o curso. Se o objetivo já for claro, passa ao planejamento.

## Aprender ao seu ritmo

- Prepare uma viagem, um projeto de trabalho, uma entrevista ou explore um interesse pessoal.
- Defina um tempo diário para explicações, ilustrações, prática e orientação sobre as respostas.
- Consulte as citações e pelo menos cinco ligações comentadas em cada documento.
- Reveja primeiro o plano e retome a primeira aula ainda não entregue após uma interrupção.

## Idiomas do curso

**English · 简体中文 · 日本語 · 한국어 · Español · Français · Deutsch · Português · Русский · العربية**

Os planos e as aulas podem ser escritos nestes idiomas. O idioma do curso é independente do tema, das fontes e do README. O árabe utiliza disposição da direita para a esquerda.

## Escolher onde guardar o curso

| Destino | O que indicar ao agente |
| --- | --- |
| PDF · HTML · DOCX · Markdown | Pasta do curso e formato. HTML inclui a imagem num único ficheiro offline; as ligações externas precisam de Internet. |
| Notion | Ligação à página principal e espaço de trabalho. |
| Obsidian | Vault local existente e subpasta. Não precisa de uma chave API. |
| Feishu | Ligação à pasta; configure a aplicação oficial e autorize o utilizador se necessário. |
| DingTalk | Pasta de documentos e organização. O administrador poderá ter de ativar o acesso CLI. |
| Tencent Docs | Raiz da página inicial ou pasta pessoal; inicie sessão e confira as permissões na página oficial. |

O agente verifica os acessos existentes, pergunta apenas pelo que falta e explica os passos. Não precisa de procurar identificadores nem de escrever ficheiros de configuração. Não cole palavras-passe ou tokens na conversa. As aprovações da organização podem exigir passos adicionais.

## Escolha como instalar

Peça ao agente para instalar a versão mais recente, preservar cursos e conexões e confirmar que o cliente consegue encontrar e usar a habilidade.

Com Node.js, execute o comando abaixo e escolha seu agente. Omita `-g` para instalar apenas no projeto.

```sh
npx skills@latest add ShawnRen57/omni-learning-anything --skill omni-learning-anything -g
```

No Claude Code:

```text
/plugin install omni-learning-anything --marketplace ShawnRen57/omni-learning-anything
```

Sem Node.js, baixe o Skill ZIP acima e importe no cliente, ou peça ao agente para instalar. [Instalação, primeiro uso e atualizações seguras](../../skills/omni-learning-anything/references/install.md)

## Começar pela conversa

```text
Instala o Skill ZIP da última Release de https://github.com/ShawnRen57/omni-learning-anything.
Mantém a pasta completa e confirma que o agente encontra a competência.
```

```text
Usa omni-learning-anything para me ensinar história da arquitetura para viajar.
Sou principiante. Planeia 30 dias, 15 minutos por dia, em português.
Guarda o curso em HTML offline na minha pasta. Mostra primeiro o plano.
```

Reveja e aprove o plano. Se o agente suportar agendamento, combine a hora e o fuso horário; caso contrário, peça para continuar quando estiver pronto. A geração começa à hora marcada e a entrega segue-se à pesquisa e verificação.

```text
Continua a partir da primeira aula ainda não entregue.
Pausa este curso e o respetivo agendamento.
Preserva o curso anterior e propõe um plano para o meu novo objetivo.
```

## Explorar exemplos

Consulte planos e PDFs diários de tecnologia, economia, música, design de produtos Agent, arquitetura e história Ming. Os arquivos mantêm as datas originais de verificação das fontes.

| Technology | Economics | Music |
| :---: | :---: | :---: |
| [![Technology](../../docs/screenshots/technology.png)](../../examples/technology/) | [![Economics](../../docs/screenshots/economics.png)](../../examples/economics/) | [![Music](../../docs/screenshots/music.png)](../../examples/music/) |

| Agent products | Architecture | Ming history |
| :---: | :---: | :---: |
| [![Agent products](../../docs/screenshots/agent-product.png)](../../examples/agent-product/) | [![Architecture](../../docs/screenshots/architecture.png)](../../examples/architecture/) | [![Ming history](../../docs/screenshots/ming-history.png)](../../examples/ming-history/) |

## Instalação e guias

[Instalar no agente](../../skills/omni-learning-anything/references/install.md) · [Formatos e fontes](../../skills/omni-learning-anything/references/setup.md) · [Ligar documentos](../../skills/omni-learning-anything/references/onboarding.md) · [Validação da versão](../../docs/release-validation-v2.6.0.md)

Esta Agent Skill utiliza as ferramentas de pesquisa, documentos e agendamento do seu agente. Apenas PDF precisa de XeLaTeX. A nuvem usa APIs/CLIs oficiais; Obsidian escreve no Vault local. A sincronização e a execução autónoma dependem do sistema anfitrião e da conta.

[MIT](../../LICENSE) · [Changelog](../../CHANGELOG.md)
