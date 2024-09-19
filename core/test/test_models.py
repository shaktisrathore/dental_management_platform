from django.test import TestCase
from django.utils import timezone
from core.models import Clinic, Doctor, Patient, Visit, Appointment, DoctorClinicAffiliation

class ModelTestCase(TestCase):
    def setUp(self):
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

    def test_clinic_str(self):
        self.assertEqual(str(self.clinic), 'Test Clinic')

    def test_doctor_str(self):
        self.assertEqual(str(self.doctor), 'Dr. Test')

    def test_patient_str(self):
        self.assertEqual(str(self.patient), 'Test Patient')

    def test_clinic_affiliated_doctors_count(self):
        DoctorClinicAffiliation.objects.create(
            doctor=self.doctor,
            clinic=self.clinic,
            office_address='789 Office St',
            working_schedule='Mon-Fri 9-5'
        )
        self.assertEqual(self.clinic.affiliated_doctors_count(), 1)

    def test_doctor_affiliated_clinics_count(self):
        DoctorClinicAffiliation.objects.create(
            doctor=self.doctor,
            clinic=self.clinic,
            office_address='789 Office St',
            working_schedule='Mon-Fri 9-5'
        )
        self.assertEqual(self.doctor.affiliated_clinics_count(), 1)

    def test_patient_last_visit(self):
        visit = Visit.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            clinic=self.clinic,
            date_time=timezone.now(),
            procedures='CL',
            notes='Regular checkup'
        )
        self.assertEqual(self.patient.last_visit(), visit)

    def test_patient_next_appointment(self):
        future_date = timezone.now() + timezone.timedelta(days=7)
        appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            clinic=self.clinic,
            date_time=future_date,
            procedure='CL'
        )
        self.assertEqual(self.patient.next_appointment(), appointment)