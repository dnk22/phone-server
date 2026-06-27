from control_api.shared.errors import ConflictError

from contracts import AutomationTaskStatus

VALID_TRANSITIONS: dict[AutomationTaskStatus, set[AutomationTaskStatus]] = {
    AutomationTaskStatus.PENDING: {AutomationTaskStatus.QUEUED},
    AutomationTaskStatus.QUEUED: {AutomationTaskStatus.ASSIGNED, AutomationTaskStatus.CANCELLED},
    AutomationTaskStatus.ASSIGNED: {
        AutomationTaskStatus.ACCEPTED,
        AutomationTaskStatus.QUEUED,
        AutomationTaskStatus.CANCELLED,
    },
    AutomationTaskStatus.ACCEPTED: {
        AutomationTaskStatus.RUNNING,
        AutomationTaskStatus.QUEUED,
        AutomationTaskStatus.CANCELLED,
    },
    AutomationTaskStatus.RUNNING: {
        AutomationTaskStatus.SUCCEEDED,
        AutomationTaskStatus.FAILED,
        AutomationTaskStatus.CANCELLED,
        AutomationTaskStatus.TIMED_OUT,
    },
    AutomationTaskStatus.SUCCEEDED: set(),
    AutomationTaskStatus.FAILED: set(),
    AutomationTaskStatus.CANCELLED: set(),
    AutomationTaskStatus.TIMED_OUT: set(),
}


def validate_transition(current: AutomationTaskStatus, desired: AutomationTaskStatus) -> None:
    if desired not in VALID_TRANSITIONS[current]:
        raise ConflictError(f"invalid task transition: {current.value} -> {desired.value}")
