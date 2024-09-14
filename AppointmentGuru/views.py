from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import csv
import pandas as pd
import os
from datetime import date

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
    
    def bookAppointment(doc_list):
        #t=list(map(str, doc_list[docName-1][-2].split("/")))
        #time=int(input(f"Select time"))
        #dt=input("Enter Date")
        #User:userName,email,phoneNumber,age,gender,password
        #Doctor:doctorName,email,phoneNumber,age,gender,specialisation,hospitalName,branch,time,password
        with open("doctors/"+str(doc_list[docName-1][2])+".csv", 'a', newline='\n') as file:
            #appointmentDate,time,patientName,gender,mailId
            writer = csv.writer(file)
            writer.writerow([str(dt), str(t[time-1]), str(details[0]), str(details[-2]), str(details[1])])
        
        with open("users/"+str(details[2])+".csv", 'a', newline="\n") as file:
            #appointmentDate,time,doctorName,hospitalName,branch
            writer = csv.writer(file)
            writer.writerow([str(dt), str(t[time-1]), str(doc_list[docName-1][0]), str(doc_list[docName-1][6]), str(doc_list[docName-1][7])])


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
        email_exists = False
        phNum_exists = False
        name = request.POST.get('name')
        email = str(request.POST.get('email'))
        phNum = str(request.POST.get('phNum'))
        age = int(request.POST.get('age'))
        gender = request.POST.get('gender')
        pwd = request.POST.get('pwd')
        if not str(email).endswith("@gmail.com"): email_exists = True
        with open('AppointmentGuru/users.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[1] == email:
                    email_exists = True
                if row[2] == phNum:
                    phNum_exists = True
        if any([email_exists, phNum_exists]):
            return render(request, 'add_user.html', {'email_exists': email_exists, 'phNum_exists': phNum_exists})
        else:
            with open("AppointmentGuru/users.csv", 'a', newline='\n') as file:
                writer = csv.writer(file)
                writer.writerow([name, email, phNum, age, gender, pwd])
            with open("AppointmentGuru/users/"+str(phNum)+".csv", 'w') as file:
                file.write("appointmentDate,time,doctorName,hospitalName,branch")
            return render(request, 'success.html', {"success":"Details updated in database"})
    return render(request, 'add_user.html')

def add_doctor(request):
    render(request, 'add_doctor.html')
    if request.method == 'POST':
        email_exists = False
        phNum_exists = False
        name = request.POST.get('name')
        email = SignupPage.checkEmail(request.POST.get('email'))
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
        # Handle form submission
        authid = str(request.POST.get('authid'))
        pwd = str(request.POST.get('pwd'))
        user_details = LoginPage().fetchData('AppointmentGuru/users.csv', authid)
        if user_details:
            # Validate password
            user_data = LoginPage().checkpwd(user_details, pwd)
            if user_data:
                # Successful login
                request.session['details'] = user_data
                return render(request, "userHome.html", {'result': user_data})
            else:
                return render(request, 'userLogin.html', {'error': True})
                #messages.error(request, 'Invalid password. Please try again.')
                #return render(request, "warning.html", {"warning": "Wrong Password"})
        else:
            return render(request, 'userLogin.html', {'invalid_authid': True})
            #messages.error(request, 'User not found. Please check the details.')
            #return render(request, "warning.html", {"warning": "User not found. Please check the details."})
    #else:
    return render(request, 'userLogin.html')

def dLogin(request):
    render(request, 'docLogin.html')
    if request.method == 'POST':
        # Handle form submission
        authid = str(request.POST.get('authid'))
        pwd = str(request.POST.get('pwd'))
        doctor_details = LoginPage().fetchData('AppointmentGuru/doctors.csv', authid)
        if doctor_details:
            # Validate password
            doctor_data = LoginPage().checkpwd(doctor_details, pwd)
            if doctor_data:
                # Successful login
                request.session['ddetails'] = doctor_data
                return render(request, "docHome.html", {'result': doctor_data})
            else:
                return render(request, 'docLogin.html', {'error': True})
                #messages.error(request, 'Invalid password. Please try again.')
                #return render(request, "warning.html", {"warning": "Wrong Password"})
        else:
            return render(request, 'docLogin.html', {'invalid_authid': True})
            #messages.error(request, 'User not found. Please check the details.')
            #return render(request, "warning.html", {"warning": "Doctor not found. Please check the details."})
    #else:
    return render(request, 'docLogin.html')

def userAppointments(request):
    details = request.session.get('details')
    #data=UserHomePage.yourAppointments(details)
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
    dfa=docData
    avSlots=None
    if request.method == 'POST':
        hosName=str(request.POST.get('hosName'))
        branch=str(request.POST.get('branch'))
        specialization=(request.POST.get('specialization'))
        doctor=(request.POST.get('doctor'))
        appointmentDate=str(request.POST.get('appointmentDate'))
        slot=str(request.POST.get('slot'))
        docData=UserHomePage.doctors(hosName, branch, specialization)
        dfa=docData
        docData=docData[["doctorName", "hospitalName", "branch", "time"]]
        request.session['docData'] = docData.to_dict()
        docs = docData.to_html()
        x=str(date.today())
        if doctor:
            docDetails=DataOfDoc[DataOfDoc["doctorName"]==doctor].drop_duplicates().to_records(index=False).tolist()
            #print(docDetails[0][8])
            avSlots=list(map(str, docDetails[0][8].split("/")))
            avSlots=pd.DataFrame(avSlots)
            #print(avSlots)
            #appointmentDate=str(request.POST.get('appointmentDate'))
            #slot=str(request.POST.get("slot"))
            print(slot)
            print(appointmentDate)
            return render(request, 'bookAppointment.html', {"result":docs, "docs":dfa, "today":x, "avSlots":avSlots, "appointmentDate": appointmentDate, "slot": slot})  # Pass appointmentDate and slot to the template
        return render(request, 'bookAppointment.html', {"result":docs, "docs":dfa, "today":x, "avSlots":avSlots, "appointmentDate": appointmentDate, "slot": slot})  # Pass appointmentDate and slot to the template
    return render(request, 'bookAppointment.html', {"details":details, "docs":dfa, "result":docs})

def selDoc(request):
    details = request.session.get('details')
    if request.method == 'POST':
        doctor=(request.POST.get('doctor'))
        dt=str(request.POST.get('dt'))
        #ts=str(request.POST.get('ts'))
        df=pd.read_csv("AppointmentGuru/doctors.csv")
        df=df[df['doctorName']==doctor]
        all_slots = []
        for time in df['time']:
            slots = list(time.split('/'))
            all_slots.append(slots)
        df1=pd.DataFrame(all_slots)
        #print(df1)
    return render(request, 'timeSlot.html', {"details":df1})

def doctorAppointments(request):
    details = request.session.get('ddetails')
    data=DoctorHomePage.yourAppointments(details)
    return render(request, "yourAppointments.html", {'data': data})

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