def calculate_monthly_savings(current_monthly_cost: float, optimized_monthly_cost: float) -> float:
    """Calcula a economia mensal entre o custo atual e o custo otimizado."""
    return current_monthly_cost - optimized_monthly_cost


def calculate_roi(investment: float, monthly_savings: float) -> float:
    """Calcula o payback em meses para o investimento."""
    if monthly_savings <= 0:
        return float('inf')
    return investment / monthly_savings


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
