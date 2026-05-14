from pathlib import Path
from datetime import datetime
from typing import Dict, List

WHATSAPP_DIR = Path(__file__).resolve().parents[1] / "core" / "whatsapp_scripts"


def generate_initial_contact_script(client_name: str, client_segment: str) -> str:
    """Gera script de primeiro contato via WhatsApp."""
    lines = [
        f"Olá {client_name}! 👋",
        "",
        "Somos da Evolumix, especialistas em otimização de custos operacionais em limpeza e higiene.",
        "",
        f"Identificamos que {client_segment.lower()}s como o seu têm oportunidades significativas de redução de custos invisíveis.",
        "",
        "Gostaria de agendar uma conversa rápida de 15 minutos para apresentar nossa abordagem consultiva?",
        "",
        "Atenciosamente,",
        "[Seu Nome]",
        "Evolumix Consultoria",
        "[Seu telefone]",
    ]
    return "\n".join(lines)


def generate_followup_script(client_name: str, scenario: Dict, days_since_contact: int) -> str:
    """Gera script de follow-up baseado no cenário de ROI."""
    savings = scenario["monthly_savings"]
    payback = scenario.get("payback_months")

    if days_since_contact <= 3:
        # Follow-up inicial
        lines = [
            f"Olá {client_name}! 👋",
            "",
            "Tudo bem? Seguindo nosso contato anterior sobre otimização de custos operacionais.",
            "",
            f"Em uma análise preliminar, identificamos uma economia mensal de R$ {savings:.0f} nos seus custos de limpeza e higiene.",
        ]
        if payback and payback < 6:
            lines.append(f"Com payback estimado em apenas {payback:.1f} meses!")
        lines.extend([
            "",
            "Quando seria um bom momento para apresentarmos o diagnóstico completo?",
            "",
            "Atenciosamente,",
            "[Seu Nome]",
        ])
    elif days_since_contact <= 7:
        # Follow-up intermediário
        lines = [
            f"Olá {client_name}! 📊",
            "",
            "Retornando nossa conversa sobre redução de custos operacionais.",
            "",
            f"Nossos clientes similares ao seu estão economizando em média R$ {savings:.0f} por mês.",
            "",
            "Posso enviar uma proposta personalizada para avaliação?",
            "",
            "Atenciosamente,",
            "[Seu Nome]",
        ]
    else:
        # Follow-up final
        lines = [
            f"Olá {client_name}! ⏰",
            "",
            "Última tentativa de contato sobre nossa consultoria em eficiência operacional.",
            "",
            f"A oportunidade de economia de R$ {savings:.0f}/mês ainda está disponível.",
            "",
            "Caso tenha interesse futuro, pode me procurar diretamente.",
            "",
            "Atenciosamente,",
            "[Seu Nome]",
        ]

    return "\n".join(lines)


def generate_objection_handling_script(objection_type: str, client_name: str, scenario: Dict) -> str:
    """Gera script para lidar com objeções comuns."""
    savings = scenario["monthly_savings"]

    scripts = {
        "preco_alto": [
            f"Olá {client_name}! 💰",
            "",
            "Entendo sua preocupação com o investimento inicial.",
            "",
            f"Mas considere: a economia mensal de R$ {savings:.0f} representa um retorno sobre investimento muito atrativo.",
            "",
            "Além disso, oferecemos comodato de equipamentos, reduzindo significativamente o investimento upfront.",
            "",
            "Podemos detalhar as opções de financiamento?",
            "",
            "Atenciosamente,",
            "[Seu Nome]",
        ],
        "nao_tem_tempo": [
            f"Olá {client_name}! ⏱️",
            "",
            "Compreendo que tempo é precioso na gestão operacional.",
            "",
            "Por isso desenvolvemos uma abordagem consultiva que minimiza interrupções:",
            "- Diagnóstico rápido (2 horas)",
            "- Implementação gradual",
            "- Acompanhamento remoto",
            "",
            f"Com economia de R$ {savings:.0f}/mês, o ROI se paga sozinho.",
            "",
            "Quando podemos agendar uma apresentação de 30 minutos?",
            "",
            "Atenciosamente,",
            "[Seu Nome]",
        ],
        "ja_tem_fornecedor": [
            f"Olá {client_name}! 🤝",
            "",
            "Respeitamos parcerias existentes e não interferimos nelas.",
            "",
            "Nossa atuação é como consultores de eficiência operacional, otimizando processos independente do fornecedor atual.",
            "",
            f"Clientes nossos com perfil similar economizaram R$ {savings:.0f} mensais mantendo seus fornecedores.",
            "",
            "Posso apresentar casos similares ao seu?",
            "",
            "Atenciosamente,",
            "[Seu Nome]",
        ],
        "duvida_resultados": [
            f"Olá {client_name}! 📈",
            "",
            "Excelente pergunta sobre garantia de resultados!",
            "",
            "Trabalhamos com:",
            "- Diagnóstico técnico detalhado",
            "- Piloto em área controlada (30 dias)",
            "- Métricas claras de acompanhamento",
            "- Garantia de performance",
            "",
            f"Economia média comprovada: R$ {savings:.0f}/mês",
            "",
            "Podemos apresentar cases de sucesso?",
            "",
            "Atenciosamente,",
            "[Seu Nome]",
        ]
    }

    return "\n".join(scripts.get(objection_type, ["Script não encontrado para esta objeção"]))


def save_whatsapp_script(script_content: str, client_name: str, script_type: str) -> Path:
    """Salva script do WhatsApp em arquivo."""
    WHATSAPP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = WHATSAPP_DIR / f"whatsapp_{script_type}_{client_name.replace(' ', '_')}_{timestamp}.txt"
    filename.write_text(script_content, encoding="utf-8")
    return filename


def get_available_objections() -> List[str]:
    """Retorna lista de objeções disponíveis para tratamento."""
    return ["preco_alto", "nao_tem_tempo", "ja_tem_fornecedor", "duvida_resultados"]