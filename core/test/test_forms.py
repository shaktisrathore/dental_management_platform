from django.test import TestCase
from core.forms import ClinicForm, DoctorForm, PatientForm, VisitForm, AppointmentForm, DoctorClinicAffiliationForm, RegistrationForm
from core.models import Clinic, Doctor

class FormTestCase(TestCase):
    def setUp(self):
        # Create a clinic and a doctor for the tests
        self.clinic = Clinic.objects.create(
            name="Test Clinic",
            phone_number="1234567890",
            city="Test City",
            state="Test State",
            address="123 Test St",
            email="test@clinic.com"
        )
        self.doctor = Doctor.objects.create(
            npi="1234567890",
            name="Dr. Test",
            email="test@doctor.com",
            phone_number="0987654321",
            specialties="CL"
        )

    def test_clinic_form_valid(self):
        form_data = {
            'name': 'New Clinic',
            'phone_number': '1234567890',
            'city': 'New City',
            'state': 'New State',
            'address': '456 New St',
            'email': 'new@clinic.com'
        }
        form = ClinicForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_doctor_form_valid(self):
        form_data = {
            'npi': '0987654321',
            'name': 'Dr. New',
            'email': 'new@doctor.com',
            'phone_number': '9876543210',
            'specialties': 'FL'
        }
        form = DoctorForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_patient_form_valid(self):
        form_data = {
            'name': 'New Patient',
            'date_of_birth': '1995-05-05',
            'address': '789 Patient St',
            'phone_number': '5556667777',
            'ssn_last_4': '5678',
            'gender': 'F'
        }
        form = PatientForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_visit_form_valid(self):
        form_data = {
            'doctor': self.doctor.id,
            'clinic': self.clinic.id,
            'date_time': '2023-05-01 14:30:00',
            'procedures': 'CL',
            'notes': 'Regular checkup'
        }
        form = VisitForm(data=form_data)
        if not form.is_valid():
            print("Visit form errors:", form.errors)
        self.assertTrue(form.is_valid())

    def test_appointment_form_valid(self):
        form_data = {
            'doctor': self.doctor.id,
            'clinic': self.clinic.id,
            'date_time': '2023-05-15 14:30:00',
            'procedure': 'CL'
        }
        form = AppointmentForm(data=form_data)
        if not form.is_valid():
            print("Appointment form errors:", form.errors)
        self.assertTrue(form.is_valid())

    def test_doctor_clinic_affiliation_form_valid(self):
        form_data = {
            'clinic': self.clinic.id,
            'office_address': '789 Office St',
            'working_schedule': 'Mon-Fri 9-5'
        }
        form = DoctorClinicAffiliationForm(data=form_data)
        if not form.is_valid():
            print("DoctorClinicAffiliation form errors:", form.errors)
        self.assertTrue(form.is_valid())

    def test_registration_form_valid(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())