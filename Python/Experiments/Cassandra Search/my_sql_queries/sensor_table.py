import datetime
from cassandra.cluster import Cluster


size = "1"
cluster = Cluster(
    ['34.196.59.158'],
    port=9042)

session = cluster.connect('zubat')
sensor_map={}


companies = ['bradesco', 'pernambucanas', 'semantix']
for company in companies:
    sensors_names = session.execute(' select * from '+company+'.sensor')
    for line in sensors_names:
        sensor_map[line.id_sensor.upper()] = line.name



rows = session.execute('select * from zubat.sensor')

for row in rows:
    if row.id_sensor.upper() in sensor_map:
        print( "INSERT INTO sensor(id, deploy_id, register_date, last_update, model, version) SELECT '"+row.id_sensor.upper()+"', deploy.id, '"+str(row.origin_date.date())+"', '"+str(row.last_update.date())+"', '"+row.model.upper()+"', "+str(row.version)+" FROM deploy join company on deploy.company_id = company.id where company.name = '"+row.company.upper()+"'; ")
        print( "INSERT INTO sensor_data_sense(sensor_id, name) VALUES ( '"+row.id_sensor.upper()+"', '"+sensor_map[row.id_sensor.upper()]+"');")







# INSERT INTO sensor(id_sensor,id_deploy,register_date,last_update,model,version) SELECT '84:16:F9:6E:EA:4E', id_deploy, '2017-06-07', '2017-07-27', 'REALTIME', 25.0 FROM deploy join company on deploy.id_company = company.id_company where company.name = 'BRADESCO';
