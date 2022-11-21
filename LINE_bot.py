import os
import json
import time
from flask import json
from flask import request
from flask import Flask
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
from dotenv import load_dotenv

LINE_BOT_API_KEY = os.getenv('LINE_BOT_API_KEY')

app = Flask(__name__)
line_bot_api = LineBotApi(LINE_BOT_API_KEY)

message = [{
            "type": "image",
            "originalContentUrl": "https://imgur.com/2rQTGtP",
            "previewImageUrl": "https://imgur.com/2rQTGtP",
        }]

line_bot_api.push_message(to="")