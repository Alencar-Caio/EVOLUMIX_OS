from pathlib import Path

from modules.proposal import build_proposal, save_proposal


def test_build_proposal_contains_client_and_scenario_id():
    scenario = {
        "id": 1,
        "client_id": 1,
        "client_name": "Cliente A",
        "current_monthly_cost": 1200.0,
        "optimized_monthly_cost": 900.0,
        "investment": 300.0,
        "monthly_savings": 300.0,
        "payback_months": 1.0,
        "created_at": "2026-01-01T00:00:00",
    }
    proposal_text = build_proposal("Cliente A", scenario)
    assert "Cliente: Cliente A" in proposal_text
    assert "Cenário ID: 1" in proposal_text


def test_save_proposal_writes_file(tmp_path: Path):
    text = "Teste de proposta"
    path = tmp_path / "proposal.txt"
    saved = save_proposal(text, 1)
    assert saved.exists()
    assert saved.read_text(encoding="utf-8") == text
