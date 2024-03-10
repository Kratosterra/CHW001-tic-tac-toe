import sqlite3


class LeaderboardManager:
    def __init__(self):
        self.conn = sqlite3.connect('./database/leaderboard.db', check_same_thread=False)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS leaderboard (player_id TEXT PRIMARY KEY, score INTEGER)''')
        self.conn.commit()

    def get_leaderboard(self):
        self.c.execute('''SELECT * FROM leaderboard ORDER BY score DESC''')
        leaderboard = self.c.fetchall()
        return leaderboard

    def update_score(self, player_id, score):
        self.c.execute('''INSERT OR IGNORE INTO leaderboard (player_id, score) VALUES (?, ?)''', (player_id, score))
        self.c.execute('''UPDATE leaderboard SET score = score + ? WHERE player_id = ?''', (score, player_id))
        self.conn.commit()
