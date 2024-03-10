import sqlite3
import requests


class DataManager:

    def __init__(self):
        self.conn = sqlite3.connect('./database/tictactoe.db', check_same_thread=False)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS scores (player_id TEXT PRIMARY KEY, wins INTEGER)''')
        self.conn.commit()

    def update_score(self, player_id):
        self.c.execute('''INSERT OR IGNORE INTO scores (player_id, wins) VALUES (?, 0)''', (player_id,))
        self.c.execute('''UPDATE scores SET wins = wins + 1 WHERE player_id = ?''', (player_id,))
        self.conn.commit()

        url = 'http://localhost:8000/update_score'
        data = {'player_id': player_id, 'score': 1}
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print(f'Score updated for player {player_id} in remote application.')
            else:
                print(f'Failed to update score for player {player_id} in remote application.')
        except Exception as e:
            print(f'Failed to update score for player {player_id} in remote application.')

    def get_scores(self, player_id):
        self.c.execute('''SELECT wins FROM scores WHERE player_id = ?''', (player_id, ))
        scores = self.c.fetchall()

        if scores is not None and len(scores) != 0:
            return scores[0][0]
        else:
            return 0
