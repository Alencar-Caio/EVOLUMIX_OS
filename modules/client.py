from pathlib import Path
import yaml

CLIENTS_FILE = Path(__file__).resolve().parents[1] / "core" / "clients.yaml"


def load_clients(path: str | Path | None = None) -> list[dict]:
    """Carrega a lista de clientes do arquivo YAML."""
    file_path = Path(path) if path else CLIENTS_FILE
    if not file_path.exists():
        return []

    data = yaml.safe_load(file_path.read_text(encoding="utf-8")) or {}
    return data.get("clients", [])


def save_clients(clients: list[dict], path: str | Path | None = None) -> None:
    """Salva a lista de clientes em YAML."""
    file_path = Path(path) if path else CLIENTS_FILE
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as arquivo:
        yaml.safe_dump({"clients": clients}, arquivo, sort_keys=False, allow_unicode=True)


def get_client_by_id(clientes: list[dict], cliente_id: int) -> dict | None:
    """Retorna um cliente pelo seu ID."""
    for cliente in clientes:
        if cliente["id"] == cliente_id:
            return cliente
    return None


def add_client(
    nome: str,
    segmento: str,
    foco_produto: str,
    contato: str | None = None,
) -> dict:
    """Adiciona um novo cliente e salva no arquivo."""
    clientes = load_clients()
    novo_id = len(clientes) + 1
    cliente = {
        "id": novo_id,
        "nome": nome,
        "segmento": segmento,
        "foco_produto": foco_produto,
        "contato": contato or "",
    }
    clientes.append(cliente)
    save_clients(clientes)
    return cliente


def display_clients(clientes: list[dict]) -> None:
    """Exibe a lista de clientes cadastrados."""
    if not clientes:
        print("Nenhum cliente cadastrado.")
        return

    print("\n--- CLIENTES CADASTRADOS ---")
    for cliente in clientes:
        print(f"\nID: {cliente['id']}")
        print(f"Nome: {cliente['nome']}")
        print(f"Segmento: {cliente['segmento']}")
        print(f"Foco do produto: {cliente['foco_produto']}")
        if cliente.get("contato"):
            print(f"Contato: {cliente['contato']}")
