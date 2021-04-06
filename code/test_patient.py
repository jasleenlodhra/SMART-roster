from unittest import TestCase
import inspect
from patient import Patient


class TestPatient(TestCase):
    """ Unit tests for the Patient class """

    def setUp(self):
        """ creates a test fixture before each test method has run """
        self.patient = Patient(1, "John Doe", "A", 1, 3, False, False,
                               True, True, "Jane", "2021-03-18", "2021-03-20", "comment", "twin")

        self.long_str = ""
        for i in range(260):
            self.long_str += "a"

    def test_getters(self):
        """ test getters """
        self.assertEqual(self.patient.get_id(), 1)
        self.assertEqual(self.patient.get_name(), "John Doe")
        self.assertEqual(self.patient.get_last_name(), "Doe")
        self.assertEqual(self.patient.get_clinical_area(), "A")
        self.assertEqual(self.patient.get_bed_num(), 1)
        self.assertEqual(self.patient.get_acuity(), 3)
        self.assertEqual(self.patient.get_transfer(), False)
        self.assertEqual(self.patient.get_a_trained(), False)
        self.assertEqual(self.patient.get_one_to_one(), True)
        self.assertEqual(self.patient.get_picc(), True)
        self.assertEqual(self.patient.get_previous_nurses(), "Jane")
        self.patient.set_previous_nurses("Amy")
        self.assertEqual(self.patient.get_previous_nurses(), "Amy")
        self.assertEqual(self.patient.get_admission_date(), "2021-03-18")
        self.assertEqual(self.patient.get_discharge_date(), "2021-03-20")
        self.assertEqual(self.patient.get_comment(), "comment")
        self.assertEqual(self.patient.get_twin(), "twin")
        self.patient.set_assigned(True)
        self.assertEqual(self.patient.get_assigned(), True)

    def test_invalid_id(self):
        """id"""
        with self.assertRaises(ValueError):
            Patient("1", "John Doe", "A", 1, 3, False, False,
                    True, True, "Jane", "2021-03-18", "2021-03-20", "comment", "twin")
        with self.assertRaises(ValueError):
            Patient(-1, "John Doe", "A", 1, 3, False, False,
                    True, True, "Jane", "2021-03-18", "2021-03-20", "comment", "twin")
        with self.assertRaises(ValueError):
            Patient(None, "John Doe", "A", 1, 3, False, False,
                    True, True, "Jane", "2021-03-18", "2021-03-20", "comment", "twin")

    def test_invalid_name(self):
        with self.assertRaises(ValueError):
            Patient(1, 1, "A", 1, 3, False, False,
                    True, True, "Jane", "2021-03-18", "2021-03-20", "comment", "twin")
        with self.assertRaises(ValueError):
            Patient(1, "", "A", 1, 3, False, False,
                    True, True, "Jane", "2021-03-18", "2021-03-20", "comment", "twin")
        with self.assertRaises(ValueError):
            Patient(1, self.long_str, "A", 1, 3, False, False,
                    True, True, "Jane", "2021-03-18", "2021-03-20", "comment", "twin")

    def test_to_dict(self):
        """to_dict"""
        self.patient.assigned = True
        self.assertEqual(self.patient.to_dict(), {"id": 1, "first_name": "John", "last_name": "Doe", "clinical_area": "A",
                                                  "bed_num": 1, "acuity": 3, "a_trained": False, "transfer": False,
                                                  "picc": True, "one_to_one": True, "previous_nurses": "Jane",
                                                  "admission_date": "2021-03-18", "discharge_date": "2021-03-20",
                                                  "comments": "comment", "twin": "twin"})
