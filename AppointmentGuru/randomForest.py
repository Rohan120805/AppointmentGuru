import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

dfa = pd.read_csv('AppointmentGuru/insurance.csv')
le = LabelEncoder()
dfa['sex'] = le.fit_transform(dfa['sex'])
dfa['smoker'] = le.fit_transform(dfa['smoker'])
dfa['region'] = le.fit_transform(dfa['region'])

X = dfa.drop('charges', axis=1)
y = dfa['charges']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, random_state=42)

rf_model = RandomForestRegressor(n_estimators=250, random_state=42)
rf_model.fit(X_train, y_train)

joblib.dump(rf_model, 'AppointmentGuru/randomForest.pkl')