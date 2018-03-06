import datetime
from cassandra.cluster import Cluster
import requests

date = datetime.datetime.now()
time = date - datetime.timedelta(hours=1)
API_ENDPOINT= "https://xrxt46u84h.execute-api.us-east-1.amazonaws.com/Develop"

size = "1"
cluster = Cluster(
    ['34.196.59.158'],
    port=9042)

responseSensor= ""
keyspacesString = ""
sendMessage = False
keyspacesMap = {
"pernambucanas" : 0,
    "bradesco" : 0,
    "claro" : 0
}

session = cluster.connect('zubat')
for keyspace in keyspacesMap:
    rows = session.execute('select id_sensor, name from '+keyspace+'.sensor')

    for row in rows.current_rows:

        sensor_data = session.execute("select * from "+keyspace+".measurement where id_sensor = '"+row.id_sensor+"' and date_time > '"+str(time)[:-3]+"' order by date_time desc limit "+size)
        if sensor_data.current_rows.__len__() == 0:
            sendMessage = True
            keyspacesMap[keyspace] += 1
            # responseSensor += row.id_sensor.upper() + "(" + keyspace + ") "

    keyspacesString = keyspace.capitalize() +" "+str(keyspacesMap[keyspace])+" \\n"


print(keyspacesMap)

message = "Alguns sensores nao reportaram dados apartir das "+str(time)+" \\n As seguintes empresas possuem as quantidades descritas com sensores a quantidade de sensores que não reportaram: \\n "+ keyspacesString

data = '{"message": "'+message+'", "topic":"Falha nos sensores as '+str(date)[:-7]+'"}'

headers = {'Content-Type': 'application/json'}

r = requests.post(url = API_ENDPOINT, data = data, headers=headers)

pastebin_url = r.text
print("The pastebin URL is : %s"%pastebin_url)
