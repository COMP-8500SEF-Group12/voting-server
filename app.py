from flask import Flask, jsonify, request

app = Flask(__name__)

voting_data = [
    {
        "voting_id": "1",
        "voting_name": "Select meeting location",
        "voting_date": "2024-10-15"
    },
    {
        "voting_id": "2",
        "voting_name": "Select meeting time",
        "voting_date": "2024-10-15"
    },
]

user_voting_records = {
    "s123456": {"voting_id": "1", "is_voted": False}
}

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
voting_success_detail = {
        "is_voted": True,
		"voting_id": "1",
		"voting_numbers": "10",
		"voting_name": "Voting for the location and time period",
		"voting_description": "Please participate in the voting",
		"voting_date": "2024/10/15",
		"voting_options": [
			 {
                "option_id": "1",
                "option_title": "Select meeting location",
                "option_type": "single",
                "option_list": [
                    {"list_id": "1", "list_title": "MC", "list_percentage": "30"},
                    {"list_id": "2", "list_title": "JCC" , "list_percentage": "40"},
                    {"list_id": "3", "list_title": "IOH", "list_percentage": "20"}
                ]
            },
            {
                "option_id": "2",
                "option_title": "Select meeting time",
                "option_type": "multi",
                "option_list": [
                    {"list_id": "1", "list_title": "9:00-12:00", "list_percentage": "50"},
                    {"list_id": "2", "list_title": "12:00-14:00" , "list_percentage": "30"},
                    {"list_id": "3", "list_title": "18:00-21:00" , "list_percentage": "20" }
                ]
            }
		]
		
	}
valid_voting_options = {
    "1": ["1", "2", "3"],
    "2": ["1", "2"]
}

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/voting-lists', methods=['GET'])
def get_voting_lists():
    return jsonify({"voting_lists": voting_data}), 200

@app.route('/voting-detail', methods=['GET'])
def view_voting_detail():
    # 获取传入的query参数
    voting_id = request.args.get('voting_id')
    user_id = request.args.get('user_id')


    # 检查isVoted
    user_vote_status = user_voting_records.get(user_id, {}).get("is_voted", False)
    if user_vote_status:
        return jsonify(voting_success_detail), 200
    else:
    # 如果存在，就返回结
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

@app.route('/vote', methods=['POST'])
def participate_voting():
    # 从请求体中获取用户提交的JSON数据
    data = request.get_json()

    # 提取相关数据
    user_id = data.get('user_id')
    user_nickname = data.get('user_nickname')
    voting_id = data.get('voting_id')
    votes = data.get('votes')
    print(user_id, user_nickname, voting_id, votes)
    # 验证请求数据的完整性
    if not user_id or not user_nickname or not voting_id or not votes:
        return jsonify({"error": "Invalid request data"}), 400

    # 验证投票ID是否有效
    if voting_id not in valid_voting_options:
        return jsonify({"error": "Invalid voting ID"}), 400

    # 把用户的投票记录改为 True
    user_voting_records[user_id] = {"voting_id": voting_id, "is_voted": True}
    
    # 返回成功响应
    return jsonify({"message": "Vote successfully recorded"}), 200




