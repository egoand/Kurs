class Staff:
    def __init__(self, id, name, type_, role):
        self.id = id
        self.name = name
        self.type = type_
        self.role = role

    @classmethod
    def from_row(cls, row):
        return cls(row['id'], row['name'], row['type'], row['role'])