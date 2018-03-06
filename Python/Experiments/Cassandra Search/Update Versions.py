import datetime
from cassandra.cluster import Cluster

# keyspace = "dds"
# keyspace = "bradesco"
# keyspace = "claro"
# keyspace = "pernambucanas"
keyspace = "semantix"

campaign = 1
date = datetime.datetime.now()
version = 1
model = "Pendriveless"


cluster = Cluster(
    ['34.196.59.158'],
    port=9042)

session = cluster.connect('zubat')
rows = session.execute('select id_sensor, name from '+keyspace+'.sensor where id_campaign = '+str(campaign)+' ALLOW FILTERING')

# rows = session.execute("select id_sensor from zubat.sensor where company = '"+str(keyspace)+"' and model = 'wifi' ALLOW FILTERING")

for row in rows.current_rows:
    print "update zubat.sensor set version = "+str(version)+" , last_update = '"+str(date)[:-3]+"', model = '"+model+"' where id_sensor = '"+row.id_sensor+"'; // "


# list = ["D4:6E:0E:4F:28:A0","84:16:F9:AC:21:54","84:16:F9:AC:52:4C","60:E3:27:93:33:30","98:DE:D0:A0:61:2A","98:DE:D0:DB:D3:BE","D4:6E:0E:4F:49:9A"]

#
# for mac in list:
#     print "update zubat.sensor set version = " + str(version) + " , last_update = '" + str(date)[:-3] + "', model = '" + model + "' where id_sensor = '" + mac + "'; // "