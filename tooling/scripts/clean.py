from pathlib import Path
from shutil import rmtree

CACHE_DIR_NAMES = {
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
}


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    for path in root.rglob("*"):
        if path.is_dir() and path.name in CACHE_DIR_NAMES:
            rmtree(path)
    for path in root.rglob("*.egg-info"):
        if path.is_dir():
            rmtree(path)


if __name__ == "__main__":
    main()
