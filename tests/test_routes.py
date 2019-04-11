from tests.test_base import BaseClass


class UIRouteTests(BaseClass):

    def test_home_page_route(self):
        response = self.client.get(
            '/'
        )
        self.assertEqual(response.status_code, 200)

    def test_login_page_route(self):
        response = self.client.get(
            '/login.html'
        )
        self.assertEqual(response.status_code, 200)

    def test_signup_page_route(self):
        response = self.client.get(
            '/signup.html'
        )
        self.assertEqual(response.status_code, 200)

    def test_compose_message_page_route(self):
        response = self.client.get(
            '/components/compose.html'
        )
        self.assertEqual(response.status_code, 200)

    def test_group_page_route(self):
        response = self.client.get(
            '/components/groups.html'
        )
        self.assertEqual(response.status_code, 200)
