from db import db
from repositories.account_repo import AccountRepository
from repositories.staff_repo import StaffRepository
from repositories.task_repo import TaskRepository
from vm.auth_service import AuthService
from vm.task_service import TaskService
from models.staff import Staff


def make_account_repo():
    return AccountRepository(db)


def make_staff_repo():
    return StaffRepository(db)


def make_task_repo():
    return TaskRepository(db)


def make_auth_service():
    return AuthService(make_account_repo())


def make_task_service():
    return TaskService(make_task_repo())


def load_staff():
    return [Staff.from_row(r) for r in make_staff_repo().load_all()]