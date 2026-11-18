import pytest
from vm.rating_service import RatingService


def test_map_initialized_with_zeros(make_staff):
    staff = [make_staff(name="A"), make_staff(name="B")]
    m = RatingService().build_map([], staff)
    assert m["A"] == {"p": 0, "t": 0, "tot": 0}
    assert m["B"] == {"p": 0, "t": 0, "tot": 0}


def test_completed_task_adds_to_p(make_task, make_staff):
    staff = [make_staff(name="A")]
    task = make_task(status="completed", performers="A",
                     ratings=[{"name": "X", "score": 80}, {"name": "Y", "score": 90}])
    m = RatingService().build_map([task], staff)
    assert m["A"]["p"] == 85
    assert m["A"]["t"] == 0
    assert m["A"]["tot"] == 85


def test_assigned_and_in_progress_add_to_t(make_task, make_staff):
    staff = [make_staff(name="A")]
    tasks = [
        make_task(status="assigned", performers="A", ratings=[{"name": "X", "score": 80}]),
        make_task(status="in_progress", performers="A", ratings=[{"name": "X", "score": 100}]),
    ]
    m = RatingService().build_map(tasks, staff)
    assert m["A"]["t"] == 180
    assert m["A"]["p"] == 0
    assert m["A"]["tot"] == 180


def test_task_without_ratings_is_ignored(make_task, make_staff):
    staff = [make_staff(name="A")]
    task = make_task(status="completed", performers="A", ratings=[])
    m = RatingService().build_map([task], staff)
    assert m["A"]["tot"] == 0


def test_unknown_performer_is_skipped(make_task, make_staff):
    staff = [make_staff(name="A")]
    task = make_task(status="completed", performers="Неизвестный",
                     ratings=[{"name": "X", "score": 80}])
    m = RatingService().build_map([task], staff)
    assert m["A"]["tot"] == 0