# Import required libraries

import dash_table
import pandas as pd
import numpy as np
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from aiocassandra import aiosession

"""This function it is a python package that will connect to Cassandra and load the data faster """
async def read_cassandra(host, username, password, keyspace):
    """
    https://github.com/aio-libs/aiocassandra/blob/master/example.py

    :return:
    """
    # patches and adds `execute_future`, `execute_futures` and `prepare_future`
    # to `cassandra.cluster.Session`

    cluster = Cluster(
        contact_points=[host],
        auth_provider=PlainTextAuthProvider(username=username, password=password)
    )
    session = cluster.connect()
    session.set_keyspace(keyspace)
    aiosession(session)

    # if non-blocking prepared statements is really needed:
    query = await session.prepare_future('SELECT * FROM healthcare_db.device_patient')

    df = pd.DataFrame(await session.execute_future(query))

    return df



#-- These are the counts for the blue
def get_total_counts(df):
    """

    :param df:
    :return:
    """

    # filter the dataframe to just id, reading_id and alert
    df2 = df[['id', 'reading_id', 'alert']]

    # Group the age segment by unique names (as each patient has more than one record) to count the specific segments
    total_patients = df2['id'].nunique()
    total_readings = df2['reading_id'].nunique()

    # Remove Null or Nan values in Alert Column
    df2 = df2[df2['alert'].notna()]

    # Get count of alerts where alert contains EMERGENCY!
    total_emergencies = df2['alert'][df2['alert'].str.contains('EMERGENCY!')].count()

    # Get count of alerts where alert contains WARNINGS!
    total_warnings = df2['alert'][df2['alert'].str.contains('WARNING!')].count()

    total_alerts = total_emergencies + total_warnings

    return total_patients, total_readings, total_alerts, total_emergencies, total_warnings


# -- These are the counts for the green
def get_alert_counts(df):

    alerts = create_alert_table(df)
    alerts = alerts[['alert']]

    hypertension = alerts['alert'][alerts['alert'].str.contains('HYPERTENSION')].count()
    hypothermia = alerts['alert'][alerts['alert'].str.contains('HYPOTHERMIA')].count()
    hyperthermia = alerts['alert'][alerts['alert'].str.contains('HYPERTHERMIA')].count()
    fever = alerts['alert'][alerts['alert'].str.contains('FEVER')].count()
    hyperglycemia = alerts['alert'][alerts['alert'].str.contains('HYPERGLYCEMIA')].count()
    tachycardia = alerts['alert'][alerts['alert'].str.contains('TACHYCARDIA')].count()

    return hypertension,hypothermia, hyperthermia, fever, hyperglycemia, tachycardia


# -- This filters the table for ALERTS
def create_alert_table(df):

    df = df[df['alert'].notna()]
    # keep only the columns we need
    df = df[['timestamp','name', 'phone', 'alert', 'latitude', 'longitude']]

    return df


# -- This creates the alert graph for dash on the dashboard
def create_alert_graph(df):
    """
    Create Dash datatable from Pandas DataFrame.
    """

    df = create_alert_table(df)

    df = df.sort_values('timestamp', ascending=False)
    df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')

    table = dash_table.DataTable(
        id='alert-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        sort_action="native",
        sort_mode='single',
        page_size=20
    )
    return table


# -- Functions to generate the Dropdown Pie Chart Data -- #
def get_bmi_segment(df):
    """

    :param df:
    :return:
    """

    # filter the dataframe to just names and bmi
    bmis = df[['name','bmi']]

    # create a list of our conditions
    conditions = [
        (bmis['bmi'] < 18.5),
        (bmis['bmi'] > 18.5) & (bmis['bmi'] <= 25),
        (bmis['bmi'] > 25) & (bmis['bmi'] <= 30),
        (bmis['bmi'] > 30) & (bmis['bmi'] <= 35),
        (bmis['bmi'] > 35)
        ]

    # create a list of the values we want to assign for each condition
    values = ['Underweight 18', 'Normal', 'Overweight', 'Obese','Extremely Obese']

    # create a new column and use np.select to assign values to it using our lists as arguments
    bmis['bmi_segment'] = np.select(conditions, values)

    #Group the age segment by unique names (as each patient has more than one record) to count the age segments
    bmi_segments = bmis.groupby('bmi_segment')['name'].nunique()

    return bmi_segments


def get_existing_segments(df, segment):
    """

    :param df:
    :param segment: string (age, status, condition, bmi, gender)
    :return:
    """

    # filter the dataframe to just names and ages
    df2 = df[['name', segment]]

    #Group the age segment by unique names (as each patient has more than one record) to count the specific segments
    series = df2.groupby(segment)['name'].nunique()

    return series


def get_age_segment(df):
    """

    :param df:
    :return:
    """

    # filter the dataframe to just names and ages
    ages = df[['name','age']]


    # create a list of our conditions
    conditions = [
        (ages['age'] < 18), #1
        (ages['age'] >= 18) & (ages['age'] <= 39), #2
        (ages['age'] >= 40) & (ages['age'] <= 49),
        (ages['age'] >= 50) & (ages['age'] <= 59),
        (ages['age'] >= 60) & (ages['age'] <= 69),
        (ages['age'] >= 70) & (ages['age'] <= 79),
        (ages['age'] >= 80)
        ]

    # create a list of the values we want to assign for each condition
    values = ['Below 18', #1
              '18 to 39', #2
              '40 to 49', '50 to 59','60 to 69','70 to 79','Over 80']

    # create a new column and use np.select to assign values to it using our lists as arguments
    ages['age_segment'] = np.select(conditions, values)
    print(ages)
    #Group the age segment by unique names (as each patient has more than one record) to count the age segments
    age_segments = ages.groupby('age_segment')['name'].nunique()

    return age_segments


def get_postcode_segment(df):

    df = df[['name', 'address']]
    df = pd.concat([df[["name"]], df["address"].str.split(',', expand=True)], axis=1)
    df = df[["name", 1]]
    df.columns = ['name', 'postcode']

    #Group the age segment by unique names (as each patient has more than one record) to count the specific segments
    series = df.groupby('postcode')['name'].nunique()

    return series


def filter_dataframe(df, disease, status, age, gender,
                     bmi, temperature, heartrate, bloodsugar, systolic, diastolic):

    filtered_data = df[
        (df["condition"].isin(disease)) # Filter by diseases/conditions
        & (df["status"].isin(status)) # Filter by status
        & (df["gender"].isin(gender)) # Filter by gender
        & (df["age"] >= age[0]) & (df["age"] <= age[1]) # Filter between ages
        & (df["bmi"] >= bmi[0]) & (df["age"] <= bmi[1]) # Filter by BMI
        # Filter between heart rate
        & (df["heart_rate"] >= heartrate[0]) & (df["heart_rate"] <= heartrate[1])
        # Filter between body temperature
        & (df["body_temperature"] >= temperature[0]) & (df["body_temperature"] <= temperature[1])
        # Filter between blood sugar
        & (df["blood_sugar_level"] >= bloodsugar[0]) & (df["blood_sugar_level"] <= bloodsugar[1])
        # Filter between blood pressure top (systolic)
        & (df["blood_pressure_top"] >= systolic[0]) & (df["blood_pressure_top"] <= systolic[1])
        # Filter between blood pressure bottom (diastolic)
        & (df["blood_pressure_bottom"] >= diastolic[0]) & (df["blood_pressure_bottom"] <= diastolic[1])
        ]

    # keep only the columns we need
    filtered_data = filtered_data[['name', 'condition','reading_id',
          'heart_rate', 'blood_pressure_top', 'blood_pressure_bottom', 'body_temperature',
          'blood_sugar_level', 'timestamp', 'longitude', 'latitude']]

    return filtered_data


def produce_health_stats(df,name):

    try:
        df["name"] == name
    except:
        return None, None, None, None

    index = list(df.index.values)
    heart_rate = df.loc[df['name'] == name]["heart_rate"].tolist()
    body_temperature = df.loc[df['name'] == name]["body_temperature"].tolist()
    blood_sugar = df.loc[df['name'] == name]["blood_sugar_level"].tolist()
    timestamp = df.loc[df['name'] == name]["timestamp"].tolist()

    return index, timestamp, heart_rate, body_temperature, blood_sugar


def produce_blood_pressure(df,name):

    try:
        df["name"] == name
    except:
        return None, None, None, None

    index = list(df.index.values)
    blood_pressure_top = df.loc[df['name'] == name]["blood_pressure_top"].tolist()
    blood_pressure_bottom = df.loc[df['name'] == name]["blood_pressure_bottom"].tolist()
    timestamp = df.loc[df['name'] == name]["timestamp"].tolist()

    return index, timestamp, blood_pressure_top, blood_pressure_bottom