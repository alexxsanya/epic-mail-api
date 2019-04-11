from tests.test_base import BaseClass
import json


class UserAPITests(BaseClass):

    def test_create_user(self):
        self.assertEqual(self.signup.status_code, 200)

    def test_create_user_existent_user(self):
        self.signup
        response = self.client.post(
            '/api/v1/auth/signup',
            data=self.existent_user,
            content_type="application/json"
        )

        self.assertIn("Your Email address already exist in the system",
                      str(response.data))

    def test_cant_create_user_with_an_invalid_email(self):
        response = self.client.post(
            '/api/v1/auth/signup',
            data=self.missing_email,
            content_type="application/json"
        )
        self.assertIn("Invalid email format for", str(response.data))

    def test_cant_create_user_without_password(self):
        response = self.client.post(
            '/api/v1/auth/signup',
            data=self.invalid_password,
            content_type="application/json"
        )
        self.assertIn(
            "Password should be atleast 6 char a combination of",
            str(response.data))

    def test_cant_create_user_without_valid_name(self):
        response = self.client.post(
            '/api/v1/auth/signup',
            data=self.invalid_firstname,
            content_type="application/json"
        )
        self.assertIn(
            "Firstname should be atleast 2 letters without ",
            str(response.data))

    def test_cant_create_user_with_same_name(self):
        response = self.client.post(
            '/api/v1/auth/signup',
            data=self.same_first_lastname,
            content_type="application/json"
        )
        self.assertIn("Firstname & Lastname can not be the same",
                      str(response.data))

    def test_cant_create_user_with_invalid_lastname(self):
        response = self.client.post(
            '/api/v1/auth/signup',
            data=self.invalid_lastname,
            content_type="application/json"
        )
        self.assertIn(
            "Lastname should be atleast 2 letters without ", str(response.data))

    def test_cant_create_user_with_same_emails(self):
        response = self.client.post(
            '/api/v1/auth/signup',
            data=self.same_user_recoveremail,
            content_type="application/json"
        )
        self.assertIn(
            "Recovery email & your choosen email address ", str(response.data))

    def test_user_cant_log_in_without_username(self):
        response = self.client.post(
            '/api/v1/auth/login',
            data=self.missing_email,
            content_type="application/json"
        )
        self.assertIn("Invalid email format for", str(response.data))

    def test_user_cant_log_in_without_password(self):
        response = self.client.post(
            '/api/v1/auth/login',
            data=self.invalid_password,
            content_type="application/json"
        )
        self.assertIn("Password should be atleast 6 char a ",
                      str(response.data))

    def test_user_cant_log_in_inexistent_cred(self):
        response = self.client.post(
            '/api/v1/auth/login',
            data=self.incorrect_cred,
            content_type="application/json"
        )
        self.assertIn("No user with supplied password or email address",
                      str(response.data))

    def test_user_can_access_documentation(self):
        response = self.client.get(
            '/api/v1/doc'
        )
        self.assertEqual(response.status_code, 302)

    def test_get_all_users(self):
        response = self.client.get(
            'api/v1/auth/users'
        )
        self.assertEqual(response.status_code, 200)
