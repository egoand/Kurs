class LoginVM:
    def __init__(self, auth_service):
        self._auth = auth_service
        self.user = None

    def login(self, login, password):
        user, err = self._auth.login(login, password)
        if err:
            return None, err
        self.user = user
        return user, None