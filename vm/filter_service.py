class FilterService:
    def __init__(self, query="", status="all", ascending=False):
        self.query = query
        self.status = status
        self.ascending = ascending

    def apply(self, tasks):
        result = [
            t for t in tasks
            if not self.query or self.query.lower() in
            (t.title + t.description + t.performers + t.date_range()).lower()
        ]
        if self.status != "all":
            result = [t for t in result if t.status == self.status]
        result.sort(
            key=lambda t: (t.status == "archived",
                           t.start_date.toordinal() if self.ascending else -t.start_date.toordinal())
        )
        return result