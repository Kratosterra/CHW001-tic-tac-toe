class Board:
    def __init__(self):
        self.board = [' '] * 9

    def display(self):
        print("-------------")
        for i in range(0, 9, 3):
            print(f"| {self.board[i]} | {self.board[i + 1]} | {self.board[i + 2]} |")
            print("-------------")
