import unittest
from unittest import mock
from flask import request, url_for

from main import app, get_user_pfp, remove_previous_pfp

import mysql.connector

from nurse import Nurse


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

        stmt_u = "SHOW TABLES LIKE 'users'"
        self.cursor.execute(stmt_u)
        result_u = self.cursor.fetchone()
        if not result_u:
            self.cursor.execute(
                """CREATE TABLE `users` (
                    `user_id` int NOT NULL AUTO_INCREMENT,
                    `username` varchar(60) NOT NULL,
                    `password` varchar(255) NOT NULL,
                    `first_name` varchar(60) NOT NULL,
                    `last_name` varchar(60) NOT NULL,
                    `profile_img` varchar(255) DEFAULT NULL,
                    PRIMARY KEY (`user_id`))"""
            )

        stmt_p = "SHOW TABLES LIKE 'patients'"
        self.cursor.execute(stmt_p)
        result_p = self.cursor.fetchone()
        if not result_p:
            self.cursor.execute(
                """CREATE TABLE `patients` (
                    `id` int NOT NULL AUTO_INCREMENT,
                    `name` varchar(250) NOT NULL,
                    `clinical_area` varchar(100) DEFAULT NULL,
                    `bed_num` int DEFAULT NULL,
                    `acuity` int DEFAULT NULL,
                    `a_trained` tinyint(1) DEFAULT NULL,
                    `transfer` tinyint(1) DEFAULT NULL,
                    `iv` tinyint(1) DEFAULT NULL,
                    `one_to_one` tinyint(1) DEFAULT NULL,
                    `previous_nurses` varchar(250) DEFAULT NULL,
                    `admission_date` varchar(250) DEFAULT NULL,
                    `discharged_date` varchar(250) DEFAULT '-',
                    `comments` varchar(250) DEFAULT NULL,
                    `twin` int DEFAULT NULL,
                    PRIMARY KEY (`id`))"""
            )

        stmt_n = "SHOW TABLES LIKE 'nurses'"
        self.cursor.execute(stmt_n)
        result_n = self.cursor.fetchone()
        if not result_n:
            self.cursor.execute(
                """CREATE TABLE `nurses` (
                    `id` int NOT NULL AUTO_INCREMENT,
                    `name` varchar(250) DEFAULT '',
                    `clinical_area` varchar(250) DEFAULT NULL,
                    `bed_num` int DEFAULT NULL,
                    `rotation` varchar(250) DEFAULT NULL,
                    `group_num` int DEFAULT NULL,
                    `fte` decimal(3,2) DEFAULT NULL,
                    `skill_level` int DEFAULT NULL,
                    `a_trained` tinyint(1) DEFAULT NULL,
                    `transfer` tinyint(1) DEFAULT NULL,
                    `iv` int DEFAULT NULL,
                    `advanced_role` varchar(250) DEFAULT NULL,
                    `previous_patients` varchar(250) DEFAULT NULL,
                    `dta` varchar(250) DEFAULT '',
                    `comments` varchar(250) DEFAULT '',
                    `priority` int DEFAULT NULL,
                    `current_shift` tinyint(1) DEFAULT NULL,
                    PRIMARY KEY (`id`)) """
            )

        stmt_rp = "SHOW TABLES LIKE 'reference_page'"
        self.cursor.execute(stmt_rp)
        result = self.cursor.fetchone()
        if not result:
            self.cursor.execute(
                """CREATE TABLE `reference_page` (
                    `id` int NOT NULL AUTO_INCREMENT,
                    `clinical_area` varchar(1500) DEFAULT NULL,
                    `rotation` varchar(1500) DEFAULT NULL,
                    `group_def` varchar(1000) DEFAULT NULL,
                    `fte` varchar(1000) DEFAULT NULL,
                    `skill_level` varchar(1500) DEFAULT NULL,
                    `a_trained` varchar(1500) DEFAULT NULL,
                    `transfer` varchar(1500) DEFAULT NULL,
                    `iv_trained` varchar(1500) DEFAULT NULL,
                    `advanced_role` varchar(1500) DEFAULT NULL,
                    `dta` varchar(1500) DEFAULT NULL,
                    `fixed_` varchar(1000) DEFAULT NULL,
                    `flexible` varchar(1000) DEFAULT NULL,
                    PRIMARY KEY (`id`)) """
            )

        self.cursor.execute(
            """INSERT INTO users VALUES
            (1,'charge_nurse', 'Password1', 'Charge', 'Nurse', 'dog.png')"""
        )

        self.cursor.execute(
            """INSERT INTO patients VALUES
            (1,'not discharged','F',3,5,1,0,0,0,'[2,5]','2020-11-18','-','',0),
            (2,'patient discharged','F',6,3,1,0,1,1,'[]','2020-11-18','2020-11-20','',1)"""
        )

        self.cursor.execute(
            """INSERT INTO nurses VALUES
            (1,'Rebecca Smith','B',1,'A01',1,0.50,
             5,0,0,3,'None','[27]','','',2,1),
            (2,'Holly Baker','D',3,'3',1,1.00,4,1,1,2,'Charge','[1, 2, 21]','1','1',2,0)"""
        )

        self.cursor.execute(
            """INSERT INTO `reference_page` VALUES
            (1,'Section which the nurse is assigned to (e.g. A,B,C,D,E, etc.)',
            'Indicates when and which area a nurse rotates to from their usual clinical area (e.g. A01, B04, AB05, etc.)',
            'Group in which the nurse is assigned (1, 2, 3 ,4, etc.)',
            'Full Time Equivalent i.e. can be booked for full time (0 is NOT FTE, 1 is FTE)',
            'A general scale to determine nurse skill level related to being acute trained, CPAP trained, ventilator trained, advanced acute trained (on a scale from 1 to 5)',
            'Whether a nurse has specialty training (yes or no)','Whether a nurse is trained in patient transport (yes or no)',
            'Whether a nurse is trained in administrating IV drips (yes or no)',
            'Indicates the advanced roles a nurse is trained to perform. The L prior to the role name indicates a nurse is currently in training to a particular role (Charge, Support, Code)sd',
            'Duty to Accommodate i.e. restrictions on the types of patient a nurse can be assigned tosd','Group of nurses that should be maintained in their patient assignment',
            'Group of nurses to fill support roles, bumped if conflict with fixed nurse in patient assignment')"""
        )

        self.app = app.test_client()

    def tearDown(self):
        if self.connection is not None and self.connection.is_connected():
            self.cursor.execute("DROP TABLE users")
            self.cursor.execute("DROP TABLE patients")
            self.cursor.execute("DROP TABLE nurses")
            self.cursor.execute("DROP TABLE reference_page")
            self.connection.close()

    def test_connection(self):
        self.assertTrue(self.connection.is_connected())

    def test_home(self):
        self.app.post(
            '/loginUser', data={'username': 'charge_nurse', 'password': 'Password1'})
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_no_login(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/login')

    def test_update_current_nurses(self):
        self.app.post(
            '/loginUser', data={'username': 'charge_nurse', 'password': 'Password1'})
        response = self.app.post(
            '/updateCurrNurses', data={'current_nurses_list': 'some nurses', 'fixed': 1, 'flex': 2})
        self.assertEqual(response.status_code, 200)

    def test_update_adv_role(self):
        self.app.post(
            '/loginUser', data={'username': 'charge_nurse', 'password': 'Password1'})
        response = self.app.post('/updateAdvRole', data={'support_nurses_list': 'support list', 'charge_nurses_list': 'charge list',
                                                         'code_nurses_list': 'code list'})
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        self.app.post(
            '/loginUser', data={'username': 'charge_nurse', 'password': 'Password1'})
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_register_no_login(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/login')

    def test_registerUser(self):
        self.app.post(
            '/loginUser', data={'username': 'charge_nurse', 'password': 'Password1'})
        response = self.app.post(
            '/registerUser', data={'username': 'A_username', 'first_name': 'John',
                                   'last_name': 'Doe', 'password': 'Password1', 'password_conf': 'Password1'})
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_login_user(self):
        response = self.app.post(
            '/loginUser', data={'username': 'charge_nurse', 'password': 'Password1'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/')

    def test_invalid_login_user(self):
        response = self.app.post(
            '/loginUser', data={'username': 'charge_nurse', 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/login')

    def test_edit_reference(self):
        response = self.app.post('/editReference', data={'clinical_area': 'clinical_area', 'rotation': 'rotation',
                                                         'group': 'group', 'fte': 'fte', 'skill_level': 'skill_level',
                                                         'a_trained': 'a_trained', 'transfer': 'transfer', 'iv_trained': 'iv_trained',
                                                         'dta': 'dta', 'advanced_role': 'advanced_role', 'fixed': 'fixed',
                                                         'flexible': 'flexible'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/settings')

    def test_nurse_records_redirect(self):
        response = self.app.get('/nurseRecords')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/login')

    def test_nurse_records(self):
        self.app.post(
            '/loginUser', data={'username': 'charge_nurse', 'password': 'Password1'})
        response = self.app.get('/nurseRecords')
        self.assertEqual(response.status_code, 200)

    def test_add_nurse_records(self):
        response = self.app.post('/addNurseRecords', data={'create_nurse_name': 'new nurse', 'create_nurse_area': 'A',
                                                           'create_nurse_rotation': 'A05', 'create_nurse_group': 2,
                                                           'create_nurse_fte': 0.5, 'create_nurse_skill': 3,
                                                           'create_a_trained_toggle': 1, 'create_transfer_toggle': 1,
                                                           'create_iv_toggle': 1, 'L_check_2': 3, 'L_check_1': 'L',
                                                           'create_advanced_role': 'advanced', 'create_nurse_dta': 'dta',
                                                           'create_nurse_comments': 'comments'})
        self.assertEqual(response.status_code, 302)

    def test_add_nurse_records_exceptions(self):
        response = self.app.post('/addNurseRecords', data={'create_nurse_name': 'new nurse', 'create_nurse_area': 'A',
                                                           'create_nurse_rotation': 'A05', 'create_nurse_group': 2,
                                                           'create_nurse_fte': 0.5, 'create_nurse_skill': 3,
                                                           'create_advanced_role': 'advanced',
                                                           'create_nurse_dta': 'dta', 'create_nurse_comments': 'comments'})
        self.assertEqual(response.status_code, 302)

    def test_edit_nurse_records(self):
        response = self.app.post('/editNurseRecords', data={'edit_nurse_id': 1, 'edit_nurse_name': 'new name', 'edit_nurse_area': 'B',
                                                            'edit_nurse_rotation': 'B01', 'edit_nurse_group': 3, 'edit_nurse_fte': 1.0,
                                                            'edit_nurse_skill': 1, 'edit_advanced_role': 'advance',
                                                            'edit_nurse_dta': 'dta', 'edit_nurse_comments': 'some comments',
                                                            'edit_a_trained_toggle': 1, 'edit_transfer_toggle': 1, 'edit_iv_toggle': 1,
                                                            'L_check_4': 3, 'L_check_3': 'L'})
        self.assertEqual(response.status_code, 302)

    def test_edit_nurse_records_exceptions(self):
        response = self.app.post('/editNurseRecords', data={'edit_nurse_id': 1, 'edit_nurse_name': 'new name', 'edit_nurse_area': 'B',
                                                            'edit_nurse_rotation': 'B01', 'edit_nurse_group': 3, 'edit_nurse_fte': 1.0,
                                                            'edit_nurse_skill': 1, 'edit_advanced_role': 'advance',
                                                            'edit_nurse_dta': 'dta', 'edit_nurse_comments': 'some comments'})
        self.assertEqual(response.status_code, 302)

    def test_delete_nurse_records(self):
        response = self.app.post(
            '/deleteNurseRecords', data={'remove_nurse_id': 162})
        self.assertEqual(response.status_code, 302)

    def test_delete_nurse_records_failed(self):
        response = self.app.post(
            '/deleteNurseRecords', data={'remove_nurse_id': 2})
        self.assertEqual(response.status_code, 200)

    def test_patient_records(self):
        self.app.post(
            '/loginUser', data={'username': 'charge_nurse', 'password': 'Password1'})
        response = self.app.get('/patientRecords')
        self.assertEqual(response.status_code, 200)

    # def test_add_patient_records_exceptions(self):
    #     # request.referrer = 'http://localhost:5000/currentPNSheet'
    #     response = self.app.post('/addPatientRecords', data={'create_patient_name': 'new patient', 'create_patient_area': "A",
    #                                                          'create_patient_bed_number': 5, 'create_acuity_level': 3,
    #                                                          'create_patient_date_admitted': '2021-04-01', 'create_patient_comments': ''})
    #     self.assertEqual(response.status_code, 302)

    # def test_add_patient_records(self):
    #     # request.referrer = 'http://localhost:5000/currentPNSheet'
    #     response = self.app.post('/addPatientRecords', data={'create_patient_name': 'new patient', 'create_patient_area': "A",
    #                                                          'create_patient_bed_number': 5, 'create_acuity_level': 3,
    #                                                          'create_patient_date_admitted': '2021-04-01', 'create_patient_comments': '',
    #                                                          'create_a_trained_toggle': 1, 'create_transfer_toggle': 1,
    #                                                          'create_iv_toggle': 1, 'create_twin_toggle': 1, 'create_one_to_one_toggle': 1})
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.location, "STUPID")

    def test_edit_patient_records(self):
        response = self.app.post('/editPatientRecords', data={'edit_patient_id': 110, 'edit_patient_name': 'newer name',
                                                              'edit_patient_area': 'B', 'edit_patient_bed_number': 1, 'edit_acuity_level': 1,
                                                              'edit_date_admitted': '2021-03-20', 'edit_date_discharged': '2021-04-01',
                                                              'edit_comments': 'some fancy comments', 'edit_a_trained_toggle': 1,
                                                              'edit_transfer_toggle': 1, 'edit_iv_toggle': 1, 'edit_one_to_one_toggle': 1,
                                                              'edit_twin_toggle': 1})
        self.assertEqual(response.status_code, 302)

    def test_edit_patient_records_exception(self):
        response = self.app.post('/editPatientRecords', data={'edit_patient_id': 110, 'edit_patient_name': 'newer name',
                                                              'edit_patient_area': 'B', 'edit_patient_bed_number': 1, 'edit_acuity_level': 1,
                                                              'edit_date_admitted': '2021-03-20', 'edit_date_discharged': '2021-04-01',
                                                              'edit_comments': 'some fancy comments'})
        self.assertEqual(response.status_code, 302)

    def test_delete_patient_records(self):
        response = self.app.post(
            '/deletePatientRecords', data={'remove_patient_id': 110})
        self.assertEqual(response.status_code, 302)

    def test_delete_patient_records_failed(self):
        response = self.app.post(
            '/deletePatientRecords', data={'remove_patient_id': 2})
        self.assertEqual(response.status_code, 200)

    def test_patient_archives(self):
        self.app.post(
            '/loginUser', data={'username': 'charge_nurse', 'password': 'Password1'})
        response = self.app.get('/patientArchives')
        self.assertEqual(response.status_code, 200)

    # def test_add_patient_archives(self):
    #     response = self.app.post('/addPatientArchives', data={'create_patient_name': 'new patient', 'create_patient_area': 'A',
    #                                                           'create_patient_bed_number': 5, 'create_acuity_level': 3, 'create_patient_date_admitted': '2021-04-01',
    #                                                           'create_patient_comments': 'some cool comments', 'create_a_trained_toggle': 1,
    #                                                           'create_transfer_toggle': 1, 'create_iv_toggle': 1, 'create_one_to_one_toggle': 1,
    #                                                           'create_twin_toggle': 1})
    #     self.assertEqual(response.status_code, 400)

    # def test_add_patient_archives_exceptions(self):
    #     response = self.app.post('/addPatientArchives', data={'create_patient_name': 'new patient', 'create_patient_area': 'A',
    #                                                           'create_patient_bed_number': 5, 'create_acuity_level': 3, 'create_patient_date_admitted': '2021-04-01',
    #                                                           'create_patient_comments': 'some cool comments'})
    #     self.assertEqual(response.status_code, 400)

    def test_edit_patient_archives(self):
        response = self.app.post('/editPatientArchives', data={'edit_patient_id': 110, 'edit_patient_name': 'newer name',
                                                               'edit_patient_area': 'B', 'edit_patient_bed_number': 1, 'edit_acuity_level': 1,
                                                               'edit_date_admitted': '2021-03-20', 'edit_date_discharged': '2021-04-01',
                                                               'edit_comments': 'some fancy comments', 'edit_a_trained_toggle': 1,
                                                               'edit_transfer_toggle': 1, 'edit_iv_toggle': 1, 'edit_one_to_one_toggle': 1,
                                                               'edit_twin_toggle': 1})
        self.assertEqual(response.status_code, 302)

    def test_edit_patient_archives_exceptions(self):
        response = self.app.post('/editPatientArchives', data={'edit_patient_id': 110, 'edit_patient_name': 'newer name',
                                                               'edit_patient_area': 'B', 'edit_patient_bed_number': 1, 'edit_acuity_level': 1,
                                                               'edit_date_admitted': '2021-03-20', 'edit_date_discharged': '2021-04-01',
                                                               'edit_comments': 'some fancy comments'})
        self.assertEqual(response.status_code, 302)

    def test_delete_patient_archives(self):
        response = self.app.post(
            '/deletePatientArchives', data={'remove_patient_id': 117})
        self.assertEqual(response.status_code, 302)

    def test_delete_patient_archives_failed(self):
        response = self.app.post(
            '/deletePatientArchives', data={'remove_patient_id': 2})
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        self.app.post(
            '/loginUser', data={'username': 'charge_nurse', 'password': 'Password1'})
        response = self.app.get('/profile')
        self.assertEqual(response.status_code, 200)

    def test_profile_no_login(self):
        response = self.app.get('/profile')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/login')

    def test_upload_image(self):
        # self.app.request.file =
        response = self.app.post('/upload_image')
        self.assertEqual(response.status_code, 302)
        # self.assertEqual(response.location, 'http://localhost/profile')

    # def test_remove_previous_pfp(self):
    #     self.app.post(
    #         '/loginUser', data={'username': 'A_username', 'password': 'Password1'})
    #     remove_previous_pfp()

    # def test_change_password_new_ps_not_match(self):
    #     self.app.post(
    #         '/loginUser', data={'username': 'A_username', 'password': 'Password1'})
    #     response = self.app.post('/changePassword', data={'oldPassword': 'Password1', 'newPassword': 'newPassword',
    #                                                       'confirmPassword': 'Password1'})
    #     self.assertEqual(response.status_code, 302)

    # def test_change_password_old_ps_not_match(self):
    #     self.app.post(
    #         '/loginUser', data={'username': 'A_username', 'password': 'Password1'})
    #     response = self.app.post('/changePassword', data={'oldPassword': 'wrong_password', 'newPassword': 'newPassword',
    #                                                       'confirmPassword': 'newPassword'})
    #     self.assertEqual(response.status_code, 302)

    # def test_change_password(self):
    #     # self.app.post(
    #     #     '/loginUser', data={'username': 'A_username', 'password': 'Password1'})
    #     # response = self.app.post('/changePassword', data={'oldPassword': 'Password1', 'newPassword': 'newPassword',
    #     #                                                   'confirmPassword': 'newPassword'})
    #     self.app.post(
    #         '/loginUser', data={'username': 'A_username', 'password': 'newPassword'})
    #     response = self.app.post('/changePassword', data={'oldPassword': 'newPassword', 'newPassword': 'Password1',
    #                                                       'confirmPassword': 'Password1'})
    #     self.assertEqual(response.status_code, 302)

# data={'username': 'A_username', 'first_name': 'John',
#         'last_name': 'Doe', 'password': 'Password1', 'password_conf': 'Password1'}

    def test_settings(self):
        self.app.post(
            '/loginUser', data={'username': 'charge_nurse', 'password': 'Password1'})
        response = self.app.get('/settings')
        self.assertEqual(response.status_code, 200)

    def test_settings_no_login(self):
        response = self.app.get('/settings')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/login')

    def test_current_CAASheet(self):
        self.app.post(
            '/loginUser', data={'username': 'charge_nurse', 'password': 'Password1'})
        response = self.app.get('/currentCAASheet')
        self.assertEqual(response.status_code, 200)

    def test_current_CAASheet_no_login(self):
        response = self.app.get('/currentCAASheet')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/login')

    def test_future_CAASheet(self):
        response = self.app.get('/futureCAASheet')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/login')

    def test_future_CAASheet_state(self):
        response = self.app.post('/futureCAASheetState')
        self.assertEqual(response.status_code, 302)

    def test_future_save(self):
        response = self.app.post('/futureSave')
        self.assertEqual(response.status_code, 302)

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
        self.assertEqual(response.status_code, 302)

    def test_save_current_state(self):
        response = self.app.post('/saveState')
        self.assertEqual(response.status_code, 400)

    # def test_end_shift(self):
    #     response = self.app.post('/endShift')
    #     self.assertEqual(response.status_code, 404)

    def test_assign_nurse_patient(self):
        response = self.app.get('/assign')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/currentPNSheet')
