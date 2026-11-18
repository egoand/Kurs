import pytest
from datetime import date, timedelta
from models.task import Task
from models.staff import Staff


@pytest.fixture
def today():
    return date(2026, 11, 19)


@pytest.fixture
def make_task(today):
    def _make(**overrides):
        defaults = dict(
            id=1,
            title="Тестовая работа",
            status="pending",
            start_date=today + timedelta(days=5),
            end_date=today + timedelta(days=15),
            performers="",
            description="Описание",
            ratings=[],
            eval_days=3,
            eval_deadline=today + timedelta(days=2),
            marked_done=False,
            performers_done=[],
        )
        defaults.update(overrides)
        return Task(**defaults)
    return _make


@pytest.fixture
def make_staff():
    def _make(name="Егоров А.Р.", type_="teacher", role="профессор", id_=1):
        return Staff(id_, name, type_, role)
    return _make


class FakeTaskRepo:
    def __init__(self):
        self.status_updates = []
        self.assigns = []
        self.deletes = []
        self.archives = []
        self.creates = []
        self.marked_done = []
        self.ratings = []

    def load_all(self):
        return []

    def update_status(self, task_id, status):
        self.status_updates.append((task_id, status))

    def assign(self, task_id, performers):
        self.assigns.append((task_id, performers))

    def delete(self, task_id):
        self.deletes.append(task_id)

    def archive(self, task_id):
        self.archives.append(task_id)

    def create(self, title, description, eval_days, start_date, end_date, deadline):
        self.creates.append((title, description, eval_days, start_date, end_date, deadline))

    def mark_done(self, task_id, performer):
        self.marked_done.append((task_id, performer))

    def add_rating(self, task_id, evaluator, score):
        self.ratings.append((task_id, evaluator, score))


@pytest.fixture
def fake_task_repo():
    return FakeTaskRepo()


class FakeAccountRepo:
    def __init__(self, row=None):
        self.row = row
        self.last_query = None

    def find(self, login, password):
        self.last_query = (login, password)
        return self.row


@pytest.fixture
def fake_account_repo():
    return FakeAccountRepo()