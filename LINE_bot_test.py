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

message = [{
            "type": "image",
            "originalContentUrl": "https://drive.google.com/uc?export=view&id=1fn3l1na4QOvBfFK01rVbWdfstEsriJT-",
            "previewImageUrl": "https://drive.google.com/uc?export=view&id=1fn3l1na4QOvBfFK01rVbWdfstEsriJT-",
        }]

line_bot_api.push_message("U1eda14c2e233ec0a93860224801a7e65", ImageSendMessage(original_content_url="https://drive.google.com/uc?export=view&id=1fn3l1na4QOvBfFK01rVbWdfstEsriJT-",preview_image_url="https://i.pinimg.com/474x/d8/b1/73/d8b173ac49c364587e8c7e87e6d21ca7.jpg"))
