import requests
import json
from datetime import datetime

# 定义请求的URL
url = 'http://127.0.0.1:5000/submit_vote'  # 请根据实际情况修改URL

# 定义请求的头部
headers = {
    'Content-Type': 'application/json'
}

# 定义请求的负载
payload = {
    'user_id': 's1360912',  # 替换为你想要测试的用户ID
    'voting_id': 2,  # 替换为你想要投票的投票ID
    'votes': [
        {
            'option_id': 1,
            'option_value': [1,2,3]  # 替换为你想要投票的选项值
        },
        {
            'option_id': 2,
            'option_value': [4,5,6]  # 替换为你想要投票的选项值
        }
    ]
}

# 发送POST请求
response = requests.post(url, headers=headers, data=json.dumps(payload))

# 打印响应
print(f'Status Code: {response.status_code}')
print(f'Response JSON: {response.json()}')