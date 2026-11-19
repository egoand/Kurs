class AccountRepository:
    def __init__(self, database):
        self._db = database

    def find(self, login, password):
        rows = self._db.fetch_all("""
            SELECT a.login, a.password, r.code AS role, a.name, a.staff_id
            FROM accounts a
            JOIN roles r ON r.id = a.role_id
            WHERE a.login=%s AND a.password=%s
        """, (login, password))
        return rows[0] if rows else None