from pathlib import Path
from datetime import datetime

PROPOSAL_DIR = Path(__file__).resolve().parents[1] / "core" / "proposals"


def build_proposal(client_name: str, scenario: dict) -> str:
    savings = scenario["monthly_savings"]
    payback = scenario.get("payback_months")
    investment = scenario["investment"]
    current_cost = scenario["current_monthly_cost"]
    optimized_cost = scenario["optimized_monthly_cost"]

    lines = [
        "# PROPOSTA COMERCIAL - EVOLUMIX OS",
        "",
        f"**Cliente:** {client_name}",
        f"**Cenário ID:** {scenario['id']}",
        f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 📊 Resumo do Cenário",
        "",
        f"- **Custo atual mensal:** R$ {current_cost:.2f}",
        f"- **Custo otimizado mensal:** R$ {optimized_cost:.2f}",
        f"- **Economia mensal estimada:** R$ {savings:.2f}",
        f"- **Investimento inicial:** R$ {investment:.2f}",
    ]

    if payback is None:
        lines.append("- **Payback estimado:** não é possível calcular")
    else:
        lines.append(f"- **Payback estimado:** {payback:.1f} meses")

    lines.extend([
        "",
        "## 💡 Proposta de Valor",
        "",
        "1. **Redução de custo operacional** via otimização de insumos e consumo",
        "2. **Melhoria de eficiência** da operação com acompanhamento do ROI",
        "3. **Ganho financeiro previsto** com retorno sobre investimento rápido",
        "",
        "## 🚀 Próximos Passos",
        "",
        "- ✅ Validar o escopo técnico do cliente",
        "- 📅 Apresentar cronograma de implantação",
        "- 📈 Medir economia real após 30 dias",
        "",
        "---",
        "*Proposta gerada automaticamente pelo EVOLUMIX OS*",
    ])

    return "\n".join(lines)


def save_proposal(proposal_text: str, scenario_id: int) -> Path:
    PROPOSAL_DIR.mkdir(parents=True, exist_ok=True)
    filename = PROPOSAL_DIR / f"proposal_scenario_{scenario_id}.md"
    filename.write_text(proposal_text, encoding="utf-8")
    return filename
