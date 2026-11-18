from models.account import Account


class AuthService:
    def __init__(self, account_repo):
        self._repo = account_repo

    def login(self, login, password):
        login = login.strip().lower()
        password = password.strip()
        if not login or not password:
            return None, "Заполните оба поля"
        row = self._repo.find(login, password)
        if not row:
            return None, "Неверный логин или пароль"
        acc = Account.from_row(row)
        return {"login": acc.login, "role": acc.role, "name": acc.name}, None