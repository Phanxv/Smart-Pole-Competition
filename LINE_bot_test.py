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

load_dotenv()
LINE_BOT_API_KEY = os.getenv('LINE_BOT_API_KEY')

app = Flask(__name__)
line_bot_api = LineBotApi(LINE_BOT_API_KEY)
response_file_path = "database/response_text.json"

parking_img = open("database/parking_img.json","r")
parking_img_json = json.load(parking_img)
parking_img.close()
response_text_file = open(response_file_path,"r",encoding="utf8")
response_text_json = json.load(response_text_file)
response_text_file.close()
line_bot_api.push_message("U1eda14c2e233ec0a93860224801a7e65", TextSendMessage(text=response_text_json["en"]["lot_found"] + "AE-L1"))
line_bot_api.push_message("U1eda14c2e233ec0a93860224801a7e65", ImageSendMessage(original_content_url=parking_img_json["AE-L1"]["originalContentUrl"],preview_image_url=parking_img_json["EC-L1"]["previewImageUrl"]))
