import argparse

from modules.client import add_client, display_clients, load_clients
from modules.roi import calculate_roi, calculate_monthly_savings, display_roi_results
from modules.system import display_system_info, load_config


def parse_currency(value: str, field_name: str) -> float | None:
    try:
        return float(value.replace(",", "."))
    except ValueError:
        print(f"Valor inválido para {field_name}. Operação cancelada.")
        return None


def prompt_add_client() -> None:
    print("\nAdicionar novo cliente")
    nome = input("Nome do cliente: ").strip()
    if not nome:
        print("Nome obrigatório. Operação cancelada.")
        return

    segmento = input("Segmento: ").strip()
    foco_produto = input("Foco do produto: ").strip()
    contato = input("Contato (opcional): ").strip()

    cliente = add_client(nome, segmento, foco_produto, contato)
    print(f"Cliente '{cliente['nome']}' cadastrado com ID {cliente['id']}.")


def prompt_calculate_roi() -> None:
    print("\nCalcular ROI")
    current_cost = parse_currency(input("Custo atual mensal (R$): ").strip(), "custo atual")
    if current_cost is None:
        return

    optimized_cost = parse_currency(input("Custo otimizado mensal (R$): ").strip(), "custo otimizado")
    if optimized_cost is None:
        return

    investment = parse_currency(input("Investimento inicial (R$): ").strip(), "investimento")
    if investment is None:
        return

    display_roi_results(current_cost, optimized_cost, investment)


def run_interactive_menu() -> None:
    while True:
        print("\n--- MENU INTERATIVO ---")
        print("1. Listar clientes")
        print("2. Adicionar cliente")
        print("3. Calcular ROI")
        print("4. Sair")

        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            clientes = load_clients()
            display_clients(clientes)
        elif opcao == "2":
            prompt_add_client()
        elif opcao == "3":
            prompt_calculate_roi()
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


def main() -> None:
    parser = argparse.ArgumentParser(description="EVOLUMIX OS - Sistema Comercial Inteligente")
    parser.add_argument("--interactive", action="store_true", help="Abrir menu interativo")
    parser.add_argument("--list-clients", action="store_true", help="Listar clientes cadastrados")
    parser.add_argument("--add-client", action="store_true", help="Adicionar um novo cliente")
    parser.add_argument("--calculate-roi", action="store_true", help="Calcular ROI com dados de custo")
    args = parser.parse_args()

    config = load_config()
    print("\n===== EVOLUMIX OS =====\n")
    display_system_info(config)

    if args.interactive:
        run_interactive_menu()
        return

    if args.list_clients:
        display_clients(load_clients())
        return

    if args.add_client:
        prompt_add_client()
        return

    if args.calculate_roi:
        prompt_calculate_roi()
        return

    print("\n--- CLIENTES ---")
    display_clients(load_clients())
    print("\nUse '--interactive' para abrir o menu de operações de cliente ou '--calculate-roi' para calcular ROI.")


if __name__ == "__main__":
    main()
