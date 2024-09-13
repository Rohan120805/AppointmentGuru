from django.urls import path
from . import views
urlpatterns=[
    path('', views.home, name='home'),
    path('add_user/', views.add_user, name='add_user'),
    path('userLogin/', views.uLogin, name='uLogin'),
    path('userLogin/userHome/yourAppointments/', views.userAppointments, name='yourAppointments'),
    path('userLogin/userHome/bookAppointment', views.bookAppointment, name='bookAppointment'),
    path('userLogin/userHome/bookAppointment/timeSlot', views.selDoc, name="selectTime"),
    path('userLogin/userHome/userEditDetails', views.uEditDetails, name='userEditDetails'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('doctorLogin/', views.dLogin, name='dLogin'),
    #path('userLogin/userHome/', views., name='userHome'),
    path('doctorLogin/doctorHome/yourAppointments/', views.doctorAppointments, name='docAppointments'),
    path('doctorLogin/doctorHome/todayAppointments/', views.todayAppointments, name='todayAppointments'),
]