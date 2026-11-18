import pytest
from datetime import date, timedelta
from vm.filter_service import FilterService


def test_filter_by_query_matches_title(make_task):
    tasks = [
        make_task(id=1, title="Настройка сервера"),
        make_task(id=2, title="Проверка лабораторных"),
    ]
    f = FilterService(query="сервер")
    result = f.apply(tasks)
    assert [t.id for t in result] == [1]


def test_filter_by_query_case_insensitive(make_task):
    tasks = [make_task(title="Настройка СЕРВЕРА")]
    f = FilterService(query="сервер")
    assert len(f.apply(tasks)) == 1


def test_filter_by_status(make_task):
    tasks = [
        make_task(id=1, status="pending"),
        make_task(id=2, status="completed"),
        make_task(id=3, status="pending"),
    ]
    f = FilterService(status="pending")
    result = f.apply(tasks)
    assert {t.id for t in result} == {1, 3}


def test_status_all_returns_everything(make_task):
    tasks = [make_task(id=1, status="pending"), make_task(id=2, status="archived")]
    f = FilterService(status="all")
    assert len(f.apply(tasks)) == 2


def test_sort_ascending_by_start_date(make_task, today):
    tasks = [
        make_task(id=1, start_date=today + timedelta(days=10)),
        make_task(id=2, start_date=today + timedelta(days=1)),
    ]
    f = FilterService(ascending=True)
    result = f.apply(tasks)
    assert [t.id for t in result] == [2, 1]


def test_sort_descending_by_start_date(make_task, today):
    tasks = [
        make_task(id=1, start_date=today + timedelta(days=1)),
        make_task(id=2, start_date=today + timedelta(days=10)),
    ]
    f = FilterService(ascending=False)
    result = f.apply(tasks)
    assert [t.id for t in result] == [2, 1]


def test_archived_always_at_end(make_task, today):
    tasks = [
        make_task(id=1, status="archived", start_date=today + timedelta(days=1)),
        make_task(id=2, status="pending", start_date=today + timedelta(days=10)),
    ]
    f = FilterService(ascending=True)
    result = f.apply(tasks)
    assert [t.id for t in result] == [2, 1]


def test_empty_query_and_all_status_is_identity(make_task):
    tasks = [make_task(id=1), make_task(id=2)]
    f = FilterService()
    assert len(f.apply(tasks)) == 2