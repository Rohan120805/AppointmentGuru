from django.shortcuts import render
import pandas as pd
from datetime import date, timedelta
from .models import *

def home(request):
  return render(request,'home.html',{'name':'Rohan'})
        

class UserHomePage:
    
    def alpha(details, field, data):
        df = pd.read_csv("AppointmentGuru/users.csv")
        idx = df[(df["phoneNumber"] == details[2])].index
        df.loc[idx, field] = data
        df.to_csv("AppointmentGuru/users.csv", index=False)

    def doctors(hosName, hosBranch, specs):
        if hosName=="None" and hosBranch=="None" and specs=="None":
            df=Doctor.objects.all()
        elif hosName=="None" and hosBranch=="None":
            df=Doctor.objects.all().filter(specialisation=specs)
        elif hosBranch=="None" and specs=="None":
            df=Doctor.objects.all().filter(hospitalName=hosName)
        elif hosName=="None" and specs=="None":
            df=Doctor.objects.all().filter(branch=hosBranch)
        elif hosName=="None":
            df=Doctor.objects.all().filter(branch=hosBranch, specialisation=specs)
        elif hosBranch=="None":
            df=Doctor.objects.all().filter(hospitalName=hosName, specialisation=specs)
        elif specs=="None":
            df=Doctor.objects.all().filter(hospitalName=hosName, branch=hosBranch)
        else:
            df=Doctor.objects.all().filter(hospitalName=hosName, branch=hosBranch, specialisation=specs)
        print(df)
        return df
    

class DoctorHomePage:
    #doctorName,email,phoneNumber,age,gender,specialisation,hospitalName,branch,time,password

    def yourAppointments(details):
        df=pd.read_csv("AppointmentGuru/doctors/"+str(details[2])+".csv")
        #print(df)
        return df.to_html()
    
    def todayAppointments(details):
        print(date.today())
        df=pd.read_csv("AppointmentGuru/doctors/"+str(details[2])+".csv")
        df=df[df["appointmentDate"]==str(date.today())]
        print(df)
        return df.to_html()

    def alpha(details, field, data):
        df = pd.read_csv("AppointmentGuru/doctors.csv")
        idx = df[(df["phoneNumber"] == details[2])].index
        df.loc[idx, field] = data
        df.to_csv("AppointmentGuru/doctors.csv", index=False)


def add_user(request):
    #render(request, 'add_user.html')
    if request.method == 'POST':
        invalid = False
        userExists = False
        name = request.POST.get('name')
        uemail = str(request.POST.get('email'))
        phNum = str(request.POST.get('phNum'))
        age = int(request.POST.get('age'))
        gender = request.POST.get('gender')
        pwd = request.POST.get('pwd')
        if not str(uemail).endswith("@gmail.com"):
            invalid = True
        else:
            try:
                if Customer.objects.get(email=uemail) or Customer.objects.get(phoneNumber=phNum):
                    userExists = True
            except:
                userExists = False
        if invalid or userExists:
            return render(request, 'add_user.html', {'invalid': invalid, 'userExists': userExists})
        else:
            customer = Customer(name=name, email=uemail, phoneNumber=phNum, age=age, gender=gender, password=pwd)
            customer.save()
            return render(request, 'success.html', {"success": "Details updated in database"})
    return render(request, 'add_user.html')

def add_doctor(request):
    if request.method == 'POST':
        invalid = False
        doctorExists = False
        name = request.POST.get('name')
        demail = request.POST.get('email')
        phNum = request.POST.get('phNum')
        age = int(request.POST.get('age'))
        gender = request.POST.get('gender')
        spec = request.POST.get('spec')
        hosName = request.POST.get('hosName')
        branch = request.POST.get('branch')
        time = request.POST.get('time')
        pwd = request.POST.get('pwd')
        if not str(demail).endswith("@gmail.com"):
            invalid = True
        else:
            try:
                if Doctor.objects.get(email=demail) or Doctor.objects.get(phoneNumber=phNum):
                    doctorExists = True
            except:
                doctorExists = False
        if invalid or doctorExists:
            return render(request, 'add_doctor.html', {'invalid': invalid, 'doctorExists': doctorExists})
        else:
            doctor = Doctor(doctorName=name, email=demail, phoneNumber=phNum, age=age, gender=gender, specialisation=spec, hospitalName=hosName, branch=branch, time=time, password=pwd)
            doctor.save()
            return render(request, 'success.html', {"success": "Details updated in database"})
    return render(request, 'add_doctor.html')

def uLogin(request):
    render(request, 'userLogin.html')
    if request.method == 'POST':
        authid = str(request.POST.get('authid'))
        pwd = str(request.POST.get('pwd'))
        try:
            if authid.isalnum():
                userDetails = Customer.objects.get(phoneNumber=authid, password=pwd)
            else:
                userDetails = Customer.objects.get(email=authid, password=pwd)
            user = {
            'name': userDetails.name,
            'email': userDetails.email,
            'phoneNumber': userDetails.phoneNumber,
            'age': userDetails.age,
            'gender': userDetails.gender,
            }
        except Exception as e:
            userDetails=False
        if userDetails:
            if userDetails.password==pwd:
                request.session['user'] = user
                return render(request, "userHome.html", {'result': user})
            else:
                return render(request, 'userLogin.html', {'error': True})
        else:
            return render(request, 'userLogin.html', {'error': True})
    return render(request, 'userLogin.html')

def dLogin(request):
    render(request, 'docLogin.html')
    if request.method == 'POST':
        authid = str(request.POST.get('authid'))
        pwd = str(request.POST.get('pwd'))
        try:
            if authid.isalnum():
                doctorDetails = Doctor.objects.get(phoneNumber=authid, password=pwd)
            else:
                doctorDetails = Customer.objects.get(email=authid, password=pwd)
            doctor = {
            'name': doctorDetails.doctorName,
            'email': doctorDetails.email,
            'phoneNumber': doctorDetails.phoneNumber,
            'age': doctorDetails.age,
            'gender': doctorDetails.gender,
            'branch': doctorDetails.branch,
            'hospitalName': doctorDetails.hospitalName,
            'specialisation': doctorDetails.specialisation,
            }
        except Exception as e:
            doctorDetails=False
        if doctorDetails:
            if doctorDetails.password==pwd:
                request.session['doctor'] = doctor
                return render(request, "docHome.html", {'result': doctor})
            else:
                return render(request, 'docLogin.html', {'error': True})
        else:
            return render(request, 'docLogin.html', {'error': True})
    return render(request, 'docLogin.html')

def userAppointments(request):
    user = request.session.get('user')
    appointments=Appointment.objects.all().filter(patientPhoneNumber=user["phoneNumber"])
    return render(request, "yourAppointments.html", {'appointments': appointments})

def uEditDetails(request):#todo
    details = request.session.get('details')
    if request.method == 'POST':
        choice = str(request.POST.get('choice'))
        value = request.POST.get('value')
        UserHomePage.alpha(details, choice, value)
        return render(request, 'success.html', {"success":"Details updated in database", "choice":choice, "value":value})
    return render(request, 'userEditDetails.html', {"details":details})

def bookAppointment(request):#todo
    user = request.session.get('user')
    docData=UserHomePage.doctors("None", "None", "None")
    if request.method == 'POST':
        hosName=str(request.POST.get('hosName'))
        branch=str(request.POST.get('branch'))
        specialization=(request.POST.get('specialization'))
        doctor=(request.POST.get('doctor'))
        docData=UserHomePage.doctors(hosName, branch, specialization)
        if doctor:
            return render(request, 'slot.html', {"details":user, "today":str(date.today()), "tomorrow":date.today()+timedelta(days=1)})
        return render(request, 'bookAppointment.html', {"doctors":docData, "today":str(date.today())})
    return render(request, 'bookAppointment.html', {"details":user, "doctors":docData})

def selectSlot(request, doctorPhoneNumber):#todo
    user = request.session.get('user')
    doctor=Doctor.objects.get(phoneNumber=doctorPhoneNumber)
    slots=list(map(str, doctor.time.split('/')))
    if request.method == 'POST':
        appointmentDate=request.POST.get('appointmentDate')
        slot=request.POST.get('slot')
        #user: name, email, phoneNumber, age, gender
        #doctor: doctorName, email, phoneNumber, age, gender, specialisation, hospitalName, branch, time
        #appointment: doctorName, doctorMailId, doctorPhoneNumber, patientName, patientMailId, patientPhoneNumber, date, time, hospitalName, branch, specialisation
        appointment = Appointment(doctorName=doctor.doctorName, doctorMailId=doctor.email, doctorPhoneNumber=doctor.phoneNumber, patientName=user['name'], patientMailId=user['email'], patientPhoneNumber=user['phoneNumber'], date=appointmentDate, time=slot, hospitalName=doctor.hospitalName, branch=doctor.branch, specialisation=doctor.specialisation)
        appointment.save()
        return render(request, 'success.html', {"choice":appointmentDate, "value":slot})
    return render(request, 'slot.html', {"details":user, "tomorrow":date.today()+timedelta(days=1), "phoneNumber":doctorPhoneNumber, "slots":slots})

def doctorAppointments(request):#success
    doctor=request.session.get('doctor')
    fDate=request.POST.get('date')
    if fDate:
        appointments = Appointment.objects.all().filter(doctorName=doctor['name'], date=fDate)
        return render(request, "doctorAppointments.html", {'appointments':appointments})
    appointments = Appointment.objects.all().filter(doctorName=doctor['name'])
    return render(request, "doctorAppointments.html", {'appointments':appointments})

def todayAppointments(request):#success
    doctor=request.session.get('doctor')
    print(doctor['name'])
    appointments = Appointment.objects.all().filter(doctorName=doctor['name'], date=date.today())
    print(appointments)
    context = {
        'appointments': appointments,
    }
    return render(request, "todayAppointments.html", context)

def dEditDetails(request):#todo
    details = request.session.get('ddetails')
    if request.method == 'POST':
        choice = str(request.POST.get('choice'))
        value = request.POST.get('value')
        DoctorHomePage.alpha(details, choice, value)
        return render(request, 'success.html', {"success":"Details updated in database", "choice":choice, "value":value})
    return render(request, 'doctorEditDetails.html', {"details":details})