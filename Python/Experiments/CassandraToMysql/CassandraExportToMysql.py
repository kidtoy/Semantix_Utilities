import mysql.connector
from cassandra.cluster import Cluster

cluster = Cluster(
    ['34.196.59.158'],
    port=9042)
session = cluster.connect('zubat')

cnx = mysql.connector.connect(user='zubat', password='zubat#112358',
                              host='sensedb.cenacuetgbbz.us-east-1.rds.amazonaws.com',
                              database='sense2')
cursor = cnx.cursor()

insert_company_table = ("INSERT INTO company(name,type) VALUES (%s,%s) ")
insert_deploy_table = (
"INSERT INTO deploy(company_id, name,date_time_start,date_time_end,street_address,zip,city,state,internal_id) VALUES(%s,%s, %s,%s,%s,%s,%s,%s,%s) ")
insert_deploy_data_sense = (
"INSERT INTO deploy_data_sense(deploy_id, sense_time, week_days, holiday) VALUES (%s, %s, %s, %s)")
insert_sensor_table = (
"INSERT INTO sensor(id, deploy_id, register_date, last_update, model, version) VALUES (%s, %s, %s, %s, %s, %s) ")
insert_sensor_data_sense_table = ("INSERT INTO sensor_data_sense(sensor_id, name) VALUES ( %s, %s )")
insert_whitelist_table = (
"INSERT INTO whitelist_sense(mac_address, deploy_id) VALUES ( %s, %s)")
insert_whitelist_person_data_table = (
"INSERT INTO whitelist_person_data_sense(whitelist_id, keyword, content) VALUES (%s, %s, %s)")

companies = ("BRADESCO", "SEMANTIX", "PERNAMBUCANAS")
companies_data = {
    "BRADESCO": {"type": "BANK"},
    "PERNAMBUCANAS": {"type": "STORE"},
    "SEMANTIX": {"type": "OFFICE"}
}


def company_table():
    for x in companies:
        cursor.execute(insert_company_table, (x, companies_data[x]['type']))
        companies_data[x]["id"] = cursor.lastrowid


def deploy_table():
    brad = (
    companies_data["BRADESCO"]["id"], 'POC', '2017-05-12 17:00:00', '2019-05-12 17:00:00', 'CIDADE DE DEUS, DPI',
    '06029000', 'OSASCO', 'SP', '9999')
    cursor.execute(insert_deploy_table, (brad))
    companies_data["BRADESCO"]["deploy_id"] = cursor.lastrowid
    brad_data = (companies_data["BRADESCO"]["deploy_id"], '09:00-18:00', '1,2,3,4,5,6,7', 'false')
    cursor.execute(insert_deploy_data_sense, (brad_data))

    pern = (companies_data["PERNAMBUCANAS"]["id"], 'LOJA MODELO', '2017-02-01 12:00:00', '2019-02-01 12:00:00',
            'AV. ROTARY, 624 - SAO BERNARDO PLAZA SHOPPING - PISO L2', '09721000', 'SAO BERNARDO DO CAMPO', 'SP', '527')
    cursor.execute(insert_deploy_table, (pern))
    companies_data["PERNAMBUCANAS"]["deploy_id"] = cursor.lastrowid
    pern_data = (companies_data["PERNAMBUCANAS"]["deploy_id"], '10:00-22:00', '1,2,3,4,5,6,7', 'true')
    cursor.execute(insert_deploy_data_sense, (pern_data))

    sem = (companies_data["SEMANTIX"]["id"], 'SEMANTIX TEASER', '2019-11-30 21:00:00', '2019-11-30 21:00:00',
           'RUA ESTELA, 96 - TERCEIRO/QUARTO ANDAR', '04011000', 'SAO PAULO', 'SP', '3F')
    cursor.execute(insert_deploy_table, (sem))
    companies_data["SEMANTIX"]["deploy_id"] = cursor.lastrowid
    sem_data = (companies_data["SEMANTIX"]["deploy_id"], '06:00-22:00', '2,3,4,5,6', 'false')
    cursor.execute(insert_deploy_data_sense, (sem_data))


def sensor_table():
    sensor_map = create_sensor_map()
    rows = session.execute('select * from zubat.sensor')
    for row in rows:
        if row.id_sensor.upper() in sensor_map:
            data = (
            row.id_sensor.upper(), companies_data[row.company.upper()]["deploy_id"], str(row.origin_date.date()),
            str(row.last_update.date()), row.model.upper(), str(row.version))
            cursor.execute(insert_sensor_table, data)

            sensor_data = (row.id_sensor.upper(), sensor_map[row.id_sensor.upper()])
            cursor.execute(insert_sensor_data_sense_table, sensor_data)


def create_sensor_map():
    sensor_map = {}
    for company in companies:
        sensors_names = session.execute(' select * from ' + company + '.sensor')
        for line in sensors_names:
            sensor_map[line.id_sensor.upper()] = line.name
    return sensor_map


def whitelist_table():
    for company in companies:
        rows = session.execute('select * from ' + company + '.whitelist allow filtering')
        for row in rows:
            if len(row.mac_address) == 17:
                data = (row.mac_address.upper(), companies_data[company]['deploy_id'])
                cursor.execute(insert_whitelist_table, data)
                lastid = cursor.lastrowid

                data2 = (lastid, "PERSON", row.person)
                cursor.execute(insert_whitelist_person_data_table, data2)

                data3 = (lastid, "SCORE", str(row.score))
                cursor.execute(insert_whitelist_person_data_table, data3)

                data4 = (lastid, "SENTIMENT", row.sentiment.upper())
                cursor.execute(insert_whitelist_person_data_table, data4)


company_table()
deploy_table()
sensor_table()
whitelist_table()
cnx.commit()
cursor.close()
cnx.close()