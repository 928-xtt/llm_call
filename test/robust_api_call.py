# call_deepseek_with_retry
# 模拟llmapi调用时可能出现的各种异常
#    APITimeoutError,
#    RateLimitError,
#    APIConnectionError,
#    APIStatusError

import os
import time

from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, APITimeoutError, APIConnectionError, APIStatusError

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise ValueError("没找到 API Key，请检查 .env 文件")

client = OpenAI(
    api_key=api_key,  # 建议用环境变量替代
    base_url="https://api.deepseek.com",
    timeout=30.0
)


def call_deepseek_with_retry(prompt, max_retries=3):
    """
        带重试机制的安全调用函数
        max_retries: 最大重试次数
    """
    retry_count = 0
    while retry_count <= max_retries:
        try:
            response = client.chat.completions.create(
                model="deepseek-v4-flash",
                messages=[{"role": "user", "content": prompt}],
                stream=False
            )
            return response.choices[0].message.content
            # ---------------- 超时处理 ----------------
        except APITimeoutError:
            retry_count += 1
            wait_time = 2 ** retry_count
            print(f"⏰ 请求超时，第 {retry_count} 次重试，等待 {wait_time} 秒...")
            if retry_count > max_retries:
                return "抱歉，多次重试后仍然超时，请稍后再试。"
            time.sleep(wait_time)
            # ---------------- 429 限流处理 ----------------
        except RateLimitError:
            retry_count += 1
            wait_time = 2 ** retry_count
            print(f"🚦 触发限流(429)，第 {retry_count} 次重试，等待 {wait_time} 秒...")
            if retry_count > max_retries:
                return "调用太频繁了，请稍后再试。"
            time.sleep(wait_time)
            # ---------------- 网络连接问题 ----------------
        except APIConnectionError:
            retry_count += 1
            wait_time = 2 ** retry_count
            print(f"🔌 网络连接失败，第 {retry_count} 次重试，等待 {wait_time} 秒...")
            if retry_count > max_retries:
                return "网络连接异常，请检查网络后重试。"
            time.sleep(wait_time)
            # ---------------- 其他 API 错误（如 401 Key错误） ----------------
        except APIStatusError as e:
            print(f"❌ API返回错误，状态码: {e.status_code}")
            print(f"错误信息: {e.message}")
            # 401/403 这种错误重试也没用，直接返回
            return f"API错误({e.status_code})，请检查API Key或账户余额。"

        # ---------------- 兜底：未知异常 ----------------
        except Exception as e:
            print(f"未知异常: {type(e).__name__}: {e}")
            return f"发生未知错误: {e}"


# 模拟各种异常出现处理
if __name__ == "__main__":

    print("=== 测试正常调用 ===")
    result = call_deepseek_with_retry("你好，介绍一下你自己")
    print(result)

    print("\n=== 测试错误调用（故意用错的Key）===")


    # # 临时创建一个错误client来测试401
    bad_client = OpenAI(api_key="sk-wrong-key", base_url="https://api.deepseek.com")

    # 临时替换全局client

    original_client = client
    client = bad_client
    result = call_deepseek_with_retry("测试")
    print(result)
    client = original_client  # 恢复


    # print("\n=== 测试错误调用（超时）===")
    # bad_client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com",timeout=0.0001)
    # # # 临时替换全局client
    # # import types
    # original_client = client
    # client = bad_client
    # result = call_deepseek_with_retry("测试")
    # print(result)
    # client = original_client  # 恢复


    # print("\n=== 测试错误调用（网络连接错误）===")
    # bad_client = OpenAI(api_key=api_key, base_url="https://api.deepseek.comaaabbbccc")
    # # # 临时替换全局client
    # # import types
    # original_client = client
    # client = bad_client
    # result = call_deepseek_with_retry("测试")
    # print(result)
    # client = original_client  # 恢复
