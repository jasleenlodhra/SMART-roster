import unittest
from unittest import mock
from flask import request, url_for

from main import app

import mysql.connector


class TestMain(unittest.TestCase):
    connection = None

    def setUp(self):
        config = {
            "host": "localhost",
            "user": "root",
            "passwd": "MyNewPassword",
            "database": "smartroster",
            "auth_plugin": "mysql_native_password"
        }
        self.connection = mysql.connector.connect(**config)

        self.app = app.test_client()

    def tearDown(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()

    def test_connection(self):
        self.assertTrue(self.connection.is_connected())

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)

    def test_update_current_nurses(self):
        response = self.app.get('/updateCurrNurses')
        self.assertEqual(response.status_code, 404)

    def test_update_adv_role(self):
        response = self.app.get('/updateAdvRole')
        self.assertEqual(response.status_code, 404)

    def test_register(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 302)

    def test_registerUser(self):
        response = self.app.get('/registerUser')
        self.assertEqual(response.status_code, 404)

    def test_login(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_login_user(self):
        response = self.app.get('/loginUser')
        self.assertEqual(response.status_code, 404)

    def test_logout(self):
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)

    def test_edit_reference(self):
        response = self.app.get('/editReference')
        self.assertEqual(response.status_code, 404)

    def test_nurse_records(self):
        response = self.app.get('/nurseRecords')
        self.assertEqual(response.status_code, 302)

    def test_add_nurse_records(self):
        response = self.app.get('/addNurseRecords')
        self.assertEqual(response.status_code, 404)

    def test_edit_nurse_records(self):
        response = self.app.get('/editNurseRecords')
        self.assertEqual(response.status_code, 404)

    def test_delete_nurse_records(self):
        response = self.app.get('/deleteNurseRecords')
        self.assertEqual(response.status_code, 404)

    # @mock.patch('flask_login.utils._get_user')
    # def test_patient_records(self):
    #     response = self.app.get('/patientRecords')
    #     self.assertEqual(response.status_code, 302)

    def test_add_patient_records(self):
        response = self.app.get('/addPatientRecords')
        self.assertEqual(response.status_code, 404)

    def test_edit_patient_records(self):
        response = self.app.get('/editPatientRecords')
        self.assertEqual(response.status_code, 404)

    def test_delete_patient_records(self):
        response = self.app.get('/deletePatientRecords')
        self.assertEqual(response.status_code, 404)

    # def test_patient_archives(self):
    #     response = self.app.get('/patientArchives')
    #     self.assertEqual(response.status_code, 302)

    def test_add_patient_archives(self):
        response = self.app.get('/addPatientArchives')
        self.assertEqual(response.status_code, 404)

    def test_edit_patient_archives(self):
        response = self.app.get('/editPatientArchives')
        self.assertEqual(response.status_code, 404)

    def test_delete_patient_archives(self):
        response = self.app.get('/deletePatientArchives')
        self.assertEqual(response.status_code, 404)

    def test_profile(self):
        response = self.app.get('/profile')
        self.assertEqual(response.status_code, 302)

    def test_upload_image(self):
        response = self.app.get('/upload_image')
        self.assertEqual(response.status_code, 404)

    def test_change_password(self):
        response = self.app.get('/changePassword')
        self.assertEqual(response.status_code, 404)

    def test_settings(self):
        response = self.app.get('/settings')
        self.assertEqual(response.status_code, 302)

    def test_current_CAASheet(self):
        response = self.app.get('/currentCAASheet')
        self.assertEqual(response.status_code, 302)

    def test_future_CAASheet(self):
        response = self.app.get('/futureCAASheet')
        self.assertEqual(response.status_code, 302)

    def test_future_CAASheet_state(self):
        response = self.app.get('/futureCAASheetState')
        self.assertEqual(response.status_code, 404)

    def test_future_save(self):
        response = self.app.get('/futureSave')
        self.assertEqual(response.status_code, 404)

    def test_current_PNSheet(self):
        response = self.app.get('/currentPNSheet')
        self.assertEqual(response.status_code, 302)

    def test_past_PNSheet(self):
        response = self.app.get('/pastPNSheet')
        self.assertEqual(response.status_code, 302)

    def test_past_PNSheetState(self):
        response = self.app.get('/pastPNSheetState')
        self.assertEqual(response.status_code, 404)

    def test_save_current_state(self):
        response = self.app.get('/saveState')
        self.assertEqual(response.status_code, 404)

    def test_end_shift(self):
        response = self.app.get('/endShift')
        self.assertEqual(response.status_code, 404)

    def test_assign_nurse_patient(self):
        response = self.app.get('/assign')
        self.assertEqual(response.status_code, 302)
