class Staff:
    def __init__(self, id, name, type_, role):
        self.id = id
        self.name = name
        self.type = type_
        self.role = role

    @classmethod
    def from_row(cls, row):
        type_code = row.get('type_code') or row.get('type') or 'support'
        position = row.get('position') or ''
        department = row.get('department') or ''
        role = f"{position} | {department}".strip(' |')
        return cls(row['id'], row['name'], type_code, role)