from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments',null=True)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments',null=True)
    appointment_date = models.DateTimeField(null=True)
    disease=models.CharField(max_length=30,null=True)
    image=models.ImageField(upload_to='pics/',null=True)
    
    @property
    def imageURL(self):
        if self.image:
            return self.image.url
        return ''

class Doctor_details(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    cv = models.FileField(upload_to='cv/')
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    @property
    def imageURL(self):
        try:
            url = self.cv.url
        except:
            url = ''
        return url
    

class ConsultationSchedule(models.Model):
    doctor = models.ForeignKey(Doctor_details, on_delete=models.CASCADE)
    day_of_week = models.PositiveSmallIntegerField(choices=[
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday')
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()

