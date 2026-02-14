class Usuario:
    def __init__(self, id: int, username: str, password_hash: str, email: str = None, is_admin: bool = False):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.is_admin = is_admin
