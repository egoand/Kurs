import pytest
from datetime import date, timedelta


def test_today_fixture(today):
    assert isinstance(today, date)


def test_make_task_defaults(make_task):
    task = make_task()
    assert task.id == 1
    assert task.title == "Тестовая работа"
    assert task.status == "pending"
    assert task.eval_days == 3
    assert task.marked_done is False
    assert task.ratings == []
    assert task.performers_done == []


def test_make_task_overrides(make_task, today):
    task = make_task(id=42, title="Другая", status="done")
    assert task.id == 42
    assert task.title == "Другая"
    assert task.status == "done"
    assert task.start_date == today + timedelta(days=5)


def test_make_staff(make_staff):
    staff = make_staff()
    assert staff.id == 1
    assert staff.name == "Егоров А.Р."
    assert staff.type == "teacher"
    assert staff.role == "профессор"


def test_make_staff_overrides(make_staff):
    staff = make_staff(id_=7, name="Иванов И.И.", type_="student", role="староста")
    assert staff.id == 7
    assert staff.name == "Иванов И.И."
    assert staff.type == "student"
    assert staff.role == "староста"


def test_fake_task_repo_records_calls(fake_task_repo):
    repo = fake_task_repo
    repo.update_status(1, "done")
    repo.assign(1, "Егоров")
    repo.delete(2)
    repo.archive(3)
    repo.create("T", "D", 3, None, None, None)
    repo.mark_done(1, "Егоров")
    repo.add_rating(1, "Егоров", 5)

    assert repo.status_updates == [(1, "done")]
    assert repo.assigns == [(1, "Егоров")]
    assert repo.deletes == [2]
    assert repo.archives == [3]
    assert repo.creates == [("T", "D", 3, None, None, None)]
    assert repo.marked_done == [(1, "Егоров")]
    assert repo.ratings == [(1, "Егоров", 5)]
    assert repo.load_all() == []


def test_fake_account_repo_found(fake_account_repo):
    fake_account_repo.row = {"login": "admin", "role": "admin"}
    result = fake_account_repo.find("admin", "123")
    assert result == {"login": "admin", "role": "admin"}
    assert fake_account_repo.last_query == ("admin", "123")


def test_fake_account_repo_not_found(fake_account_repo):
    result = fake_account_repo.find("nobody", "pass")
    assert result is None
    assert fake_account_repo.last_query == ("nobody", "pass")