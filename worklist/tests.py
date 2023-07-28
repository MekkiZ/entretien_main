"""DON'T MODIFY THESE TESTS."""
import json
from datetime import date
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import RequestsClient
from patient.models import Patient
from worklist.models import Worklist
from worklist.serializers import WorklistSerializer

def populate_db():
    Patient.objects.create(first_name="Patient 1", last_name="Patient 1", birthdate=date(1950, 1, 1), emergency=True, wound="F")
    Patient.objects.create(first_name="Patient 2", last_name="Patient 2", birthdate=date(2000, 1, 1), emergency=True, wound="F")
    Patient.objects.create(first_name="Patient 8", last_name="Patient 8", birthdate=date(1980, 1, 1), wound="K")
    Patient.objects.create(first_name="Patient 9", last_name="Patient 9", birthdate=date(1990, 1, 1), wound="S")
    Patient.objects.create(first_name="Patient 6", last_name="Patient 6", birthdate=date(1960, 1, 1), wound="K")
    Patient.objects.create(first_name="Patient 3", last_name="Patient 3", birthdate=date(2010, 1, 1), emergency=True, wound="F")
    Patient.objects.create(first_name="Patient 7", last_name="Patient 7", birthdate=date(1970, 1, 1), wound="H")
    Patient.objects.create(first_name="Patient 4", last_name="Patient 4", birthdate=date(1910, 1, 1), wound="H")
    Patient.objects.create(first_name="Patient 0", last_name="Patient 0", birthdate=date(1930, 1, 1), emergency=True, wound="F")
    Patient.objects.create(first_name="Patient 5", last_name="Patient 5", birthdate=date(1935, 1, 1), wound="S")
    Patient.objects.create(first_name="Patient 10", last_name="Patient 10", birthdate=date(2010, 1, 1), wound="A")

class WorklistTestCase(TestCase):
    def setUp(self):
        populate_db()
    
    def test_worklist_list(self):
        """Patients should be sort by emergency then birthdate"""
        worklist=Worklist()
        patients = worklist.get_patients()
        self.assertEqual(patients.count(), Worklist.MAX_USERS)
        for i in range(Worklist.MAX_USERS):
            self.assertEqual(patients[i], Patient.objects.get(first_name=f"Patient {i}"))

    def test_serializers(self):
        wklst = Worklist()
        patients = wklst.get_patients()
        srlzr = WorklistSerializer(wklst)
        for i in range(Worklist.MAX_USERS):
            self.assertEqual(srlzr.data["patients"][i]["first_name"], patients[i].first_name)
            self.assertEqual(srlzr.data["patients"][i]["last_name"], patients[i].last_name)
            self.assertEqual(srlzr.data["patients"][i]["birthdate"], patients[i].birthdate_formatted)
            self.assertFalse("secret_id" in srlzr.data["patients"][i])

    def test_wound_stats(self):
        wklst = Worklist()
        wound_stats = WorklistSerializer(wklst).data["wound_stats"]
        self.assertEqual(wound_stats["F"], 4)
        self.assertEqual(wound_stats["K"], 2)
        self.assertEqual(wound_stats["S"], 2)
        self.assertEqual(wound_stats["H"], 2)


class WorklistAPITestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = RequestsClient()
        populate_db()
        Worklist.objects.create()

    def test_api_list(self):
        """Get method should return serialized worklist."""
        response = self.client.get('http://localhost:8000/api/worklist/')
        self.assertEqual(len(json.loads(response.content)[0]['patients']), 10)