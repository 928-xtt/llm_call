import time
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

print("开始提问（流式输出）：\n")

response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[{"role": "user", "content": "写一首关于程序员加班的七言绝句"}],
    stream=True  # 开启流式
)

# 响应结果流式输出打印
# 遍历迭代器
for chunk in response:
    # print(chunk)
    content = chunk.choices[0].delta.content
    # 注意：流式输出时，第一个或最后一个 chunk 的 content 可能是 None
    if content:
        print(content, end="", flush=True)  # end的意义是不让流式输出的打印结果换行      flush的作用是直接打印响应结果，避免python接收响应结果后缓存
        time.sleep(0.1)

print("\n\n输出完毕")

# ChatCompletionChunk(id='1b77010d-efed-4db8-9d69-9b1f5ac549ab', choices=[Choice(
#     delta=ChoiceDelta(content=None, function_call=None, refusal=None, role='assistant', tool_calls=None,
#                       reasoning_content=''), finish_reason=None, index=0, logprobs=None)], created=1788921277,
#                     model='deepseek-v4-flash', object='chat.completion.chunk', moderation=None, obfuscation=None,
#                     service_tier=None, system_fingerprint='a26a7955944dc5c60445bff77fac9c8e', usage=None)
