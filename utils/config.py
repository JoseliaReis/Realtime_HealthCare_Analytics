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

# Color Maps to change the colors oh the all patient Statisc
color_map_bmi = ['#440154', '#471164', '#482071', '#472e7c', '#443b84']
color_map_health = ['#2e1e3b', '#413d7b', '#37659e', '#348fa7', '#40b7ad', '#8bdab2']
color_map_age = ['#26818e', '#228b8d', '#1f958b', '#1fa088', '#24aa83', ]
color_map_condition = ['#2fb47c', '#42be71', '#58c765', '#70cf57', '#8bd646']
color_map_gender = ['#a8db34', '#c5e021', '#e2e418', '#fde725']

color_map_full = ['#440154', '#471164', '#482071', '#472e7c', '#443b84',
                  '#2e1e3b', '#413d7b', '#37659e', '#348fa7', '#40b7ad', '#8bdab2',
                  '#26818e', '#228b8d', '#1f958b', '#1fa088', '#24aa83',
                  '#2fb47c', '#42be71', '#58c765', '#70cf57', '#8bd646',
                  '#a8db34', '#c5e021', '#e2e418', '#fde725']

color_map_small = ['#4878d0', '#ee854a', '#6acc64', '#d65f5f', '#956cb4', '#8c613c', '#dc7ec0', '#797979', '#d5bb67', '#82c6e2']

