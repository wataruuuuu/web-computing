from openai import OpenAI
import os

# 環境変数からAPIキーを取得
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Say this is a test"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")