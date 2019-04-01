from tests.test_base import BaseClass
import json


class TestGroupAPI(BaseClass):

    def test_create_group_with_details(self):
        response = self.client.post(
            '/api/v1/groups',
            data=self.group,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        group = json.loads(response.data.decode())['data'][0]
        self.assertIn('devs', str(group))

    def test_group_duplicate_is_denied(self):
        self.client.post(
            '/api/v1/groups',
            data=self.group,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        response = self.client.post(
            '/api/v1/groups',
            data=self.group,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )

        self.assertIn('Group name -', str(response.data))

    def test_create_group_with_invalid_name(self):
        response = self.client.post(
            '/api/v1/groups',
            data=self.invalid_group_name,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.assertIn(
            b'Name should at 4 char but not exceed 50', response.data)

    def test_create_group_with_invalid_role(self):
        response = self.client.post(
            '/api/v1/groups',
            data=self.invalid_group_role,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.assertIn(b'Role should be atleast 10 char but', response.data)

    def test_get_all_my_groups(self):
        self.client.post(
            '/api/v1/groups',
            data=self.group,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.client.post(
            '/api/v1/groups',
            data=self.group2,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )

        response = self.client.get(
            '/api/v1/groups',
            headers=dict(Authorization='Bearer ' + self.token)
        )
        groups = json.loads(response.data.decode())['data']

        self.assertEqual(2, len(groups))

    def test_update_group_name(self):
        self.client.post(
            '/api/v1/groups',
            data=self.group,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        response = self.client.patch(
            '/api/v1/groups/1/developer',
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.assertIn('developer', str(response.data))

    def test_delete_group(self):
        self.client.post(
            '/api/v1/groups',
            data=self.group,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        response = self.client.delete(
            '/api/v1/groups/1',
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.assertIn('deleted', str(response.data))

    def test_add_member_to_a_group(self):
        self.signup
        self.client.post(
            '/api/v1/groups',
            data=self.group,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        response = self.client.post(
            'api/v1/groups/1/users',
            data=self.g_member,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )

        self.assertIn(b'junior dev', response.data)

    def test_duplicate_members_in_group_not_allowed(self):
        self.signup
        self.client.post(
            '/api/v1/groups',
            data=self.group,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.client.post(
            'api/v1/groups/1/users',
            data=self.g_member,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )

        response = self.client.post(
            'api/v1/groups/1/users',
            data=self.g_member,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )

        self.assertIn(b'is already a member of group', response.data)

    def test_remove_member_to_a_group(self):
        self.signup
        self.client.post(
            '/api/v1/groups',
            data=self.group2,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        response = self.client.delete(
            '/api/v1/groups/1/users/1',
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.assertIn(b'deleted from group', response.data)

    def test_send_message_to_group_of_members(self):
        self.signup
        self.signup2
        self.client.post(
            '/api/v1/groups',
            data=self.group,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.client.post(
            'api/v1/groups/1/users',
            data=self.g_member,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.client.post(
            'api/v1/groups/1/users',
            data=self.g_member2,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )

        response = self.client.post(
            '/api/v1/groups/1/messages',
            data=self.group_msg,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        sent_to = json.loads(response.data.decode())
        self.assertEqual(2, len(sent_to))

    def test_message_is_only_sent_to_existent_group(self):
        self.signup
        self.client.post(
            '/api/v1/groups',
            data=self.group,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        self.client.post(
            'api/v1/groups/1/users',
            data=self.g_member,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        response = self.client.post(
            '/api/v1/groups/2/messages',
            data=self.group_msg,
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )

        self.assertIn(b"No group with id", response.data)
