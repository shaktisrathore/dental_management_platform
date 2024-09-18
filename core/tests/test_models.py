from django.test import TestCase
from django.utils import timezone
from ..models import Clinic, Doctor, DoctorClinicAffiliation, Patient, Visit, Appointment
from datetime import timedelta

class ClinicModelTests(TestCase):
    
    def setUp(self):
        self.clinic = Clinic.objects.create(
            name="Bright Smile Dental",
            phone_number="1234567890",
            city="New York",
            state="NY",
            address="123 Main St",
            email="contact@brightsmile.com"
        )
        self.doctor = Doctor.objects.create(
            npi="1234567890",
            name="Dr. John Doe",
            email="dr.john@example.com",
            phone_number="0987654321",
            specialties="CL"
        )
        DoctorClinicAffiliation.objects.create(
            doctor=self.doctor,
            clinic=self.clinic,
            office_address="Office 101",
            working_schedule="Mon-Fri 9AM-5PM"
        )
        self.patient = Patient.objects.create(
            name="Jane Doe",
            date_of_birth="1990-01-01",
            address="456 Maple St",
            phone_number="5551234567",
            ssn_last_4="1234",
            gender="F"
        )
        self.patient.doctors.add(self.doctor)
    
    def test_clinic_str(self):
        self.assertEqual(str(self.clinic), "Bright Smile Dental")

    def test_affiliated_doctors_count(self):
        self.assertEqual(self.clinic.affiliated_doctors_count(), 1)

    # def test_affiliated_patients_count(self):
    #     # Create an appointment for the patient at this clinic
    #     Appointment.objects.create(
    #         patient=self.patient,
    #         doctor=self.doctor,
    #         clinic=self.clinic,
    #         date_time=timezone.now() + timedelta(days=1),
    #         procedure="CL"
    #     )
    #     self.assertEqual(self.clinic.affiliated_patients_count(), 1)


class DoctorModelTests(TestCase):

    def setUp(self):
        self.clinic = Clinic.objects.create(
            name="Bright Smile Dental",
            phone_number="1234567890",
            city="New York",
            state="NY",
            address="123 Main St",
            email="contact@brightsmile.com"
        )
        self.doctor = Doctor.objects.create(
            npi="1234567890",
            name="Dr. John Doe",
            email="dr.john@example.com",
            phone_number="0987654321",
            specialties="CL"
        )
        self.patient = Patient.objects.create(
            name="Jane Doe",
            date_of_birth="1990-01-01",
            address="456 Maple St",
            phone_number="5551234567",
            ssn_last_4="1234",
            gender="F"
        )
        self.patient.doctors.add(self.doctor)
        DoctorClinicAffiliation.objects.create(
            doctor=self.doctor,
            clinic=self.clinic,
            office_address="Office 101",
            working_schedule="Mon-Fri 9AM-5PM"
        )
    
    def test_doctor_str(self):
        self.assertEqual(str(self.doctor), "Dr. John Doe")

    def test_affiliated_clinics_count(self):
        self.assertEqual(self.doctor.affiliated_clinics_count(), 1)

    # def test_affiliated_patients_count(self):
    #     self.assertEqual(self.doctor.affiliated_patients_count(), 1)


class PatientModelTests(TestCase):

    def setUp(self):
        self.clinic = Clinic.objects.create(
            name="Bright Smile Dental",
            phone_number="1234567890",
            city="New York",
            state="NY",
            address="123 Main St",
            email="contact@brightsmile.com"
        )
        self.doctor = Doctor.objects.create(
            npi="1234567890",
            name="Dr. John Doe",
            email="dr.john@example.com",
            phone_number="0987654321",
            specialties="CL"
        )
        self.patient = Patient.objects.create(
            name="Jane Doe",
            date_of_birth="1990-01-01",
            address="456 Maple St",
            phone_number="5551234567",
            ssn_last_4="1234",
            gender="F"
        )
        self.patient.doctors.add(self.doctor)
        self.visit = Visit.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            clinic=self.clinic,
            date_time=timezone.now() - timedelta(days=1),
            procedures="CL"
        )
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            clinic=self.clinic,
            date_time=timezone.now() + timedelta(days=1),
            procedure="CL"
        )

    def test_patient_str(self):
        self.assertEqual(str(self.patient), "Jane Doe")

    def test_last_visit(self):
        self.assertEqual(self.patient.last_visit(), self.visit)

    def test_next_appointment(self):
        self.assertEqual(self.patient.next_appointment(), self.appointment)