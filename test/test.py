import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

df = pd.read_csv("../data/healthcare_data.csv", low_memory=False)

def filter_dataframe(df, disease, status, age, gender,
                     bmi, temperature, heartrate, bloodsugar, systolic, diastolic):

    filtered_data = df[
        (df["condition"].isin(disease)) # Filter by diseases/conditions
        & (df["status"].isin(status)) # Filter by status
        & (df["gender"].isin(gender)) # Filter by gender
        & ((df["age"] >= age[0]) & (df["age"] <= age[1])) # Filter between ages
        & ((df["bmi"] >= bmi[0]) & (df["age"] <= bmi[1])) # Filter by BMI
        # Filter between heart rate
        & ((df["heart_rate"] >= heartrate[0]) & (df["heart_rate"] <= heartrate[1]))
        # Filter between body temperature
        & ((df["body_temperature"] >= temperature[0]) & (df["body_temperature"] <= temperature[1]))
        # Filter between blood sugar
        & ((df["blood_sugar_level"] >= bloodsugar[0]) & (df["blood_sugar_level"] <= bloodsugar[1]))
        # Filter between blood pressure top (systolic)
        & ((df["blood_pressure_top"] >= systolic[0]) & (df["blood_pressure_top"] <= systolic[1]))
        # Filter between blood pressure bottom (diastolic)
    & ((df["blood_pressure_bottom"] >= diastolic[0]) & (df["blood_pressure_bottom"] <= diastolic[1]))
        ]

    # keep only the columns we need
    filtered_data = filtered_data[['name', 'condition','reading_id',
          'heart_rate', 'blood_pressure_top', 'blood_pressure_bottom', 'body_temperature',
          'blood_sugar_level', 'timestamp', 'longitude', 'latitude']]

    return filtered_data

statuses = ["critical unhealthy", "stable unhealthy", "stable healthy"]
diseases = ["hypertension", "none", "diabetes", "heart disease"]
timestamps = ["0"]
ages = [0, 100]
genders = ['Male', 'Female']
bmi = [0,50]
temperature = [0,100]
heartrate = [0,600]
bloodsugar= [0,600]
systolic= [0,600]
diastolic = [0,600]

newdf = filter_dataframe(df, diseases, statuses, ages, genders,
                     bmi, temperature, heartrate, bloodsugar, systolic, diastolic)

newdf = newdf.reindex(newdf.columns.tolist(), axis = 1)
newdf = newdf.to_dict("records")
print(newdf)