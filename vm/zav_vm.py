from vm.rating_service import RatingService
from vm.filter_service import FilterService
from vm.pagination import Paginator


class ZavVM:
    def __init__(self, task_service, staff_list):
        self._service = task_service
        self._staff = staff_list
        self.tasks = self._service.load_all()
        self.filter = FilterService()
        self.paginator = Paginator()
        self.shown = []
        self._rating_service = RatingService()

    def _refresh_statuses(self):
        if self._service.expire_overdue(self.tasks):
            self.tasks = self._service.load_all()

    def refresh(self):
        self._refresh_statuses()
        self.shown = self.filter.apply(self.tasks)
        return self.paginator.slice(self.shown)

    def rating_map(self):
        return self._rating_service.build_map(self.tasks, self._staff)

    def assign(self, task, names):
        self._service.assign(task, names)

    def delete(self, task):
        self._service.delete(task)
        self.tasks = [t for t in self.tasks if t.id != task.id]

    def archive(self, task):
        self._service.archive(task)
        self.tasks = self._service.load_all()

    def create(self, title, description, eval_days, start_date, end_date):
        err = self._service.create(title, description, eval_days, start_date, end_date)
        if not err:
            self.tasks = self._service.load_all()
        return err

    def edit_performers(self, task, performers):
        names = [x.strip() for x in performers.split(",") if x.strip()]
        self._service.assign(task, names)
        self.tasks = self._service.load_all()