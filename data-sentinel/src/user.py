import re

class User:
    def __init__(self, email, name=None):
        if not self._is_valid_email(email):
            raise ValueError(f"Invalid email address: {email}")
        self._email = email
        self._name = name

    @staticmethod
    def _is_valid_email(email):
        # Simple regex for validating an email address
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    @property
    def email(self):
        return self._email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def __repr__(self):
        return f"User(email={self.email!r}, name={self.name!r})"

    def __str__(self):
        return f"User: {self.name} <{self.email}>"

# Exemplo de uso
try:
    user = User("example@example.com", "John Doe")
    print(user)
except ValueError as e:
    print(e)