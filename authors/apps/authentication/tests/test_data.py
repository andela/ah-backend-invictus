class TestData:
    """
    class houses data that will be used for the 
    different test scenarios.
    """

    def __init__(self):
        self.signup_data = {
            "user": {
                "username": "sanyat",
                "email": "sanyakennetht@gmail.com",
                "password": "@sanya1234"
            }
        }
        self.blank_username_on_signup = {
            "user": {
                "username": "",
                "email": "sanyakenneth@gmail.com",
                "password": "sanya1234"
            }
        }
        self.blank_email_on_signup = {
            "user": {
                "username": "sanya",
                "email": "",
                "password": "sanya1234"
            }
        }
        self.blank_password_on_signup = {
            "user": {
                "username": "sanya",
                "email": "sanyakenneth@gmail.com",
                "password": ""
            }
        }
        self.invalid_email_on_signup = {
            "user": {
                "username": "sanya",
                "email": "sanyakennethgmail.com",
                "password": "sanya1234"
            }
        }
        self.invalid_password_on_signup = {
            "user": {
                "username": "sanya",
                "email": "sanyakenneth@gmail.com",
                "password": "s"
            }
        }
        self.invalid_password_length = {
            "user": {
                "username": "sanya",
                "email": "sanyakenneth@gmail.com",
                "password": "sa"
            }
        }
        self.login_data = {
           "user": {
                "email": "sanyaken@gmail.com",
                "password": "sanyaken123456"
            } 
        }
        self.login_data2 = {
           "user": {
                "email": "kenned@gmail.com",
                "password": "kenned123456"
            } 
        }
        self.login_data_admin = {
           "user": {
                "email": "admin@gmail.com",
                "password": "admin123456"
            } 
        }
        self.wrong_login_data = {
           "user": {
                "email": "sanyakenneth@gmail.com",
                "password": "sanya1234"
            } 
        }
        self.blank_email = {
           "user": {
                "email": "",
                "password": "sanya1234"
            } 
        }
        self.blank_password = {
           "user": {
                "email": "sanyakenneth@gmail.com",
                "password": ""
            } 
        }
        self.no_email_on_login = {
           "user": {
                "password": "kensanya1234"
            } 
        }
        self.no_password_on_login = {
           "user": {
                "email": "sanyakenneth@gmail.com"
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
