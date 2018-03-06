# macList = ["D4:6E:0E:4F:28:A0","D4:6E:0E:4F:2F:CE", "84:16:F9:AC:4C:E6","84:16:F9:AC:4D:0E","D4:6E:0E:4F:51:40"] # Semantix
# macList = ['D4:6E:0E:4F:2F:CE','84:16:F9:AC:49:D0','D4:6E:0E:4F:28:A0','84:16:F9:AC:4D:78']
# macList = ["18:D6:C7:43:51:A6","60:E3:27:93:33:30","98:DE:D0:DB:D3:BE","98:DE:D0:DB:BE:F8","18:D6:C7:43:29:7C"] # Bradesco
# macList = ['18:D6:C7:43:26:48','18:D6:C7:43:29:4C','98:DE:D0:DB:C0:8E','98:DE:D0:90:BD:D2','98:DE:D0:DB:C1:74']
# macList = ['98:DE:D0:90:BD:D2','98:DE:D0:DB:C0:8E','18:D6:C7:43:29:4C']


keyspace = "pernambucanas"
# keyspace = "semantix"
# keyspace = "claro"
# keyspace = "bradesco"
# keyspace = "dds"

# latitude = "-23.57736" # Semantix
# longitude = "-46.64627"

# latitude = "-23.57736" # Claro
# longitude = "-46.64194"

# latitude = "-23.72314" #Pernambucanas
# longitude = "-46.54293"

updatetime = "2017-06-27 07:05:00"
id_campaign = "1"
# name_campaign = "SemantixTeaser"
# name = "Green Serial Debug"

for mac in macList:

    # print "insert into "+keyspace+".sensor (id_sensor, date_time, date_time_update, id_campaign, latitude, longitude, name, name_campaign) VALUES ('"+mac+"', '"+datetime+"', '"+datetime+"', "+id_campaign+", "+latitude+", "+longitude+", '"+name+"', '"+name_campaign+"');"
    print "update zubat.sensor set last_update = '"+updatetime+"', company = '"+keyspace+"' where id_sensor = '"+mac+"';"