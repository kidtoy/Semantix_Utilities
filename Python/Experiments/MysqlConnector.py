import mysql.connector

cnx = mysql.connector.connect(user="crawlerhomo.c70tjvzezo6q.us-west-1.rds.amazonaws.com:1433",

password="skJWxvVGDKxwNRUXiWc2aTwyVK2iwhwOq3yNmjiQUFaxmSksEkiD4D1NdRVxXgad7yOkIUYsnYNyGVQ96X",
                              host='54.183.189.234',
                              database='Crawler')

print cnx.connection_id
cnx.close