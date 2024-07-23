"""
MediaWiki API (https://www.mediawiki.org/wiki/API:Main_page) のサンプル
run: python mediaWiki.py
"""

import sys
import urllib.request
import urllib.parse
import json


def main():
    # APIエンドポイント
    url = "http://ja.wikipedia.org/w/api.php?{}"
    # クエリパラメータ（記述方法の詳細はマニュアル参照）
    data = {"action"  : "query",                        # 操作(検索用)
            "prop"    : "categories",                  # 応答の種類
            "titles"  : "イギリス",                         # クエリ（タイトル）
            "format"  : "json"                         # レスポンス型式をJSONに指定
            }

    query = urllib.parse.urlencode(data) # urlの後ろにつける部分の整形
    response = urllib.request.urlopen(url.format(query)).read() # url+queryし、検索
    json_result = json.loads(response.decode('utf-8')) # json形式に変換

    # json形式のデータから目的の部分(categories)を抽出
    for d in json_result["query"]["pages"].values():
        for c in d["categories"]:
            print(c["title"])


if __name__ == "__main__":
    main()
