class UserTestData:
    """User Test Data."""

    def __init__(self):
        self.user_registration = {
            "user": {
                "username": "mwinel",
                "email": "mwinel@live.com",
                "password": "12345678"
            }
        }

        self.user_login = {
            "user": {
                "email": "mwinel@live.com",
                "password": "12345678"
            }
        }

        self.activated_user = {
            "user": {
                "username": "mwinel",
                "email": "mwinel@live.com",
                "password": "12345678",
                "email_verified": True
            }
        }
