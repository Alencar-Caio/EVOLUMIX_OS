from pathlib import Path

from modules.client import add_client, load_clients, save_clients


def test_save_and_load_clients(tmp_path: Path):
    path = tmp_path / "clients.yaml"
    clients = [
        {"id": 1, "nome": "Cliente A", "segmento": "Hotelaria", "foco_produto": "Sabonete", "contato": "a@ex.com"}
    ]
    save_clients(clients, path)

    loaded = load_clients(path)
    assert loaded == clients


def test_add_client_creates_entry(tmp_path: Path, monkeypatch):
    path = tmp_path / "clients.yaml"
    monkeypatch.setattr("modules.client.CLIENTS_FILE", path)

    cliente = add_client("Cliente B", "Limpeza", "Dosador", "b@ex.com")
    assert cliente["id"] == 1
    assert cliente["nome"] == "Cliente B"
    assert load_clients(path)[0]["nome"] == "Cliente B"
