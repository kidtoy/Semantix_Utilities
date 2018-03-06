# import sys
import datetime
import os
import requests
import json
import shutil
from cassandra.cluster import Cluster

#Set access keys
api_key = "?api_key=d47bb60118d94110ae2d322dc1d2049f"
headers = {'Authorization' : 'Basic ZmVsaXBlLnlvc2hpZGFAc2VtYW50aXguY29tLmJyOlNlbWFudGl4IzAx',
           "Content-Type" : "application/json"}

#Get data NUCs macs/agency from cassandra
def cassandraData(server,port):
    try:
        cluster = Cluster(
          [server],
          port=port)

        session = cluster.connect('zubat')
        values = session.execute("SELECT * from zubat.gateway")
    except Exception as e:
        return {}
    cassData = {}
    for x in values:
      cassData[x.mac_address.upper()] = [x.company, x.branch]
    print(cassData)
    return cassData


def cleanPaths():
    for the_file in os.listdir(os.path.dirname(os.path.realpath(__file__))):
        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), the_file)
        try:
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
                print(e)


def getWhitelist(server,port,company):
    try:
        cluster = Cluster(
          [server],
          port=port)

        session = cluster.connect('zubat')
        branch = session.execute("select distinct branch from "+company+".newwhitelist")
    except Exception as e:
        return False
    for item in branch:
        print(item)
        values = session.execute("SELECT * from "+company+".newwhitelist where branch = '"+item.branch+"'")
        try:
            os.mkdir(os.path.dirname(os.path.realpath(__file__)) + '/'+company + "-" + item.branch + "-branch")
        except OSError:
            pass

        whitelist = open(os.path.dirname(os.path.realpath(__file__)) + '/'+company + "-" + item.branch + "-branch" + "/whitelist.csv", 'a')
        whitelist.write("person,mac_address\n")
        for value in values:
            whitelist.write(str(value.person)+","+value.mac_address+"\n")
        whitelist.close()
        return True


def getTenantGUID():
  url = 'https://api.helixdevicecloud.com/rest/usermanagement/v1/profile'+api_key
  r = requests.get(url, headers=headers)
  jsonformatresponse = json.loads(r.content.decode("utf-8"))
  return jsonformatresponse["tenantGuid"]

def getDevices():

  getDevices = 'https://api.helixdevicecloud.com/rest/systemmanagement/v1/devices' + api_key
  rDev = requests.get(getDevices, headers=headers)
  jsonformatresponse = json.loads(rDev.content.decode("utf-8"))
  devices = []
  for x in jsonformatresponse["data"]["items"]:
    devices.append({"mac_address" : str(x["properties"]["macAddress"]).upper(),"uuid" : x["uuid"]})
  return devices

def createSession(tenantGuid, devices):
  devicesUuid = []
  for device in devices:
    devicesUuid.append(device["uuid"])
  payload = {
    "type": "c2d",
    "devices": devicesUuid
  }
  createSessionUrl = "https://api.helixdevicecloud.com/rest/csp/v1/filemgmt/"+tenantGuid+"/session"+ api_key
  response = requests.post(createSessionUrl, headers=headers, data=json.dumps(payload))
  return json.loads(response.content.decode("utf-8"))

def uniteData(cassData, hdcData):
    data = {}
    print("printing cassData "+str(cassData))
    for value in hdcData:
        company,branch = cassData[value["mac_address"]]
        if company not in data:
            data[company] = {}
        if branch not in data[company]:
            data[company][branch] = []
        data[company][branch].append(value)
    return data


def getSessions(tenantGuid):
    createSessionUrl = "https://api.helixdevicecloud.com/rest/csp/v1/filemgmt/" + tenantGuid + "/session" + api_key
    r2 = requests.get(createSessionUrl, headers=headers)
    if r2.status_code != 200 and r2.status_code != 204:
        return None
    content = json.loads(r2.content.decode("utf-8"))
    return content


def deleteSession(tenantGuid, sessionId):
    createSessionUrl = "https://api.helixdevicecloud.com/rest/csp/v1/filemgmt/" + tenantGuid + "/session/"+sessionId + api_key
    r2 = requests.delete(createSessionUrl, headers=headers)
    return r2.status_code


def sendFileSession(tenantGuid, sessionId, branch,company):
    sendSessionUrl = "https://api.helixdevicecloud.com/rest/csp/v1/filemgmt/" + tenantGuid + "/upload/"+sessionId + api_key
    special_headers = {'Authorization': 'Basic ZmVsaXBlLnlvc2hpZGFAc2VtYW50aXguY29tLmJyOlNlbWFudGl4IzAx',
                       'Accept': 'application/json'}
    print("THIS BRANCH SEND FILE = "+str(branch)+str(company))

    try:
        files = {'file' : open(os.path.dirname(os.path.realpath(__file__))+"/"+str(company)+"-"+str(branch)+"-branch/whitelist.csv","rb")}
    except Exception as e:
        print(e)
        return False
    r2 = requests.post(sendSessionUrl, headers=special_headers, files=files)
    return r2.status_code


def executeSession(tenantGuid, sessionId):
    executeUrl = "https://api.helixdevicecloud.com/rest/csp/v1/filemgmt/"+tenantGuid+"/complete/"+sessionId+api_key
    r = requests.post(executeUrl, headers=headers)
    return r.status_code


def cleanSessions(tenantGuid):
    for session in getSessions(tenantGuid=tenantGuid):
        sessionId = session["session"]
        createSessionUrl = "https://api.helixdevicecloud.com/rest/csp/v1/filemgmt/" + tenantGuid + "/session/"+sessionId + api_key
        r2 = requests.delete(createSessionUrl, headers=headers)
        print(r2.content)


def main():

## Create Whitelist to deploy for each branch
    # getWhitelist('34.196.59.158',9042)
    #
    devices = getDevices()
    dataCass = cassandraData('34.196.59.158',9042)
    cleanPaths()
    data_s = uniteData(dataCass,devices)
    print(data_s)
    # print("DATA_S = " + str(data_s))
    for company, dataSet in data_s.items():
        for branch, data in dataSet.items():
            print("THIS COMPANY : "+str(company))
            getWhitelist('34.196.59.158',9042,company)
            print(data)
            session = createSession(getTenantGUID(),data)
            print("Im Here : "+str(session))
            sendFileSession(getTenantGUID(), session["session"], branch,company)
            print("CHECK FILES SESSIONS = "+str(getSessions(getTenantGUID())))
            executeSession(getTenantGUID(), session["session"])
            # deleteSession(getTenantGUID(), session["session"])
    # #

if __name__ == "__main__":
    # cleanSessions(getTenantGUID())
    main()
    # getSessions(getTenantGUID())





