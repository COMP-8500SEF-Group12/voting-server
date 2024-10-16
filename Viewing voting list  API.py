from flask import Flask, jsonify


# 创建Flask应用
app = Flask(__name__)


# 投票列表的数据
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


# 定义/voting-lists的GET API
@app.route('/voting-lists', methods=['GET'])
def get_voting_lists():
    # 返回包含投票信息的JSON数据
    return jsonify({"voting_lists": voting_data}), 200


# 运行应用
if __name__ == '__main__':
    app.run(debug=True)