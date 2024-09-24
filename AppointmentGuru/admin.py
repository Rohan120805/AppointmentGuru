from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Hospital)