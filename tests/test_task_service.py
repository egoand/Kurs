import pytest
from datetime import date, timedelta
from vm.task_service import TaskService


def test_create_returns_error_on_empty_title(fake_task_repo, today):
    svc = TaskService(fake_task_repo)
    err = svc.create("", "desc", 3, today, today + timedelta(days=5))
    assert err == "Введите название"
    assert fake_task_repo.creates == []


def test_create_returns_error_when_end_before_start(fake_task_repo, today):
    svc = TaskService(fake_task_repo)
    err = svc.create("T", "d", 3, today + timedelta(days=5), today)
    assert err == "Дата завершения раньше даты начала"
    assert fake_task_repo.creates == []


def test_create_passes_correct_deadline(fake_task_repo, today):
    svc = TaskService(fake_task_repo)
    start = today + timedelta(days=10)
    err = svc.create("T", "d", 3, start, start + timedelta(days=5))
    assert err is None
    title, desc, ev, sd, ed, deadline = fake_task_repo.creates[0]
    assert title == "T"
    assert ev == 3
    assert deadline == start - timedelta(days=3)


def test_expire_overdue_marks_pending_as_evaluated(fake_task_repo, today, make_task):
    svc = TaskService(fake_task_repo, today_fn=lambda: today)
    overdue = make_task(status="pending", eval_deadline=today - timedelta(days=1))
    changed = svc.expire_overdue([overdue])
    assert changed is True
    assert overdue.status == "evaluated"
    assert fake_task_repo.status_updates == [(1, "evaluated")]


def test_expire_overdue_ignores_non_pending(fake_task_repo, today, make_task):
    svc = TaskService(fake_task_repo, today_fn=lambda: today)
    t = make_task(status="completed", eval_deadline=today - timedelta(days=1))
    assert svc.expire_overdue([t]) is False


def test_expire_overdue_ignores_future_deadline(fake_task_repo, today, make_task):
    svc = TaskService(fake_task_repo, today_fn=lambda: today)
    t = make_task(status="pending", eval_deadline=today + timedelta(days=1))
    assert svc.expire_overdue([t]) is False


def test_assign_sets_performers_and_status(fake_task_repo, make_task):
    svc = TaskService(fake_task_repo)
    t = make_task(status="evaluated")
    svc.assign(t, ["A", "B"])
    assert t.performers == "A, B"
    assert t.status == "assigned"
    assert fake_task_repo.assigns == [(1, "A, B")]


def test_archive_sets_status(fake_task_repo, make_task):
    svc = TaskService(fake_task_repo)
    t = make_task(status="completed")
    svc.archive(t)
    assert t.status == "archived"
    assert fake_task_repo.archives == [1]


def test_delete_calls_repo(fake_task_repo, make_task):
    svc = TaskService(fake_task_repo)
    svc.delete(make_task())
    assert fake_task_repo.deletes == [1]


def test_can_rate_true_for_pending_undated(fake_task_repo, today, make_task):
    svc = TaskService(fake_task_repo, today_fn=lambda: today)
    t = make_task(status="pending", eval_deadline=today + timedelta(days=1))
    assert svc._can_rate(t, "X") is True


def test_can_rate_false_when_already_rated(fake_task_repo, today, make_task):
    svc = TaskService(fake_task_repo, today_fn=lambda: today)
    t = make_task(status="pending", eval_deadline=today + timedelta(days=1),
                  ratings=[{"name": "X", "score": 80}])
    assert svc._can_rate(t, "X") is False


def test_can_rate_false_after_deadline(fake_task_repo, today, make_task):
    svc = TaskService(fake_task_repo, today_fn=lambda: today)
    t = make_task(status="pending", eval_deadline=today - timedelta(days=1))
    assert svc._can_rate(t, "X") is False


def test_can_rate_false_when_not_pending(fake_task_repo, today, make_task):
    svc = TaskService(fake_task_repo, today_fn=lambda: today)
    t = make_task(status="assigned", eval_deadline=today + timedelta(days=1))
    assert svc._can_rate(t, "X") is False


def test_add_rating_rejects_out_of_range(fake_task_repo, today, make_task):
    svc = TaskService(fake_task_repo, today_fn=lambda: today)
    t = make_task(status="pending", eval_deadline=today + timedelta(days=1))
    assert svc.add_rating(t, "X", 0) == "Оценка 1–100"
    assert svc.add_rating(t, "X", 101) == "Оценка 1–100"


def test_add_rating_rejects_when_cannot_rate(fake_task_repo, today, make_task):
    svc = TaskService(fake_task_repo, today_fn=lambda: today)
    t = make_task(status="completed", eval_deadline=today + timedelta(days=1))
    assert svc.add_rating(t, "X", 80) == "Оценка недоступна"


def test_add_rating_success_appends(fake_task_repo, today, make_task):
    svc = TaskService(fake_task_repo, today_fn=lambda: today)
    t = make_task(status="pending", eval_deadline=today + timedelta(days=1))
    err = svc.add_rating(t, "X", 80)
    assert err is None
    assert t.ratings == [{"name": "X", "score": 80}]
    assert fake_task_repo.ratings == [(1, "X", 80)]


def test_start_fails_before_start_date(fake_task_repo, today, make_task):
    svc = TaskService(fake_task_repo, today_fn=lambda: today)
    t = make_task(status="assigned", start_date=today + timedelta(days=1))
    err = svc.start(t)
    assert err is not None
    assert "начнётся" in err
    assert t.status == "assigned"


def test_start_success_sets_in_progress(fake_task_repo, today, make_task):
    svc = TaskService(fake_task_repo, today_fn=lambda: today)
    t = make_task(status="assigned", start_date=today)
    assert svc.start(t) is None
    assert t.status == "in_progress"


def test_complete_single_performer(fake_task_repo, today, make_task):
    svc = TaskService(fake_task_repo, today_fn=lambda: today)
    t = make_task(status="in_progress", start_date=today, performers="A")
    assert svc.complete(t, "A") is None
    assert t.status == "completed"
    assert fake_task_repo.status_updates == [(1, "completed")]


def test_complete_multi_waits_for_all(fake_task_repo, today, make_task):
    svc = TaskService(fake_task_repo, today_fn=lambda: today)
    t = make_task(status="in_progress", start_date=today, performers="A, B")
    svc.complete(t, "A")
    assert t.status == "in_progress"
    assert "A" in t.performers_done
    assert fake_task_repo.marked_done == [(1, "A")]
    assert fake_task_repo.status_updates == []

    svc.complete(t, "B")
    assert t.status == "completed"
    assert fake_task_repo.status_updates == [(1, "completed")]


def test_complete_fails_before_start_date(fake_task_repo, today, make_task):
    svc = TaskService(fake_task_repo, today_fn=lambda: today)
    t = make_task(status="in_progress", start_date=today + timedelta(days=1), performers="A")
    err = svc.complete(t, "A")
    assert err is not None
    assert t.status == "in_progress"