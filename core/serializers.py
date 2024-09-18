from rest_framework import serializers
from .models import Clinic, Doctor, DoctorClinicAffiliation, Patient, Visit, Appointment

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ['id', 'name', 'phone_number', 'city', 'state', 'address', 'email']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'npi', 'name', 'email', 'phone_number', 'specialties']

class DoctorClinicAffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorClinicAffiliation
        fields = ['id', 'doctor', 'clinic', 'office_address', 'working_schedule']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name', 'date_of_birth', 'address', 'phone_number', 'ssn_last_4', 'gender']

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ['id', 'patient', 'doctor', 'clinic', 'date_time', 'procedures', 'notes']

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'clinic', 'date_time', 'procedure', 'date_booked']
