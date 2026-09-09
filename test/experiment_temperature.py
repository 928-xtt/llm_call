from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise ValueError("没找到 API Key，请检查 .env 文件")

temperatures_to_test = [0.0, 1.0, 1.5]

prompt = "用一句话总结AIAgent开发的工作内容"

client = OpenAI(
    api_key=api_key,  # 建议用环境变量替代
    base_url="https://api.deepseek.com"
)

for temp in temperatures_to_test:
    print(f"\n===============temperature = {temp}===================")
    for i in range(3):
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[{"role": "user", "content": prompt}],
            stream=False,
            temperature=temp
        )
        result = response.choices[0].message.content
        print(f"第{i+1}次响应结果为：{result}")
print("\n试验结束")