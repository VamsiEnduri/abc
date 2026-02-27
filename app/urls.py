from django.urls import path
from .views import home,register,login,login_validation,doctorsDashboard,patientsDashboard,patientsAppointmentBooking,patientsAppointments,create_patient_profile,delete_patient_profile
urlpatterns=[
    path("",home),
    path("register/",register),
    path("login/",login),
    path("login_validation/",login_validation),
    path("doctorsDashboard/<int:id>/",doctorsDashboard),
    path("doctorsDashboard/<int:id>/appointments/",doctorsDashboard),
    path("doctorsDashboard/<int:id>/profile/",doctorsDashboard),
    path("patientsDashboard/<int:id>/",patientsDashboard),
    path("patientsDashboard/<int:id>/appointments/",patientsDashboard),
    path("patientsDashboard/<int:id>/appointments/book_appointment/",patientsAppointmentBooking,name="book_appointment"),
    path("patientsDashboard/<int:id>/appointments/my_appointments/",patientsAppointments,name="my_appointments"),
    path("patientsDashboard/<int:id>/profile/",patientsDashboard),
    path("patientsDashboard/<int:id>/profile/create/", create_patient_profile),
    path("patientsDashboard/<int:id>/profile/delete/", delete_patient_profile,name="_delete"),
]