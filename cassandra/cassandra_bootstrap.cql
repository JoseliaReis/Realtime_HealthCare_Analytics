# connect to cassandra via cqlsh
cqlsh localhost 9042 --cqlversion 3.4.4

# create keyspace
CREATE KEYSPACE IF NOT EXISTS heathcare_db
WITH REPLICATION = {
  'class': 'SimpleStrategy',
  'replication_factor': '3'
};

# Use Keyspace
use heathcare_db;

# Create content immutable set
CREATE type heathcare_db.device_readings(
  reading_ID TEXT,
  heart_rate INT,
  blood_pressure_top INT,
  blood_pressure_bottom INT,
  body_temperature DECIMAL,
  timestamp BIGINT ,
  longitude TEXT,
  latitude TEXT
);




# create table
CREATE TABLE IF NOT EXISTS heathcare_db.device_patient(
  patient_id TEXT,
  name TEXT,
  age INT,
  email TEXT,
  phone TEXT,
  address TEXT,
  condition TEXT,
  bmi DECIMAL,
  status TEXT,
  device_id TEXT, 
  content MAP<text,FROZEN<device_readings>>,
  PRIMARY KEY(patient_id)
);
