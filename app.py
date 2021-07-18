import pandas as pd
from shapely.geometry import Point, shape

from flask import Flask
from flask import render_template
import json


data_path = 'input/'
n_samples = 30000

def get_age_segment(age):
    if age < 18:
        return 'Below 18'
    elif 18 <= age <= 39:
        return '18-39'
    elif 40 <= age <= 49:
        return '40-49'
    elif 50 <= age <= 59:
        return '50-59'
    elif 60 <= age <= 69:
        return '60-69'
    elif 70 <= age <= 79:
        return '70-79'
    else:
        return '80+'

def get_bmi_segment(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 > bmi <= 25:
        return 'Normal'
    elif 25 > bmi <= 30:
        return 'Overweight'
    elif 30 > bmi <= 35:
        return 'Obese'
    else:
        return 'Extremely Obese'


def get_bloodpressure_segment(top, bottom):
    if 120 < top < 130 and bottom < 80:
        return 'Elevated Risk'
    elif top >= 130 and bottom <= 80:
        return 'High BP'
    else:
        return 'Normal'

def get_temperature_segment(temperature):
    if temperature < 35.0:
        return 'Hypothermia'
    elif 36.5 > temperature <= 37.5:
        return 'Normal'
    elif 37.5 > temperature <= 38.3:
         return 'Hyperthermia'
    else:
         return 'Hyperpyrexia'

def get_bloodsugar_segment(bloodsugar):
    if bloodsugar < 60:
        return 'Hypoglicemia'
    elif 60 > bloodsugar <= 180:
        return 'Normal'
    elif 180 > bloodsugar <= 280:
        return 'High'
    else:
        return 'Hyperglicemia'

def get_heartrate_segment(heartrate):

    if heartrate < 60 :
        return 'Under 60 pbm'
    elif 60 > heartrate <= 120:
        return '60 to 120bpm'
    elif 120 > heartrate <= 200:
        return '120 to 200'
    else:
        return 'Above 200bpm'

def get_location(longitude, latitude, provinces_json):
    
    point = Point(longitude, latitude)

    for record in provinces_json['features']:
        polygon = shape(record['geometry'])
        if polygon.contains(point):
            return record['properties']['id']
    return 'Co. Dublin'


with open(data_path + '/geojson/dublin_postcodes_en.json') as data_file:
    provinces_json = json.load(data_file)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():

    df = pd.read_csv(data_path + 'data.csv')

    df['age_segment'] = df['age'].apply(lambda age: get_age_segment(age))
    df['bmi_segment'] = df['bmi'].apply(lambda bmi: get_bmi_segment(bmi))
    df['location'] = df.apply(lambda row: get_location(row['longitude'], row['latitude'], provinces_json), axis=1)
    df['bloodpressure_segment'] = df.apply(lambda row: get_bloodpressure_segment(row['blood_pressure_top'], row['blood_pressure_bottom']), axis=1)
    df['temperature_segment'] = df['body_temperature'].apply(lambda bmi: get_temperature_segment(bmi))
    df['bloodsugar_segment'] = df['blood_sugar_level'].apply(lambda bmi: get_bloodsugar_segment(bmi))
    df['heartrate_segment'] = df['heart_rate'].apply(lambda bmi: get_heartrate_segment(bmi))

    cols_to_keep = ['bloodpressure_segment', 'temperature_segment','bloodsugar_segment','heartrate_segment',
                    'timestamp', 'longitude', 'bmi_segment', 'latitude', 'condition',
                    'status', 'gender', 'age_segment', 'location']

    df_clean = df[cols_to_keep].dropna()
    return df_clean.to_json(orient='records')




if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
