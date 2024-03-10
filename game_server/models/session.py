import time

from models.tic_tac_toe_game import TicTacToeGame


class Session:
    def __init__(self, player1, player2, game = None):
        self.player1 = {"player": player1, "last_activity": time.time(), "sign": "X"}
        self.player2 = {"player": player2, "last_activity": time.time(), "sign": "O"}
        self.game = game

    def write_activity(self, player):
        if self.player1["player"] == player:
            self.player1["last_activity"] = time.time()
        elif self.player2["player"] == player:
            self.player2["last_activity"] = time.time()