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
