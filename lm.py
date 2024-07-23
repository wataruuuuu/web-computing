from news import fetch_news
from openai import OpenAI
import os
from dotenv import load_dotenv

# クイズの生成
def make_quiz(text, key):
    # OpenAI APIのキーを設定
    client = OpenAI(api_key=key)

    # プロンプト1: 3つの3択問題を生成
    prompt1 = f"""
    # 命令
    次の英文について、高校生の理解度を試すための、英語の3択問題を3つ作成してください。出力形式は以下の通りです。
    ただし、本文中に書いてある事実と内容と知識だけを使い、他の知識に言及したり想定してはいけません。
    {text}
    
    # 出力形式
    Q1: Text of the quiz.
    
    A) Choice1
    B) Choice2
    C) Choice3
    
    Q2: Text of the quiz.
    
    A) Choice1
    B) Choice2
    C) Choice3
    
    Q3: Text of the quiz.
    
    A) Choice1
    B) Choice2
    C) Choice3
    """

    # クイズ生成リクエスト
    response1 = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a high school English teacher."},
            {"role": "user", "content": prompt1}
        ],
        max_tokens=1000
    )

    # 生成された3択クイズ
    return response1.choices[0].message.content

def make_answer(text, quiz ,key):
    # OpenAI APIのキーを設定
    client = OpenAI(api_key=key)
    
    # プロンプト2: 解答と解説を生成
    prompt2 = f"""
    # 命令
    次のニュース記事と3択問題について、それぞれの問題に対する解答と解説を100文字程度で書いてください。
    出力の例を以下に示す。解説は日本語にしてください。
    ニュース記事:
    {text}

    3択問題:
    {quiz}
    
    # 出力形式
    Q1:
    C) This is the text of the correct choice.
    解説: 正しい答えになる根拠をここで示す。
    
    Q3:
    C) This is the text of the correct choice.
    解説: 正しい答えになる根拠をここで示す。    
    """

    # 解答と解説生成リクエスト
    response2 = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a high school English teacher."},
            {"role": "user", "content": prompt2}
        ],
        max_tokens=1000
    )

    # 生成された解答と解説
    return response2.choices[0].message.content
    
    
if __name__ == "__main__":
    
    # API key
    load_dotenv()
    OPEN_AI_API_KEY = os.environ["OPEN_AI_API_KEY"]
    NEWS_API_KEY = os.environ["NEWS_API_KEY"]
    
    # ニュースの各種データを取得
    news_data = fetch_news(NEWS_API_KEY)
    title = news_data["title"]
    url = news_data["url"]
    text = news_data["text"]
    
    
    # 生成されたクイズと解答・解説を取得
    quiz = make_quiz(text, OPEN_AI_API_KEY)
    ans = make_answer(text, quiz, OPEN_AI_API_KEY)
    
    with open("/Users/wataru/Documents/WebComp/data/title.txt", 'w') as fo:
        fo.write(title)
        fo.write("\n")
        fo.write(url)
    
    with open("/Users/wataru/Documents/WebComp/data/text.txt", 'w') as fo:
        fo.write(text)
        
    with open("/Users/wataru/Documents/WebComp/data/quiz.txt", 'w') as fo:
        fo.write(quiz)
        
    with open("/Users/wataru/Documents/WebComp/data/answers_and_explanations.txt", 'w') as fo:
        fo.write(ans)