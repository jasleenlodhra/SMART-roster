import unittest
import mysql.connector

from nurse import Nurse
from patient import Patient
from assignment import main_assign, grab_patients, grab_nurses, get_patient_constraints, make_and_execute_sql_query, to_object, calculate_weights, sort_eligible_nurse_objects_acuity, assign


class TestAssignment(unittest.TestCase):
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

        stmt_p = "SHOW TABLES LIKE 'patients'"
        self.cursor.execute(stmt_p)
        result = self.cursor.fetchone()
        if not result:
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
        result = self.cursor.fetchone()
        if not result:
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

        self.assignments = {}
        self.patients = []
        self.nurses = []
        self.twins = []

        self.patient_1 = Patient(
            1, 'not discharged', 'F', 3, 5, 1, 0, 0, 0, '[2,5]', '2020-11-18', '-', '', 0)
        self.patient_1.assigned = 0

        self.patient_2 = Patient(2, 'patient discharged', 'F', 6,
                                 3, 1, 0, 1, 1, '[]', '2020-11-18', '2020-11-20', '', 1)
        self.patient_2.assigned = 1

        self.current_n = Nurse(1, 'Rebecca Smith', 'B', 1, 'A01',
                               1, 0.50, 5, 0, 0, 3, 'None', '[27]', '', '', 2, 1)

    def tearDown(self):
        if self.connection is not None and self.connection.is_connected():
            self.cursor.execute("DROP TABLE patients")
            self.cursor.execute("DROP TABLE nurses")
            self.connection.close()

    def test_grab_patient(self):
        output = grab_patients(self.patients, self.cursor, self.twins)
        self.assertEqual(output[0][0].id, self.patient_1.id)
        self.assertEqual(output[1], [])

    def test_grab_nurse(self):
        output = grab_nurses(self.nurses, self.assignments, self.cursor)
        self.assertEqual(output[0][0].id, self.current_n.id)
        self.assertEqual(
            output[1], {1: {'num_patients': 0, 'patients': [], 'prev_p': []}})

    def test_patient_constraints(self):
        output = get_patient_constraints(self.patient_1)
        self.assertEqual(output, (0, 1, 5, 0, 0, 'F', 0))

    def test_make_and_execute_sql_query(self):
        output = make_and_execute_sql_query(4, 0, 0, self.cursor)
        self.assertEqual(output[0][0], self.current_n.id)

    def test_to_object(self):
        eligible_nurses = make_and_execute_sql_query(4, 0, 0, self.cursor)
        output = to_object(eligible_nurses, self.assignments)
        self.assertEqual(output[0][0].id, 1)
        self.assertEqual(output[1], {})

    def test_calculate_weights(self):
        eligible_nurses = make_and_execute_sql_query(4, 0, 0, self.cursor)
        eligible_nurse_objects, assignments = to_object(
            eligible_nurses, self.assignments)
        output = calculate_weights(
            eligible_nurse_objects, 'F', 0, self.patient_1, assignments, self.cursor)
        self.assertEqual(output, [1])

    def test_sort_eligible_nurse_objects_acuity(self):
        eligible_nurses = make_and_execute_sql_query(4, 0, 0, self.cursor)
        eligible_nurse_objects, assignments = to_object(
            eligible_nurses, self.assignments)
        output = sort_eligible_nurse_objects_acuity(eligible_nurse_objects)
        self.assertEqual(output[0].id, 1)

    def test_assign(self):
        eligible_nurses = make_and_execute_sql_query(4, 0, 0, self.cursor)

        eligible_nurse_objects, assignments = to_object(
            eligible_nurses, self.assignments)

        sorted_eligible_nurses = sort_eligible_nurse_objects_acuity(
            eligible_nurse_objects)

        eligible_max_nurses = calculate_weights(
            eligible_nurse_objects, 'F', 0, self.patient_2, assignments, self.cursor)

        assignments = {1: {"num_patients": 2, "patients": []}}
        output = assign(sorted_eligible_nurses, eligible_max_nurses,
                        assignments, 0, self.patient_1, 0, self.twins)
        self.assertEqual(output, {1: {'num_patients': 3, 'patients': [1]}})

    def test_main_assign(self):
        output = main_assign(self.cursor)
        self.assertEqual(output, None)
