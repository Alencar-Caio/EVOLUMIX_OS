import typer

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

app = typer.Typer(help="EVOLUMIX OS - Sistema Comercial Inteligente")


def parse_currency(value: str, field_name: str) -> float | None:
    try:
        return float(value.replace(",", "."))
    except ValueError:
        typer.echo(f"Valor inválido para {field_name}. Operação cancelada.")
        return None


def prompt_add_client() -> None:
    typer.echo("\nAdicionar novo cliente")
    nome = typer.prompt("Nome do cliente").strip()
    if not nome:
        typer.echo("Nome obrigatório. Operação cancelada.")
        raise typer.Exit()

    segmento = typer.prompt("Segmento").strip()
    foco_produto = typer.prompt("Foco do produto").strip()
    contato = typer.prompt("Contato (opcional)").strip()

    cliente = add_client(nome, segmento, foco_produto, contato)
    typer.echo(f"Cliente '{cliente['nome']}' cadastrado com ID {cliente['id']}.")


def prompt_select_client(clientes: list[dict]) -> dict | None:
    if not clientes:
        typer.echo("Nenhum cliente cadastrado. Adicione um cliente antes.")
        return None

    display_clients(clientes)
    raw_id = typer.prompt("Digite o ID do cliente para ROI").strip()
    if not raw_id.isdigit():
        typer.echo("ID inválido. Operação cancelada.")
        return None

    cliente = get_client_by_id(clientes, int(raw_id))
    if cliente is None:
        typer.echo("Cliente não encontrado. Operação cancelada.")
        return None

    return cliente


def prompt_calculate_roi() -> None:
    typer.echo("\nCalcular ROI")
    clientes = load_clients()
    cliente = prompt_select_client(clientes)
    if cliente is None:
        return

    current_cost = parse_currency(typer.prompt("Custo atual mensal (R$)").strip(), "custo atual")
    if current_cost is None:
        return

    optimized_cost = parse_currency(typer.prompt("Custo otimizado mensal (R$)").strip(), "custo otimizado")
    if optimized_cost is None:
        return

    investment = parse_currency(typer.prompt("Investimento inicial (R$)").strip(), "investimento")
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
    typer.echo(f"Cenário de ROI salvo como ID {scenario['id']} para o cliente {cliente['nome']}.")


def prompt_list_roi_scenarios() -> None:
    display_roi_scenarios(load_roi_scenarios())


def prompt_generate_proposal() -> None:
    typer.echo("\nGerar proposta de vendas")
    scenarios = load_roi_scenarios()
    if not scenarios:
        typer.echo("Nenhum cenário de ROI disponível. Gere um cenário antes.")
        raise typer.Exit()

    display_roi_scenarios(scenarios)
    raw_id = typer.prompt("Digite o ID do cenário para gerar proposta").strip()
    if not raw_id.isdigit():
        typer.echo("ID inválido. Operação cancelada.")
        raise typer.Exit()

    scenario = get_roi_scenario_by_id(scenarios, int(raw_id))
    if scenario is None:
        typer.echo("Cenário não encontrado. Operação cancelada.")
        raise typer.Exit()

    proposal_text = build_proposal(scenario["client_name"], scenario)
    file_path = save_proposal(proposal_text, scenario["id"])
    typer.echo(f"Proposta salva em: {file_path}")


def prompt_add_pipeline_item() -> None:
    typer.echo("\nAdicionar cenário ao pipeline")
    scenarios = load_roi_scenarios()
    if not scenarios:
        typer.echo("Nenhum cenário de ROI disponível. Gere um cenário antes.")
        raise typer.Exit()

    display_roi_scenarios(scenarios)
    raw_id = typer.prompt("Digite o ID do cenário para adicionar ao pipeline").strip()
    if not raw_id.isdigit():
        typer.echo("ID inválido. Operação cancelada.")
        raise typer.Exit()

    scenario = get_roi_scenario_by_id(scenarios, int(raw_id))
    if scenario is None:
        typer.echo("Cenário não encontrado. Operação cancelada.")
        raise typer.Exit()

    item = add_pipeline_item(
        client_id=scenario["client_id"],
        client_name=scenario["client_name"],
        scenario_id=scenario["id"],
    )
    typer.echo(f"Cenário adicionado ao pipeline com ID {item['id']}.")


def prompt_advance_pipeline() -> None:
    typer.echo("\nAtualizar etapa do pipeline")
    items = load_pipeline()
    if not items:
        typer.echo("Nenhum item no pipeline.")
        raise typer.Exit()

    display_pipeline(items)
    raw_id = typer.prompt("Digite o ID do item do pipeline").strip()
    if not raw_id.isdigit():
        typer.echo("ID inválido. Operação cancelada.")
        raise typer.Exit()

    item = get_pipeline_item_by_id(items, int(raw_id))
    if item is None:
        typer.echo("Item não encontrado. Operação cancelada.")
        raise typer.Exit()

    typer.echo("Status disponíveis:")
    for stage in STAGES:
        typer.echo(f"- {stage}")

    new_status = typer.prompt("Digite o novo status").strip()
    if new_status not in STAGES:
        typer.echo("Status inválido. Operação cancelada.")
        raise typer.Exit()

    updated = update_pipeline_status(item["id"], new_status)
    if updated is None:
        typer.echo("Falha ao atualizar o item do pipeline.")
        raise typer.Exit()

    typer.echo(f"Item {item['id']} atualizado para {new_status}.")


def run_interactive_menu() -> None:
    while True:
        typer.echo("\n--- MENU INTERATIVO ---")
        typer.echo("1. Listar clientes")
        typer.echo("2. Adicionar cliente")
        typer.echo("3. Calcular ROI para cliente")
        typer.echo("4. Listar cenários de ROI salvos")
        typer.echo("5. Gerar proposta de ROI")
        typer.echo("6. Adicionar cenário ao pipeline")
        typer.echo("7. Atualizar etapa do pipeline")
        typer.echo("8. Sair")

        opcao = typer.prompt("Escolha uma opção").strip()
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
            typer.echo("Saindo...")
            break
        else:
            typer.echo("Opção inválida. Tente novamente.")


@app.command()
def interactive() -> None:
    """Abrir menu interativo."""
    config = load_config()
    typer.echo("\n===== EVOLUMIX OS =====\n")
    display_system_info(config)
    run_interactive_menu()


@app.command("list-clients")
def list_clients() -> None:
    """Listar clientes cadastrados."""
    display_clients(load_clients())


@app.command("add-client")
def add_client_cmd() -> None:
    """Adicionar um novo cliente."""
    config = load_config()
    typer.echo("\n===== EVOLUMIX OS =====\n")
    display_system_info(config)
    prompt_add_client()


@app.command("calculate-roi")
def calculate_roi_cmd() -> None:
    """Calcular ROI com dados de custo."""
    config = load_config()
    typer.echo("\n===== EVOLUMIX OS =====\n")
    display_system_info(config)
    prompt_calculate_roi()


@app.command("list-roi")
def list_roi_cmd() -> None:
    """Listar cenários de ROI salvos."""
    config = load_config()
    typer.echo("\n===== EVOLUMIX OS =====\n")
    display_system_info(config)
    prompt_list_roi_scenarios()


@app.command("generate-proposal")
def generate_proposal_cmd() -> None:
    """Gerar proposta a partir de um cenário de ROI."""
    config = load_config()
    typer.echo("\n===== EVOLUMIX OS =====\n")
    display_system_info(config)
    prompt_generate_proposal()


@app.command("list-pipeline")
def list_pipeline_cmd() -> None:
    """Listar itens do pipeline comercial."""
    config = load_config()
    typer.echo("\n===== EVOLUMIX OS =====\n")
    display_system_info(config)
    display_pipeline(load_pipeline())


@app.command("add-pipeline")
def add_pipeline_cmd() -> None:
    """Adicionar um cenário de ROI ao pipeline."""
    config = load_config()
    typer.echo("\n===== EVOLUMIX OS =====\n")
    display_system_info(config)
    prompt_add_pipeline_item()


@app.command("advance-pipeline")
def advance_pipeline_cmd() -> None:
    """Atualizar etapa de um item do pipeline."""
    config = load_config()
    typer.echo("\n===== EVOLUMIX OS =====\n")
    display_system_info(config)
    prompt_advance_pipeline()


if __name__ == "__main__":
    app()
