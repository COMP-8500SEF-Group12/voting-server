from flask import Flask, jsonify, request

# 创建Flask应用
app = Flask(__name__)

# 投票结果详情
voting_results_data = {
    "1": {
        "voting_id": "1",
        "voting_name": "Voting for the location and time period",
        "voting_description": "Vote",
        "voting_date": "2024/10/14",
        "voting_numbers": 10,  # 投票总人数
        "voting_options": [
            {
                "option_id": "1",
                "option_title": "Select meeting location",
                "option_type": "single",
                "option_text": None,
                "option_list": [
                    {"list_id": "1", "list_title": "MC", "list_percentage": "40%"},
                    {"list_id": "2", "list_title": "JCC", "list_percentage": "35%"},
                    {"list_id": "3", "list_title": "IOH", "list_percentage": "25%"}
                ]
            },
            {
                "option_id": "2",
                "option_title": "Select meeting time",
                "option_type": "multi",
                "option_text": None,
                "option_list": [
                    {"list_id": "1", "list_title": "13:00-14:00", "list_percentage": "15%"},
                    {"list_id": "2", "list_title": "14:00-15:00", "list_percentage": "30%"},
                    {"list_id": "3", "list_title": "15:00-16:00", "list_percentage": "20%"},
                    {"list_id": "4", "list_title": "16:00-17:00", "list_percentage": "15%"},
                    {"list_id": "5", "list_title": "17:00-18:00", "list_percentage": "10%"},
                    {"list_id": "6", "list_title": "18:00-19:00", "list_percentage": "10%"}
                ]
            },
            {
                "option_id": "3",
                "option_title": "Comments",
                "option_type": "text",
                "option_text": "User's comments",
                "option_list": []
            }
        ]
    }
}

# 定义“查看投票结果”API
@app.route('/voting-result', methods=['GET'])
def get_voting_result():
    # 获取传入的query参数
    voting_id = request.args.get('voting_id')
    user_id = request.args.get('user_id')

    # 验证voting_id是否存在
    voting_result = voting_results_data.get(voting_id)

    if voting_result:
        # 构建返回的JSON数据
        response_data = {
            "voting_id": voting_result["voting_id"],
            "voting_numbers": voting_result["voting_numbers"],
            "voting_name": voting_result["voting_name"],
            "voting_description": voting_result["voting_description"],
            "voting_date": voting_result["voting_date"],
            "voting_options": voting_result["voting_options"]
        }
        return jsonify(response_data), 200
    else:
        # 如果没有找到对应的投票，返回404错误
        return jsonify({"error": "Voting result not found"}), 404

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
