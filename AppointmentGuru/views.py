from django.shortcuts import render, redirect, get_object_or_404
import pandas as pd
from datetime import date, timedelta
from .models import Doctor, Customer, Appointment, Hospital, Feedback
from .forms import FeedbackForm
from django.core.mail import send_mail
from django.conf import settings
import joblib
from django.core.serializers.json import DjangoJSONEncoder
import json

def home(request):
  return render(request,'home.html',{'name':'Rohan'})

def daily(age, gender):
    DAILY_REQUIREMENTS = {
        'Female': {
            (4, 8):  {'Calories': 1200, 'Proteins': 19, 'Fats': 70, 'Sodium': 2300, 'Fiber': 25, 'Carbs': 260, 'Sugar': 50},
            (9, 13): {'Calories': 1600, 'Proteins': 34, 'Fats': 70, 'Sodium': 2300, 'Fiber': 26, 'Carbs': 290, 'Sugar': 50},
            (14, 18): {'Calories': 1800, 'Proteins': 46, 'Fats': 70, 'Sodium': 2300, 'Fiber': 26, 'Carbs': 300, 'Sugar': 50},
            (19, 30): {'Calories': 2000, 'Proteins': 46, 'Fats': 70, 'Sodium': 2300, 'Fiber': 28, 'Carbs': 310, 'Sugar': 50},
            (31, 50): {'Calories': 1800, 'Proteins': 46, 'Fats': 70, 'Sodium': 2300, 'Fiber': 28, 'Carbs': 300, 'Sugar': 50},
            (51, 70): {'Calories': 1600, 'Proteins': 46, 'Fats': 70, 'Sodium': 2300, 'Fiber': 28, 'Carbs': 260, 'Sugar': 50},
            (71, 100): {'Calories': 1500, 'Proteins': 46, 'Fats': 70, 'Sodium': 2300, 'Fiber': 28, 'Carbs': 250, 'Sugar': 50},
        },
        'Male': {
            (4, 8):  {'Calories': 1400, 'Proteins': 19, 'Fats': 70, 'Sodium': 2300, 'Fiber': 25, 'Carbs': 270, 'Sugar': 50},
            (9, 13): {'Calories': 1800, 'Proteins': 34, 'Fats': 70, 'Sodium': 2300, 'Fiber': 31, 'Carbs': 300, 'Sugar': 50},
            (14, 18): {'Calories': 2200, 'Proteins': 52, 'Fats': 70, 'Sodium': 2300, 'Fiber': 31, 'Carbs': 320, 'Sugar': 50},
            (19, 30): {'Calories': 2400, 'Proteins': 56, 'Fats': 70, 'Sodium': 2300, 'Fiber': 34, 'Carbs': 330, 'Sugar': 50},
            (31, 50): {'Calories': 2200, 'Proteins': 56, 'Fats': 70, 'Sodium': 2300, 'Fiber': 34, 'Carbs': 300, 'Sugar': 50},
            (51, 70): {'Calories': 2000, 'Proteins': 56, 'Fats': 70, 'Sodium': 2300, 'Fiber': 30, 'Carbs': 280, 'Sugar': 50},
            (71, 100): {'Calories': 1800, 'Proteins': 56, 'Fats': 70, 'Sodium': 2300, 'Fiber': 30, 'Carbs': 250, 'Sugar': 50},
        }
    }
    for age_range, requirements in DAILY_REQUIREMENTS[gender].items():
        if age_range[0] <= age <= age_range[1]:
            return requirements

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
                if Customer.objects.filter(email=uemail).exists():
                    userExists = True
                elif Customer.objects.filter(phoneNumber=phNum).exists():
                    userExists = True
            except Customer.DoesNotExist:
                userExists = False
        if invalid or userExists:
            return render(request, 'add_user.html', {'invalid': invalid, 'userExists': userExists})
        else:
            customer = Customer(name=name, email=uemail, phoneNumber=phNum, age=age, gender=gender, password=pwd)
            customer.save()
            user = {
            'name': name,
            'email': uemail,
            'phoneNumber': phNum,
            'age': age,
            'gender': gender,
            }
            request.session['user'] = user
            return render(request, "userHome.html", {'result': user})
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
        spec = request.POST.get('specialisation')
        hosName = request.POST.get('hosName')
        hosBranch = request.POST.get('branch')
        time = request.POST.get('time')
        max_patients_per_slot = int(request.POST.get('max_patients_per_slot'))
        hosId = request.POST.get('hosId')
        pwd = request.POST.get('pwd')
        print(hosName, hosBranch)
        id=Hospital.objects.get(hospitalName=hosName, branch=hosBranch)
        if not str(demail).endswith("@gmail.com"):
            invalid = True
        else:
            try:
                if Doctor.objects.filter(email=demail).exists() or Doctor.objects.filter(phoneNumber=phNum).exists():
                    doctorExists = True
            except Doctor.DoesNotExist:
                doctorExists = False
        if hosId==id.code:
            if invalid or doctorExists:
                return render(request, 'add_doctor.html', {'invalid': invalid, 'doctorExists': doctorExists, 'invalidID': False})
            else:
                doctor = Doctor(doctorName=name, email=demail, phoneNumber=phNum, age=age, gender=gender, specialisation=spec, hospitalName=hosName, branch=hosBranch, time=time, password=pwd, max_patients_per_slot=max_patients_per_slot)
                doctor.save()
                return render(request, 'success.html', {"success": "Details updated in database. Go back to login page."})
        else:
            return render(request, 'add_doctor.html', {'invalid': invalid, 'doctorExists': doctorExists, 'invalidID': True})
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
                daily(user["age"], user["gender"])
                return redirect('userHome')
            else:
                return render(request, 'userLogin.html', {'error': True})
        else:
            return render(request, 'userLogin.html', {'error': True})
    return render(request, 'userLogin.html')

def userHome(request):
    user = request.session.get('user')
    return render(request, 'userHome.html', {'result': user, 'requirements': daily(user["age"], user["gender"])})

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
    appointments = Appointment.objects.all().filter(patientPhoneNumber=user["phoneNumber"])
    appointments_list = list(appointments.values('doctorName', 'hospitalName', 'date', 'specialisation', 'time', 'doctorPhoneNumber','patientPhoneNumber', 'id', 'branch'))
    for appointment in appointments_list:
        feedback = Feedback.objects.filter(appointment_id=appointment['id']).first()
        if feedback:
            appointment['rating'] = feedback.rating
            appointment['comments'] = feedback.comments
        else:
            appointment['rating'] = None
        appointment['title'] = f"{appointment['doctorName']}"
        appointment['start'] = appointment['date']
        appointment['description'] = f"Doctor Name: {appointment['doctorName']}\nSpecialisation: {appointment['specialisation']}\nHospital Name: {appointment['hospitalName']}\nBranch: {appointment['branch']}\nSlot: {appointment['time']}"
        # del appointment['doctorName']
        del appointment['hospitalName']
        # del appointment['date']
        del appointment['specialisation']
        # del appointment['time']
        del appointment['doctorPhoneNumber']
        del appointment['patientPhoneNumber']
        # del appointment['id']
    appointments_json = json.dumps(appointments_list, cls=DjangoJSONEncoder)
    return render(request, "yourAppointments.html", {'appointments_json': appointments_json, 'appointments':appointments_list})

def uEditDetails(request):#todo
    details = request.session.get('details')
    if request.method == 'POST':
        choice = str(request.POST.get('choice'))
        value = request.POST.get('value')
        UserHomePage.alpha(details, choice, value)
        return render(request, 'success.html', {"success":"Details updated in database", "choice":choice, "value":value})
    return render(request, 'userEditDetails.html', {"details":details})

def bookAppointment(request):#success
    user = request.session.get('user')
    docData=UserHomePage.doctors("None", "None", "None")
    if request.method == 'POST':
        hosName=str(request.POST.get('hosName'))
        branch=str(request.POST.get('branch'))
        specialization=(request.POST.get('specialization'))
        doctor=(request.POST.get('doctor'))
        docData=UserHomePage.doctors(hosName, branch, specialization)
        print(hosName, branch, specialization)
        if doctor:
            return render(request, 'slot.html', {"details":user, "today":str(date.today()), "tomorrow":date.today()+timedelta(days=1)})
        return render(request, 'bookAppointment.html', {"doctors":docData, "today":str(date.today())})
    return render(request, 'bookAppointment.html', {"details":user, "doctors":docData})

def selectSlot(request, doctorPhoneNumber):#success
    user = request.session.get('user')
    doctor=Doctor.objects.get(phoneNumber=doctorPhoneNumber)
    slots=list(map(str, doctor.time.split('/')))
    if request.method == 'POST':
        appointmentDate=request.POST.get('appointmentDate')
        slot=request.POST.get('slot')
        #user: name, email, phoneNumber, age, gender
        #doctor: doctorName, email, phoneNumber, age, gender, specialisation, hospitalName, branch, time
        #appointment: doctorName, doctorMailId, doctorPhoneNumber, patientName, patientMailId, patientPhoneNumber, date, time, hospitalName, branch, specialisation
        #checks the number of appointments in a slot
        appointments = Appointment.objects.filter(doctorPhoneNumber=doctorPhoneNumber, date=appointmentDate, time=slot)
        if appointments.count() >= doctor.max_patients_per_slot:
            return render(request, 'slot.html', {
                'details': user,
                'tomorrow': date.today()+timedelta(days=1),
                'end': date.today()+timedelta(days=7),
                'phoneNumber': doctorPhoneNumber,
                'slots': slots,
                'error': 'This slot is fully booked. Please choose another slot.'
            })
        

        appointment = Appointment(doctorName=doctor.doctorName, doctorMailId=doctor.email, doctorPhoneNumber=doctor.phoneNumber, patientName=user['name'], patientMailId=user['email'], patientPhoneNumber=user['phoneNumber'], date=appointmentDate, time=slot, hospitalName=doctor.hospitalName, branch=doctor.branch, specialisation=doctor.specialisation)
        appointment.save()
        #sends mail to users after booking appointment
        subject = 'Appointment Confirmation'
        message = f'Dear {user["name"]},\n\nYour appointment with Dr. {doctor.doctorName} on {appointmentDate} at {slot} has been confirmed.\n\nThank you,\nAppointment Guru'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user['email']]
        send_mail(subject, message, from_email, recipient_list)

        return render(request, 'success.html', {"success":f"Your appointment has been confirmed with Dr. {doctor.doctorName}", "choice":f"Date: {appointmentDate}", "value":f"Time: {slot}"})
    return render(request, 'slot.html', {"details":user, "tomorrow":date.today()+timedelta(days=1),"end":date.today()+timedelta(days=7), "phoneNumber":doctorPhoneNumber, "slots":slots})

def doctorAppointments(request):
    doctor = request.session.get('doctor')
    fDate = request.POST.get('date')
    if fDate:
        appointments = Appointment.objects.all().filter(doctorName=doctor['name'], date=fDate)
    else:
        appointments = Appointment.objects.all().filter(doctorName=doctor['name'])
    
    appointments_list = list(appointments.values('patientName', 'date', 'time', 'patientMailId'))
    for appointment in appointments_list:
        appointment['title'] = f"{appointment['patientName']}"
        appointment['start'] = appointment['date']
        appointment['description'] = f"Patient Name: {appointment['patientName']}\nMail ID: {appointment['patientMailId']}\nSlot: {appointment['time']}"
        del appointment['patientName']
        del appointment['date']
        del appointment['time']
        del appointment['patientMailId']
    
    appointments_json = json.dumps(appointments_list, cls=DjangoJSONEncoder)
    return render(request, "doctorAppointments.html", {'appointments_json': appointments_json})

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

def insurance_predictor(request):
    if request.method == 'POST':
        age = int(request.POST.get('age'))
        sex = int(request.POST.get('sex'))
        bmi = float(request.POST.get('bmi'))
        children = int(request.POST.get('children'))
        smoker = int(request.POST.get('smoker'))
        region = int(request.POST.get('region'))


        new_data = pd.DataFrame({'age': [age], 'sex': [sex], 'bmi': [bmi], 'children': [children], 'smoker': [smoker], 'region': [region]})
        rf_model = joblib.load('AppointmentGuru/randomForest.pkl')
        new_pred = rf_model.predict(new_data)
        prediction=round(new_pred[0], 2)

        return render(request, 'insurance.html', {'prediction': prediction})
    return render(request, 'insurance.html')

def submit_feedback(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.appointment = appointment
            feedback.save()
            return redirect('feedback_success')
    else:
        form = FeedbackForm()
    return render(request, 'submit_feedback.html', {'form': form, 'appointment': appointment})

def feedback_success(request):
    return render(request, 'feedback_success.html')