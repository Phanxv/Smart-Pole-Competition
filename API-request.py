import requests
import json
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
import os

json_file = open("database/parking_lot_status.json", "r")
parking_json_object = json.load(json_file)
json_file.close()
load_dotenv()

PLANETCOMM_USERNAME = os.getenv('PLANETCOMM_USERNAME')
PLANETCOMM_PASSWORD = os.getenv('PLANETCOMM_PASSWORD')

AE_parking_entityid_list = ["2ee366a0-dcbc-11ec-bd0b-9df640eab97d",
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
                            "7d0ae0b0-dcbc-11ec-bd0b-9df640eab97d"]

EC_parking_entityid_list = ["89df06e0-dcbc-11ec-bd0b-9df640eab97d",
                            "8da16610-dcbc-11ec-bd0b-9df640eab97d",
                            "91574220-dcbc-11ec-bd0b-9df640eab97d",
                            "96af8390-dcbc-11ec-bd0b-9df640eab97d",
                            "9b1accf0-dcbc-11ec-bd0b-9df640eab97d",
                            "9fcbf8f0-dcbc-11ec-bd0b-9df640eab97d"]

parking_status = []


def request_access_token():
    API_ENDPOINT = "https://api.planetcloud.cloud/tni/digitalcampus/api/auth/login"
    headers = {"Content-Type": "application/json"}

    data = {"username": PLANETCOMM_USERNAME,
            "password": PLANETCOMM_PASSWORD}

    access_token_response = requests.post(
        url=API_ENDPOINT, headers=headers, json=data)
    access_token_js = json.loads(access_token_response.text)
    return access_token_js["token"]

#start_time = time.time()

def request_parking_status():
    access_token = request_access_token()

    for i in range(1,16) :
        API_ENDPOINT = "https://api.planetcloud.cloud/tni/digitalcampus/api/plugins/telemetry/DEVICE/" + AE_parking_entityid_list[i-1] + "/values/timeseries"
        headers = {"X-Authorization": "Bearer "+access_token}
        parking_status_response = requests.get(url=API_ENDPOINT, headers=headers)
        parking_status_js = parking_status_response.json()
        parking_status_temp = parking_status_js["status"][0]["value"]
        # print(parking_status_temp)
        if(parking_json_object["AE"][str(i)] != "reserved" or parking_status_temp == "true") :
            parking_json_object["AE"][str(i)] = parking_status_temp
        elif(parking_status_temp == "false" and parking_json_object["AE"][str(i)] == "reserved") :
            parking_json_object["AE"][str(i)] = "reserved"
        json_file = open("database/parking_lot_status.json", "w")
        json.dump(parking_json_object, json_file, indent=1)
        json_file.close()

    for i in range(1,7) :
        API_ENDPOINT = "https://api.planetcloud.cloud/tni/digitalcampus/api/plugins/telemetry/DEVICE/" + EC_parking_entityid_list[i-1] + "/values/timeseries"
        headers = {"X-Authorization": "Bearer "+access_token}
        parking_status_response = requests.get(url=API_ENDPOINT, headers=headers)
        parking_status_js = parking_status_response.json()
        parking_status_temp = parking_status_js["status"][0]["value"]
        # print(parking_status_temp)
        if(parking_json_object["EC"][str(i)] != "reserved" or parking_status_temp == "true") :
            parking_json_object["EC"][str(i)] = parking_status_temp
        elif(parking_status_temp == "false" and parking_json_object["EC"][str(i)] == "reserved") :
            parking_json_object["EC"][str(i)] = "reserved"
        parking_json_object["EC"][str(i)] = parking_status_temp
        json_file = open("database/parking_lot_status.json", "w")
        json.dump(parking_json_object, json_file, indent=1)
        json_file.close()
    
    now = datetime.now()
    current_time = now.strftime("%c")
    print("parking status updated at : ", current_time)

def clear_temp():
    temp = open("temp.txt",'w')
    temp.write("")
    temp.close()
    now = datetime.now()
    current_time = now.strftime("%c")
    print("temp file cleared at : ", current_time)

schedule.every(1).minutes.do(request_parking_status)
schedule.every(5).minutes.do(clear_temp)
while True:
    schedule.run_pending()
    time.sleep(1)


#request_parking_status()

#print(parking_status)
# measure execution time
#print("--- execution time : %s seconds ---" % (time.time() - start_time))
