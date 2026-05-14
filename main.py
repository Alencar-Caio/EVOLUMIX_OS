from modules.system import load_config, display_system_info


def main() -> None:
    config = load_config()

    print("\n===== EVOLUMIX OS =====\n")
    display_system_info(config)


if __name__ == "__main__":
    main()
