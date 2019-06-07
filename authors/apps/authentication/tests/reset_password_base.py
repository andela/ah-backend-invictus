from rest_framework.test import APIClient, APITestCase


class BaseTestCase(APITestCase):
    """ 
    Base Test class for out tests in this app
    Class will also house the setup and teardown
    methods for our tests.
    """
    def setUp(self):
        # Initialize the Testclient for the tests
        self.client = APIClient()
        self.reset_email_data = {
                "email": "sanyakenneth@gmail.com", "url": "joel"
            }
        self.reset_new_passwords_data = {
                "password": "abc?54321",
                "confirm_password": "abc?54321"
            }
        self.reset_invalid_new_passwords_data = {
                "password": "987654321",
                "confirm_password": "987654321"
            }
        self.reset_same_password_data = {
                "password": "?ad87654321",
                "confirm_password": "?ad87654321"
            }
