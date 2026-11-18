import pytest
from datetime import date
from models.task import Task
from models.account import Account
from models.staff import Staff


def test_performer_list_strips_and_splits(make_task):
    t = make_task(performers="A, B , C")
    assert t.performer_list() == ["A", "B", "C"]


def test_performer_list_empty(make_task):
    assert make_task(performers="").performer_list() == []


def test_average_score_rounds_half_up(make_task):
    t = make_task(ratings=[{"name": "X", "score": 80}, {"name": "Y", "score": 91}])
    assert t.average_score() == 86  # 85.5 -> 86


def test_average_score_none_when_no_ratings(make_task):
    assert make_task(ratings=[]).average_score() is None


def test_rated_by_true(make_task):
    t = make_task(ratings=[{"name": "X", "score": 80}])
    assert t.rated_by("X") is True
    assert t.rated_by("Y") is False


def test_date_range_format(make_task, today):
    t = make_task(start_date=date(2025, 1, 1), end_date=date(2025, 1, 10))
    assert t.date_range() == "01.01.2025 – 10.01.2025"


def test_status_label_and_badge(make_task):
    t = make_task(status="pending")
    assert t.status_label() == "Ожидает оценки"
    assert t.status_badge() == "await"


def test_meta_text_contains_deadline_for_pending(make_task, today):
    t = make_task(status="pending", eval_deadline=date(2025, 2, 1))
    assert "Сбор оценок до: 01.02.2025" in t.meta_text()


def test_account_from_row():
    row = {"login": "zav@kaf", "password": "12345", "role": "zav", "name": "Зав"}
    acc = Account.from_row(row)
    assert acc.login == "zav@kaf"
    assert acc.role == "zav"


def test_staff_from_row():
    row = {"id": 1, "name": "Егоров А.Р.", "type": "teacher", "role": "профессор"}
    s = Staff.from_row(row)
    assert s.type == "teacher"
    assert s.name == "Егоров А.Р."