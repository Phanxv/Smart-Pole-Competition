import json

json_file = open("database/parking_lot_status.json", "r")
parking_json_object = json.load(json_file)
json_file.close()

for i in range(1,16) :
            if i< 6 :
                parking_json_object["EC"][str(i)] = "true"
            parking_json_object["AE"][str(i)] = "true"
                
json_file = open("database/parking_lot_status.json", "w")
json.dump(parking_json_object, json_file, indent=1)
json_file.close()