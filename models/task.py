from models.status import get_status


class Task:
    def __init__(self, id, title, status, start_date, end_date, performers,
                 description, ratings, eval_days, eval_deadline, marked_done,
                 performers_done):
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

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row['id'],
            title=row['title'],
            status=row['status'],
            start_date=row['start_date'],
            end_date=row['end_date'],
            performers=row['performers'] or '',
            description=row['description'] or '',
            ratings=row['ratings'] or [],
            eval_days=row['eval_days'] or 3,
            eval_deadline=row['eval_deadline'] or row['start_date'],
            marked_done=row['marked_done'] or False,
            performers_done=list(row['performers_done'] or []),
        )

    def date_range(self):
        return f"{self.start_date.strftime('%d.%m.%Y')} – {self.end_date.strftime('%d.%m.%Y')}"

    def average_score(self):
        if not self.ratings:
            return None
        return round(sum(r["score"] for r in self.ratings) / len(self.ratings))

    def performer_list(self):
        return [x.strip() for x in self.performers.split(",") if x.strip()]

    def rated_by(self, name):
        return any(r["name"] == name for r in self.ratings)

    def status_label(self):
        return get_status(self.status).label

    def status_badge(self):
        return get_status(self.status).badge

    def meta_text(self):
        s = f"Срок: {self.date_range()}    Сотрудники: {self.performers or '—'}"
        if self.status == "pending" and self.eval_deadline:
            s += f"    Сбор оценок до: {self.eval_deadline.strftime('%d.%m.%Y')}"
        return s