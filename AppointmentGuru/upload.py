import random
import string
import pandas as pd
from .models import *

df=pd.read_csv("App1/AppointmentGuru/doctors.csv")
hospitals=[]
for i in df['hospitalName'].unique():
    hospitals.append(i)

branches=[]
for j in df['branch'].unique():
    branches.append(j)

def generate_random_string(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def generate_unique_strings(count=30, length=10):
    unique_strings = set()
    while len(unique_strings) < count:
        new_string = generate_random_string(length)
        unique_strings.add(new_string)
    return list(unique_strings)

random_strings = generate_unique_strings()
for s in random_strings:
    print(s)

for hospital in hospitals:
    for branch, rand in branches, random_strings:
        hospital = Hospital(hospitalName=hospital, branch=branch, code=rand)
        hospital.save()