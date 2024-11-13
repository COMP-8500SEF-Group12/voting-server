import requests
import json

# 定义请求的URL
url = 'http://127.0.0.1:5000/create-voting'  # 请根据实际情况修改URL

# 定义请求的头部
headers = {
    'Content-Type': 'application/json'
}

# 定义请求的负载
payload = {
    'voting_name': 'Sample Voting',
    'voting_description': 'This is a sample voting description.',
    'status': 'open',
    'created_by': 's1360912',  # 替换为你想要测试的用户ID
    'voting_options': [
        {
            'option_title': 'Option 1',
            'option_type': 'single',
            'option_list': [
                {'list_title': 'List Item 1'},
                {'list_title': 'List Item 2'}
            ]
        },
        {
            'option_title': 'Option 2',
            'option_type': 'multi',
            'option_list': [
                {'list_title': 'List Item 3'},
                {'list_title': 'List Item 4'}
            ]
        }
    ]
}

# 发送POST请求
response = requests.post(url, headers=headers, data=json.dumps(payload))

# 打印响应
print(f'Status Code: {response.status_code}')
print(f'Response JSON: {response.json()}')