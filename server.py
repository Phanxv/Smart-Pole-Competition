import os
import json
import time
from flask import json
from flask import request
from flask import Flask
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.models import ImageSendMessage
from linebot.exceptions import LineBotApiError
from dotenv import load_dotenv

#load data from database
parking_file_path = "database/parking_lot_status.json"
userdatase_file_path = "database/user_database.json"
response_file_path = "database/response_text.json"
load_dotenv()
parking_json_file = open(parking_file_path, "r")
parking_json_object = json.load(parking_json_file)
parking_json_file.close()
user_database_json = []
user_database_file = open(userdatase_file_path,"r")
user_database_json = json.load(user_database_file)
user_database_file.close()
response_text_file = open(response_file_path,"r",encoding="utf8")
response_text_json = json.load(response_text_file)
response_text_file.close()
parking_img = open("database/parking_img.json","r")
parking_img_json = json.load(parking_img)
parking_img.close()
LINE_BOT_API_KEY = os.getenv('LINE_BOT_API_KEY')

#initialize server and LINE bot
app = Flask(__name__)
line_bot_api = LineBotApi(LINE_BOT_API_KEY)

AE_parking_status_list = []
EC_parking_status_list = []

def find_parking_space(usr_input) :
    if usr_input == 'a' :
        for i in [1,2,9,3,10,4,11,5,12,6,13,7,14,8,15] :
            if parking_json_object["AE"][str(i)] == "false" :
                parking_json_object["AE"][str(i)] = "reserved"
                parking_json_file = open(parking_file_path, "w")
                json.dump(parking_json_object, parking_json_file, indent=1)
                parking_json_file.close()
                return "AE-L"+str(i)
    if usr_input == 'e' :
        for i in [1,2,9,3,10,4,11,5,12,6,13,7,14,8,15] :
            if parking_json_object["AE"][str(i)] == "false" :
                parking_json_object["AE"][str(i)] = "reserved"
                parking_json_file = open(parking_file_path, "w")
                json.dump(parking_json_object, parking_json_file, indent=1)
                parking_json_file.close()
                return "AE-L"+str(i)
        for i in range(1,7) :
            if parking_json_object["EC"][str(i)] == "false" :
                parking_json_object["EC"][str(i)] = "reserved"
                parking_json_file = open(parking_file_path, "w")
                json.dump(parking_json_object, parking_json_file, indent=1)
                parking_json_file.close()
                return "EC-L"+str(i)
    if usr_input == 'c' :
        for i in range(1,7) :
            if parking_json_object["EC"][str(i)] == "false" :
                parking_json_object["EC"][str(i)] = "reserved"
                parking_json_file = open(parking_file_path, "w")
                json.dump(parking_json_object, parking_json_file, indent=1)
                parking_json_file.close()
                return "EC-L"+str(i)
    return "404"

@app.route('/webhook', methods = ['POST','GET'])

def api_root() :
    message = request.json
    print(json.dumps(request.json, indent=1))
    try :
        user_message = message["events"][0]["message"]["text"]
        parsed_message = user_message.lower().replace(" ","").strip()
        reply_token = message["events"][0]["replyToken"]
        user_id = message["events"][0]["source"]["userId"]
    except KeyError :
        pass
    #user_profile = json.loads(str(line_bot_api.get_profile(user_id)))
    if parsed_message in ["register","ลงทะเบียน","REGISTER_JP_PLACEHOLDER"] :
        if not user_id in user_database_json :
            user_database_json.update({user_id:{"lang":"NON","plate":"NON","building":"NON"}})
            if parsed_message == "register" :
                user_database_json[user_id]['lang'] = 'en'
            elif parsed_message == "ลงทะเบียน" :
                user_database_json[user_id]['lang'] = 'th'
            elif parsed_message == "REGISTER_JP_PLACEHOLDER" :
                user_database_json[user_id]['lang'] = 'jp'
            user_database_file = open(userdatase_file_path,"w")
            json.dump(user_database_json, user_database_file, indent=2)
            user_database_file.close()
            line_bot_api.push_message(user_id, TextSendMessage(text=response_text_json[user_database_json[user_id]["lang"]]["plate_ask"]))
            #line_bot_api.reply_message(reply_token, TextSendMessage(text='กรุณาเลือกภาษาที่ต้องการใช้\nPlease choose the language\n言語を選択してください\n\nภาษาไทย พิมพ์ TH\nType EN for English'))
        elif user_id in user_database_json :
            line_bot_api.reply_message(reply_token, TextSendMessage(text=response_text_json[user_database_json[user_id]["lang"]]["registered"]))
    elif user_database_json[user_id]["plate"] == "NON" :
        user_database_json[user_id]["plate"] = parsed_message
        user_database_file = open(userdatase_file_path,"w")
        json.dump(user_database_json, user_database_file, indent=2)
        user_database_file.close()
        line_bot_api.reply_message(reply_token, TextSendMessage(text=response_text_json[user_database_json[user_id]["lang"]]["plate_regis"] + "\n" + user_database_json[user_id]["plate"]))
        line_bot_api.push_message(user_id, TextSendMessage(text=response_text_json[user_database_json[user_id]["lang"]]["building_ask"]))
    elif user_database_json[user_id]["building"] == "NON" :
        if parsed_message in ['a','b','c','d','e'] :
            user_database_json[user_id]["building"] = parsed_message
            user_database_file = open(userdatase_file_path,"w")
            json.dump(user_database_json, user_database_file, indent=2)
            user_database_file.close()
            line_bot_api.reply_message(reply_token, TextSendMessage(text=response_text_json[user_database_json[user_id]["lang"]]["building_regis"] + user_database_json[user_id]["building"]))
            line_bot_api.push_message(user_id, TextSendMessage(text=response_text_json[user_database_json[user_id]["lang"]]["regis_fin"]["1"] + user_database_json[user_id]["plate"] + response_text_json[user_database_json[user_id]["lang"]]["regis_fin"]["2"] + user_database_json[user_id]["building"].upper() + response_text_json[user_database_json[user_id]["lang"]]["regis_fin"]["3"]))
        else :
            line_bot_api.reply_message(reply_token, TextSendMessage(text=response_text_json[user_database_json[user_id]["lang"]]["building_notfound"]))
            line_bot_api.push_message(user_id, TextSendMessage(text=response_text_json[user_database_json[user_id]["lang"]]["building_ask"]))

    elif parsed_message in ["ลบข้อมูล","delete"] :
        user_database_json[user_id]["lang"] = "NON"
        user_database_json[user_id]["plate"] = "NON"
        user_database_json[user_id]["building"] = "NON"
    '''else :
        if user_database_json[user_id]        
            print('userId :' + user_id)
        print('user profile :')
        print(json.dumps(user_profile, indent=1))'''
    
    '''
    print("message : " + parsed_message)
    print("reply token : " + reply_token)
    if parsed_message in ['A','E','C'] :
        space_found = find_parking_space(parsed_message)
        if space_found != '404' :
            line_bot_api.reply_message(reply_token, TextSendMessage(text='ที่จอดรถใกล้ ตึก' + parsed_message + ' ที่ระบบแนะนำให้คุณคือ ' + space_found))
        else :
            line_bot_api.reply_message(reply_token, TextSendMessage(text='ไม่มีที่จอดรถว่างใกล้ตึก ' + parsed_message + ' ที่ตรวจพบจาก smart pole'))
    elif parsed_message in ['help','วิธีใช้งาน','ช่วยเหลือ'] :
        print("")
    else :
        line_bot_api.reply_message(reply_token, TextSendMessage(text='ตัวเลือกไม่ถูกต้อง'))'''
    return "OK"

@app.route('/lpr', methods = ['POST'])
def process() :
    nplate = str(request.data.decode('utf-8'))
    temp = open("temp.txt",'r')
    temp_obj = temp.read()
    temp.close()
    for i in user_database_json :
        if nplate == user_database_json[i]['plate'] and not i in temp_obj:
            lot = find_parking_space(user_database_json[i]['building'])
            if lot == "404" :
                print("space not found")
                line_bot_api.push_message(i, TextSendMessage(text=response_text_json[user_database_json[i]["lang"]]["lot_notfound"]))
            else :
                print(nplate + ' found, parking space data sent to ' + i)
                line_bot_api.push_message(i, TextSendMessage(text=response_text_json[user_database_json[i]["lang"]]["lot_found"] + lot))
                line_bot_api.push_message(i, ImageSendMessage(original_content_url=parking_img_json[lot]["originalContentUrl"],preview_image_url=parking_img_json[lot]["previewImageUrl"]))
                temp = open("temp.txt",'a')
                temp.write('\n')
                temp.write(i)
        elif nplate in temp_obj :
            print("same plate detected")
            

    return "OK"
if __name__ == '__main__' :
    app.run(debug=True)

