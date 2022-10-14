import json
import time
from flask import json
from flask import request
from flask import Flask
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

app = Flask(__name__)
line_bot_api = LineBotApi('token')

json_file = open("parking_lot_status_dummy.json", "r")
parking_json_object = json.load(json_file)
json_file.close()

AE_parking_status_list = []
EC_parking_status_list = []

def find_parking_space(usr_input) :
    if usr_input == 'A' :
        for i in range(1,16) :
            if parking_json_object["AE"][str(i)] == "true" :
                parking_json_object["AE"][str(i)] = "reserved"
                json_file = open("parking_lot_status_dummy.json", "w")
                json.dump(parking_json_object, json_file, indent=1)
                json_file.close()
                return "AE-L"+str(i)
    if usr_input == 'E' :
        for i in range(1,16) :
            if parking_json_object["AE"][str(i)] == "true" :
                parking_json_object["AE"][str(i)] = "reserved"
                json_file = open("parking_lot_status_dummy.json", "w")
                json.dump(parking_json_object, json_file, indent=1)
                json_file.close()
                return "AE-L"+str(i)
            if i < 7 and parking_json_object["EC"][str(i)] == "true" :
                parking_json_object["EC"][str(i)] = "reserved"
                json_file = open("parking_lot_status_dummy.json", "w")
                json.dump(parking_json_object, json_file, indent=1)
                json_file.close()
                return "EC-L"+str(i)
    if usr_input == 'C' :
        for i in range(1,7) :
            if parking_json_object["EC"][str(i)] == "true" :
                parking_json_object["EC"][str(i)] = "reserved"
                json_file = open("parking_lot_status_dummy.json", "w")
                json.dump(parking_json_object, json_file, indent=1)
                json_file.close()
                return "EC-L"+str(i)
    return 404

@app.route('/webhook', methods = ['POST'])

def api_root() :
    message = request.json
    print(json.dumps(request.json, indent=1))
    parsed_message = message["events"][0]["message"]["text"]
    reply_token = message["events"][0]["replyToken"]
    print("message : " + parsed_message)
    print("reply token : " + reply_token)
    if parsed_message in ['A','E','C'] :
        space_found = find_parking_space(parsed_message)
        if space_found != '404' :
            line_bot_api.reply_message(reply_token, TextSendMessage(text='ที่จอดรถใกล้ ตึก' + parsed_message + ' ที่ระบบแนะนำให้คุณคือ ' + space_found))
        else :
            line_bot_api.reply_message(reply_token, TextSendMessage(text='ไม่มีที่จอดรถว่างใกล้ตึก ' + parsed_message + ' ที่ตรวจพบจาก smart pole'))
    elif parsed_message in ['help','วิธีใช้งาน','ช่วยเหลือ'] :
            line_bot_api.reply_message(reply_token, TextSendMessage(text='วิธีการใช้งาน intelligent parking'))
    else :
        line_bot_api.reply_message(reply_token, TextSendMessage(text='ตัวเลือกไม่ถูกต้อง'))
    return "OK"

if __name__ == '__main__' :
    app.run(debug=True)

