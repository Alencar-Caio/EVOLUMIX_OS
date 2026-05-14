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

## GitHub Actions

O repositório inclui uma pipeline básica de CI em `.github/workflows/python-ci.yml` para validar a execução do projeto.
