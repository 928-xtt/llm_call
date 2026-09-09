from idlelib import history

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise ValueError("没找到 API Key，请检查 .env 文件")

client = OpenAI(
    api_key=api_key,  # 建议用环境变量替代
    base_url="https://api.deepseek.com"
)

print("🤖 聊天机器人已启动（输入 'quit' 退出）")

# 记录历史对话（大模型没有记忆，需要我们每次把上下文传给它）
history_messages = [{"role": "system", "content": "你是一个幽默的程序员助手"}]

while True:
    # 用户输入
    user_input = input("\n👤 我: ")
    if user_input.strip().lower() == "quit":
        break

    history_messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=history_messages,
        stream=True  # 开启流式
    )

    ai_reply = ""  # 用来收集AI完整的回复，方便存入历史

    # 响应结果流式输出打印
    # 遍历迭代器
    for chunk in response:
        content = chunk.choices[0].delta.content
        # 注意：流式输出时，第一个或最后一个 chunk 的 content 可能是 None
        if content:
            print(content, end="", flush=True)  # end的意义是不让流式输出的打印结果换行      flush的作用是直接打印响应结果，避免python接收响应结果后缓存
            ai_reply += content  # 拼接每次的碎片

    history_messages.append({"role": "assistant", "content": ai_reply})


print("\n\n输出完毕")

