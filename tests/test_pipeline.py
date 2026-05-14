from pathlib import Path

from modules.pipeline import (
    PIPELINE_FILE,
    add_pipeline_item,
    get_pipeline_item_by_id,
    load_pipeline,
    save_pipeline,
    update_pipeline_status,
)


def test_pipeline_save_and_load(tmp_path: Path, monkeypatch):
    path = tmp_path / "pipeline.yaml"
    monkeypatch.setattr("modules.pipeline.PIPELINE_FILE", path)

    items = [
        {"id": 1, "client_id": 1, "client_name": "Cliente A", "scenario_id": 1, "status": "Prospect"}
    ]
    save_pipeline(items, path)
    loaded = load_pipeline(path)
    assert loaded == items


def test_add_and_update_pipeline_item(tmp_path: Path, monkeypatch):
    path = tmp_path / "pipeline.yaml"
    monkeypatch.setattr("modules.pipeline.PIPELINE_FILE", path)

    item = add_pipeline_item(client_id=1, client_name="Cliente A", scenario_id=1)
    assert item["id"] == 1
    assert item["status"] == "Prospect"

    updated = update_pipeline_status(item["id"], "Proposta")
    assert updated is not None
    assert updated["status"] == "Proposta"
    assert get_pipeline_item_by_id(load_pipeline(path), item["id"])["status"] == "Proposta"
