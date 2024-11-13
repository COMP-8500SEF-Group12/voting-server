from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from db_config import get_db_connection
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# API-1
# 用户登录

@app.route('/login', methods=['POST'])
def login():
    user_id = request.json.get('user_id')

    if not user_id:
        return jsonify({'user_id': None, 'status': 0, 'message': 'User ID is required'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute('SELECT user_id FROM Users WHERE user_id = %s', (user_id,))
        user = cur.fetchone()

        if user:
            return jsonify({'user_id': user_id, 'status': 1,'message':''})
        else:
            return jsonify({'user_id': user_id, 'status': 0,'message':''})
    except Exception as e:
        return jsonify({'user_id': user_id, 'status': 0, 'message': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# API-2
# 创建投票

@app.route('/create-voting', methods=['POST'])
def create_voting():
    data = request.json

    voting_name = data.get('voting_name')
    voting_description = data.get('voting_description')
    status = data.get('status')
    created_by = data.get('created_by')
    voting_options = data.get('voting_options', [])

    if not all([voting_name, voting_description, status, created_by]):
        return jsonify({'message': 'Missing required fields'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # 插入投票记录
        cur.execute('''
            INSERT INTO Votings (voting_name, voting_description, voting_date, status, created_at, updated_at, create_user_id,delete_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING voting_id
        ''', (
        voting_name, voting_description, datetime.now().date(), status, datetime.now(), datetime.now(), created_by,'N'))

        voting_id = cur.fetchone()[0]

        # 插入投票选项和选项列表
        for option in voting_options:
            option_title = option.get('option_title')
            option_type = option.get('option_type')
            option_list = option.get('option_list', [])

            if not all([option_title, option_type]):
                return jsonify({'message': 'Missing required fields in voting options'}), 400

            cur.execute('''
                INSERT INTO VotingOptions (voting_id, option_title, option_type, created_at)
                VALUES (%s, %s, %s, %s) RETURNING option_id
            ''', (voting_id, option_title, option_type, datetime.now()))

            option_id = cur.fetchone()[0]

            for list_item in option_list:
                list_title = list_item.get('list_title')

                if not list_title:
                    return jsonify({'message': 'Missing required fields in option list'}), 400

                cur.execute('''
                    INSERT INTO OptionList (option_id, list_title, created_at)
                    VALUES (%s, %s, %s)
                ''', (option_id, list_title, datetime.now()))

        conn.commit()

        return jsonify({'message': 'Voting created successfully', 'voting_id': voting_id}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'message': str(e)}), 500
    finally:
        cur.close()
        conn.close()



# API-3
# 用户查看投票列表
@app.route('/voting-lists', methods=['POST'])
def voting_lists():
    print(11111111111111)
    if request.method == 'GET':
        user_id = request.args.get('user_id')
    elif request.method == 'POST':
        data = request.json
        user_id = data.get('user_id')
    if not user_id:
        return jsonify({'message': 'User ID is required'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # 检查用户是否有投票权限
        cur.execute('SELECT has_vote_permission FROM Users WHERE user_id = %s', (user_id,))
        user = cur.fetchone()
        print(user)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        is_has_authority = user[0]

        # 获取投票列表
        cur.execute('''
            SELECT voting_id, voting_name, voting_date, create_user_id
            FROM Votings
        ''')
        votings = cur.fetchall()
        print(votings)
        voting_lists = []
        for voting in votings:
            voting_lists.append({
                'voting_id': voting[0],
                'voting_name': voting[1],
                'voting_date': voting[2].strftime('%Y-%m-%d'),
                'is_auth_delete': voting[3] == user_id
            })

        return jsonify({
            'voting_lists': voting_lists,
            'is_has_authority': is_has_authority
        })
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# API-4
# 删除投票

@app.route('/delete-voting', methods=['POST'])
def delete_voting():
    data = request.json
    user_id = data.get('user_id')
    voting_id = data.get('voting_id')

    if not user_id or not voting_id:
        return jsonify({'message': 'User ID and Voting ID are required'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # 检查投票是否存在并验证创建者
        cur.execute('SELECT * FROM Votings WHERE voting_id = %s AND create_user_id = %s', (voting_id, user_id))
        voting = cur.fetchone()

        if not voting:
            return jsonify({'message': 'Voting not found or unauthorized'}), 404

        # 更新delete_status
        cur.execute(
            'UPDATE Votings SET delete_status = %s, updated_at = %s WHERE voting_id = %s',
            ('Y', datetime.utcnow(), voting_id)
        )
        conn.commit()

        return jsonify({'message': 'Voting marked as deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# API-7
# 查看投票结果

@app.route('/voting-result', methods=['GET', 'POST'])
def get_vote_results():
    if request.method == 'POST':
        data = request.get_json()
        voting_id = data.get('voting_id')
        user_id = data.get('user_id')  # 假设 user_id 也需要处理
    elif request.method == 'GET':
        voting_id = request.args.get('voting_id')
        user_id = request.args.get('user_id')  # 假设 user_id 也需要处理

    if not voting_id:
        return jsonify({"error": "voting_id is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        query = """
        SELECT result_id, voting_id, option_id, list_id, vote_count, list_percentage, last_updated
        FROM VoteResults
        WHERE voting_id = %s
        """
        cur.execute(query, (voting_id,))
        results = cur.fetchall()

        results_dict = []
        for result in results:
            results_dict.append({
                'result_id': result[0],
                'voting_id': result[1],
                'option_id': result[2],
                'list_id': result[3],
                'vote_count': result[4],
                'list_percentage': result[5],
                'last_updated': result[6].strftime('%Y-%m-%d %H:%M:%S')
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify(results_dict), 200

# API-5
# 投票
@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    data = request.get_json()
    user_id = data.get('user_id')
    voting_id = data.get('voting_id')
    votes = data.get('votes')

    if not user_id or not voting_id or not votes:
        return jsonify({"error": "user_id, voting_id, and votes are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 检查用户是否已经投票
        cursor.execute("""
            SELECT COUNT(*) FROM Votes
            WHERE user_id = %s AND voting_id = %s AND is_voted = TRUE
        """, (user_id, voting_id))
        vote_count = cursor.fetchone()[0]

        if vote_count > 0:
            return jsonify({"error": "User has already voted"}), 400

        # 插入投票记录
        for vote in votes:
            option_id = vote.get('option_id')
            option_values = vote.get('option_value')

            if isinstance(option_values, str):
                option_values = [option_values]

            for list_id in option_values:
                # 确保 list_id 是整数类型
                try:
                    list_id = int(list_id)
                except ValueError:
                    return jsonify({"error": f"Invalid list_id: {list_id}. It must be an integer."}), 400

                cursor.execute("""
                    INSERT INTO Votes (user_id, voting_id, option_id, list_id, is_voted, vote_date, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (user_id, voting_id, option_id, list_id, True, datetime.now(), datetime.now()))

                # 更新 VoteResults 表
                cursor.execute("""
                    INSERT INTO VoteResults (voting_id, option_id, list_id, vote_count, last_updated)
                    VALUES (%s, %s, %s, 1, %s)
                    ON CONFLICT (voting_id, option_id, list_id)
                    DO UPDATE SET vote_count = VoteResults.vote_count + 1, last_updated = %s
                """, (voting_id, option_id, list_id, datetime.now(), datetime.now()))

        # 更新列表百分比
        cursor.execute("""
            SELECT option_id, list_id, SUM(vote_count) as total_votes
            FROM VoteResults
            WHERE voting_id = %s
            GROUP BY option_id, list_id
        """, (voting_id,))
        results = cursor.fetchall()

        for result in results:
            option_id = result[0]
            list_id = result[1]
            total_votes = result[2]

            cursor.execute("""
                SELECT SUM(vote_count) FROM VoteResults WHERE voting_id = %s AND option_id = %s
            """, (voting_id, option_id))
            option_total_votes = cursor.fetchone()[0]

            list_percentage = (total_votes / option_total_votes) * 100 if option_total_votes else 0

            cursor.execute("""
                UPDATE VoteResults
                SET list_percentage = %s
                WHERE voting_id = %s AND option_id = %s AND list_id = %s
            """, (list_percentage, voting_id, option_id, list_id))

        conn.commit()

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Vote submitted successfully"}), 200


# API-6
# 查看具体某个投票
@app.route('/voting-detail', methods=['GET', 'POST'])
def get_voting_info():
    if request.method == 'POST':
        data = request.get_json()
        voting_id = data.get('voting_id')
        user_id = data.get('user_id')
    elif request.method == 'GET':
        voting_id = request.args.get('voting_id')
        user_id = request.args.get('user_id')

    if not voting_id or not user_id:
        return jsonify({"error": "voting_id and user_id are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # 查询用户是否已经投票
    cursor.execute("""
        SELECT COUNT(*) FROM Votes
        WHERE user_id = %s AND voting_id = %s AND is_voted = TRUE
    """, (user_id, voting_id))
    vote_count = cursor.fetchone()[0]

    is_voted = vote_count > 0


    try:
        # 查询投票信息
        cursor.execute("""
            SELECT voting_id, voting_name, voting_description, voting_date
            FROM Votings
            WHERE voting_id = %s
        """, (voting_id,))
        voting_info = cursor.fetchone()

        if not voting_info:
            return jsonify({"error": "Voting not found"}), 404

        # 查询投票选项和选项列表
        cursor.execute("""
            SELECT vo.option_id, vo.option_title, vo.option_type, ol.list_id, ol.list_title
            FROM VotingOptions vo
            JOIN OptionList ol ON vo.option_id = ol.option_id
            WHERE vo.voting_id = %s
        """, (voting_id,))
        options = cursor.fetchall()

        # 构建返回的 JSON 数据
        voting_data = {
            "is_voted": is_voted,
            "voting_id": voting_info[0],
            "voting_name": voting_info[1],
            "voting_description": voting_info[2],
            "voting_date": voting_info[3].strftime('%Y 年 %m 月 %d 日'),
            "voting_options": []
        }
        option_dict = {}
        for option in options:
            option_id = option[0]
            if option_id not in option_dict:
                option_dict[option_id] = {
                    "option_id": option_id,
                    "option_title": option[1],
                    "option_type": option[2],
                    "option_list": []
                }
            option_dict[option_id]["option_list"].append({
                "list_id": option[3],
                "list_title": option[4]
            })

        voting_data["voting_options"] = list(option_dict.values())

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify(voting_data), 200


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000), host='0.0.0.0')




