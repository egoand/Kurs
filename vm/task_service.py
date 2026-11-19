from datetime import date, timedelta


class TaskService:
    def __init__(self, task_repo, today_fn=None):
        self._repo = task_repo
        self._today = today_fn or date.today

    def load_all(self):
        from models.task import Task
        return [Task.from_row(r) for r in self._repo.load_all()]

    def expire_overdue(self, tasks):
        changed = False
        for t in tasks:
            if t.status == "pending" and self._today() > t.eval_deadline:
                self._repo.update_status(t.id, "evaluated", changed_by="system")
                t.status = "evaluated"
                changed = True
        return changed

    def assign(self, task, names):
        ids = []
        for name in names:
            sid = self._repo.staff_id_by_name(name)
            if sid:
                ids.append(sid)
        self._repo.assign(task.id, ids)
        task.status = "assigned"

    def delete(self, task):
        self._repo.delete(task.id)

    def archive(self, task, changed_by="zav"):
        self._repo.archive(task.id, changed_by)
        task.status = "archived"

    def create(self, title, description, eval_days, start_date, end_date):
        if not title:
            return "Введите название"
        if end_date < start_date:
            return "Дата завершения раньше даты начала"
        deadline = start_date - timedelta(days=eval_days)
        self._repo.create(title, description, eval_days, start_date, end_date, deadline)
        return None

    def add_rating(self, task, evaluator, score):
        if score < 1 or score > 100:
            return "Оценка 1–100"
        if not self._can_rate(task, evaluator):
            return "Оценка недоступна"
        sid = self._repo.staff_id_by_name(evaluator)
        if not sid:
            return "Сотрудник не найден"
        self._repo.add_rating(task.id, sid, score)
        task.ratings.append({"staff_id": sid, "name": evaluator, "score": score})
        return None

    def start(self, task):
        if self._today() < task.start_date:
            return f"Работа начнётся {task.start_date.strftime('%d.%m.%Y')}"
        self._repo.update_status(task.id, "in_progress", changed_by=task.performers)
        task.status = "in_progress"
        return None

    def complete(self, task, performer):
        if self._today() < task.start_date:
            return f"Нельзя раньше {task.start_date.strftime('%d.%m.%Y')}"
        performers = task.performer_list()
        sid = self._repo.staff_id_by_name(performer)
        if not sid:
            return "Сотрудник не найден"
        if len(performers) > 1:
            if performer not in task.performers_done:
                self._repo.mark_done(task.id, sid)
                task.performers_done.append(performer)
            task.marked_done = True
            if all(p in task.performers_done for p in performers):
                self._repo.update_status(task.id, "completed", changed_by=performer)
                task.status = "completed"
        else:
            self._repo.mark_done(task.id, sid)
            self._repo.update_status(task.id, "completed", changed_by=performer)
            task.status = "completed"
        return None

    def _can_rate(self, task, evaluator):
        if task.status != "pending":
            return False
        if task.rated_by(evaluator):
            return False
        return self._today() <= task.eval_deadline