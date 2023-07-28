"""DON'T MODIFY THESE TESTS."""
from datetime import date
from django.test import TestCase
from patient.models import Patient


class PatientTestCase(TestCase):
    def setUp(self):
        self.jean_mi = Patient.objects.create(first_name="jean michel", last_name="cobaye",
                                              birthdate=date(1950, 12, 27))
        self.jean_mi_jr = Patient.objects.create(first_name="jean michel jr", last_name="cobaye",
                                                 birthdate=date(2010, 12, 11))

    def test_fullname(self):
        """Test fullname."""
        self.assertEqual(self.jean_mi.fullname, "Jean Michel COBAYE")

    def test_age(self):
        """Test age behaviour."""
        self.assertEqual(self.jean_mi.age, 72)
        self.assertEqual(self.jean_mi_jr.age, 12)

    def test_age_at_date(self):
        """Test age behaviour."""
        self.assertEqual(self.jean_mi.age_at_date(date(2030, 1, 1)), 79)
        self.assertEqual(self.jean_mi_jr.age_at_date(date(2012, 1, 1)), 1)
        self.assertEqual(self.jean_mi_jr.age_at_date(date(2009, 1, 1)), "unborn")

    def test_majority(self):
        """Test majority."""
        self.assertTrue(self.jean_mi.has_majority)
        self.assertFalse(self.jean_mi_jr.has_majority)

    def test_birthdate_format(self):
        """Test birthdate format."""
        self.assertEqual(self.jean_mi.birthdate_formatted, "27/12 1950")
        self.assertEqual(self.jean_mi_jr.birthdate_formatted, "11/12 2010")

    def test_patient_is_wounded(self):
        """Patient should be wounded when has a wound."""
        self.jean_mi.wound = 'S'
        self.jean_mi.save()
        self.assertTrue(self.jean_mi.is_wounded())

    def test_patient_broke_his_leg(self):
        """Patient broke one of his legs."""
        self.assertFalse(self.jean_mi.is_wounded())
        self.assertFalse(self.jean_mi.emergency)
        self.assertTrue(self.jean_mi.can_walk())
        self.jean_mi.break_his_leg()
        self.assertTrue(self.jean_mi.is_wounded())
        self.assertTrue(self.jean_mi.emergency)
        self.assertFalse(self.jean_mi.can_walk())

    '''def test_age_order_patient(self):
        """Patient should be in correct order."""
        Patient.objects.all().delete()
        Patient.objects.create(first_name="Patient 0", last_name="Patient 0", birthdate=date(1950, 1, 1))
        Patient.objects.create(first_name="Patient 5", last_name="Patient 5", birthdate=date(2000, 1, 1))
        Patient.objects.create(first_name="Patient 3", last_name="Patient 3", birthdate=date(1980, 1, 1))
        Patient.objects.create(first_name="Patient 4", last_name="Patient 4", birthdate=date(1990, 1, 1))
        Patient.objects.create(first_name="Patient 1", last_name="Patient 1", birthdate=date(1960, 1, 1))
        Patient.objects.create(first_name="Patient 6", last_name="Patient 6", birthdate=date(2010, 1, 1))
        Patient.objects.create(first_name="Patient 2", last_name="Patient 2", birthdate=date(1970, 1, 1))
        self.assertEqual(Patient.objects.last(), Patient.objects.get(first_name="Patient 6"))
        self.assertEqual(Patient.objects.first(), Patient.objects.get(first_name="Patient 0"))
        self.assertEqual(Patient.objects.all()[3], Patient.objects.get(first_name="Patient 3"))'''
