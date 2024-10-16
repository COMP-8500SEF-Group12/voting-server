from flask import Flask, request, jsonify

# 创建Flask应用
app = Flask(__name__)

# 假设的数据库，记录用户投票的状态
user_voting_records = {}

# 假设的投票选项（仅为示例用途）
valid_voting_options = {
    "1": ["1", "2", "3"],  # 投票ID 1 对应的选项ID列表
    "2": ["1", "2"]  # 投票ID 2 对应的选项ID列表
}

# 定义“参与投票”API
@app.route('/vote', methods=['POST'])
def participate_voting():
    # 从请求体中获取用户提交的JSON数据
    data = request.get_json()

    # 提取相关数据
    user_id = data.get('user_id')
    user_nickname = data.get('user_nickname')
    voting_id = data.get('voting_id')
    votes = data.get('votes')

    # 验证请求数据的完整性
    if not user_id or not user_nickname or not voting_id or not votes:
        return jsonify({"error": "Invalid request data"}), 400

    # 验证投票ID是否有效
    if voting_id not in valid_voting_options:
        return jsonify({"error": "Invalid voting ID"}), 400

    # 处理用户的投票选项
    for vote in votes:
        option_id = vote.get('option_id')
        option_value = vote.get('option_value')

        # 验证选项ID是否在合法的选项列表中
        if option_id not in valid_voting_options[voting_id]:
            return jsonify({"error": f"Invalid option ID {option_id} for voting ID {voting_id}"}), 400

        # 存储用户投票信息
        # 假设这里我们将投票记录保存在user_voting_records中
        if user_id not in user_voting_records:
            user_voting_records[user_id] = []

        user_voting_records[user_id].append({
            "voting_id": voting_id,
            "option_id": option_id,
            "option_value": option_value
        })

    # 返回成功响应
    return jsonify({"message": "Vote successfully recorded"}), 200

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
