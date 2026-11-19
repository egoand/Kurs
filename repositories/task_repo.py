class TaskRepository:
    def __init__(self, database):
        self._db = database

    def load_all(self):
        return self._db.fetch_all("""
            SELECT t.id, t.title, t.description,
                   s.code AS status, s.name AS status_name, s.badge AS status_badge,
                   s.is_archived,
                   t.start_date, t.end_date, t.eval_days, t.eval_deadline,
                   t.created_at, t.archived_at,
                   COALESCE((
                       SELECT json_agg(json_build_object(
                           'staff_id', a.staff_id,
                           'name', st.name,
                           'is_done', a.is_done
                       ) ORDER BY st.name)
                       FROM task_assignments a
                       JOIN staff st ON st.id = a.staff_id
                       WHERE a.task_id = t.id
                   ), '[]') AS assignments,
                   COALESCE((
                       SELECT json_agg(json_build_object(
                           'staff_id', r.staff_id,
                           'name', st.name,
                           'score', r.score
                       ) ORDER BY st.name)
                       FROM task_ratings r
                       JOIN staff st ON st.id = r.staff_id
                       WHERE r.task_id = t.id
                   ), '[]') AS ratings
            FROM tasks t
            JOIN task_statuses s ON s.id = t.status_id
            ORDER BY t.id
        """)

    def _status_id(self, code):
        rows = self._db.fetch_all(
            "SELECT id FROM task_statuses WHERE code=%s", (code,))
        return rows[0]['id'] if rows else None

    def update_status(self, task_id, status_code, changed_by=None):
        sid = self._status_id(status_code)
        self._db.execute(
            "UPDATE tasks SET status_id=%s, archived_at=%s WHERE id=%s",
            (sid,
             "NOW()" if status_code == "archived" else None,
             task_id))
        self._db.execute(
            "INSERT INTO task_status_history (task_id, status_id, changed_by) VALUES (%s, %s, %s)",
            (task_id, sid, changed_by))

    def assign(self, task_id, staff_ids):
        self._db.execute("DELETE FROM task_assignments WHERE task_id=%s", (task_id,))
        for sid in staff_ids:
            self._db.execute(
                "INSERT INTO task_assignments (task_id, staff_id) VALUES (%s, %s)",
                (task_id, sid))
        self.update_status(task_id, "assigned")

    def delete(self, task_id):
        self._db.execute("DELETE FROM tasks WHERE id=%s", (task_id,))

    def archive(self, task_id, changed_by=None):
        self.update_status(task_id, "archived", changed_by)

    def create(self, title, description, eval_days, start_date, end_date, deadline):
        sid = self._status_id("pending")
        self._db.execute("""
            INSERT INTO tasks (title, description, status_id, start_date, end_date, eval_days, eval_deadline)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (title, description, sid, start_date, end_date, eval_days, deadline))
        self._db.execute(
            "INSERT INTO task_status_history (task_id, status_id, changed_by) "
            "SELECT id, %s, 'system' FROM tasks ORDER BY id DESC LIMIT 1", (sid,))

    def mark_done(self, task_id, staff_id):
        self._db.execute(
            "UPDATE task_assignments SET is_done=TRUE, done_at=NOW() "
            "WHERE task_id=%s AND staff_id=%s", (task_id, staff_id))

    def add_rating(self, task_id, staff_id, score):
        self._db.execute(
            "INSERT INTO task_ratings (task_id, staff_id, score) VALUES (%s, %s, %s) "
            "ON CONFLICT (task_id, staff_id) DO UPDATE SET score=EXCLUDED.score",
            (task_id, staff_id, score))

    def staff_id_by_name(self, name):
        rows = self._db.fetch_all("SELECT id FROM staff WHERE name=%s", (name,))
        return rows[0]['id'] if rows else None