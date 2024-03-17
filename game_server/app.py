from flask import Flask, request, jsonify
import time

from models.tic_tac_toe_game import TicTacToeGame
from models.session import Session
from models.data_manager import DataManager

app = Flask(__name__)

sessions = []
data_manager = DataManager()

INACTIVITY_TIMEOUT = 30


@app.route('/join_game', methods=['POST'])
def join_game():
    check_inactivity()

    player_id = request.json.get('player_id')

    for session in sessions:
        if player_id in (session.player1['player'], session.player2['player']):
            session.write_activity(player_id)
            if session.player1['player'] is not None and session.player2['player'] is not None:
                return jsonify({'message': 'Game is started! You are already in a game!'}), 403
            return jsonify({'message': 'Wait for opponent! You are already in a game!'}), 400

    for session in sessions:
        if session.player2['player'] is None:
            session.player2['player'] = player_id
            session.game = TicTacToeGame()
            session.write_activity(player_id)
            return jsonify({'message': 'Game started!'}), 202

    new_session = Session(player_id, None)
    sessions.append(new_session)
    new_session.write_activity(player_id)
    return jsonify({'message': 'Waiting for opponent to join...'}), 201


@app.route('/make_move', methods=['POST'])
def make_move():
    check_inactivity()

    player_id = request.json.get('player_id')
    position = request.json.get('position')

    now_session_index, now_player = find_session_and_player(player_id)

    if now_player is None or now_session_index is None:
        return jsonify({'message': 'You are not in a game or session ended!'}), 404

    session = sessions[now_session_index]
    session.write_activity(player_id)
    game_state = session.game

    match now_player:
        case 1:
            if game_state.current_player != session.player1['sign']:
                return jsonify({'message': 'It is not your turn!'}), 403

        case 2:
            if game_state.current_player != session.player2['sign']:
                return jsonify({'message': 'It is not your turn!'}), 403

    if game_state.make_move(position):
        if game_state.winner or game_state.is_draw:
            if game_state.winner != 'Draw':
                data_manager.update_score(player_id)
            winner = game_state.winner
            restart_game(session)
            return jsonify({'message': f'Player {winner} wins!' if winner != 'Draw' else 'It\'s a tie!'}), 205
        else:
            return jsonify({'message': 'Move successful'}), 200
    else:
        return jsonify({'message': 'Invalid move or game over!'}), 400


@app.route('/get_game_state', methods=['POST'])
def get_game_state():
    check_inactivity()

    player_id = request.json.get('player_id')

    now_session_index, now_player = find_session_and_player(player_id)

    if now_player is None or now_session_index is None:
        return jsonify({'message': 'You are not in a game or session ended!'}), 404

    session = sessions[now_session_index]
    session.write_activity(player_id)
    game_state = session.game

    match now_player:
        case 1:
            return jsonify({
                'you': session.player1['sign'],
                'board': game_state.board,
                'current_player': game_state.current_player,
                'your_score': data_manager.get_scores(session.player1['player']),
                'opponent_score': data_manager.get_scores(session.player2['player']),
            }), 200
        case 2:
            return jsonify({
                'you': session.player2['sign'],
                'board': game_state.board,
                'current_player': game_state.current_player,
                'your_score': data_manager.get_scores(session.player2['player']),
                'opponent_score': data_manager.get_scores(session.player1['player']),
            }), 200

    return jsonify({'message': 'Unknown player!'}), 403


def check_inactivity():
    current_time = time.time()

    inactive_players = []
    for session in sessions:
        last_activity_1 = session.player1['last_activity']
        last_activity_2 = session.player2['last_activity']
        if current_time - last_activity_1 > INACTIVITY_TIMEOUT:
            inactive_players.append(session.player1)
        if current_time - last_activity_2 > INACTIVITY_TIMEOUT:
            inactive_players.append(session.player2)

        print(f"Player 1 id: {session.player1['player']} | last activity: {current_time - last_activity_1}")
        print(f"Player 2 id: {session.player2['player']} | last activity: {current_time - last_activity_2}")
    for player_id in inactive_players:
        index = 0
        for session in sessions:
            if player_id == session.player1:
                print(f"Player {session.player1['player']} has been disconnected due to inactivity. Session ended!")
                del sessions[index]
            elif player_id == session.player2:
                print(f"Player {session.player2['player']} has been disconnected due to inactivity. Session ended!")
                del sessions[index]
            index += 1


def restart_game(session):
    print(f"[{session}] Game restarted...")
    session.game.reset()


def find_session_and_player(player_id):
    now_player = None
    now_session_index = None
    for session in sessions:
        if player_id == session.player1['player']:
            now_player = 1
            now_session_index = sessions.index(session)
            break
        elif player_id == session.player2['player']:
            now_player = 2
            now_session_index = sessions.index(session)
            break
    return now_session_index, now_player


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
