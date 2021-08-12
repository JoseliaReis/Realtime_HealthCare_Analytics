"""
This file includes all the configuration required for Plotly Dash Dashboard

"""

# --------- CASSANDRA CONFIGURATION --------- #

host = '127.0.0.1'
username = 'cassandra'
password = 'cassandra'
keyspace = 'healthcare_db'
fetch_size = 10000000

# --------- DASH CONFIGURATION --------- #

# Dash configuration for dropdowns
diseases = ['diabetes', 'hypertension', 'heart disease', 'none']
genders = ["Male", "Female"]
statuses = ['stable unhealthy','stable healthy','critical unhealthy', 'emergency']


gender_options = [{'label': 'Female', 'value': 'Female'},
                   {'label': 'Male', 'value': 'Male'}]

disease_options = [{'label': 'diabetes', 'value': 'diabetes'},
                   {'label': 'hypertension', 'value': 'hypertension'},
                   {'label': 'heart disease', 'value': 'heart disease'},
                   {'label': 'none', 'value': 'none'}]

health_options = [{'label': 'stable unhealthy', 'value': 'stable unhealthy'},
                  {'label': 'stable healthy', 'value': 'stable healthy'},
                  {'label': 'critical unhealthy', 'value': 'critical unhealthy'},
                  {'label': 'emergency', 'value': 'emergency'}]

patient_statistics = ['Patients by BMI', 'Patients by Health Status', 'Patients by Age',
                      'Patients by Condition', 'Patients by Gender', 'Patients by Postcode']


# Create global chart template
mapbox_access_token = "pk.eyJ1IjoiYnJpYW5ob3VyaWdhbiIsImEiOiJja3JtN2VhOTUxbm5wMnBvNWVia2tncW92In0.tRvm3Wd57OOxTYGaDydSTw"

# Color Maps to change the colors!
color_map_bmi = ['#440154', '#471164', '#482071', '#472e7c', '#443b84']
color_map_health = ['#3f4889', '#3a548c', '#34608d', '#2f6c8e', '#2a768e']
color_map_age = ['#26818e', '#228b8d', '#1f958b', '#1fa088', '#24aa83', ]
color_map_condition = ['#2fb47c', '#42be71', '#58c765', '#70cf57', '#8bd646']
color_map_gender = ['#a8db34', '#c5e021', '#e2e418', '#fde725']

color_map_full = ['#440154', '#471164', '#482071', '#472e7c', '#443b84',
                  '#3f4889', '#3a548c', '#34608d', '#2f6c8e', '#2a768e',
                  '#26818e', '#228b8d', '#1f958b', '#1fa088', '#24aa83',
                  '#2fb47c', '#42be71', '#58c765', '#70cf57', '#8bd646',
                  '#a8db34', '#c5e021', '#e2e418', '#fde725']

color_map_small = ['#482071', '#2a768e', '#8bd646', '#fde725']


# --------- PYSTEST CONFIGURATION --------- #

# dictionary of keys with lists as values to use during testing
mock_data = {
    "ages_low": [18, 50],
    "ages_high": [50, 90],
    "bmi_low": [19, 30],
    "bmi_high": [30, 40],
    "temp_low": [34.0, 36.9],
    "temp_high": [37.0, 41.8],
    "heartrate_low": [40, 200],
    "heartrate_high": [200, 300],
    "bloodsugar_low": [35, 200],
    "bloodsugar_high": [200, 400],
    "systolic_low": [100, 140],
    "systolic_high": [140, 220],
    "diastolic_low": [40, 100],
    "diastolic_high": [100, 150]
}