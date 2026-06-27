from pathlib import Path
from uuid import uuid4


def load_or_create_agent_id(data_dir: Path, configured_id: str | None = None) -> str:
    if configured_id:
        return configured_id
    data_dir.mkdir(parents=True, exist_ok=True)
    identity_file = data_dir / "agent-id"
    if identity_file.exists():
        return identity_file.read_text(encoding="utf-8").strip()
    agent_id = f"agent-{uuid4()}"
    identity_file.write_text(agent_id, encoding="utf-8")
    return agent_id
