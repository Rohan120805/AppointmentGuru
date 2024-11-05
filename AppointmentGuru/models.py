from django.db import models

    
class Doctor(models.Model):

    genderChoices = (
        ("Male", "Male"),
        ("Female", "Female"),
    )

    specialisationChoices = (
        ("oncology", "oncology"),
        ("nephrology", "nephrology"),
        ("neurology", "neurology"),
        ("cardiology", "cardiology"),
        ("gastroenterology", "gastroenterology"),
    )

    hospitalNameChoices = (
        ("star hospitals", "star hospitals"),
        ("yashoda hospitals", "yashoda hospitals"),
        ("apollo hospitals", "apollo hospitals"),
        ("kim's hospitals", "kim's hospitals"),
        ("care hospitals", "care hospitals"),
    )

    branchChoices = (
        ("banjara hills", "banjara Hills"),
        ("secunderabad", "secunderabad"),
        ("jubilee hills", "jubilee Hills"),
        ("malakpet", "malakpet"),
        ("gachibowli", "gachibowli"),
    )

    doctorName = models.CharField(max_length=100, default=None)
    email = models.EmailField(max_length=100, default=None)
    phoneNumber = models.CharField(max_length=20, default=None)
    age=models.IntegerField(default=None)
    gender=models.CharField(choices=genderChoices, max_length=6, default=None)
    specialisation=models.CharField(choices=specialisationChoices, max_length=30, default=None)
    hospitalName=models.CharField(choices=hospitalNameChoices, max_length=30, default=None)
    branch=models.CharField(choices=branchChoices, max_length=30, default=None)
    time=models.CharField(max_length=40, default=None)
    max_patients_per_slot = models.IntegerField(default=5)
    password=models.CharField(max_length=20, default=None)

    def __str__(self):
        return self.doctorName

class Customer(models.Model):

    gender_choices = (
        ("Male", "Male"),
        ("Female", "Female"),
    )

    name = models.CharField(max_length=100, default=None)
    email = models.EmailField(max_length=100, default=None)
    phoneNumber = models.CharField(max_length=20, default=None)
    age=models.IntegerField(default=None)
    gender=models.CharField(choices=gender_choices, max_length=6, default=None)
    password=models.CharField(max_length=20, default=None)

    def __str__(self):
        return self.name
    
class Appointment(models.Model):
    
    doctorName=models.CharField(max_length=50, default=None)
    doctorMailId=models.CharField(max_length=150, default=None)
    doctorPhoneNumber=models.CharField(max_length=20, default=None)
    patientName=models.CharField(max_length=50, default=None)
    patientMailId=models.CharField(max_length=150, default=None)
    patientPhoneNumber=models.CharField(max_length=20, default=None)
    date=models.CharField(max_length=15, default=None)
    time=models.CharField(max_length=25, default=None)
    hospitalName=models.CharField(max_length=30, default=None)
    branch=models.CharField(max_length=30, default=None)
    specialisation=models.CharField(max_length=20, default=None)

    def __str__(self):
        return f"{self.doctorName} -> {self.patientName}"
    
class Hospital(models.Model):

    hospitalName=models.CharField(max_length=50, default=None)
    branch=models.CharField(max_length=30, default=None)
    code=models.CharField(max_length=15, default=None)

    def __str__(self):
        return f"{self.hospitalName} -> {self.branch}"