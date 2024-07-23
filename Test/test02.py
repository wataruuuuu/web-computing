import requests
import json
from pprint import pprint
from IPython.display import HTML


#AIPキー、エンドポイント、検索キーワードの設定
subscription_key = "d67447600b8c4be1b44b17a2b2589a84"
search_url = "https://api.bing.microsoft.com/v7.0/news/search"
search_term = "Microsoft"

#ヘッダーとパラメータの設定
headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
params  = params  = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
#params  = {"q":"", "mkt": "setLang", "setLang": "en"}

#リクエストを送り、リスポンスを受け取る
response = requests.get(search_url, headers=headers, params=params)
data = response.json()

# raise_for_statusを呼び出して、エラーチェックを行う
try:
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f'HTTP error occurred: {e}')
else:
    print('Success!')

pprint(data)

"""
search_results = response.json()

descriptions = [article["description"] for article in search_results["value"]]

pprint(descriptions)

rows = "\n".join(["<tr><td>{0}</td></tr>".format(desc) for desc in descriptions])
HTML("<table>"+rows+"</table>")"""