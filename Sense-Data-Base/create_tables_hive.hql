## Prod table
CREATE EXTERNAL TABLE $KEYSPACE.prod_measurement(date_time timestamp,id_campaign int, vendor String, mac_address String, distance tinyint,date_time_record timestamp, rssi int, ssid String)
PARTITIONED BY (id_sensor String)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS PARQUET

## Stager table (Prod table have de partitioned columns)
CREATE EXTERNAL TABLE $KEYSPACE.raw_measurement(id_sensor String, date_time timestamp,id_campaign int, vendor String, mac_address String, distance tinyint,date_time_record timestamp, rssi int, ssid String)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS PARQUET

## Analytics Table
CREATE EXTERNAL TABLE $KEYSPACE.analytics(
id_deploy int,
date_time timestamp,
metric string,
key string,
value float)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS PARQUET

## Formatted_measurement_prod
CREATE EXTERNAL TABLE $KEYSPACE.formatted_measurement_prod(
id_deploy int,
id_visit long,
date_time_start timestamp,
permanency int,
visit_value tinyint,
mac_address string)
ROW FORMAT DELIMITED
FIELDS TERMIATED BY ','
STORED AS PARQUET

## Visit_data
CREATE EXTERNAL TABLE $KEYSPACE.visit_data(
id_visit long,
id_sensor string,
frequency int)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS PARQUET
