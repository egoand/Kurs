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
                self._repo.update_status(t.id, "evaluated")
                t.status = "evaluated"
                changed = True
        return changed

    def assign(self, task, names):
        performers = ", ".join(names)
        self._repo.assign(task.id, performers)
        task.performers = performers
        task.status = "assigned"

    def delete(self, task):
        self._repo.delete(task.id)

    def archive(self, task):
        self._repo.archive(task.id)
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
        self._repo.add_rating(task.id, evaluator, score)
        task.ratings.append({"name": evaluator, "score": score})
        return None

    def start(self, task):
        if self._today() < task.start_date:
            return f"Работа начнётся {task.start_date.strftime('%d.%m.%Y')}"
        self._repo.update_status(task.id, "in_progress")
        task.status = "in_progress"
        return None

    def complete(self, task, performer):
        if self._today() < task.start_date:
            return f"Нельзя раньше {task.start_date.strftime('%d.%m.%Y')}"
        performers = task.performer_list()
        if len(performers) > 1:
            if performer not in task.performers_done:
                self._repo.mark_done(task.id, performer)
                task.performers_done.append(performer)
            task.marked_done = True
            if all(p in task.performers_done for p in performers):
                self._repo.update_status(task.id, "completed")
                task.status = "completed"
        else:
            self._repo.update_status(task.id, "completed")
            task.status = "completed"
        return None

    def _can_rate(self, task, evaluator):
        if task.status != "pending":
            return False
        if task.rated_by(evaluator):
            return False
        return self._today() <= task.eval_deadline