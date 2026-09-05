import requests  # 导入刚安装的第三方库
import json  # 导入Python内置的json模块

# 我们用一个免费的测试API（可以把它想象成你公司后端写的一个接口）
url = "https://jsonplaceholder.typicode.com/users/1"

try:
    # 1. 发送GET请求（相当于 Java HttpClient.sendGet()）
    print(f"正在请求: {url}")
    response = requests.get(url, timeout=5)

    # 2. 检查状态码（200表示成功）
    if response.status_code == 200:
        # 3. 解析返回的JSON数据
        # response.text 是返回的原始字符串
        # response.json() 会自动把JSON字符串转成 Python 的字典，极其方便！
        user_data = response.json()

        print("\n--- 提取关键字段 ---")
        # 在Python里，字典取值就像Java里的Map.get("key")
        print(f"用户ID: {user_data['id']}")
        print(f"用户名: {user_data['username']}")
        print(f"邮箱: {user_data['email']}")

        # 演示用 json.dumps 把字典再转回格式化的JSON字符串（类似Java的ObjectMapper.writeValueAsString）
        print("\n--- 演示 json.dumps ---")
        formatted_json = json.dumps(user_data, indent=4)
        print(formatted_json)
    else:
        print(f"请求失败，状态码: {response.status_code}")

except requests.exceptions.RequestException as e:
    # 相当于Java的 catch (Exception e)
    print(f"网络出错了: {e}")
