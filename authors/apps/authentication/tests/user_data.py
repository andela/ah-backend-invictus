class UserTestData:
    """User Test Data."""

    def __init__(self):
    
        self.user_login = {
            "user": {
                "email": "mwinel@live.com",
                "password": "1234$qwe"
            }
        }

        self.activated_user = {
            "user": {
                "username": "mwinel",
                "email": "mwinel@live.com",
                "password": "1234$qwe",
                "email_verified": True
                }
        }

        self.user_registration = {
            "user": {
               "username": "mwinel",
                "email": "mwinel@live.com",
                "password": "1234$qwe",
            }
        }
        self.invalid_username = {
            "user": {
                "username": "edn",
                "email": "edna@example.com",
                "password": "edna@1234"
            }
        }
        self.username_with_space = {
            "user": {
                "username": "ed na",
                "email": "edna@example.com",
                "password": "edna@1234"
            }
        }
        self.invalid_password = {
            "user": {
                "username": "edina",
                "email": "edna@example.com",
                "password": "edna@23"
            }
        }
        self.non_numeric_password = {
            "user": {
                "username": "edina",
                "email": "edna@example.com",
                "password": "@nakajugo"
            }
        }
        self.password_with_space = {
            "user": {
                "username": "edina",
                "email": "edna@example.com",
                "password": "@naka1 jugo"
            }
        }
        self.username_with_no_characters = {
            "user": {
                "username": ".....",
                "email": "edna@example.com",
                "password": "@naka1jugo"
            }
        }
