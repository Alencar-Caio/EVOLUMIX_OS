from datetime import datetime
from pathlib import Path
import yaml

ROI_FILE = Path(__file__).resolve().parents[1] / "core" / "roi_scenarios.yaml"


def calculate_monthly_savings(current_monthly_cost: float, optimized_monthly_cost: float) -> float:
    """Calcula a economia mensal entre o custo atual e o custo otimizado."""
    return current_monthly_cost - optimized_monthly_cost


def calculate_roi(investment: float, monthly_savings: float) -> float:
    """Calcula o payback em meses para o investimento."""
    if monthly_savings <= 0:
        return float('inf')
    return investment / monthly_savings


def load_roi_scenarios(path: str | Path | None = None) -> list[dict]:
    """Carrega a lista de cenários de ROI do arquivo YAML."""
    file_path = Path(path) if path else ROI_FILE
    if not file_path.exists():
        return []

    data = yaml.safe_load(file_path.read_text(encoding="utf-8")) or {}
    return data.get("roi_scenarios", [])


def save_roi_scenarios(scenarios: list[dict], path: str | Path | None = None) -> None:
    """Salva a lista de cenários de ROI em YAML."""
    file_path = Path(path) if path else ROI_FILE
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as arquivo:
        yaml.safe_dump({"roi_scenarios": scenarios}, arquivo, sort_keys=False, allow_unicode=True)


def get_roi_scenario_by_id(scenarios: list[dict], scenario_id: int) -> dict | None:
    """Retorna um cenário de ROI pelo seu ID."""
    for scenario in scenarios:
        if scenario["id"] == scenario_id:
            return scenario
    return None


def add_roi_scenario(
    client_id: int,
    client_name: str,
    current_monthly_cost: float,
    optimized_monthly_cost: float,
    investment: float,
) -> dict:
    """Adiciona e salva um cenário de ROI associado a um cliente."""
    scenarios = load_roi_scenarios()
    scenario_id = len(scenarios) + 1
    savings = calculate_monthly_savings(current_monthly_cost, optimized_monthly_cost)
    payback_months = calculate_roi(investment, savings)
    scenario = {
        "id": scenario_id,
        "client_id": client_id,
        "client_name": client_name,
        "current_monthly_cost": current_monthly_cost,
        "optimized_monthly_cost": optimized_monthly_cost,
        "investment": investment,
        "monthly_savings": savings,
        "payback_months": None if payback_months == float('inf') else round(payback_months, 2),
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    scenarios.append(scenario)
    save_roi_scenarios(scenarios)
    return scenario


def display_roi_results(current_monthly_cost: float, optimized_monthly_cost: float, investment: float) -> None:
    savings = calculate_monthly_savings(current_monthly_cost, optimized_monthly_cost)
    payback = calculate_roi(investment, savings)

    print("\n--- RESULTADO DO ROI ---")
    print(f"Custo atual mensal: R$ {current_monthly_cost:.2f}")
    print(f"Custo otimizado mensal: R$ {optimized_monthly_cost:.2f}")
    print(f"Economia mensal estimada: R$ {savings:.2f}")
    if payback == float('inf'):
        print("Payback: não é possível calcular (economia mensal não positiva)")
    else:
        print(f"Payback estimado: {payback:.1f} meses")


def display_roi_scenarios(scenarios: list[dict]) -> None:
    if not scenarios:
        print("Nenhum cenário de ROI salvo.")
        return

    print("\n--- CENÁRIOS DE ROI SALVOS ---")
    for scenario in scenarios:
        print(f"\nID: {scenario['id']} ({scenario['created_at']})")
        print(f"Cliente: {scenario['client_name']} (ID {scenario['client_id']})")
        print(f"Custo atual: R$ {scenario['current_monthly_cost']:.2f}")
        print(f"Custo otimizado: R$ {scenario['optimized_monthly_cost']:.2f}")
        print(f"Economia mensal: R$ {scenario['monthly_savings']:.2f}")
        payback = scenario.get('payback_months')
        print(f"Payback estimado: {payback if payback is not None else 'não calculado'} meses")
