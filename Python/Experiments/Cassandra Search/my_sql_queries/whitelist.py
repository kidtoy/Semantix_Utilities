import datetime
from cassandra.cluster import Cluster


size = "1"
cluster = Cluster(
    ['34.196.59.158'],
    port=9042)

session = cluster.connect('zubat')
# companies = session.execute('select distinct company from zubat.sensor allow filtering')
companies = ['BRADESCO','PERNAMBUCANAS','SEMANTIX']
for company in companies:
    rows = session.execute('select * from '+company+'.whitelist allow filtering')
    for row in rows:
        if len(row.mac_address) == 17:
            print("INSERT INTO whitelist_sense(mac_address, deploy_id) SELECT '"+row.mac_address.upper()+"', deploy.id FROM deploy join company on deploy.company_id = company.id where company.name = '"+company+"'; ")
            print("INSERT INTO whitelist_person_data_sense(whitelist_id, keyword, content) SELECT whitelist_sense.id, 'NAME', '"+row.person+"' from whitelist_sense join (SELECT deploy.id, company.name from deploy join company on deploy.company_id = company.id) as deploycompany on whitelist_sense.deploy_id = deploycompany.id where mac_address = '"+row.mac_address.upper()+"' and  deploycompany.name = '"+company+"';")
            print("INSERT INTO whitelist_person_data_sense(whitelist_id, keyword, content) SELECT whitelist_sense.id, 'SCORE', '" + str(row.score) + "' from whitelist_sense join (SELECT deploy.id, company.name from deploy join company on deploy.company_id = company.id) as deploycompany on whitelist_sense.deploy_id = deploycompany.id where mac_address = '" + row.mac_address.upper() + "' and  deploycompany.name = '"+company+"';")
            print("INSERT INTO whitelist_person_data_sense(whitelist_id, keyword, content) SELECT whitelist_sense.id, 'SENTIMENT', '" + row.sentiment.upper() + "' from whitelist_sense join (SELECT deploy.id, company.name from deploy join company on deploy.company_id = company.id) as deploycompany on whitelist_sense.deploy_id = deploycompany.id where mac_address = '" + row.mac_address.upper() + "' and  deploycompany.name = '"+company+"';")

