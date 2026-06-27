import pytest
from control_api.modules.automation_tasks.state_machine import validate_transition
from control_api.shared.errors import ConflictError

from contracts import AutomationTaskStatus


def test_invalid_task_transition_is_rejected() -> None:
    with pytest.raises(ConflictError):
        validate_transition(AutomationTaskStatus.QUEUED, AutomationTaskStatus.SUCCEEDED)
