from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np

dfa = pd.read_csv('insurance.csv')
le = LabelEncoder()
dfa['sex'] = le.fit_transform(dfa['sex'])
dfa['smoker'] = le.fit_transform(dfa['smoker'])
dfa['region'] = le.fit_transform(dfa['region'])

print(dfa.describe())
X = dfa.drop('charges', axis=1)
y = dfa['charges']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# 18,female,31.92,0,no,northeast,2205.9808
new_data = pd.DataFrame({'age': [18], 'sex': [1], 'bmi': [31.92], 'children': [0], 'smoker': [0], 'region': [1]})

rf_model = RandomForestRegressor(n_estimators=250, random_state=42)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
mse_rf = mean_squared_error(y_test, y_pred_rf)
new_pred = rf_model.predict(new_data)
r2 = r2_score(y_test, y_pred_rf)
print(f"MSE with random forest: {mse_rf}")
print(f'Predicted charges: {new_pred[0]:.2f}')
print('Accuracy: ',r2)