class Account:
    def __init__(self, login, password, role, name):
        self.login = login
        self.password = password
        self.role = role
        self.name = name

    @classmethod
    def from_row(cls, row):
        return cls(row['login'], row['password'], row['role'], row['name'])