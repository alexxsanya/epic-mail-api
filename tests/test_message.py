from tests.test_base import BaseClass
import json


class TestMessageAPI(BaseClass):

    def test_missing_access_token(self):
        response = self.client.post(
            '/api/v1/messages',
            data=self.message,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn('Missing Authorization Header', str(response.data))

    def test_invalid_token(self):
        token = "eyJ0Ows41oPPtvBkiMCuVbavjce5KxFbk1DbIKJkgiid5Lk"
        response = self.client.post(
            '/api/v1/messages', data=self.message,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + token)
        )
        self.assertEqual(response.status_code, 422)
        self.assertIn('Not enough segments', str(response.data))

    def test_message_without_subject(self):
        response = self.client.post(
            '/api/v1/messages', data=self.missing_subject,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.assertIn('atleast a 4 letter Subject', str(response.data))

    def test_message_without_valid_body(self):
        response = self.client.post(
            '/api/v1/messages', data=self.missing_body,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.assertIn('atleast a 4 letter Message Body', str(response.data))

    def test_message_without_valid_receiver_email(self):
        response = self.client.post(
            '/api/v1/messages', data=self.invalid_receiver,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.assertIn('Invalid email format for ', str(response.data))

    def test_send_message_with_valid_fields(self):
        response = self.client.post(
            '/api/v1/messages', data=self.message,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.assertIn("Message successfully sent", str(response.data))

    def test_get_all_sent_messages(self):
        self.client.post(
            '/api/v1/messages', data=self.message,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.client.post(
            '/api/v1/messages', data=self.message2,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        response = self.client.get(
            '/api/v1/messages/sent',
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hey You', response.data)

    def test_get_specific_message_by_id(self):
        self.client.post(
            '/api/v1/messages', data=self.message,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.client.post(
            '/api/v1/messages', data=self.message2,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        response = self.client.get(
            '/api/v1/messages/2',
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Message successfully retrieved', str(response.data))

    def test_get_message_with_invalid_id(self):
        self.client.post(
            '/api/v1/messages', data=self.message,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        response = self.client.get(
            '/api/v1/messages/2',
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.assertIn('No message with supplied message', str(response.data))

    def test_delete_my_existing_message(self):
        self.client.post(
            '/api/v1/messages', data=self.message,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        response = self.client.delete(
            '/api/v1/messages/1',
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.assertIn(b"has been deleted", response.data)

    def test_delete_message_with_invalid_id(self):
        response = self.client.delete(
            '/api/v1/messages/1000',
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.assertIn(b"No message with provided i", response.data)

    def test_message_cant_be_deleted_by_not_owner(self):
        login2 = self.client.post(
            '/api/v1/auth/login',
            data=self.user2,
            content_type="application/json"
        )
        token2 = json.loads(login2.data.decode())['data'][0]['token']
        self.client.post(
            '/api/v1/messages', data=self.message,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + token2)
        )
        response = self.client.delete(
            '/api/v1/messages/1',
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.assertIn(
            b'You are not permitted to delete this message', response.data)

    def test_can_receiver_delete_message(self):
        login2 = self.client.post(
            '/api/v1/auth/login',
            data=self.user2,
            content_type="application/json"
        )
        token2 = json.loads(login2.data.decode())['data'][0]['token']
        self.client.post(
            '/api/v1/messages', data=self.message2,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + token2)
        )
        response = self.client.delete(
            '/api/v1/messages/1',
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.assertIn(b'has been deleted', response.data)

    def test_get_my_unread_message(self):
        response = self.client.get(
            '/api/v1/messages/unread',
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.assertIn(b"[]", response.data)

    def test_get_my_received_messages(self):
        login2 = self.client.post(
            '/api/v1/auth/login',
            data=self.user,
            content_type="application/json"
        )
        token2 = json.loads(login2.data.decode())['data'][0]['token']
        self.client.post(
            '/api/v1/messages', data=self.message2,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + token2)
        )
        response = self.client.get(
            '/api/v1/messages',
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.assertIn(b'Hey Bella', response.data)
