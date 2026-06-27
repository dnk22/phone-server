import importlib

MODULES = ("control_api.main", "device_agent.main", "common", "contracts", "observability")


def main() -> None:
    for module in MODULES:
        importlib.import_module(module)


if __name__ == "__main__":
    main()
