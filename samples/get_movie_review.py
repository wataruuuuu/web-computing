"""
みんなのシネマビュー(https://www.jtnews.jp/)から映画一覧とレビューと収集する
run: python get_movie_review.py > 出力先
***ディスク容量に注意！***
"""

import sys
import urllib.request
import time
import json
from bs4 import BeautifulSoup  # htmlの解析


def get_movie_review():
    # baseURL
    URL = "http://www.jtnews.jp/cgi-bin/review.cgi"
    for NO in range(1, 1000):
        # baseURLに情報を付け足して、目的のhtmlを取得
        html = urllib.request.urlopen(URL + "?TITLE_NO={}".format(NO)).read()
        # htmlをparse
        soup = BeautifulSoup(html, "html.parser") # ホントはlxml推奨。html.parserなら確実に動く

        # 映画のタイトルの取得
        title = soup.findAll("title")[0].get_text().replace(" - みんなのシネマレビュー", "")
        # タイトルがなければレビューの取得を飛ばす
        if len(title) > 0:
            t = title
        else:
            time.sleep(2) # dos攻撃対策
            continue

        # レビューの取得
        revs = []
        count = 0
        for rev in soup.findAll("div"):
            if "REV_" in str(rev):
                revs.append(rev.get_text())
                count += 1
            if count > 9: # 10件で切る
                break

        # json形式で保存
        d = {"id": NO, "title": t, "reviews": revs}
        print(json.dumps(d, ensure_ascii=False))
        # 呼び出すときは、for l in sys.stdin; + json.loads(l) で１行ずつ

        time.sleep(5) # dos攻撃対策


def main():
    get_movie_review()


if __name__ == "__main__":
    main()
