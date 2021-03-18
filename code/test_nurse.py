from unittest import TestCase
import inspect
from nurse import Nurse


class TestNurse(TestCase):
    """ Unit tests for the Nurse class """

    def setUp(self):
        """ creates a test fixture before each test method has run """
        self.nurse = Nurse(12, "Jane", "A", 7, "a", 5, 1.1,
                           0, True, True, False, "charge", "previous", "dta", "comment", True, True)

        self.long_str = ""
        for i in range(260):
            self.long_str += "a"

    def test_getters(self):
        self.assertEqual(self.nurse.get_id(), 12)
        self.assertEqual(self.nurse.get_name(), "Jane")
        self.assertEqual(self.nurse.get_clinical_area(), "A")
        self.assertEqual(self.nurse.get_bed_num(), 7)
        self.assertEqual(self.nurse.get_rotation(), "a")
        self.assertEqual(self.nurse.get_group(), 5)
        self.assertEqual(self.nurse.get_fte(), 1.1)
        self.assertEqual(self.nurse.get_skill_level(), 0)
        self.assertEqual(self.nurse.get_a_trained(), True)
        self.assertEqual(self.nurse.get_transfer(), True)
        self.assertEqual(self.nurse.get_picc(), False)
        self.assertEqual(self.nurse.get_advanced_role(), "charge")
        self.assertEqual(self.nurse.get_previous_patients(), "previous")
        self.assertEqual(self.nurse.get_dta(), "dta")
        self.assertEqual(self.nurse.get_comment(), "comment")
        self.assertEqual(self.nurse.get_priority(), True)
        self.assertEqual(self.nurse.get_current_shift(), True)
        self.nurse.set_assigned(True)
        self.assertEqual(self.nurse.get_assigned(), True)

    def test_invalid_id(self):
        """id"""
        with self.assertRaises(ValueError):
            Nurse("12", "Jane", "A", 7, "a", 5, 1.1,
                  0, True, True, False, "charge", "previous", "dta", "comment", True, True)
        with self.assertRaises(ValueError):
            Nurse(-2, "Jane", "A", 7, "a", 5, 1.1,
                  0, True, True, False, "charge", "previous", "dta", "comment", True, True)
        with self.assertRaises(ValueError):
            Nurse(None, "Jane", "A", 7, "a", 5, 1.1,
                  0, True, True, False, "charge", "previous", "dta", "comment", True, True)

    def test_invalid_bed_num(self):
        """bed_num"""
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", "7", "a", 5, 1.1,
                  0, True, True, False, "charge", "previous", "dta", "comment", True, True)
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", None, "a", 5, 1.1,
                  0, True, True, False, "charge", "previous", "dta", "comment", True, True)
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", -1, "a", 5, 1.1,
                  0, True, True, False, "charge", "previous", "dta", "comment", True, True)
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 15, "a", 5, 1.1,
                  0, True, True, False, "charge", "previous", "dta", "comment", True, True)

    def test_invalid_group(self):
        """group"""
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", "5", 1.1,
                  0, True, True, False, "charge", "previous", "dta", "comment", True, True)
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", None, 1.1,
                  0, True, True, False, "charge", "previous", "dta", "comment", True, True)
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", -1, 1.1,
                  0, True, True, False, "charge", "previous", "dta", "comment", True, True)

    def test_invalid_skill_level(self):
        """skill_level"""
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", 5, 1.1,
                  "0", True, True, False, "charge", "previous", "dta", "comment", True, True)
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", 5, 1.1,
                  None, True, True, False, "charge", "previous", "dta", "comment", True, True)
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", 5, 1.1,
                  -1, True, True, False, "charge", "previous", "dta", "comment", True, True)
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", 5, 1.1,
                  6, True, True, False, "charge", "previous", "dta", "comment", True, True)

    def test_invalid_name(self):
        """name"""
        with self.assertRaises(ValueError):
            Nurse(12, 12, "A", 7, "a", 5, 1.1,
                  0, True, True, False, "charge", "previous", "dta", "comment", True, True)
        with self.assertRaises(ValueError):
            Nurse(12, self.long_str, "A", 7, "a", 5, 1.1,
                  0, True, True, False, "charge", "previous", "dta", "comment", True, True)
        with self.assertRaises(ValueError):
            Nurse(12, None, "A", 7, "a", 5, 1.1,
                  0, True, True, False, "charge", "previous", "dta", "comment", True, True)

    def test_invalid_clinical_area(self):
        """clinical_area"""
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", 1, 7, "a", 5, 1.1,
                  0, True, True, False, "charge", "previous", "dta", "comment", True, True)
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "AB", 7, "a", 5, 1.1,
                  0, True, True, False, "charge", "previous", "dta", "comment", True, True)
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", None, 7, "a", 5, 1.1,
                  0, True, True, False, "charge", "previous", "dta", "comment", True, True)

    def test_invalid_rotation(self):
        """rotation"""
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, 1, 5, 1.1,
                  0, True, True, False, "charge", "previous", "dta", "comment", True, True)
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, self.long_str, 5, 1.1,
                  0, True, True, False, "charge", "previous", "dta", "comment", True, True)
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, None, 5, 1.1,
                  0, True, True, False, "charge", "previous", "dta", "comment", True, True)

    def test_invalid_advanced_role(self):
        """advanced_role"""
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", 5, 1.1,
                  0, True, True, False, 1, "previous", "dta", "comment", True, True)
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", 5, 1.1,
                  0, True, True, False, self.long_str, "previous", "dta", "comment", True, True)
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", 5, 1.1,
                  0, True, True, False, None, "previous", "dta", "comment", True, True)

    def test_invalid_previous_patients(self):
        """previous_patients"""
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", 5, 1.1,
                  0, True, True, False, "charge", 1, "dta", "comment", True, True)
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", 5, 1.1,
                  0, True, True, False, "charge", None, "dta", "comment", True, True)
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", 5, 1.1,
                  0, True, True, False, "charge", self.long_str, "dta", "comment", True, True)

    def test_invalid_dta(self):
        """dta"""
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", 5, 1.1,
                  0, True, True, False, "charge", "previous", 1, "comment", True, True)
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", 5, 1.1,
                  0, True, True, False, "charge", "previous", self.long_str, "comment", True, True)
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", 5, 1.1,
                  0, True, True, False, "charge", "previous", None, "comment", True, True)

    def test_invalid_comments(self):
        """comments"""
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", 5, 1.1,
                  0, True, True, False, "charge", "previous", "dta", 1, True, True)
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", 5, 1.1,
                  0, True, True, False, "charge", "previous", "dta", None, True, True)
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", 5, 1.1,
                  0, True, True, False, "charge", "previous", "dta", self.long_str, True, True)

    def test_invalid_fte(self):
        """fte"""
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", 5, None,
                  0, True, True, False, "charge", "previous", "dta", "comment", True, True)
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", 5, -1,
                  0, True, True, False, "charge", "previous", "dta", "comment", True, True)

    def test_invalid_a_trained(self):
        """a_trained"""
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", 5, 1.1,
                  0, None, True, False, "charge", "previous", "dta", "comment", True, True)

    def test_invalid_transfer(self):
        """transfer"""
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", 5, 1.1,
                  0, True, None, False, "charge", "previous", "dta", "comment", True, True)

    def test_invalid_picc(self):
        """picc"""
        with self.assertRaises(ValueError):
            Nurse(12, "Jane", "A", 7, "a", 5, 1.1,
                  0, True, True, None, "charge", "previous", "dta", "comment", True, True)

    def test_to_dict(self):
        """to_dict"""
        self.nurse.assigned = True
        self.assertEqual(self.nurse.to_dict(), {"id": 12, "name": "Jane", "clinical_area": "A", "bed_num": 7, "rotation": "a", "fte": 1.1,
                                                "group": 5, "skill_level": 0, "a_trained": True, "transfer": True, "picc": False, "advanced_role": "charge", "previous_patients": "previous",
                                                "dta": "dta", "comments": "comment", "priority": True, "current shift": True, "assigned": True})
