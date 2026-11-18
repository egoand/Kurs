class Paginator:
    def __init__(self, page=1, page_size=10):
        self.page = page
        self.page_size = page_size

    def slice(self, items):
        total_pages = max(1, (len(items) + self.page_size - 1) // self.page_size)
        if self.page > total_pages:
            self.page = 1
        start = (self.page - 1) * self.page_size
        return items[start:start + self.page_size], total_pages