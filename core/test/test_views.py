from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Clinic, Doctor, Patient, Visit, Appointment, DoctorClinicAffiliation

class CoreViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        
        self.clinic = Clinic.objects.create(
            name='Test Clinic',
            phone_number='1234567890',
            city='Test City',
            state='Test State',
            address='123 Test St',
            email='test@clinic.com'
        )
        self.doctor = Doctor.objects.create(
            npi='1234567890',
            name='Dr. Test',
            email='doctor@test.com',
            phone_number='0987654321',
            specialties='CL'
        )
        self.patient = Patient.objects.create(
            name='Test Patient',
            date_of_birth='1990-01-01',
            address='456 Patient St',
            phone_number='1122334455',
            ssn_last_4='1234',
            gender='M'
        )

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/dashboard.html')

    def test_clinic_list_view(self):
        response = self.client.get(reverse('clinic_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/clinic/clinic_list.html')
        self.assertContains(response, 'Test Clinic')

    def test_clinic_detail_view(self):
        response = self.client.get(reverse('clinic_detail', args=[self.clinic.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/clinic/clinic_detail.html')
        self.assertContains(response, 'Test Clinic')

    def test_doctor_list_view(self):
        response = self.client.get(reverse('doctor_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/doctor/doctor_list.html')
        self.assertContains(response, 'Dr. Test')

    def test_doctor_detail_view(self):
        response = self.client.get(reverse('doctor_detail', args=[self.doctor.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/doctor/doctor_detail.html')
        self.assertContains(response, 'Dr. Test')

    def test_patient_list_view(self):
        response = self.client.get(reverse('patient_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/patient/patient_list.html')
        self.assertContains(response, 'Test Patient')

    def test_patient_detail_view(self):
        response = self.client.get(reverse('patient_detail', args=[self.patient.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/patient/patient_detail.html')
        self.assertContains(response, 'Test Patient')

    def test_add_visit(self):
        response = self.client.post(reverse('add_visit', args=[self.patient.pk]), {
            'doctor': self.doctor.pk,
            'clinic': self.clinic.pk,
            'date_time': '2023-05-01 14:30:00',
            'procedures': 'CL',
            'notes': 'Regular checkup'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful submission
        self.assertTrue(Visit.objects.filter(patient=self.patient).exists())

    def test_schedule_appointment(self):
        response = self.client.post(reverse('schedule_appointment', args=[self.patient.pk]), {
            'doctor': self.doctor.pk,
            'clinic': self.clinic.pk,
            'date_time': '2023-05-15 14:30:00',
            'procedure': 'CL'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful submission
        self.assertTrue(Appointment.objects.filter(patient=self.patient).exists())

    def test_add_doctor_clinic_affiliation(self):
        response = self.client.post(reverse('add_doctor_clinic_affiliation', args=[self.doctor.pk]), {
            'clinic': self.clinic.pk,
            'office_address': '789 Office St',
            'working_schedule': 'Mon-Fri 9-5'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful submission
        self.assertTrue(DoctorClinicAffiliation.objects.filter(doctor=self.doctor, clinic=self.clinic).exists())

    def test_delete_patient(self):
        response = self.client.post(reverse('delete_patient', args=[self.patient.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Patient.objects.filter(pk=self.patient.pk).exists())