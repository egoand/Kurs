from dataclasses import dataclass


@dataclass(frozen=True)
class StatusInfo:
    key: str
    label: str
    badge: str


STATUSES = {
    "pending": StatusInfo("pending", "Ожидает оценки", "await"),
    "evaluated": StatusInfo("evaluated", "Оценена", "eval"),
    "assigned": StatusInfo("assigned", "Назначена", "asg"),
    "in_progress": StatusInfo("in_progress", "В процессе", "prog"),
    "completed": StatusInfo("completed", "Выполнена", "done"),
    "archived": StatusInfo("archived", "", "arch"),
}


def get_status(key):
    return STATUSES[key]