from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Clinic, Patient, Doctor
from rest_framework import status

class APIViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_api_add_clinic(self):
        response = self.client.post(reverse('api_add_clinic'), {
            'name': 'API Clinic',
            'phone_number': '1234567890',
            'city': 'API City',
            'state': 'API State',
            'address': '789 API St',
            'email': 'api@clinic.com'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Clinic.objects.filter(name='API Clinic').exists())
        clinic = Clinic.objects.get(name='API Clinic')
        self.assertEqual(clinic.phone_number, '1234567890')
        self.assertEqual(clinic.email, 'api@clinic.com')

    def test_api_add_doctor(self):
        response = self.client.post(reverse('api_add_doctor'), {
            'npi': '1234567890',
            'name': 'Dr. API',
            'email': 'dr.api@example.com',
            'phone_number': '0987654321',
            'specialties': 'CL'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Doctor.objects.filter(name='Dr. API').exists())
        doctor = Doctor.objects.get(name='Dr. API')
        self.assertEqual(doctor.npi, '1234567890')
        self.assertEqual(doctor.email, 'dr.api@example.com')

    def test_api_add_patient(self):
        response = self.client.post(reverse('api_add_patient'), {
            'name': 'API Patient',
            'date_of_birth': '2000-01-01',
            'address': '123 Patient St',
            'phone_number': '1122334455',
            'ssn_last_4': '1234',
            'gender': 'M'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Patient.objects.filter(name='API Patient').exists())
        patient = Patient.objects.get(name='API Patient')
        self.assertEqual(patient.date_of_birth.strftime('%Y-%m-%d'), '2000-01-01')
        self.assertEqual(patient.phone_number, '1122334455')

    def test_api_get_clinic_info(self):
        clinic = Clinic.objects.create(
            name='Info Clinic',
            phone_number='9876543210',
            city='Info City',
            state='Info State',
            address='321 Info St',
            email='info@clinic.com'
        )
        response = self.client.get(reverse('api_get_clinic_info', args=[clinic.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Info Clinic')
        self.assertEqual(response.data['phone_number'], '9876543210')
        self.assertEqual(response.data['email'], 'info@clinic.com')

    def test_api_add_clinic_invalid_data(self):
        response = self.client.post(reverse('api_add_clinic'), {
            'name': 'Invalid Clinic',
            # Missing required fields
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_add_doctor_invalid_data(self):
        response = self.client.post(reverse('api_add_doctor'), {
            'name': 'Dr. Invalid',
            # Missing required fields
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_add_patient_invalid_data(self):
        response = self.client.post(reverse('api_add_patient'), {
            'name': 'Invalid Patient',
            # Missing required fields
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_get_nonexistent_clinic_info(self):
        non_existent_id = 9999  # Assuming this ID doesn't exist
        response = self.client.get(reverse('api_get_clinic_info', args=[non_existent_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)