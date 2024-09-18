from django import forms
from .models import Clinic, Doctor, Patient, Visit, Appointment, DoctorClinicAffiliation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator


class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = ['name', 'phone_number', 'city', 'state', 'address', 'email']

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['npi', 'name', 'email', 'phone_number', 'specialties']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'date_of_birth', 'address', 'phone_number', 'ssn_last_4', 'gender']

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['doctor', 'clinic', 'date_time', 'procedures', 'notes']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'clinic', 'date_time', 'procedure']

class DoctorClinicAffiliationForm(forms.ModelForm):
    class Meta:
        model = DoctorClinicAffiliation
        fields = ['clinic', 'office_address', 'working_schedule']

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
