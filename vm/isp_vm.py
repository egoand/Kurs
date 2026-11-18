from vm.filter_service import FilterService
from vm.pagination import Paginator


class IspVM:
    def __init__(self, user, task_service, task_repo):
        self.user = user
        self._service = task_service
        self._repo = task_repo
        self.tasks = self._service.load_all()
        self.filter = FilterService()
        self.paginator = Paginator()
        self.shown = []

    def _refresh_statuses(self):
        if self._service.expire_overdue(self.tasks):
            self.tasks = self._service.load_all()

    def _source(self, lst):
        return self.filter.apply(lst)

    def refresh_history(self):
        self._refresh_statuses()
        self.shown = self._source(self.tasks)
        return self.paginator.slice(self.shown)

    def my_tasks(self):
        result = []
        for t in self.tasks:
            if t.status in ("evaluated", "pending") and t.rated_by(self.user["name"]):
                continue
            if t.performers and self.user["name"] in t.performer_list():
                result.append(t)
        return result

    def refresh_my(self):
        self._refresh_statuses()
        self.shown = self._source(self.my_tasks())
        return self.paginator.slice(self.shown)

    def can_rate(self, task):
        return self._service._can_rate(task, self.user["name"])

    def rate(self, task, score):
        return self._service.add_rating(task, self.user["name"], score)

    def start(self, task):
        return self._service.start(task)

    def complete(self, task):
        return self._service.complete(task, self.user["name"])