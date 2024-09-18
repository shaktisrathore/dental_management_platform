from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('clinics/', views.clinic_list, name='clinic_list'),
    path('clinics/<int:pk>/', views.clinic_detail, name='clinic_detail'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:patient_pk>/add_visit/', views.add_visit, name='add_visit'),
    path('patients/<int:patient_pk>/schedule_appointment/', views.schedule_appointment, name='schedule_appointment'),
    path('doctors/<int:doctor_pk>/add_affiliation/', views.add_doctor_clinic_affiliation, name='add_doctor_clinic_affiliation'),
    path('clinics/add/', views.add_clinic, name='add_clinic'),
    path('doctors/add/', views.add_doctor, name='add_doctor'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('patients/<int:pk>/delete/', views.delete_patient, name='delete_patient'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='welcome'), name='logout'),
    path('register/', views.register, name='register'),
    
    # API endpoints
    path('api/clinics/add/', views.api_add_clinic, name='api_add_clinic'),
    path('api/doctors/add/', views.api_add_doctor, name='api_add_doctor'),
    path('api/patients/add/', views.api_add_patient, name='api_add_patient'),
    path('api/clinics/<int:pk>/', views.api_get_clinic_info, name='api_get_clinic_info'),
]