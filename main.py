import argparse

from modules.client import add_client, display_clients, get_client_by_id, load_clients
from modules.proposal import build_proposal, save_proposal
from modules.pipeline import (
    add_pipeline_item,
    display_pipeline,
    get_pipeline_item_by_id,
    load_pipeline,
    STAGES,
    update_pipeline_status,
)
from modules.roi import (
    add_roi_scenario,
    display_roi_results,
    display_roi_scenarios,
    get_roi_scenario_by_id,
    load_roi_scenarios,
)
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


def prompt_select_client(clientes: list[dict]) -> dict | None:
    if not clientes:
        print("Nenhum cliente cadastrado. Adicione um cliente antes.")
        return None

    display_clients(clientes)
    raw_id = input("Digite o ID do cliente para ROI: ").strip()
    if not raw_id.isdigit():
        print("ID inválido. Operação cancelada.")
        return None

    cliente = get_client_by_id(clientes, int(raw_id))
    if cliente is None:
        print("Cliente não encontrado. Operação cancelada.")
        return None

    return cliente


def prompt_calculate_roi() -> None:
    print("\nCalcular ROI")
    clientes = load_clients()
    cliente = prompt_select_client(clientes)
    if cliente is None:
        return

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
    scenario = add_roi_scenario(
        client_id=cliente["id"],
        client_name=cliente["nome"],
        current_monthly_cost=current_cost,
        optimized_monthly_cost=optimized_cost,
        investment=investment,
    )
    print(f"Cenário de ROI salvo como ID {scenario['id']} para o cliente {cliente['nome']}.")


def prompt_list_roi_scenarios() -> None:
    display_roi_scenarios(load_roi_scenarios())


def prompt_generate_proposal() -> None:
    print("\nGerar proposta de vendas")
    scenarios = load_roi_scenarios()
    if not scenarios:
        print("Nenhum cenário de ROI disponível. Gere um cenário antes.")
        return

    display_roi_scenarios(scenarios)
    raw_id = input("Digite o ID do cenário para gerar proposta: ").strip()
    if not raw_id.isdigit():
        print("ID inválido. Operação cancelada.")
        return

    scenario = get_roi_scenario_by_id(scenarios, int(raw_id))
    if scenario is None:
        print("Cenário não encontrado. Operação cancelada.")
        return

    proposal_text = build_proposal(scenario["client_name"], scenario)
    file_path = save_proposal(proposal_text, scenario["id"])
    print(f"Proposta salva em: {file_path}")


def prompt_add_pipeline_item() -> None:
    print("\nAdicionar cenário ao pipeline")
    scenarios = load_roi_scenarios()
    if not scenarios:
        print("Nenhum cenário de ROI disponível. Gere um cenário antes.")
        return

    display_roi_scenarios(scenarios)
    raw_id = input("Digite o ID do cenário para adicionar ao pipeline: ").strip()
    if not raw_id.isdigit():
        print("ID inválido. Operação cancelada.")
        return

    scenario = get_roi_scenario_by_id(scenarios, int(raw_id))
    if scenario is None:
        print("Cenário não encontrado. Operação cancelada.")
        return

    item = add_pipeline_item(
        client_id=scenario["client_id"],
        client_name=scenario["client_name"],
        scenario_id=scenario["id"],
    )
    print(f"Cenário adicionado ao pipeline com ID {item['id']}.")


def prompt_advance_pipeline() -> None:
    print("\nAtualizar etapa do pipeline")
    items = load_pipeline()
    if not items:
        print("Nenhum item no pipeline.")
        return

    display_pipeline(items)
    raw_id = input("Digite o ID do item do pipeline: ").strip()
    if not raw_id.isdigit():
        print("ID inválido. Operação cancelada.")
        return

    item = get_pipeline_item_by_id(items, int(raw_id))
    if item is None:
        print("Item não encontrado. Operação cancelada.")
        return

    print("Status disponíveis:")
    for stage in STAGES:
        print(f"- {stage}")

    new_status = input("Digite o novo status: ").strip()
    if new_status not in STAGES:
        print("Status inválido. Operação cancelada.")
        return

    updated = update_pipeline_status(item["id"], new_status)
    if updated is None:
        print("Falha ao atualizar o item do pipeline.")
        return

    print(f"Item {item['id']} atualizado para {new_status}.")


def run_interactive_menu() -> None:
    while True:
        print("\n--- MENU INTERATIVO ---")
        print("1. Listar clientes")
        print("2. Adicionar cliente")
        print("3. Calcular ROI para cliente")
        print("4. Listar cenários de ROI salvos")
        print("5. Gerar proposta de ROI")
        print("6. Adicionar cenário ao pipeline")
        print("7. Atualizar etapa do pipeline")
        print("8. Sair")

        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            clientes = load_clients()
            display_clients(clientes)
        elif opcao == "2":
            prompt_add_client()
        elif opcao == "3":
            prompt_calculate_roi()
        elif opcao == "4":
            prompt_list_roi_scenarios()
        elif opcao == "5":
            prompt_generate_proposal()
        elif opcao == "6":
            prompt_add_pipeline_item()
        elif opcao == "7":
            prompt_advance_pipeline()
        elif opcao == "8":
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
    parser.add_argument("--list-roi", action="store_true", help="Listar cenários de ROI salvos")
    parser.add_argument("--generate-proposal", action="store_true", help="Gerar proposta a partir de um cenário de ROI")
    parser.add_argument("--list-pipeline", action="store_true", help="Listar itens do pipeline comercial")
    parser.add_argument("--add-pipeline", action="store_true", help="Adicionar cenário de ROI ao pipeline")
    parser.add_argument("--advance-pipeline", action="store_true", help="Atualizar etapa de um item do pipeline")
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

    if args.list_roi:
        prompt_list_roi_scenarios()
        return

    if args.generate_proposal:
        prompt_generate_proposal()
        return

    if args.list_pipeline:
        display_pipeline(load_pipeline())
        return

    if args.add_pipeline:
        prompt_add_pipeline_item()
        return

    if args.advance_pipeline:
        prompt_advance_pipeline()
        return

    print("\n--- CLIENTES ---")
    display_clients(load_clients())
    print("\nUse '--interactive' para abrir o menu de operações de cliente, '--calculate-roi' para calcular ROI ou '--list-roi' para ver cenários salvos.")


if __name__ == "__main__":
    main()
