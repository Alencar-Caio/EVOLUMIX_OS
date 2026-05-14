# EVOLUMIX_OS

Sistema operacional comercial inteligente para a Evolumix, focado em reduzir custo invisível operacional em vendas de higiene e limpeza.

## Visão geral

- Arquitetura de pilares estratégicos
- Engenharia de valor
- Diagnóstico consultivo
- Automação de proposta e ROI

## Status atual

- `main.py` já lê o arquivo `core/EVOLUMIX_FOUNDATION_v1.yaml`
- O sistema já carrega arquitetura base e pilares estratégicos
- Ainda faltam memória de clientes, cálculo de ROI automatizado e geração de propostas

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
python3 main.py
```

Isso exibe a arquitetura do sistema e os clientes cadastrados.

## Funções de cliente

- `python3 main.py --interactive` — abre um menu interativo para listar e adicionar clientes
- `python3 main.py --list-clients` — lista apenas os clientes
- `python3 main.py --add-client` — adiciona um cliente com perguntas no terminal

## ROI

- `python3 main.py --calculate-roi` — calcula ROI com dados de custo mensal e investimento inicial
- `python3 main.py --list-roi` — lista os cenários de ROI salvos
- `python3 main.py --generate-proposal` — gera uma proposta a partir de um cenário de ROI
- no modo interativo, escolha a opção "Calcular ROI", "Listar cenários de ROI salvos" ou "Gerar proposta de ROI"

## Pipeline comercial

- `python3 main.py --list-pipeline` — lista os itens do pipeline comercial
- `python3 main.py --add-pipeline` — adiciona um cenário de ROI ao pipeline
- `python3 main.py --advance-pipeline` — atualiza o status de um item no pipeline
- no modo interativo, escolha "Adicionar cenário ao pipeline" ou "Atualizar etapa do pipeline"

Os clientes são salvos em `core/clients.yaml`.
Cenários de ROI são salvos em `core/roi_scenarios.yaml`.
Propostas geradas são salvas em `core/proposals/`.
Pipeline é salvo em `core/pipeline.yaml`.

## GitHub Actions

O repositório inclui uma pipeline básica de CI em `.github/workflows/python-ci.yml` para validar a execução do projeto.
