from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phNum = models.CharField(max_length=15)
    password = models.CharField(max_length=14)
    c_password = models.CharField(max_length=14)
    role = models.CharField(max_length=15)

    specialization = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Patient(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phNum = models.CharField(max_length=15)
    password = models.CharField(max_length=14)
    c_password = models.CharField(max_length=14)
    role = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="appointments"
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="appointments"
    )
    problem = models.TextField()
    appointment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        default="Pending"
    )

    def __str__(self):
        return f"{self.patient.name} → {self.doctor.name}"


class PatientProfile(models.Model):
    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    age = models.IntegerField()
    blood_group = models.CharField(max_length=5)
    address = models.TextField()

    def __str__(self):
        return f"{self.patient.name} Profile"