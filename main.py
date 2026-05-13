import yaml

with open("core/EVOLUMIX_FOUNDATION_v1.yaml", "r", encoding="utf-8") as arquivo:
    dados = yaml.safe_load(arquivo)

print("\n===== EVOLUMIX OS =====\n")

print("Sistema:", dados["sistema"]["nome"])
print("Versão:", dados["sistema"]["versao"])
print("Empresa:", dados["empresa"]["nome"])

print("\n--- PILARES ESTRATÉGICOS ---")

for nome, info in dados["pilares"].items():
    print(f"\n[{nome.upper()}]")
    
    if "marca" in info:
        print("Marca:", info["marca"])

    print("Focos:")
    for foco in info["foco"]:
        print(" -", foco)