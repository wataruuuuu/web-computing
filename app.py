from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
	ApiClient, Configuration, MessagingApi,
	ReplyMessageRequest, TextMessage
)
from linebot.v3.webhooks import (
	FollowEvent, MessageEvent, TextMessageContent
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


## Flask アプリのインスタンス化
app = Flask(__name__)

## LINE のアクセストークン読み込み
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

## コールバックのおまじない
@app.route("/callback", methods=['POST'])
def callback():
	# get X-Line-Signature header value
	signature = request.headers['X-Line-Signature']

	# get request body as text
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)

	# handle webhook body
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
		abort(400)

	return 'OK'


## 友達追加時のメッセージ送信
@handler.add(FollowEvent)
def handle_follow(event):
	## APIインスタンス化
	with ApiClient(configuration) as api_client:
		line_bot_api = MessagingApi(api_client)

	## 返信
	line_bot_api.reply_message(ReplyMessageRequest(
		replyToken=event.reply_token,
		messages=[TextMessage(text='Thank You!')]
	))


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    
	# APIインスタンス化
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

	# 受信メッセージの中身を取得
    #received_message = event.message.text
    
    news_dict = fetch_news(NEWS_API_KEY)
    url = news_dict["url"]
    text = news_dict["text"]
    reply0 = url
    reply1 = url
    q_and_a = make_quiz(text, OPEN_AI_API_KEY)
    quiz = q_and_a["quiz"]
    answers_and_explanations = q_and_a["answers_and_explanations"]
    reply2 = quiz
    reply3 = answers_and_explanations

    line_bot_api.reply_message(ReplyMessageRequest(
        replyToken=event.reply_token,
        messages=[TextMessage(text=reply0), TextMessage(text=reply1), TextMessage(text=reply2), TextMessage(text=reply3)]
    ))

## 起動確認用ウェブサイトのトップページ
@app.route('/', methods=['GET'])
def toppage():
	return 'Hello world!'

## ボット起動コード
if __name__ == "__main__":
	## ローカルでテストする時のために、`debug=True` にしておく
	app.run(host="0.0.0.0", port=8000, debug=True)
