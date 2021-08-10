# connect to cassandra via cqlsh
cqlsh localhost 9042 --cqlversion 3.4.4

# create keyspace
CREATE KEYSPACE IF NOT EXISTS healthcare_db
WITH REPLICATION = {
  'class': 'SimpleStrategy',
  'replication_factor': '3'
};

# Use Keyspace
use healthcare_db;

# Create content immutable set
CREATE type healthcare_db.device_readings(
  reading_ID TEXT,
  heart_rate INT,
  blood_pressure_top INT,
  blood_pressure_bottom INT,
  body_temperature DECIMAL,
  timestamp BIGINT ,
  longitude TEXT,
  latitude TEXT,
  alert TEXT
);




# create table
CREATE TABLE IF NOT EXISTS healthcare_db.device_patient(
  id TEXT,
  name TEXT,
  age INT,
  gender TEXT,
  phone TEXT,
  address TEXT,
  condition TEXT,
  bmi DECIMAL,
  status TEXT,
  device_id TEXT, 
  reading_id TEXT,
  heart_rate INT,
  blood_pressure_top INT,
  blood_pressure_bottom INT,
  body_temperature DECIMAL,
  blood_sugar_level INT,
  timestamp TIMESTAMP ,
  longitude TEXT,
  latitude TEXT,
  alert TEXT,
  PRIMARY KEY (reading_id,timestamp)
);
