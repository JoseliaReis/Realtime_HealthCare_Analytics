# import packages
import csv
from faker import Faker
from random import randint
import random
import decimal



# define the number os patients
RECORD_COUNT = 50
# define the patient condition
Condition = ["diabetes","hypertension","heart disease","none"]
# create the faker
fake = Faker()

# function to create the csv file with patient information created by faker
def create_csv_file():
    # create the columns
    with open('./generator_patient.csv', 'w', newline='') as csvfile:
        fieldnames = ['ID',
                      'Name',
                      'Age',
                      'Condition',
                      'BMI',
                      'E-mail',
                      'Phone',
                      'Address'
                      ]
        # write to the csv
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #generate the data
        writer.writeheader()
        for i in range(RECORD_COUNT):
            writer.writerow(
                {
                    'ID': fake.unique.random_int(min=1, max=50),
                    'Name': fake.name(),
                    'Age': randint(18, 90),
                    'Condition': random.choice(Condition),
                    'BMI': random.randint(1855, 3000)/100,
                    'E-mail': fake.email(),
                    'Phone': fake.phone_number(),
                    'Address': fake.address(),


                }
            )

# This is the main method
if __name__ == '__main__':
    # call the function to write to csv
    create_csv_file()
    print('Generating Sensor Data')
