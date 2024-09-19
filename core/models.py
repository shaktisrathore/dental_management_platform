from django.db import models
from django.utils import timezone

class Clinic(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    address = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return self.name

    def affiliated_doctors_count(self):
        return self.doctorclinicaffiliation_set.count()

    def affiliated_patients_count(self):
        return Patient.objects.filter(appointments__clinic=self).distinct().count()

class Doctor(models.Model):
    SPECIALTIES = [
        ('CL', 'Cleaning'),
        ('FL', 'Filling'),
        ('RC', 'Root Canal'),
        ('CR', 'Crown'),
        ('TW', 'Teeth Whitening'),
    ]

    npi = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    specialties = models.CharField(max_length=2, choices=SPECIALTIES)
    clinics = models.ManyToManyField(Clinic, through='DoctorClinicAffiliation')

    def __str__(self):
        return self.name

    def affiliated_clinics_count(self):
        return self.clinics.count()

    def affiliated_patients_count(self):
        return Patient.objects.filter(appointments__doctor=self).distinct().count()

class DoctorClinicAffiliation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    office_address = models.TextField()
    working_schedule = models.TextField()

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    ssn_last_4 = models.CharField(max_length=4)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    doctors = models.ManyToManyField(Doctor, related_name='patients')

    def __str__(self):
        return self.name

    def last_visit(self):
        return self.visits.order_by('-date_time').first()

    def next_appointment(self):
        return self.appointments.filter(date_time__gt=timezone.now()).order_by('date_time').first()

    def last_visit_date(self):
        last_visit = self.last_visit()
        return last_visit.date_time.strftime('%Y-%m-%d') if last_visit else 'N/A'

    def next_appointment_date(self):
        next_appointment = self.next_appointment()
        return next_appointment.date_time.strftime('%Y-%m-%d') if next_appointment else 'N/A'

    def last_visit_datetime(self):
        last_visit = self.last_visit()
        return last_visit.date_time.strftime('%Y-%m-%d %H:%M') if last_visit else 'N/A'

    def next_appointment_datetime(self):
        next_appointment = self.next_appointment()
        return next_appointment.date_time.strftime('%Y-%m-%d %H:%M') if next_appointment else 'N/A'

    def last_visit_doctor(self):
        last_visit = self.last_visit()
        return last_visit.doctor.name if last_visit else 'N/A'

    def last_visit_procedures(self):
        last_visit = self.last_visit()
        return dict(Visit.PROCEDURES).get(last_visit.procedures, 'N/A') if last_visit else 'N/A'

    def next_appointment_doctor(self):
        next_appointment = self.next_appointment()
        return next_appointment.doctor.name if next_appointment else 'N/A'

    def next_appointment_procedure(self):
        next_appointment = self.next_appointment()
        return dict(Appointment.PROCEDURES).get(next_appointment.procedure, 'N/A') if next_appointment else 'N/A'

class Visit(models.Model):
    PROCEDURES = [
        ('CL', 'Cleaning'),
        ('FL', 'Filling'),
        ('RC', 'Root Canal'),
        ('CR', 'Crown'),
        ('TW', 'Teeth Whitening'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    procedures = models.CharField(max_length=2, choices=PROCEDURES)
    notes = models.TextField(blank=True)

class Appointment(models.Model):
    PROCEDURES = [
        ('CL', 'Cleaning'),
        ('FL', 'Filling'),
        ('RC', 'Root Canal'),
        ('CR', 'Crown'),
        ('TW', 'Teeth Whitening'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    date_time = models.DateField()
    procedure = models.CharField(max_length=2, choices=PROCEDURES)
    date_booked = models.DateTimeField(auto_now_add=True)
