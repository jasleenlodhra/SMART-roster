import unittest
from unittest import mock
from flask import request, url_for

from main import app, get_user_pfp, remove_previous_pfp

import mysql.connector


class TestMain(unittest.TestCase):
    connection = None

    def setUp(self):
        config = {
            "host": "localhost",
            "user": "root",
            "passwd": "MyNewPassword",
            "database": "test",
            "auth_plugin": "mysql_native_password"
        }
        self.connection = mysql.connector.connect(**config)

        self.cursor = self.connection.cursor()

        stmt = "SHOW TABLES LIKE 'users'"
        self.cursor.execute(stmt)
        result = self.cursor.fetchone()
        print("RESULT", result)
        if not result:
            self.cursor.execute(
                """CREATE TABLE `users` (
                    `user_id` int NOT NULL AUTO_INCREMENT,
                    `username` varchar(60) NOT NULL,
                    `password` varchar(255) NOT NULL,
                    `first_name` varchar(60) NOT NULL,
                    `last_name` varchar(60) NOT NULL,
                    `profile_img` varchar(255) DEFAULT NULL,
                    PRIMARY KEY (`user_id`)
                )""")

        self.app = app.test_client()

    def tearDown(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()

    def test_connection(self):
        self.assertTrue(self.connection.is_connected())

    # def test_get_user_pfp(self):
    #     # response = self.app.get('/')
    #     # output = get_user_pfp()
    #     # assert output == None
    #     with self.app:
    #         with self.app.session_transaction() as sess:
    #             sess['id'] = 'charge_nurse'
    #             response = self.app.get('loginUser')
    #             self.assertEqual(response.location, 'http://localhost/')

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/login')

    # def test_update_current_nurses(self):
    #     response = self.app.post('/updateCurrNurses')
    #     self.assertEqual(response.status_code, 405)

    # def test_update_adv_role(self):
    #     response = self.app.post('/updateAdvRole')
    #     self.assertEqual(response.status_code, 404)

    def test_register(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/login')

    def test_registerUser(self):
        response = self.app.post(
            '/registerUser', data={'username': 'A_username', 'first_name': 'John',
                                   'last_name': 'Doe', 'password': 'Password1', 'password_conf': 'Password1'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/')

    def test_login(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_login_user(self):
        response = self.app.post('/loginUser')
        self.assertEqual(response.status_code, 404)

    def test_logout(self):
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/login')

    def test_edit_reference(self):
        response = self.app.get('/editReference')
        self.assertEqual(response.status_code, 404)
        # self.assertEqual(response.location, 'http://localhost/login')

    def test_nurse_records(self):
        response = self.app.get('/nurseRecords')
        self.assertEqual(response.status_code, 302)

    def test_add_nurse_records(self):
        response = self.app.post('/addNurseRecords')
        self.assertEqual(response.status_code, 404)

    def test_edit_nurse_records(self):
        response = self.app.post('/editNurseRecords')
        self.assertEqual(response.status_code, 404)

    def test_delete_nurse_records(self):
        response = self.app.post('/deleteNurseRecords')
        self.assertEqual(response.status_code, 404)

    # @mock.patch('flask_login.utils._get_user')
    # def test_patient_records(self):
    #     response = self.app.get('/patientRecords')
    #     self.assertEqual(response.status_code, 302)

    def test_add_patient_records(self):
        response = self.app.post('/addPatientRecords')
        self.assertEqual(response.status_code, 404)

    def test_edit_patient_records(self):
        response = self.app.post('/editPatientRecords')
        self.assertEqual(response.status_code, 404)

    def test_delete_patient_records(self):
        response = self.app.post('/deletePatientRecords')
        self.assertEqual(response.status_code, 404)

    # def test_patient_archives(self):
    #     response = self.app.get('/patientArchives')
    #     self.assertEqual(response.status_code, 302)

    def test_add_patient_archives(self):
        response = self.app.post('/addPatientArchives')
        self.assertEqual(response.status_code, 404)

    def test_edit_patient_archives(self):
        response = self.app.post('/editPatientArchives')
        self.assertEqual(response.status_code, 404)

    def test_delete_patient_archives(self):
        response = self.app.post('/deletePatientArchives')
        self.assertEqual(response.status_code, 404)

    def test_profile(self):
        response = self.app.get('/profile')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/login')

    def test_upload_image(self):
        response = self.app.post('/upload_image')
        self.assertEqual(response.status_code, 404)
        # self.assertEqual(response.location, 'http://localhost/profile')

    def test_change_password(self):
        response = self.app.post('/changePassword')
        self.assertEqual(response.status_code, 404)

    def test_settings(self):
        response = self.app.get('/settings')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/login')

    def test_current_CAASheet(self):
        response = self.app.get('/currentCAASheet')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/login')

    def test_future_CAASheet(self):
        response = self.app.get('/futureCAASheet')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/login')

    def test_future_CAASheet_state(self):
        response = self.app.post('/futureCAASheetState')
        self.assertEqual(response.status_code, 404)

    def test_future_save(self):
        response = self.app.post('/futureSave')
        self.assertEqual(response.status_code, 404)

    def test_current_PNSheet(self):
        response = self.app.get('/currentPNSheet')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/login')

    def test_past_PNSheet(self):
        response = self.app.get('/pastPNSheet')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/login')

    def test_past_PNSheetState(self):
        response = self.app.post('/pastPNSheetState')
        self.assertEqual(response.status_code, 404)

    def test_save_current_state(self):
        response = self.app.post('/saveState')
        self.assertEqual(response.status_code, 404)

    def test_end_shift(self):
        response = self.app.post('/endShift')
        self.assertEqual(response.status_code, 404)

    def test_assign_nurse_patient(self):
        response = self.app.get('/assign')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/currentPNSheet')
