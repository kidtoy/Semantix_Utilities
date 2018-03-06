# macList = ["D4:6E:0E:4F:28:A0","D4:6E:0E:4F:2F:CE", "84:16:F9:AC:4C:E6","84:16:F9:AC:4D:0E","D4:6E:0E:4F:51:40"] # Semantix
# macList = ['D4:6E:0E:4F:2F:CE','84:16:F9:AC:49:D0','D4:6E:0E:4F:28:A0','84:16:F9:AC:4D:78']
# macList = ["18:D6:C7:43:51:A6","60:E3:27:93:33:30","98:DE:D0:DB:D3:BE","98:DE:D0:DB:BE:F8","18:D6:C7:43:29:7C"] # Bradesco
# macList = ['18:D6:C7:43:26:48','18:D6:C7:43:29:4C','98:DE:D0:DB:C0:8E','98:DE:D0:90:BD:D2','98:DE:D0:DB:C1:74']



# macList = ['98:DE:D0:DB:D3:BE','60:E3:27:93:33:30','18:D6:C7:43:29:7C']
# macList = [ 'D4:6E:0E:4F:28:A0','D4:6E:0E:4F:56:00']

# macList = {
#     "18:D6:C7:43:4A:94" : "Lab Semantix Realtime 1",
#     "60:E3:27:93:35:76" : "Lab Sematnix Realtime 2",
#     "84:16:F9:AC:4D:78" : "Lab Semantix Realtime 3",
#     "84:16:F9:AC:4C:E6" : "Lab Semantix Realtime 4"
#     # "D4:6E:0E:4F:2F:CE" : "Gabi s Memento",
#     # "18:D6:C7:43:26:48" : "Kenji s Memento",
#     # "84:16:F9:AC:4C:E6" : "Meeting s Memento",
#     # "60:E3:27:93:33:30" : "Bruno s Memento"
# }

# macList = {
# "18:A6:F7:AF:4D:54" : "Baia Fundo",
# "84:16:F9:AC:4A:06" : "Baia Centro",
# "98:DE:D0:DB:C7:86" : "Baia Entrada	",
# "98:DE:D0:DB:CC:CE" : "Entrada - Seguranca",
# "60:E3:27:93:35:7E" : "TVs"
# }

macList={
"84:16:F9:AC:51:34" : "Reuniao Quarto",
    "98:DE:D0:DB:C4:48" : "Entrada Terceiro",
    "18:D6:C7:43:4A:94" : "Mesa Kenji",
    "98:DE:D0:A0:61:2A" : "Mesa Gabriel",
    "18:D6:C7:43:26:48" : "Reuniao Terceiro"

}

# macList = {
#     "D4:6E:0E:4F:56:00" : "Claro Teste 1",
#     "98:DE:D0:DB:D3:BE" : "Claro Teste 2",
#     "84:16:F9:AC:52:4C" : "Claro Teste 3",
#     "D4:6E:0E:4F:28:A0" : "Claro Teste 4",
#     "60:E3:27:93:33:30" : "Claro Teste 5"
# }

keyspace = "semantix"
# keyspace = "claro"
# keyspace = "bradesco"
# keyspace = "dds"
# keyspace = "pernambucanas"

latitude = "-23.57736" # Semantix
longitude = "-46.64627"

# latitude = "-23.57736" # Claro
# longitude = "-46.64194"

# latitude = "-23.72314" #Pernambucanas
# longitude = "-46.54293"
#
datetime = "2017-09-19 12:00:00"
id_campaign = "1"
name_campaign = "Semantix Teaser"
model = "Pendriveless"
origin_date = "2017-09-19 12:00:00"
version = "1"

for mac in macList.items():

    print "insert into "+keyspace+".sensor (id_sensor, date_time, date_time_update, id_campaign, latitude, longitude, name, name_campaign) VALUES ('"+mac[0]+"', '"+datetime+"', '"+datetime+"', "+id_campaign+", "+latitude+", "+longitude+", '"+mac[1]+"', '"+name_campaign+"');"

    print "UPDATE zubat.sensor set company = '"+keyspace+"', last_update = '"+datetime+"', model = '"+model+"', origin_date = '"+origin_date+"', version = "+version+" where id_sensor = '"+mac[0]+"';"


    # print "insert into "+keyspace+".sensor (id_sensor, date_time, date_time_update, id_campaign, latitude, longitude, name, name_campaign) VALUES ('"+mac(0)+"', '"+datetime+"', '"+datetime+"', "+id_campaign+", "+latitude+", "+longitude+", '"+mac(1)+"', '"+name_campaign+"');"
    # print "insert into zubat.sensor (id_sensor, company, last_update, model, origin_date, version) VALUES ('"+mac+"', '"+keyspace+"', '"+datetime+"', 'wifi', '"+datetime+"', 8);"