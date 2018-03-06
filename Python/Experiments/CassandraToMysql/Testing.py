import mysql.connector

cnx = mysql.connector.connect(user='lambda', password='LAMBDA@112358',
                              host='sensedb.cenacuetgbbz.us-east-1.rds.amazonaws.com',
                              database='sense')
cursor = cnx.cursor()

query = ("SELECT * from sensor")
cursor.execute(query)

for values in cursor:
    print(values)

cnx.close()