# import packages to use
import csv
import uuid
import datetime
import time
from faker import Faker
from random import randint, uniform, choice

# Device type (this is a dictionary of key/value pairs)
# variables


#Configuration

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
              'latitude',
              'alert']

patient_count = 100
fake = Faker() #

def create_unique_id():
    """
    This function creates a hexadecimal UUID (Unique ID) for each reading
    that can be used as primary key for database
    :return: reading_id
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
        heart_rate = randint(40, 300)
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
        blood_pressure_top = randint(100, 220)
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
        blood_pressure_bottom = randint(50, 140)
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
        body_temperature = round(uniform(35.0, 41.9), 2)
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
        blood_sugar_level = randint(35, 400)
    else:
        # else blood sugar level is normal range
        blood_sugar_level = randint(35, 199)

    return blood_sugar_level

def create_phone_number():
    country_code = "+353"
    prefix = ["-81", "-82", "-88", "-84"]
    digits = ""
    for i in range(7):
        digit = randint(0, 9)
        digits += str(digit)

    phone_number = country_code + choice(prefix) + "-" + digits

    return phone_number

def create_geolocation(coordinate_type):
    """
    This function create latitiude and longitude coordinates for Dublin Area
    eg 53.406750, -6.238861
    :return: latitude and longitude
    """
    if coordinate_type == "latitude":
        coordinate = round(uniform(53.40, 53.20), 6)
    if coordinate_type == "longitude":
        coordinate = round(uniform(-6.44, -6.20), 6)

    return coordinate


def create_time_of_measurement():
    """
    This function creates a timestamp of the current time using ISO format
    eg. 2021-06-25T15:24:17
    :return: time_of_measurement
    """

    list_timestamps = []

    currentTime = int(round(time.time()))
    yesterdayTime = currentTime - (24 * 60 * 60)

    for timestamp in range(yesterdayTime, currentTime):
        if timestamp % 60 == 0:
            converted_timestamp = datetime.datetime.utcfromtimestamp(timestamp)
            list_timestamps.append(converted_timestamp)

    return list_timestamps


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

    if condition == 'none':
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

    #pick gender
    gender = choice(['Male', 'Female'])
    if gender == "Male":
        name = fake.name_male()
    else:
        name = fake.name_female()

    patient_payload = {
        fieldnames[0]: fake.unique.random_int(min=1, max=patient_count),
        fieldnames[1]: name,
        fieldnames[2]: randint(18, 70),
        fieldnames[3]: gender,
        fieldnames[4]: create_phone_number(),
        fieldnames[5]: create_dublin_address(),
        fieldnames[6]: health[0],
        fieldnames[7]: health[1],
        fieldnames[8]: health[2],
        fieldnames[9]: create_device_id(),
    }
    # this will return as dictionary
    return patient_payload


def create_sensor_content(timestamp):
    """
    This function creates the sensor payload content by calling all the functions to
    generate the data eg - body temperature, heart_reate etc
    :return: payload (dictionary of keys: values)
    """

    sensor_payload = {
        fieldnames[10]: create_unique_id(),
        fieldnames[11]: create_heart_rate(emergency=True),
        fieldnames[12]: create_blood_pressure_top(emergency=True),
        fieldnames[13]: create_blood_pressure_bottom(emergency=True),
        fieldnames[14]: create_body_temperature(emergency=True),
        fieldnames[15]: create_blood_sugar_level(emergency=True),
        fieldnames[16]: timestamp,
        fieldnames[17]: create_geolocation("longitude"),
        fieldnames[18]: create_geolocation("latitude"),
    }
    # this will return as dictionary
    return sensor_payload


def create_emergency_alerts(patient_payload, sensor_payload):

    # Get the values from the patient payload already generated
    age = patient_payload.get(fieldnames[2])
    condition = patient_payload.get(fieldnames[6])
    bmi = patient_payload.get(fieldnames[7])
    status = patient_payload.get(fieldnames[8])

    # Get the values from the sensor payload already generated
    heart_rate = sensor_payload.get(fieldnames[11])
    bp_top = sensor_payload.get(fieldnames[12])
    bp_bottom = sensor_payload.get(fieldnames[13])
    body_temp = sensor_payload.get(fieldnames[14])
    blood_sugar = sensor_payload.get(fieldnames[15])
    message = "" # set empty as default

    # condition 1
    if condition == "hypertension" and status == 'critical unhealthy' and bp_top > 160 and bp_bottom > 110:
        message = "EMERGENCY! VERY HIGH BP DETECTED: "+ \
                  "{0} patient with ({1}) has blood pressure {2}\{3}".format(status, condition, bp_top, bp_bottom),
    # Condition 2
    if body_temp < 35:
        message = "EMERGENCY! HYPOTHERMIA DETECTED: " + \
                  "Patient has body temperature of {0} celcius".format(body_temp)

    # Condition 3
    if body_temp > 40:
        message = "EMERGENCY! HYPERTHERMIA DETECTED: " + \
                  "Patient has body temperature of {0} celcius".format(body_temp)

    # Condition 4
    if age > 70 and condition != "stable healthy" and body_temp > 39:
        message = "WARNING! FEVER DETECTED: " + \
        "Patient aged {0} with condition {1} has body temperature of {2} celcius".format(age, condition, body_temp)

    # Condition 5
    if blood_sugar > 300 and condition == "diabetes":
        message = "EMERGENCY! HYPERGLEACIMIA DETECTED: " + \
                  "Patient with {0} has blood sugar level of {1} mg/dl".format(condition, blood_sugar)

    # Condition 6
    if heart_rate > 200 and bmi > 30:
        message = "WARNING! HIGH HEART RATE DETECTED: " + \
        "Patient with BMI {0} with condition {1} has heart rate of {2} BPM".format(bmi, condition, heart_rate)

    alert_payload = {fieldnames[19]: message}

    return alert_payload



def write_to_csv():
    """
    This function writes a payload to csv file to view if information is correct
    :return: writes csv file to hard drive
    """

    # the ./ means that the code will be stored in the same folder that we are running
    csv_file = "./healthcare_data.csv"
    timestamps = create_time_of_measurement()
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
            print("Generating Patient Data for {0} patients".format(patient_count))
            for i in range(patient_count):
                # create 50 patients
                patient = create_patient_content()
                for timestamp in timestamps:
                    # create the payload/sensor content
                    sensor = create_sensor_content(timestamp)
                    emergency = create_emergency_alerts(patient,sensor)
                    # join the patient data to the sensor & alert data
                    records = {**patient, **sensor, **emergency}
                    # write the payload/content to the csv file
                    writer.writerow(records)
    except IOError:
        print("I/O error")


# This is the main method
if __name__ == '__main__':
    # call the function to write to csv
    write_to_csv()