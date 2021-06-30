# import packages to use
import csv
import uuid
import datetime
import time
from random import randint, uniform

# Device type (this is a dictionary of key/value pairs)
# variables
devices = {"type_1": "SMARTWATCH1",
           "type_2": "SMARTWATCH2",
           "type_3": "SMARTWATCH3"}


# function to use to create diferent values
def get_patient_db():
    pass


# to create a unique id
def create_unique_id():
    """
    This function creates a hexadecimal UUID (Unique ID) for each reading
    that can be used as primary key for database
    :return: reading_id
    """
    reading_id = ''.join(uuid.uuid4().hex)
    return reading_id


def create_heart_rate():
    """
    This function creates a random integer between 40 & 220 for the heartrate
    eg. 100
    :return: heart_rate
    """
    heart_rate = randint(40, 220)
    return heart_rate


def create_blood_pressure_top():
    """
    This function creates a random integer between 100 & 180 for the blood pressure top
    eg. 175
    :return: blood_pressure_top
    """
    blood_pressure_top = randint(100, 180)
    return blood_pressure_top


def create_blood_pressure_bottom():
    """
    This function creates a random integer between 50 & 100 for the blood pressure bottom
    eg. 88
    :return: blood_pressure_bottom
    """
    blood_pressure_bottom = randint(50, 100)
    return blood_pressure_bottom


def create_body_temperature(emergency=True):
    """
    This function creates a random decimal between 34.0 & 41.9 for the body temperature
    if emergency is True, generate above 39.4. Default value for emergency is False
    :return: blood_pressure_bottom
    """
    if emergency is True:
        # to generate an emergency body temperature
        #  2 means that is just two decimal numbers
        body_temperature = round(uniform(39.4, 41.9), 2)
    else:
        # else body temperature is normal range
        body_temperature = round(uniform(35.0, 39.3), 2)

    return body_temperature


def create_blood_sugar_level(emergency=True):
    """
    This function creates a random integer between 35 & 400 for the blood sugar levels
    if emergency is True, generate above 200. Default value for emergency is False
    :return: blood_sugar_level
    """

    if emergency is True:
        # to generate an emergency blood sugar level
        blood_sugar_level = randint(200, 400)
    else:
        # else blood sugar level is normal range
        blood_sugar_level = randint(35, 199)

    return blood_sugar_level


def create_time_of_measurement():
    """
    This function creates a timestamp of the current time using ISO format
    eg. 2021-06-25T15:24:17
    :return: time_of_measurement
    """
    # Returns the current Unix System Time from Computer eg. 1624635237
    unix_time = int(round(time.time()))

    # Convert the unix time to UTC format timestamp eg. 2021-06-25 15:33:57
    dt = datetime.datetime.utcfromtimestamp(unix_time)

    # Convert the UTC format to ISO format eg. 2021-06-25T15:33:57
    time_of_measurement = dt.isoformat()

    return time_of_measurement


def create_sensor_content():
    """
    This function creates the sensor payload content by calling all the functions to
    generate the data eg - body temperature, heart_reate etc
    :return: payload (dictionary of keys: values)
    """
    payload = {
        'reading_id': create_unique_id(),
        'type': devices['type_2'],  # choose SMARTWATCH1
        'heart_rate': create_heart_rate(),
        'blood_pressure_top': create_blood_pressure_top(),
        'blood_pressure_bottom': create_blood_pressure_bottom(),
        'body_temperature': create_body_temperature(emergency=True),
        'blood_sugar_level': create_blood_sugar_level(emergency=True),
        'time_of_measurement': create_time_of_measurement()
    }
    # this will return as dictionary
    return payload


def write_to_csv():
    """
    This function writes a payload to csv file to view if information is correct
    :return: writes csv file to hard drive
    """
    # this fucntion will create the csv columns
    csv_columns = ['reading_id', 'type', 'content', 'heart_rate',
                   'blood_pressure_top',
                   'blood_pressure_bottom',
                   'body_temperature',
                   'blood_sugar_level',
                   'time_of_measurement']
    # the ./ means that the code will be stored in the same folder that we are running
    csv_file = "./generator_device.csv"

    # error checking
    try:
        print("Generating Sensor Data")
        # create a new csv file using csv_file variable
        # open means new csv file
        # w means write
        with open(csv_file, 'w') as csvfile:
            # use the csv file that were generated
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            # write the header/column names in csv file
            writer.writeheader()
            # generate for 100 records
            for i in range(1000):
                # create the payload/sensor content
                payload = create_sensor_content()
                # write the payload/content to the csv file
                writer.writerow(payload)
    except IOError:
        print("I/O error")


# This is the main method
if __name__ == '__main__':
    # call the function to write to csv
    write_to_csv()
