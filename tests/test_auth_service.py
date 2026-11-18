import pytest
from vm.auth_service import AuthService


def test_login_success(fake_account_repo):
    fake_account_repo.row = {
        "login": "zav@kaf", "password": "12345",
        "role": "zav", "name": "Заведующий",
    }
    svc = AuthService(fake_account_repo)
    user, err = svc.login("zav@kaf", "12345")
    assert err is None
    assert user == {"login": "zav@kaf", "role": "zav", "name": "Заведующий"}


def test_login_wrong_credentials(fake_account_repo):
    fake_account_repo.row = None
    svc = AuthService(fake_account_repo)
    user, err = svc.login("bad", "bad")
    assert user is None
    assert err == "Неверный логин или пароль"


def test_login_empty_login(fake_account_repo):
    svc = AuthService(fake_account_repo)
    user, err = svc.login("", "12345")
    assert user is None
    assert err == "Заполните оба поля"


def test_login_empty_password(fake_account_repo):
    svc = AuthService(fake_account_repo)
    user, err = svc.login("zav@kaf", "")
    assert user is None
    assert err == "Заполните оба поля"


def test_login_strips_and_lowercases(fake_account_repo):
    fake_account_repo.row = {
        "login": "zav@kaf", "password": "12345",
        "role": "zav", "name": "Зав",
    }
    svc = AuthService(fake_account_repo)
    svc.login("  ZAV@KAF  ", "  12345  ")
    assert fake_account_repo.last_query == ("zav@kaf", "12345")