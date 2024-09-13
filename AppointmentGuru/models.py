from django.db import models

# Create your models here.
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