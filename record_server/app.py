from flask import Flask, request, jsonify

from models.leaderboard_manager import LeaderboardManager

app = Flask(__name__)

leaderboard_manager = LeaderboardManager()

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    leaderboard = leaderboard_manager.get_leaderboard()
    return jsonify(leaderboard)

@app.route('/update_score', methods=['POST'])
def update_score():
    player_id = request.json.get('player_id')
    score = request.json.get('score')
    leaderboard_manager.update_score(player_id, score)
    return jsonify({'message': f'Score updated for player {player_id}.'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
