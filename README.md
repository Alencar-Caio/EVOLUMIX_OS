# EVOLUMIX_OS

Sistema operacional comercial inteligente para a Evolumix, focado em reduzir custo invisível operacional em vendas de higiene e limpeza.

## Visão geral

Sistema completo para consultoria de eficiência operacional:

- ✅ Arquitetura de pilares estratégicos
- ✅ Engenharia de valor e cálculo de ROI
- ✅ Diagnóstico consultivo com clientes
- ✅ Automação de propostas comerciais em Markdown
- ✅ Pipeline comercial inteligente- ✅ Scripts automatizados de WhatsApp para vendas
- ✅ Tratamento automatizado de objeções- ✅ CLI moderno e interface interativa

## Status atual

✅ Sistema operacional funcional com:
- Arquitetura de pilares estratégicos carregada
- Gerenciamento completo de clientes (CRUD)
- Cálculo automatizado de ROI com payback
- Geração de propostas comerciais em Markdown
- Pipeline comercial com status tracking
- CLI moderno com Typer
- Testes automatizados completos
- CI/CD com GitHub Actions

## Como usar

1. Instale Python 3.11+.
2. Instale dependências:

```bash
python -m pip install pyyaml
```

3. Execute:

```bash
python main.py
```

## Estrutura principal

- `main.py` — motor inicial do sistema
- `core/EVOLUMIX_FOUNDATION_v1.yaml` — dados de configuração
- `core/EVOLUMIX_OS_ONBOARDING.md` — visão e roadmap
- `modules/`, `pipeline/`, `playbooks/`, `prompts/`, `roi/`, `states/` — pastas de evolução

## Dependências

Instale as dependências com:

```bash
python3 -m pip install -r requirements.txt
```

## Testes

Execute os testes com:

```bash
python3 -m pytest -q
```

## Uso básico

```bash
python3 main.py --help
```

Isso exibe os comandos disponíveis do EVOLUMIX OS.

## Comandos principais

- `python3 main.py interactive` — abre o menu interativo para listar e adicionar clientes, gerar ROI, propostas e pipeline
- `python3 main.py list-clients` — lista apenas os clientes
- `python3 main.py add-client` — adiciona um cliente com perguntas no terminal
- `python3 main.py calculate-roi` — calcula ROI com dados de custo mensal e investimento inicial
- `python3 main.py list-roi` — lista os cenários de ROI salvos
- `python3 main.py generate-proposal` — gera uma proposta a partir de um cenário de ROI
- `python3 main.py list-pipeline` — lista os itens do pipeline comercial
- `python3 main.py add-pipeline` — adiciona um cenário de ROI ao pipeline
- `python3 main.py generate-whatsapp` — gera script de WhatsApp personalizado baseado no perfil do cliente e cenário de ROI
- `python3 main.py handle-objection` — gera script para tratar objeções comuns dos clientes via WhatsApp

No modo interativo, use as opções do menu para navegar entre clientes, ROI, proposta e pipeline.

Os clientes são salvos em `core/clients.yaml`.
Cenários de ROI são salvos em `core/roi_scenarios.yaml`.
Propostas geradas são salvas em `core/proposals/` como arquivos Markdown (.md) com formatação profissional.
Pipeline é salvo em `core/pipeline.yaml`.
Scripts de WhatsApp são salvos em `core/whatsapp_scripts/` para follow-up e tratamento de objeções.

## GitHub Actions

O repositório inclui uma pipeline básica de CI em `.github/workflows/python-ci.yml` para validar a execução do projeto.
