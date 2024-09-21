from django.shortcuts import render, redirect, HttpResponse,   get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db import models
import csv
import pandas as pd
import os
from datetime import date, timedelta
from .models import Customer, Doctor

def home(request):
  return render(request,'home.html',{'name':'Rohan'})


class LoginPage:
    def checkpwd(self, data, pwd):
        fpwd=data[-1]#Fill the index op pwd
        #pwd=input("ENTER YOUR PASSWORD")
        if pwd==fpwd:
            return data
        else:
            #print("!!WRONG PASSWORD")
            return False #LoginPage.checkpwd(data)

    def fetchData(self, fname, id):
        userId = id
        userDetails = None
        with open(fname, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if userId == row[1] and not userId.isalnum():
                    row[2] = int(row[2])
                    row[3] = int(row[3])
                    userDetails = row
                    break
                elif userId.isalnum() and userId == row[2]:
                    row[2] = int(row[2])
                    row[3] = int(row[3])
                    userDetails = row
                    break
        return userDetails
        

class UserHomePage:
    
    def alpha(details, field, data):
        df = pd.read_csv("AppointmentGuru/users.csv")
        idx = df[(df["phoneNumber"] == details[2])].index
        df.loc[idx, field] = data
        df.to_csv("AppointmentGuru/users.csv", index=False)

    def yourAppointments(details):#displays all the appointments
        df=pd.read_csv("AppointmentGuru/users/"+str(details[2])+".csv")
        return df.to_html()
    
    def doctors(hosName, branch, specs):
        df=pd.read_csv("AppointmentGuru/doctors.csv")
        if hosName=="None" and branch=="None" and specs=="None":
            doc=df
        elif hosName=="None" and branch=="None":
            doc=df[(df['specialisation']==specs)]
        elif branch=="None" and specs=="None":
            doc=df[(df['hospitalName']==hosName)]
        elif hosName=="None" and specs=="None":
            doc=df[(df['branch']==branch)]
        elif hosName=="None":
            doc=df[(df["branch"]==branch) & (df['specialisation']==specs)]
        elif branch=="None":
            doc=df[(df["hospitalName"]==hosName) & (df['specialisation']==specs)]
        elif specs=="None":
            doc=df[(df["hospitalName"]==hosName) & (df["branch"]==branch)]
        else:
            doc=df[(df["hospitalName"]==hosName) & (df["branch"]==branch) & (df['specialisation']==specs)]#.drop_duplicates().to_records(index=False)
        #docs_list = [row for row in doc]
        print(doc)
        return doc
    

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
            return render(request, 'add_user.html', {'invalid':invalid, 'userExists':userExists})
        else:
            try:
               if Customer.objects.get(email=uemail) or Customer.objects.get(phoneNumber=phNum):
                   print('User exists')
                   return render(request, 'add_user.html', {'invalid': invalid, 'userExists': userExists})
            except:
                userExists=False
                customer = Customer(name=name, email=uemail, phoneNumber=phNum, age=age, gender=gender, password=pwd)
                customer.save()
                return render(request, 'success.html', {"success":"Details updated in database"})
    return render(request, 'add_user.html')

def add_doctor(request):
    render(request, 'add_doctor.html')
    if request.method == 'POST':
        email_exists = False
        phNum_exists = False
        name = request.POST.get('name')
        email = request.POST.get('email')
        phNum = request.POST.get('phNum')
        age = int(request.POST.get('age'))
        gender = request.POST.get('gender')
        spec = request.POST.get('spec')
        hosName = request.POST.get('hosName')
        branch = request.POST.get('branch')
        time = request.POST.get('time')
        pwd = request.POST.get('pwd')
        with open('AppointmentGuru/doctors.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[1] == email:
                    email_exists = True
                if row[2] == phNum:
                    phNum_exists = True
        if any([email_exists, phNum_exists]):
            return render(request, 'add_doctor.html', {'email_exists': email_exists, 'phNum_exists': phNum_exists})
        else:
            with open("AppointmentGuru/doctors.csv", 'a', newline='\n') as file:
                    writer = csv.writer(file)
                    writer.writerow([name, email, phNum, age, gender, spec, hosName, branch, time, pwd])
            with open("AppointmentGuru/doctors/"+str(phNum)+".csv", 'w') as file:
                file.write("appointmentDate,time,patientName,gender,mailId")                
            return render(request, 'success.html', {"success":"Details updated in database"})
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
                request.session['user'] = doctor
                return render(request, "docHome.html", {'result': doctor})
            else:
                return render(request, 'docLogin.html', {'error': True})
        else:
            return render(request, 'docLogin.html', {'error': True})
    return render(request, 'docLogin.html')

def userAppointments(request):
    details = request.session.get('details')
    df=pd.read_csv("AppointmentGuru/users/"+str(details[2])+".csv")
    return render(request, "yourAppointments.html", {'data': df.to_html()})

def uEditDetails(request):
    details = request.session.get('details')
    if request.method == 'POST':
        choice = str(request.POST.get('choice'))
        value = request.POST.get('value')
        UserHomePage.alpha(details, choice, value)
        return render(request, 'success.html', {"success":"Details updated in database", "choice":choice, "value":value})
    return render(request, 'userEditDetails.html', {"details":details})

def bookAppointment(request):
    details = request.session.get('details')
    DataOfDoc=pd.read_csv("AppointmentGuru/doctors.csv")
    docData=UserHomePage.doctors("None", "None", "None")
    docs=docData.to_html()
    avSlots=None
    if request.method == 'POST':
        hosName=str(request.POST.get('hosName'))
        branch=str(request.POST.get('branch'))
        specialization=(request.POST.get('specialization'))
        doctor=(request.POST.get('doctor'))
        docData=UserHomePage.doctors(hosName, branch, specialization)
        docData=docData[["doctorName", "hospitalName", "branch", "time"]]
        request.session['docData'] = docData.to_dict()
        docs = docData.to_html()
        if doctor:
            docDetails=DataOfDoc[DataOfDoc["doctorName"]==doctor].drop_duplicates().to_records(index=False).tolist()
            request.session['docDetails']=docDetails
            avSlots=list(map(str, docDetails[0][8].split("/")))
            request.session['avSlots']=avSlots
            avSlots=pd.DataFrame(avSlots)
            #appointmentDate=str(request.POST.get('appointmentDate'))
            #slot=str(request.POST.get("slot"))
            return render(request, 'slot.html', {"details":details, "today":str(date.today()), "tomorrow":date.today()+timedelta(days=1), "avSlots":avSlots, 'docDetails':docDetails})
        return render(request, 'bookAppointment.html', {"result":docs, "docs":docData, "today":str(date.today()), "avSlots":avSlots})
    return render(request, 'bookAppointment.html', {"details":details, "docs":docData, "result":docs})

def selectSlot(request):
    details = request.session.get('details')
    docDetails = request.session.get('docDetails')
    if request.method == 'POST':
        appointmentDate=request.POST.get('appointmentDate')
        slot=request.POST.get('slot')
        print(appointmentDate)
        print(slot)
        print(pd.DataFrame(request.session.get('avSlots')))
        return render(request, 'success.html', {"choice":appointmentDate, "value":slot})
    return render(request, 'slot.html', {"details":details, "today":str(date.today()), "tomorrow":date.today()+timedelta(days=1), "avSlots":pd.DataFrame(request.session.get('avSlots')), 'docDetails':docDetails})
    #return render(request, 'slot.html', {"details":details})

def doctorAppointments(request):
    # details = request.session.get('ddetails')
    # data=DoctorHomePage.yourAppointments(details)
    doctors = Doctor.objects.all().filter(specialisation = 'oncology')
    print(doctors)
    context = {
        'doctors': doctors
    }
    return render(request, "yourAppointments.html", context)

def todayAppointments(request):
    details = request.session.get('ddetails')
    print(date.today())
    df = pd.read_csv("AppointmentGuru/doctors/"+str(details[2])+".csv")
    df = df[df["appointmentDate"] == str(date.today())]
    print(df)
    html_content = df.to_html()
    return HttpResponse(html_content)

def dEditDetails(request):
    details = request.session.get('ddetails')
    if request.method == 'POST':
        choice = str(request.POST.get('choice'))
        value = request.POST.get('value')
        DoctorHomePage.alpha(details, choice, value)
        return render(request, 'success.html', {"success":"Details updated in database", "choice":choice, "value":value})
    return render(request, 'doctorEditDetails.html', {"details":details})