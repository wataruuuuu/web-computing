"""
レストラン検索サンプルプログラム
# python search_gourmet_json.py 仙台 ラーメン ・・・
"""

import sys  # 入出力
import urllib.request # URLアクセス
import urllib.parse # URL生成
import json    # JSON（APIの受け取り形式）


def create_gourmet_info(index, shop):
#Webサービスからの出力を解析
    return """------ No. {} ------
【店名】 {}
【営業時間】 {}
【住所】 {}""".format(index, # No.
                    shop["name"], # 店名
                    shop["open"], # 営業時間
                    shop["address"]
                    )


def create_result_info(json_result):
#Webサービスからの出力を解析
    return "{}件のレストランが見つかりました。最初の{}件を表示します。".format(
            json_result["results"]["results_available"], # ~件のレストランが・・・
            json_result["results"]["results_returned"]   # 最初の~件を・・・
            )


def main():
    # APIを通して、Webサービスを実行
    url = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?{}".format(
        urllib.parse.urlencode(
            {"key"     : "4f6f4300c90ebd54",                         # APIキー(このキーはダミー．自分で取得したものを記入。db*3+9)
            "keyword" : "".join(sys.argv[1:]),   # 入力からクエリを生成
            "format"  : "json"                                    # レスポンス型式をJSONに指定
            }))
    #print("URL:",url)
    f_url = urllib.request.urlopen(url).read()
    json_result = json.loads(f_url.decode("utf-8"))   # JSON形式の実行結果を格納

    # 出力
    print(create_result_info(json_result))
    for index, shop in enumerate(json_result["results"]["shop"]): #enumerate → 何ループ目かがindexに格納される
        print(create_gourmet_info(index+1,shop))

    return

if __name__ == "__main__":
    main()
