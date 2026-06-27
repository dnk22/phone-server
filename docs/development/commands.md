# Development commands

| Command             | Purpose                                            |
| ------------------- | -------------------------------------------------- |
| `make install`      | Resolve pnpm and uv workspaces and install hooks   |
| `make dev`          | Start dashboard and FastAPI                        |
| `make format`       | Apply Prettier and Ruff                            |
| `make format-check` | Verify formatting                                  |
| `make lint`         | Run ESLint and Ruff rules                          |
| `make typecheck`    | Run TypeScript and Pyright                         |
| `make test`         | Run Vitest and Pytest                              |
| `make build`        | Build TypeScript and validate Python imports       |
| `make check`        | Run the CI-equivalent quality gate                 |
| `make clean`        | Remove build output and caches, preserving `.venv` |
