CREATE TABLE IF NOT EXISTS healthcare_db.device_patient (
	patient_id text PRIMARY KEY,
	address text,
	age int,
	alert text,
	blood_pressure_bottom int,
	blood_pressure_top int,
	blood_sugar_level int,
	bmi decimal,
	body_temperature decimal,
	condition text,
	device_id text,
	gender text,
	heart_rate int,
	latitude text,
	longitude text,
	name text,
	phone text,
	reading_id text,
	status text,
	timestamp bigint)
	WITH ID = c7467e30-f939-11eb-9cbc-d7ee8570c286
	AND bloom_filter_fp_chance = 0.01
	AND dclocal_read_repair_chance = 0.1
	AND crc_check_chance = 1.0
	AND default_time_to_live = 0
	AND gc_grace_seconds = 864000
	AND min_index_interval = 128
	AND max_index_interval = 2048
	AND memtable_flush_period_in_ms = 0
	AND read_repair_chance = 0.0
	AND speculative_retry = '99PERCENTILE'
	AND comment = ''
	AND caching = { 'keys': 'ALL', 'rows_per_partition': 'NONE' }
	AND compaction = { 'max_threshold': '32', 'min_threshold': '4', 'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy' }
	AND compression = { 'chunk_length_in_kb': '64', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor' }
	AND cdc = false
	AND extensions = {  };
