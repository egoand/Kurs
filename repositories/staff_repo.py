class StaffRepository:
    def __init__(self, database):
        self._db = database

    def load_all(self):
        return self._db.fetch_all("SELECT * FROM staff ORDER BY id")