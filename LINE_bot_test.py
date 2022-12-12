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

parking_img = open("database/parking_img.json","r")
parking_img_json = json.load(parking_img)
parking_img.close()
line_bot_api.push_message("U1eda14c2e233ec0a93860224801a7e65", ImageSendMessage(original_content_url=parking_img_json["AE-L2"]["originalContentUrl"],preview_image_url=parking_img_json["AE-L2"]["previewImageUrl"]))
