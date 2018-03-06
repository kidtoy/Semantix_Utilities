macList = [
    "98:DE:D0:A0:61:2A",
    "84:16:F9:AC:31:A0",
    "84:16:F9:AC:51:34",
    "84:16:F9:AC:21:54",
    "60:E3:27:93:33:30",
    "18:D6:C7:43:4A:94"
]
keyspace = "semantix"

for mac in macList:

    print "DELETE from zubat.sensor where id_sensor = '"+mac+"';"
    print "DELETE from "+keyspace+".sensor where id_sensor = '"+mac+"';"

    # print "insert into "+keyspace+".sensor (id_sensor, date_time, date_time_update, id_campaign, latitude, longitude, name, name_campaign) VALUES ('"+mac(0)+"', '"+datetime+"', '"+datetime+"', "+id_campaign+", "+latitude+", "+longitude+", '"+mac(1)+"', '"+name_campaign+"');"
    # print "insert into zubat.sensor (id_sensor, company, last_update, model, origin_date, version) VALUES ('"+mac+"', '"+keyspace+"', '"+datetime+"', 'wifi', '"+datetime+"', 8);"