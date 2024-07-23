from newsapi import NewsApiClient
import requests
from bs4 import BeautifulSoup

newsapi = NewsApiClient(api_key='86c41b282c7e4aaa99928963c90aa836')

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(sources= 'abc-news')

#記事のURLと記事本文の書き出しを取得
url = top_headlines['articles'][0]['url']
title = top_headlines['articles'][0]['title']
begining = top_headlines['articles'][0]['content'][0:50]

#URLからタイトルとテキストデータ（本文、それ以外のデータを含む）を取得
response = requests.get(url)  # URLにGETリクエストを送信
html = response.text  # レスポンスからHTMLを取得
soup = BeautifulSoup(html, 'html.parser')  # HTMLを解析するためにBeautifulSoupオブジェクトを作成
text = soup.get_text()  # ページの本文テキストを取得

# テキストデータから本文のみを切り出し
start_index = text.find(begining)
if start_index != -1:
    extracted_text = text[start_index:].rstrip()
else:
    print("指定された文字列が見つかりません。")

