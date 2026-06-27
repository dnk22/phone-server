# Getting started

Install Node 22.13+, Python 3.12, uv, and Make. Then run:

```bash
make install
make check
```

Use `make dev` to start the dashboard and Control API development servers together. The script stops both child processes when interrupted.

Local configuration belongs in an ignored `.env` copied from `.env.example`.
