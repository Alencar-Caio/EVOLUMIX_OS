from pathlib import Path
import yaml

CONFIG_FILE = Path(__file__).resolve().parents[1] / "core" / "EVOLUMIX_FOUNDATION_v1.yaml"


def load_config(path: str | Path | None = None) -> dict:
    """Carrega o arquivo de configuração YAML do sistema."""
    config_path = Path(path) if path else CONFIG_FILE
    with config_path.open("r", encoding="utf-8") as arquivo:
        return yaml.safe_load(arquivo)


def display_system_info(config: dict) -> None:
    """Exibe informações básicas do sistema e dos pilares."""
    print("Sistema:", config["sistema"]["nome"])
    print("Versão:", config["sistema"]["versao"])
    print("Empresa:", config["empresa"]["nome"])

    print("\n--- PILARES ESTRATÉGICOS ---")
    for nome, info in config["pilares"].items():
        print(f"\n[{nome.upper()}]")
        if "marca" in info:
            print("Marca:", info["marca"])
        print("Focos:")
        for foco in info["foco"]:
            print(" -", foco)
