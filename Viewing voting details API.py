from flask import Flask, jsonify, request

# 创建Flask应用
app = Flask(__name__)

# 投票详情数据
voting_details_data = {
    "1": {
        "voting_id": "1",
        "voting_name": "Voting for the location and time period",
        "voting_description": "Please participate in the voting",
        "voting_date": "2024/10/15",
        "voting_options": [
            {
                "option_id": "1",
                "option_title": "Select meeting location",
                "option_type": "single",
                "option_list": [
                    {"list_id": "1", "list_title": "MC"},
                    {"list_id": "2", "list_title": "JCC"},
                    {"list_id": "3", "list_title": "IOH"}
                ]
            },
            {
                "option_id": "2",
                "option_title": "Select meeting time",
                "option_type": "multi",
                "option_list": [
                    {"list_id": "1", "list_title": "9:00-12:00"},
                    {"list_id": "2", "list_title": "12:00-14:00"},
                    {"list_id": "3", "list_title": "18:00-21:00"}
                ]
            }
        ]
    }
}

# 假数据：用户投票记录
user_voting_records = {
    "s123456": {"voting_id": "1", "is_voted": False}
}

# 定义“Viewing voting details” API
@app.route('/voting-detail', methods=['GET'])
def view_voting_detail():
    # 获取传入的query参数
    voting_id = request.args.get('voting_id')
    user_id = request.args.get('user_id')

    # 检查用户是否存在投票记录
    user_vote_status = user_voting_records.get(user_id, {}).get("is_voted", False)

    # 检查投票详情是否存在
    voting_detail = voting_details_data.get(voting_id)

    if voting_detail:
        # 构建返回的JSON数据
        response_data = {
            "is_voted": user_vote_status,
            "voting_id": voting_detail["voting_id"],
            "voting_name": voting_detail["voting_name"],
            "voting_description": voting_detail["voting_description"],
            "voting_date": voting_detail["voting_date"],
            "voting_options": voting_detail["voting_options"]
        }
        return jsonify(response_data), 200
    else:
        # 如果没有找到对应的投票，返回404错误
        return jsonify({"error": "Voting not found"}), 404

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)