from modules.whatsapp import (
    generate_initial_contact_script,
    generate_followup_script,
    generate_objection_handling_script,
    get_available_objections,
    save_whatsapp_script,
)


def test_generate_initial_contact_script():
    script = generate_initial_contact_script("João Silva", "Hospital")
    assert "Olá João Silva!" in script
    assert "Somos da Evolumix" in script
    assert "hospitals como o seu" in script
    assert "[Seu Nome]" in script


def test_generate_followup_script_early():
    scenario = {
        "monthly_savings": 500.0,
        "payback_months": 2.5,
    }
    script = generate_followup_script("Maria Santos", scenario, 2)
    assert "Olá Maria Santos!" in script
    assert "economia mensal de R$ 500" in script
    assert "payback estimado em apenas 2.5 meses" in script


def test_generate_followup_script_late():
    scenario = {
        "monthly_savings": 800.0,
    }
    script = generate_followup_script("Carlos Oliveira", scenario, 10)
    assert "Última tentativa de contato" in script
    assert "R$ 800/mês" in script


def test_generate_objection_handling_preco_alto():
    scenario = {"monthly_savings": 600.0}
    script = generate_objection_handling_script("preco_alto", "Ana Costa", scenario)
    assert "Olá Ana Costa! 💰" in script
    assert "economia mensal de R$ 600" in script
    assert "comodato de equipamentos" in script


def test_generate_objection_handling_tempo():
    scenario = {"monthly_savings": 400.0}
    script = generate_objection_handling_script("nao_tem_tempo", "Pedro Lima", scenario)
    assert "Olá Pedro Lima! ⏱️" in script
    assert "Diagnóstico rápido (2 horas)" in script
    assert "R$ 400/mês" in script


def test_get_available_objections():
    objections = get_available_objections()
    assert "preco_alto" in objections
    assert "nao_tem_tempo" in objections
    assert "ja_tem_fornecedor" in objections
    assert "duvida_resultados" in objections
    assert len(objections) == 4


def test_save_whatsapp_script(tmp_path):
    script_content = "Teste de script WhatsApp"
    saved_file = save_whatsapp_script(script_content, "Cliente Teste", "test")
    assert saved_file.exists()
    assert saved_file.read_text(encoding="utf-8") == script_content
    assert "whatsapp_test_Cliente_Teste_" in str(saved_file)