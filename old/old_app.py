import pandas as pd
from shapely.geometry import Point, shape

from flask import Flask
from flask import render_template
import json
from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement
from aiocassandra import aiosession

data_path = './input/'
n_samples = 30000

prepared_statements = {
    "patients": "SELECT * FROM",
    "readings": "SELECT * FROM"
}


def pandas_factory(colnames, rows):
    """

    """
    return pd.DataFrame(rows, columns=colnames)

def query_cassandra(statement="readings"):
    """

    """
    cluster = Cluster()
    session = cluster.connect()
    aiosession(session)

    session.row_factory = pandas_factory
    session.default_fetch_size = None

    query = await session.prepare_future(statement)
    dataset = session.execute(query, timeout=None)
    dataframe = dataset._current_rows

    return dataframe


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

    df = query_cassandra()
    df['patients'] = df['id'].nunique()
    df['age_segment'] = df['age'].apply(lambda age: get_age_segment(age))
    df['bmi_segment'] = df['bmi'].apply(lambda bmi: get_bmi_segment(bmi))
    df['location'] = df.apply(lambda row: get_location(row['longitude'], row['latitude'], provinces_json), axis=1)

    cols_to_keep = ['patients', 'timestamp', 'longitude', 'bmi_segment', 'latitude', 'condition', 'status', 'gender', 'age_segment', 'location']
    df_clean = df[cols_to_keep].dropna()
    return df_clean.to_json(orient='records')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
