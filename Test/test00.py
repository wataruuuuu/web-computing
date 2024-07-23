import os
from openai import OpenAI

# 環境変数からAPIキーを取得
api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)

embeddings = client.embeddings.create(
    model="text-embedding-ada-002",
    input="The food was delicious and the waiter...",
    encoding_format="float"
)

print(type(embeddings))


