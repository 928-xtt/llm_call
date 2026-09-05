from openai import OpenAI

client = OpenAI(
    api_key="sk-0469747473f140de892b826b8ab9835b",  # 建议用环境变量替代
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "你好，介绍一下你自己"}],
    stream=False
)

print(response.choices[0].message.content)
