class TaskRepository:
    def __init__(self, database):
        self._db = database

    def load_all(self):
        return self._db.fetch_all("""
            SELECT t.*,
                   COALESCE(json_agg(json_build_object('name', r.evaluator, 'score', r.score))
                            FILTER (WHERE r.id IS NOT NULL), '[]') AS ratings
            FROM tasks t
            LEFT JOIN ratings r ON r.task_id = t.id
            GROUP BY t.id
            ORDER BY t.id
        """)

    def update_status(self, task_id, status):
        self._db.execute("UPDATE tasks SET status=%s WHERE id=%s", (status, task_id))

    def assign(self, task_id, performers):
        self._db.execute(
            "UPDATE tasks SET performers=%s, status='assigned' WHERE id=%s",
            (performers, task_id)
        )

    def delete(self, task_id):
        self._db.execute("DELETE FROM tasks WHERE id=%s", (task_id,))

    def archive(self, task_id):
        self._db.execute("UPDATE tasks SET status='archived' WHERE id=%s", (task_id,))

    def create(self, title, description, eval_days, start_date, end_date, deadline):
        self._db.execute("""
            INSERT INTO tasks (title, status, start_date, end_date, description, eval_days, eval_deadline)
            VALUES (%s, 'pending', %s, %s, %s, %s, %s)
        """, (title, start_date, end_date, description, eval_days, deadline))

    def mark_done(self, task_id, performer):
        self._db.execute(
            "UPDATE tasks SET marked_done=TRUE, performers_done=array_append(performers_done, %s) WHERE id=%s",
            (performer, task_id)
        )

    def add_rating(self, task_id, evaluator, score):
        self._db.execute(
            "INSERT INTO ratings (task_id, evaluator, score) VALUES (%s, %s, %s)",
            (task_id, evaluator, score)
        )