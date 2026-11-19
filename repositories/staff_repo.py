class StaffRepository:
    def __init__(self, database):
        self._db = database

    def load_all(self):
        return self._db.fetch_all("""
            SELECT s.id, s.name, t.code AS type_code, s.position, s.department
            FROM staff s
            JOIN staff_types t ON t.id = s.type_id
            ORDER BY s.id
        """)