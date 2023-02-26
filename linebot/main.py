from hashlib import new
import imp
import os
from flask import Flask, request, abort, jsonify

import datetime

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import re

import requests
import json
import pymongo
from pymongo import MongoClient
import certifi
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from hashlib import sha256

# import openai


app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(
    '+uJnM8nUxaca1NXcMnCM3Cv0GgV/CtoM0UznD1vC5TbmNs4Fkba2bbEa+kJ7Jt/1BZ/E/io1j7ARVwkouMhyMb68A1Xfn3mGA3xx/rPOaJUAcTda/0vxXM1tHzkRIJXjQx56azMQwja2HECA/V9YtwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('1e3004899187e7cd12bbce49d4dbf9b9')

# openai.api_key = "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"

mongoClient = pymongo.MongoClient(
    "mongodb+srv://andy:acdwsx321@groupmagt.cgjzv3a.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())  # 要連結到的 connect string
iglike_auth = mongoClient["iglike_auth"]  # 指定資料庫
auth_code_table = iglike_auth["auth_code"]  # 指定資料表
auth_user_table = iglike_auth["auth_user"]  # 指定資料表


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    json_body = request.get_json()
    print("Body info: ", json_body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("error occur here!!!! (In LineBot callback function)")
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    uid = event.source.user_id  # Uc2efd8638fcf802f4966bc81032f1341

    if '授權碼=' in message:
        code = message.split('=')[1]
        res = auth_code_table.find({'sha_auth_code': code})
        for i in res:
            if i['enable'] == '1':
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="已使用過的授權碼"))
            else:
                auth_code_table.update_one({'sha_auth_code': code}, {
                                           "$set": {"enable": "1"}})  # 將授權碼改成已使用
                payload = {
                    'uid': uid,
                    'sha_auth_code': code
                }
                auth_user_table.insert_one(payload)
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="成功開通"))
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="不正確的授權碼"))

    elif '新增授權碼 ' in message:
        if uid == 'U71104f51176a5b84c2fe5555cb88275f':
            ori_auth_code = message.split(' ')[1]
            sha_auth_code = sha256(ori_auth_code.encode('utf-8')).hexdigest()
            payload = {
                'ori_auth_code': ori_auth_code,
                'sha_auth_code': sha_auth_code,
                'enable': '0'
            }
            auth_code_table.insert_one(payload)
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=f'{sha_auth_code}'))
        else:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="沒授權唷"))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
