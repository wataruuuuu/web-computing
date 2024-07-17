from newsapi import NewsApiClient
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv


def fetch_news(api_key):
    
    
    newsapi = NewsApiClient(api_key = api_key)
    top_headlines = newsapi.get_top_headlines(sources='abc-news')

    # 記事のURLと記事本文の書き出しを取得
    url = top_headlines['articles'][0]['url']
    title = top_headlines['articles'][0]['title']
    begining = top_headlines['articles'][0]['content'][0:50]
    
    # URLからタイトルとテキストデータ（本文、それ以外のデータを含む）を取得
    response = requests.get(url) 
    html = response.text  # レスポンスからHTMLを取得
    soup = BeautifulSoup(html, 'html.parser') 
    text = soup.get_text()  # ページの本文テキストを取得
    
    # テキストデータから本文データの切り出し
    start_index = text.find(begining)
    title_index = text.find(title)
    if start_index != -1:
        extracted_text = text[start_index:].rstrip()
    elif title_index != -1:
        extracted_text = text[title_index:].rstrip()
    else:
        extracted_text = text
    
    news_data = {
        "url": url,
        "title": title,
        "text": extracted_text
    }
    return news_data


if __name__ == "__main__":
    
    # API key
    load_dotenv()
    api_key= os.environ["NEWS_API_KEY"]
    
    # news_dataを取得
    news_dict = fetch_news(api_key)
    
    # 出力
    print(news_dict["url"])
    print(news_dict["title"])

    # 抽出した本文データはファイルに書き出し
    with open("/Users/wataru/Documents/WebComp/data/article.txt", "w") as fo:
        fo.write(news_dict["text"])

    
