import requests
import json
import time

start_time = time.time()

parking_entityid_list = ["2ee366a0-dcbc-11ec-bd0b-9df640eab97d",
                         "41b9a2d0-dcbc-11ec-bd0b-9df640eab97d",
                         "45f529a0-dcbc-11ec-bd0b-9df640eab97d",
                         "4a6729c0-dcbc-11ec-bd0b-9df640eab97d",
                         "504b3070-dcbc-11ec-bd0b-9df640eab97d",
                         "5462db90-dcbc-11ec-bd0b-9df640eab97d",
                         "5958d8c0-dcbc-11ec-bd0b-9df640eab97d",
                         "5d871920-dcbc-11ec-bd0b-9df640eab97d",
                         "618d3810-dcbc-11ec-bd0b-9df640eab97d",
                         "65667aa0-dcbc-11ec-bd0b-9df640eab97d",
                         "6a2b2ea0-dcbc-11ec-bd0b-9df640eab97d",
                         "6de9bd40-dcbc-11ec-bd0b-9df640eab97d",
                         "740ffd10-dcbc-11ec-bd0b-9df640eab97d",
                         "782473e0-dcbc-11ec-bd0b-9df640eab97d",
                         "7d0ae0b0-dcbc-11ec-bd0b-9df640eab97d",
                         "89df06e0-dcbc-11ec-bd0b-9df640eab97d",
                         "8da16610-dcbc-11ec-bd0b-9df640eab97d",
                         "91574220-dcbc-11ec-bd0b-9df640eab97d",
                         "96af8390-dcbc-11ec-bd0b-9df640eab97d",
                         "9b1accf0-dcbc-11ec-bd0b-9df640eab97d",
                         "9fcbf8f0-dcbc-11ec-bd0b-9df640eab97d"]

parking_status = []

def request_access_token():
    API_ENDPOINT = "https://api.planetcloud.cloud/tni/digitalcampus/api/auth/login"
    headers = {"Content-Type": "application/json"}

    data = {"username": "tniteam03@planetcomm.com",
            "password": "team03@12345"}

    access_token_response = requests.post(url=API_ENDPOINT, headers=headers, json=data)
    access_token_js = json.loads(access_token_response.text)
    return access_token_js["token"]

access_token = request_access_token()

def request_parking_status():
    for i in parking_entityid_list :
        API_ENDPOINT = "https://api.planetcloud.cloud/tni/digitalcampus/api/plugins/telemetry/DEVICE/"+i+"/values/timeseries"
        headers = {"X-Authorization": "Bearer "+access_token}
        parking_status_response = requests.get(url=API_ENDPOINT,headers=headers)
        parking_status_js = parking_status_response.json()
        parking_status_temp = parking_status_js["status"][0]["value"]
        #print(parking_status_temp)
        parking_status.append(parking_status_temp)

request_parking_status()

print(parking_status)
#measure execution time
print("--- execution time : %s seconds ---" % (time.time() - start_time))