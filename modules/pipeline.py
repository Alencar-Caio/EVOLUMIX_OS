from pathlib import Path
import yaml

PIPELINE_FILE = Path(__file__).resolve().parents[1] / "core" / "pipeline.yaml"
STAGES = ["Prospect", "Diagnóstico", "Proposta", "Negociação", "Fechado"]


def load_pipeline(path: str | Path | None = None) -> list[dict]:
    file_path = Path(path) if path else PIPELINE_FILE
    if not file_path.exists():
        return []

    data = yaml.safe_load(file_path.read_text(encoding="utf-8")) or {}
    return data.get("pipeline", [])


def save_pipeline(items: list[dict], path: str | Path | None = None) -> None:
    file_path = Path(path) if path else PIPELINE_FILE
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as arquivo:
        yaml.safe_dump({"pipeline": items}, arquivo, sort_keys=False, allow_unicode=True)


def get_pipeline_item_by_id(items: list[dict], item_id: int) -> dict | None:
    for item in items:
        if item["id"] == item_id:
            return item
    return None


def add_pipeline_item(client_id: int, client_name: str, scenario_id: int, status: str = "Prospect") -> dict:
    items = load_pipeline()
    item_id = len(items) + 1
    item = {
        "id": item_id,
        "client_id": client_id,
        "client_name": client_name,
        "scenario_id": scenario_id,
        "status": status,
    }
    items.append(item)
    save_pipeline(items)
    return item


def update_pipeline_status(item_id: int, status: str) -> dict | None:
    items = load_pipeline()
    item = get_pipeline_item_by_id(items, item_id)
    if item is None:
        return None
    item["status"] = status
    save_pipeline(items)
    return item


def display_pipeline(items: list[dict]) -> None:
    if not items:
        print("Nenhum item no pipeline.")
        return

    print("\n--- PIPELINE COMERCIAL ---")
    for item in items:
        print(f"\nID: {item['id']}")
        print(f"Cliente: {item['client_name']} (ID {item['client_id']})")
        print(f"Cenário ROI: {item['scenario_id']}")
        print(f"Status: {item['status']}")
