from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),  # 建议用环境变量替代
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "你好，介绍一下你自己"}],
    stream=False
)

print(response.choices[0].message.content)
print("""
------------------------------------------------------

""")