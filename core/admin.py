from django.contrib import admin
from .models import Clinic, Doctor, Patient, Visit, Appointment, DoctorClinicAffiliation

admin.site.register(Clinic)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Visit)
admin.site.register(Appointment)
admin.site.register(DoctorClinicAffiliation)