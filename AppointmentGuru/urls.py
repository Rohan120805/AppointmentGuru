from django.urls import path
from . import views
urlpatterns=[
    path('', views.home, name='home'),
    path('userSignUp/', views.add_user, name='userSignUp'),
    path('userLogin/', views.uLogin, name='uLogin'),
    path('userLogin/userHome/', views.userHome, name='userHome'),
    path('userLogin/userHome/yourAppointments/', views.userAppointments, name='yourAppointments'),
    path('userLogin/userHome/bookAppointment', views.bookAppointment, name='bookAppointment'),
    path('userLogin/userHome/bookAppointment/selectSlot/<str:doctorPhoneNumber>/', views.selectSlot, name='selectSlot'),    
    path('userLogin/userHome/userEditDetails', views.uEditDetails, name='userEditDetails'),
    path('doctorSignUp/', views.add_doctor, name='doctorSignUp'),
    path('doctorLogin/', views.dLogin, name='dLogin'),
    path('doctorLogin/doctorHome/doctorAppointments/', views.doctorAppointments, name='doctorAppointments'),
    path('doctorLogin/doctorHome/todayAppointments/', views.todayAppointments, name='todayAppointments'),
]