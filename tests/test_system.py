from modules.system import load_config


def test_load_config_contains_required_keys():
    config = load_config()
    assert isinstance(config, dict)
    assert "sistema" in config
    assert "empresa" in config
    assert "pilares" in config
    assert config["sistema"]["nome"] == "EVOLUMIX OS"
