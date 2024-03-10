class TicTacToeGame:
    def __init__(self):
        self.board = [' '] * 9
        self.current_player = 'X'
        self.winner = None
        self.is_draw = False

    def make_move(self, position: int) -> bool:
        if self.board[position] == ' ' and not self.winner:
            self.board[position] = self.current_player
            self.check_winner()
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self) -> None:
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for i, j, k in winning_combinations:
            if self.board[i] == self.board[j] == self.board[k] != ' ':
                self.winner = self.board[i]
                return

        if ' ' not in self.board:
            self.winner = 'Draw'
            self.is_draw = True

    def reset(self) -> None:
        self.board = [' '] * 9
        self.current_player = 'X'
        self.winner = None