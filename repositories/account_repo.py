class AccountRepository:
    def __init__(self, database):
        self._db = database

    def find(self, login, password):
        rows = self._db.fetch_all(
            "SELECT * FROM accounts WHERE login=%s AND password=%s",
            (login, password)
        )
        return rows[0] if rows else None