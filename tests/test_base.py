import unittest
from unittest import TestCase
import json
from api import create_app
from api.util import DB_Manager


class BaseClass(TestCase):
    def setUp(self):
        """
        Define test variables and initialize app
        """
        env = "testing"
        db_con = DB_Manager(env)
        self.app = create_app(env)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db_con.create_tables()

        self.user = json.dumps({
            "email": "bella@epicmail.com",
            "firstname": "Bella",
            "lastname": "Kab",
            "password": "Bella@11",
            "recovery_email": "bellah@gmail.com"
        })
        self.user2 = json.dumps({
            "email": "alex@epicmail.com",
            "firstname": "Alex",
            "lastname": "Kab",
            "password": "Alex@11",
            "recovery_email": "alex@gmail.com"
        })

        self.existent_user = json.dumps({
            "email": "bella@epicmail.com",
            "firstname": "Bella",
            "lastname": "Kab",
            "password": "Bella@11",
            "recovery_email": "bellah@gmail.com"
        })
        self.missing_email = json.dumps({
            "email": "",
            "firstname": "Bella",
            "lastname": "Kab",
            "password": "Bella@11",
            "recovery_email": "bellah@gmail.com"
        })

        self.invalid_email = json.dumps({
            "email": "alasljsd@dsfma",
            "firstname": "Bella",
            "lastname": "Kab",
            "password": "Bella@11",
            "recovery_email": "bellah@gmail.com"
        })

        self.invalid_password = json.dumps({
            "email": "bellah@epicmail.com",
            "firstname": "Bella",
            "lastname": "Kab",
            "password": "lkdsds",
            "recovery_email": "bellah@gmail.com"
        })
        self.invalid_firstname = json.dumps({
            "email": "bellah@epicmail.com",
            "firstname": "a",
            "lastname": "Kab",
            "password": "Alex@1231",
            "recovery_email": "bellah@gmail.com"
        })
        self.invalid_lastname = json.dumps({
            "email": "bellah@epicmail.com",
            "firstname": "Aalex",
            "lastname": "7676sd",
            "password": "Alex@1231",
            "recovery_email": "bellah@gmail.com"
        })
        self.same_first_lastname = json.dumps({
            "email": "bellah@epicmail.com",
            "firstname": "Alex",
            "lastname": "Alex",
            "password": "Alex@1231",
            "recovery_email": "bellah@gmail.com"
        })
        self.same_user_recoveremail = json.dumps({
            "email": "admin@epicmail.com",
            "firstname": "Admin",
            "lastname": "Alex",
            "password": "Alex@1231",
            "recovery_email": "admin@epicmail.com"
        })
        self.incorrect_cred = json.dumps({
            'email': "djskhskfa@dsfasf.dsfa",
            'password': "Asdsds@123"
        })
        self.message = json.dumps({
            "subject": "Hey You",
            "receiver": "alex@epicmail.com",
            "msgBody": "How are you doing"
        })

        self.message2 = json.dumps({
            "subject": "Hey Bella",
            "receiver": "bella@epicmail.com",
            "msgBody": "How are you doing"
        })

        self.missing_subject = json.dumps({
            "subject": "",
            "receiver": "alex@epicmail.com",
            "msgBody": "How are you doing"
        })

        self.missing_body = json.dumps({
            "subject": "Hello",
            "receiver": "alex@epicmail.com",
            "msgBody": ""
        })

        self.invalid_receiver = json.dumps({
            "subject": "Hello",
            "receiver": "alexepicmail.com",
            "msgBody": "Helo over there"
        })
        self.signup = self.client.post(
            '/api/v1/auth/signup',
            data=self.user,
            content_type="application/json"
        )

        self.signup2 = self.client.post(
            '/api/v1/auth/signup',
            data=self.user2,
            content_type="application/json"
        )

        self.login = self.client.post(
            '/api/v1/auth/login',
            data=self.user,
            content_type="application/json"
        )

        self.token = json.loads(self.login.data.decode())['data'][0]['token']

        self.group = json.dumps({
            "name": "devs",
            "role": "group for my devs"
        })

        self.group2 = json.dumps({
            "name": "ux-ui",
            "role": "group for my ux"
        })

        self.invalid_group_name = json.dumps({
            "name": "",
            "role": "group for my devs"
        })

        self.invalid_group_role = json.dumps({
            "name": "devs",
            "role": ""
        })
        self.g_member = json.dumps(
            {
                "user_id": 1,
                "user_role": "junior dev"
            })
        self.g_member2 = json.dumps(
            {
                "user_id": 2,
                "user_role": "senior dev"
            })
        self.group_msg = json.dumps({
            "subject": "Hello Team",
            "msgBody": "We have an urgent meeting",
            "parentId": 0
        })

    def tearDown(self):
        db_con = DB_Manager("testing")
        db_con.drop_tables()
