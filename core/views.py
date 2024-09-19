from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Clinic, Doctor, Patient, Visit, Appointment, DoctorClinicAffiliation
from .forms import ClinicForm, DoctorForm, PatientForm, VisitForm, AppointmentForm, DoctorClinicAffiliationForm, RegistrationForm
from .serializers import ClinicSerializer, DoctorSerializer, PatientSerializer

# Utility Functions

def handle_form_submission(request, form_class, instance=None, redirect_url=None, template_name=None, extra_context=None):
    form = form_class(request.POST, instance=instance)
    if form.is_valid():
        form.save()
        if redirect_url:
            # Include extra_context in the redirect if provided
            return redirect(redirect_url, **(extra_context or {}))
        return redirect(request.path)
    return render(request, template_name, {'form': form, 'instance': instance})


# Views

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

@login_required
def clinic_list(request):
    query = request.GET.get('search', '')
    clinics = Clinic.objects.filter(name__icontains=query)

    for clinic in clinics:
        clinic.patient_count = clinic.affiliated_patients_count()

    return render(request, 'core/clinic/clinic_list.html', {'clinics': clinics})


@login_required
def clinic_detail(request, pk):
    clinic = get_object_or_404(Clinic, pk=pk)
    if request.method == 'POST':
        return handle_form_submission(
            request, 
            ClinicForm, 
            instance=clinic, 
            redirect_url='clinic_detail', 
            template_name='core/clinic/clinic_detail.html',
            extra_context={'pk': pk}
        )
    return render(request, 'core/clinic/clinic_detail.html', {'clinic': clinic, 'form': ClinicForm(instance=clinic)})


@login_required
def doctor_list(request):
    query = request.GET.get('search', '')
    specialty_filter = request.GET.get('specialty', '')
    doctors = Doctor.objects.filter(name__icontains=query)

    if specialty_filter:
        doctors = doctors.filter(specialties=specialty_filter)

    for doctor in doctors:
        doctor.patient_count = doctor.affiliated_patients_count()

    return render(request, 'core/doctor/doctor_list.html', {'doctors': doctors, 'specialties': Doctor.SPECIALTIES})


@login_required
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        return handle_form_submission(request, DoctorForm, instance=doctor, redirect_url='doctor_detail', template_name='core/doctor/doctor_detail.html', extra_context={'pk': pk})
    return render(request, 'core/doctor/doctor_detail.html', {'doctor': doctor, 'form': DoctorForm(instance=doctor)})

@login_required
def patient_list(request):
    query = request.GET.get('search', '')
    patients = Patient.objects.filter(name__icontains=query)
    return render(request, 'core/patient/patient_list.html', {'patients': patients})

@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        return handle_form_submission(request, PatientForm, instance=patient, redirect_url='patient_detail', template_name='core/patient/patient_detail.html', extra_context={'pk': pk})
    return render(request, 'core/patient/patient_detail.html', {'patient': patient, 'form': PatientForm(instance=patient)})

@login_required
def add_visit(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.patient = patient
            visit.save()
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = VisitForm()
    return render(request, 'core/patient/add_visit.html', {'form': form, 'patient': patient})

@login_required
def schedule_appointment(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = AppointmentForm()
    return render(request, 'core/patient/schedule_appointment.html', {'form': form, 'patient': patient})

@login_required
def add_doctor_clinic_affiliation(request, doctor_pk):
    doctor = get_object_or_404(Doctor, pk=doctor_pk)
    if request.method == 'POST':
        form = DoctorClinicAffiliationForm(request.POST)
        if form.is_valid():
            affiliation = form.save(commit=False)
            affiliation.doctor = doctor
            affiliation.save()
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorClinicAffiliationForm()
    return render(request, 'core/affiliation/add_doctor_clinic_affiliation.html', {'form': form, 'doctor': doctor})

@login_required
def add_clinic(request):
    return handle_form_submission(request, ClinicForm, redirect_url='clinic_list', template_name='core/clinic/add_clinic.html')

@login_required
def add_doctor(request):
    return handle_form_submission(request, DoctorForm, redirect_url='doctor_list', template_name='core/doctor/add_doctor.html')

@login_required
def add_patient(request):
    return handle_form_submission(request, PatientForm, redirect_url='patient_list', template_name='core/patient/add_patient.html')

@login_required
def delete_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
    return render(request, 'core/confirm_delete.html', {'patient': patient})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created for {user.username}!")
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'core/register.html', {'form': form})

def welcome(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/welcome.html')

# API Views

@api_view(['POST'])
def api_add_clinic(request):
    return handle_api_submission(request, ClinicSerializer)

@api_view(['POST'])
def api_add_doctor(request):
    return handle_api_submission(request, DoctorSerializer)

@api_view(['POST'])
def api_add_patient(request):
    return handle_api_submission(request, PatientSerializer)

@api_view(['GET'])
def api_get_clinic_info(request, pk):
    clinic = get_object_or_404(Clinic, pk=pk)
    serializer = ClinicSerializer(clinic)
    return Response(serializer.data)

# API Utility Function

def handle_api_submission(request, serializer_class):
    serializer = serializer_class(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
