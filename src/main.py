# import packages to use
import csv
import uuid
import datetime
import time
from faker import Faker
from random import randint, uniform, choice

# Device type (this is a dictionary of key/value pairs)
# variables


fieldnames = ['id',
              'name',
              'age',
              'gender',
              'phone',
              'address',
              'condition',
              'bmi',
              'status',
              'device_id',
              'reading_id',
              'heart_rate',
              'blood_pressure_top',
              'blood_pressure_bottom',
              'body_temperature',
              'blood_sugar_level',
              'timestamp',
              'longitude',
              'latitude']

PATIENT_COUNT = 25
SENSOR_COUNT = 100
fake = Faker(['en-IE']) # Use Ireland Locale


def create_unique_id():
    """
    This function creates a hexadecimal UUID (Unique ID) for each reading
    that can be used as primary key for database
    : return: reading_id
    """
    reading_id = ''.join(uuid.uuid4().hex)
    return reading_id


def create_device_id():

    devices = ["SMARTWATCH1-", "SMARTWATCH2-", "SMARTWATCH3-"]

    device = choice(devices)
    id = create_unique_id()
    device_id = device + id
    return device_id


def create_heart_rate(emergency=False):
    """
    This function creates a random integer between 40 & 220 for the heartrate
    eg. 100
    :return: heart_rate
    """
    if emergency is True:
        heart_rate = randint(220, 300)
    else:
        heart_rate = randint(40, 219)

    return heart_rate


def create_blood_pressure_top(emergency=False):
    """
    This function creates a random integer between 100 & 180 for the blood pressure top
    eg. 175
    :return: blood_pressure_top
    """
    if emergency is True:
        blood_pressure_top = randint(180, 220)
    else:
        blood_pressure_top = randint(100, 179)

    return blood_pressure_top


def create_blood_pressure_bottom(emergency=False):
    """
    This function creates a random integer between 50 & 100 for the blood pressure bottom
    eg. 88
    :return: blood_pressure_bottom
    """
    if emergency is True:
         blood_pressure_bottom = randint(120, 140)
    else:
        blood_pressure_bottom = randint(50, 119)

    return blood_pressure_bottom


def create_body_temperature(emergency=False):
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


def create_blood_sugar_level(emergency=False):
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

def create_geolocation(coordinate_type):
    """
    This function create latitiude and longitude coordinates for Dublin Area
    eg 53.406750, -6.238861
    :return: latitude and longitude
    """
    if coordinate_type is "latitude":
        coordinate = round(uniform(53.40, 53.20), 6)
    if coordinate_type is "longitude":
        coordinate = round(uniform(-6.44, -6.20), 6)

    return coordinate


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
    #timestamp = dt.isoformat()

    return dt

def create_dublin_address():
    """

    :return:
    """
    postcodes = ['Dublin 1','Dublin 2', 'Dublin 3', 'Dublin 4', 'Dublin 5', 'Dublin 6',
                'Dublin 7','Dublin 8', 'Dublin 9', 'Dublin 10', 'Dublin 11', 'Dublin 12',
                'Dublin 13', 'Dublin 14', 'Dublin 15', 'Dublin 16', 'Dublin 17', 'Dublin 18',
                'Dublin 19', 'Dublin 20', 'Dublin 21', 'Dublin 22', 'Dublin 23', 'Dublin 24']

    street_address = fake.street_address()
    postcode = choice(postcodes) # Randomly chose one post code

    full_address = street_address + "," + postcode + ", Dublin, Republic of Ireland"

    return full_address


def create_health_status():
    """
    Function to create condition, health_status and BMI
    :return: list of condition, health_status, BMI
    """
    bmi = round(uniform(18.5, 40.5), 2)
    conditions = ['diabetes', 'hypertension', 'heart_disease', 'none']
    statuses = ['critical unhealthy', 'stable unhealthy', 'stable healthy']

    #Choose Random condition & status
    condition = choice(conditions)
    status = choice(statuses)

    if condition is 'none':
        if bmi < 30.0:
            status = 'stable healthy'
        else:
            status = 'stable unhealthy'

    else:
        if bmi < 30.0:
            status = 'stable unhealthy'
        else:
            status = 'critical unhealthy'


    patient_health = [condition, bmi, status]
    return patient_health


def create_patient_content():
    """

    :return:
    """
    health = create_health_status()
    gender = ['Male', 'Female']
    payload = {
        fieldnames[0]: fake.unique.random_int(min=1, max=PATIENT_COUNT),
        fieldnames[1]: fake.name(),
        fieldnames[2]: randint(18, 70),
        #TODO:add Email
        # fieldnames[3]: fake.email(),
        fieldnames[3]: choice(gender),
        fieldnames[4]: fake.phone_number(),
        fieldnames[5]: create_dublin_address(),
        fieldnames[6]: health[0],
        fieldnames[7]: health[1],
        fieldnames[8]: health[2],
        fieldnames[9]: create_device_id(),
    }
    # this will return as dictionary
    return payload


def create_sensor_content():
    """
    This function creates the sensor payload content by calling all the functions to
    generate the data eg - body temperature, heart_reate etc
    :return: payload (dictionary of keys: values)
    """
    payload = {
        fieldnames[10]: create_unique_id(),
        fieldnames[11]: create_heart_rate(emergency=False),
        fieldnames[12]: create_blood_pressure_top(emergency=False),
        fieldnames[13]: create_blood_pressure_bottom(emergency=False),
        fieldnames[14]: create_body_temperature(emergency=False),
        fieldnames[15]: create_blood_sugar_level(emergency=False),
        fieldnames[16]: create_time_of_measurement(),
        fieldnames[17]: create_geolocation("longitude"),
        fieldnames[18]: create_geolocation("latitude"),
    }
    # this will return as dictionary
    return payload



def write_to_csv():
    """
    This function writes a payload to csv file to view if information is correct
    :return: writes csv file to hard drive
    """

    # the ./ means that the code will be stored in the same folder that we are running
    csv_file = "../input/data.csv"

    # error checking
    try:
        print("Generating Healthcare Data")
        # create a new csv file using csv_file variable
        # open means new csv file
        # w means write
        with open(csv_file, 'w') as csvfile:
            # use the csv file that were generated
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # write the header/column names in csv file
            writer.writeheader()
            print("Generating Patient Data for {0} patients".format(PATIENT_COUNT))
            for i in range(PATIENT_COUNT):
                # create 50 patients
                patient = create_patient_content()
                print("Generating {0} Sensor Records for patient id {1}".format(SENSOR_COUNT, patient["id"]))
                for j in range(SENSOR_COUNT):
                    # create the payload/sensor content
                    sensor = create_sensor_content()
                    # join the patient data
                    records = {**patient, **sensor}
                    # write the payload/content to the csv file
                    writer.writerow(records)
    except IOError:
        print("I/O error")


# This is the main method
if __name__ == '__main__':
    # call the function to write to csv
    write_to_csv()
