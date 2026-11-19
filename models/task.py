from models.status import get_status


class Task:
    def __init__(self, id, title, status, start_date, end_date, performers,
                 description, ratings, eval_days, eval_deadline, marked_done,
                 performers_done, status_name=None, status_badge=None,
                 is_archived=False, assignments=None):
        self.id = id
        self.title = title
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
        self.performers = performers
        self.description = description
        self.ratings = ratings
        self.eval_days = eval_days
        self.eval_deadline = eval_deadline
        self.marked_done = marked_done
        self.performers_done = performers_done
        self._status_name = status_name
        self._status_badge = status_badge
        self.is_archived = is_archived
        self.assignments = assignments or []

    @classmethod
    def from_row(cls, row):
        assignments = row.get('assignments') or []
        performers = ", ".join(a['name'] for a in assignments)
        performers_done = [a['name'] for a in assignments if a['is_done']]
        return cls(
            id=row['id'],
            title=row['title'],
            status=row['status'],
            start_date=row['start_date'],
            end_date=row['end_date'],
            performers=performers,
            description=row['description'] or '',
            ratings=row.get('ratings') or [],
            eval_days=row['eval_days'] or 3,
            eval_deadline=row['eval_deadline'] or row['start_date'],
            marked_done=bool(performers_done),
            performers_done=performers_done,
            status_name=row.get('status_name'),
            status_badge=row.get('status_badge'),
            is_archived=row.get('is_archived', False),
            assignments=assignments,
        )

    def date_range(self):
        return f"{self.start_date.strftime('%d.%m.%Y')} – {self.end_date.strftime('%d.%m.%Y')}"

    def average_score(self):
        if not self.ratings:
            return None
        return round(sum(r["score"] for r in self.ratings) / len(self.ratings))

    def performer_list(self):
        return [a['name'] for a in self.assignments]

    def performer_ids(self):
        return [a['staff_id'] for a in self.assignments]

    def rated_by(self, name):
        return any(r["name"] == name for r in self.ratings)

    def status_label(self):
        return self._status_name or get_status(self.status).label

    def status_badge(self):
        return self._status_badge or get_status(self.status).badge

    def meta_text(self):
        s = f"Срок: {self.date_range()}    Сотрудники: {self.performers or '—'}"
        if self.status == "pending" and self.eval_deadline:
            s += f"    Сбор оценок до: {self.eval_deadline.strftime('%d.%m.%Y')}"
        return s