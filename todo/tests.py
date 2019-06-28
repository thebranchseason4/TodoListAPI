# Create your tests here.
from rest_framework.test import APITestCase

class PracticesTests(APITestCase):
    def passTravisTest(self):
        self.assertEqual(1,1)

    def failedTravisTest(self):
        self.assertEqual(1,2)
