from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
	ApiClient, Configuration, MessagingApi,
	ReplyMessageRequest, PushMessageRequest,
	TextMessage, PostbackAction
)
from linebot.v3.webhooks import (
	FollowEvent, MessageEvent, PostbackEvent, TextMessageContent
)
import os
from dotenv import load_dotenv
from news import fetch_news
from lm import make_quiz


load_dotenv()

## 環境変数を変数に割り当て
CHANNEL_ACCESS_TOKEN = os.environ["LINE_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
OPEN_AI_API_KEY = os.environ["OPEN_AI_API_KEY"]
NEWS_API_KEY = os.environ["NEWS_API_KEY"]

## ニュースの情報やクイズを格納する変数
title = ""
url = ""
quiz = ""
answers_and_explanations = ""

news_dict = fetch_news(NEWS_API_KEY)
url = news_dict["url"]
text = news_dict["text"]

q_and_a = make_quiz(text, OPEN_AI_API_KEY)
quiz = q_and_a["quiz"]
answers_and_explanations = q_and_a["answers_and_explanations"]

with open("/Users/wataru/Documents/WebComp/data/text.txt", 'w') as fo:
    fo.write(text)
    
with open("/Users/wataru/Documents/WebComp/data/quiz.txt", 'w') as fo:
    fo.write(q_and_a["quiz"])
        
with open("/Users/wataru/Documents/WebComp/data/answers_and_explanations.txt", 'w') as fo:
    fo.write(q_and_a["answers_and_explanations"])