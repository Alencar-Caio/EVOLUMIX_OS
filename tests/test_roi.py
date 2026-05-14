from pathlib import Path

from modules.roi import (
    ROI_FILE,
    add_roi_scenario,
    calculate_monthly_savings,
    calculate_roi,
    load_roi_scenarios,
    save_roi_scenarios,
)


def test_calculate_monthly_savings_and_roi():
    assert calculate_monthly_savings(1000, 800) == 200
    assert calculate_roi(200, 200) == 1
    assert calculate_roi(1000, 0) == float('inf')


def test_save_and_load_roi_scenarios(tmp_path: Path, monkeypatch):
    path = tmp_path / "roi_scenarios.yaml"
    monkeypatch.setattr("modules.roi.ROI_FILE", path)

    scenarios = [
        {
            "id": 1,
            "client_id": 1,
            "client_name": "Cliente A",
            "current_monthly_cost": 1000.0,
            "optimized_monthly_cost": 800.0,
            "investment": 200.0,
            "monthly_savings": 200.0,
            "payback_months": 1.0,
            "created_at": "2026-01-01T00:00:00",
        }
    ]
    save_roi_scenarios(scenarios, path)
    loaded = load_roi_scenarios(path)
    assert loaded == scenarios


def test_add_roi_scenario_saves_file(tmp_path: Path, monkeypatch):
    path = tmp_path / "roi_scenarios.yaml"
    monkeypatch.setattr("modules.roi.ROI_FILE", path)

    scenario = add_roi_scenario(
        client_id=1,
        client_name="Cliente B",
        current_monthly_cost=1200.0,
        optimized_monthly_cost=900.0,
        investment=300.0,
    )
    assert scenario["id"] == 1
    assert scenario["client_name"] == "Cliente B"
    assert path.exists()
