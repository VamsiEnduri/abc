from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Doctor,Patient,Appointment,PatientProfile
from django.http import HttpResponse
from .forms import PatientProfileForm
# Create your views here.
def home(req):
    return render(req,"registration.html")

def delete_patient_profile(request, id):
    patient = Patient.objects.get(id=id)
    profile = PatientProfile.objects.get(patient=patient)

    if request.method == "POST":
        profile.delete()

    return render(request, "patientsProfile.html", {
        "user": patient,
        "profile": profile
    })

def create_patient_profile(request, id):
    patient = Patient.objects.get(id=id)
    form = PatientProfileForm()

    if request.method == "POST":
        form = PatientProfileForm(request.POST)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.patient = patient
            profile.save()
    else:
        form = PatientProfileForm()
    return render(request, "patientprofile_create.html", {
        "form": form,
        "user": patient
    })

from .models import Doctor, Patient, Appointment


def patientsAppointments(req,id):
    p=Patient.objects.get(id=id)
    patient_appts=Appointment.objects.filter(patient_id=id)
    return render(req,"my_appts.html",{
          "p_appts":patient_appts,
          "p":p
    })

def patientsAppointmentBooking(request, id):
    print(id,"pid")
    patient = Patient.objects.get(id=id)
    allDoctors = Doctor.objects.all()

    if request.method == "POST":
        doctor_id = request.POST.get("doctor_id")
        problem = request.POST.get("problem")
        appointment_date = request.POST.get("appointment_date")

        # basic validation
        if not all([doctor_id, problem, appointment_date]):
            return render(request, "book_appointment.html", {
                "user": patient,
                "role": "Patient",
                "allDoctors": allDoctors,
                "error": "All fields are required"
            })

        doctor = Doctor.objects.get(id=doctor_id)

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            problem=problem,
            appointment_date=appointment_date
        )

        # after booking → redirect
        # return redirect("patientsDashboard", id=patient.id)

    # GET request
    return render(request, "book_appointment.html", {
        "user": patient,
        "role": "Patient",
        "allDoctors": allDoctors
    })


def patientsDashboard(req,id):
    LoggedINPatient=Patient.objects.get(id=id)
    profile = PatientProfile.objects.get(patient_id=LoggedINPatient)

    if "appointments" in req.path:
        template="patientsAppts2.html"
    elif "profile" in req.path:
        template="patientsProfile.html"
    else:
        template="patientsDashboard.html"    
    return render(req,template,{"user":LoggedINPatient,"profile":profile}) 

def doctorsDashboard(req,id):
    LoggedINDoctor=Doctor.objects.get(id=id)
    if "appointments" in req.path:
        template="doctorsAppointments.html"
    elif "profile" in req.path:
        template="doctorsProfile.html"
    else:
        template="doctorsDashboard.html"    
    return render(req,template,{"user":LoggedINDoctor})    

@api_view(["POST"])
def login_validation(req):
    e=req.data.get("email")
    p=req.data.get("password")
    r=req.data.get("role")
    drs=Doctor.objects.all().values()
    pts=Patient.objects.all().values()

    if r == "Doctor":
        try:
            doctor=Doctor.objects.get(email=e)
            if doctor.password == p:
                return Response({
                     "msg": "Doctor logged in successfully",
                    "role": "Doctor",
                    "r_url": "doctorsDashboard",
                    "login_id": doctor.id
                })
            else:
                return Response({"error": "Invalid password"})
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found"})
    elif r == "Patient":
        try:
            patient=Patient.objects.get(email=e)

            if patient.password == p:
                return Response(
                    {
                    "msg": "Patient logged in successfully",
                    "role": "Patient",
                    "r_url": "patientsDashboard",
                    "login_id": patient.id
                }
                )
            else:
                return Response({"error": "Invalid password"})    
        except Patient.DoesNotExist:
        
            return Response({"error": "Patient not found"})
    else:
        return Response({"error": "Invalid role"}) 

@api_view(["GET"])
def login(req):
    return render(req,"login.html")

@api_view(["POST"])
def register(req):
    n = req.data.get("n")
    e = req.data.get("e")
    ph = req.data.get("ph")
    p = req.data.get("p")
    cp = req.data.get("cp")
    r = req.data.get("r")
    s = req.data.get("s")

    if not all([n, e, ph, p, cp, r]):
        return Response({"error": "All fields required"}, status=400)

    if p != cp:
        return Response({"error": "Passwords do not match"}, status=400)

    if r == "Doctor":
        if Doctor.objects.filter(email=e).exists():
            return Response({"error": "Doctor already exists"}, status=400)

        Doctor.objects.create(
            name=n,
            email=e,
            phNum=ph,
            password=p,
            c_password=cp,
            role=r,
            specialization=s
        )

        return Response({"msg": "Doctor registered successfully"}, status=201)

    elif r == "Patient":
        if Patient.objects.filter(email=e).exists():
            return Response({"error": "Patient already exists"}, status=400)

        Patient.objects.create(
            name=n,
            email=e,
            phNum=ph,
            password=p,
            c_password=cp,
            role=r
        )

        return Response({"msg": "Patient registered successfully"}, status=201)

    return Response({"error": "Invalid role"}, status=400)