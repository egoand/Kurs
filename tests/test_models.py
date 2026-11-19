import pytest
from datetime import date
from models.task import Task
from models.account import Account
from models.staff import Staff


def test_performer_list_from_assignments(make_task):
    t = make_task(assignments=[
        {"staff_id": 1, "name": "A", "is_done": False},
        {"staff_id": 2, "name": "B", "is_done": True},
        {"staff_id": 3, "name": "C", "is_done": False},
    ])
    assert t.performer_list() == ["A", "B", "C"]


def test_performer_list_empty(make_task):
    assert make_task(assignments=[]).performer_list() == []


def test_performer_ids(make_task):
    t = make_task(assignments=[
        {"staff_id": 10, "name": "A", "is_done": False},
        {"staff_id": 20, "name": "B", "is_done": False},
    ])
    assert t.performer_ids() == [10, 20]


def test_average_score_rounds_half_up(make_task):
    t = make_task(ratings=[{"name": "X", "score": 80}, {"name": "Y", "score": 91}])
    assert t.average_score() == 86


def test_average_score_none_when_no_ratings(make_task):
    assert make_task(ratings=[]).average_score() is None


def test_rated_by_true(make_task):
    t = make_task(ratings=[{"name": "X", "score": 80}])
    assert t.rated_by("X") is True
    assert t.rated_by("Y") is False


def test_date_range_format(make_task, today):
    t = make_task(start_date=date(2025, 1, 1), end_date=date(2025, 1, 10))
    assert t.date_range() == "01.01.2025 – 10.01.2025"


def test_status_label_and_badge_from_dict(make_task):
    t = make_task(status="pending")
    assert t.status_label() == "Ожидает оценки"
    assert t.status_badge() == "await"


def test_status_label_uses_status_name_if_given(make_task):
    t = make_task(status="pending", status_name="Кастомный", status_badge="custom")
    assert t.status_label() == "Кастомный"
    assert t.status_badge() == "custom"


def test_meta_text_contains_deadline_for_pending(make_task, today):
    t = make_task(status="pending", eval_deadline=date(2025, 2, 1))
    assert "Сбор оценок до: 01.02.2025" in t.meta_text()


def test_account_from_row():
    row = {"login": "zav@kaf", "password": "12345", "role": "zav", "name": "Зав"}
    acc = Account.from_row(row)
    assert acc.login == "zav@kaf"
    assert acc.role == "zav"


def test_staff_from_row_new_schema():
    row = {
        "id": 1, "name": "Егоров А.Р.", "type_code": "teacher",
        "position": "профессор", "department": "Кафедра ПИ",
    }
    s = Staff.from_row(row)
    assert s.type == "teacher"
    assert s.name == "Егоров А.Р."
    assert "профессор" in s.role
    assert "Кафедра ПИ" in s.role


def test_staff_from_row_fallback():
    row = {"id": 2, "name": "X", "type": "support", "role": "программист"}
    s = Staff.from_row(row)
    assert s.type == "support"
    assert s.role == "программист"


def test_task_from_row_with_assignments():
    today = date(2026, 11, 19)
    row = {
        "id": 5, "title": "T", "description": "D",
        "status": "assigned", "status_name": "Назначена", "status_badge": "asg",
        "is_archived": False,
        "start_date": today, "end_date": today,
        "eval_days": 3, "eval_deadline": today,
        "created_at": None, "archived_at": None,
        "assignments": [
            {"staff_id": 1, "name": "A", "is_done": False},
            {"staff_id": 2, "name": "B", "is_done": True},
        ],
        "ratings": [{"staff_id": 3, "name": "X", "score": 80}],
    }
    t = Task.from_row(row)
    assert t.performers == "A, B"
    assert t.performer_list() == ["A", "B"]
    assert t.performer_ids() == [1, 2]
    assert t.performers_done == ["B"]
    assert t.marked_done is True
    assert t.status_label() == "Назначена"
    assert t.status_badge() == "asg"