import requests

from content.board import Board


class GameInstance:
    def __init__(self, player_id):
        self.player_id = player_id
        self.current_player = None
        self.your_sign = None
        self.your_score = None
        self.opponent_score = None
        self.board = Board()
        self.session = False


    def start(self):
        data = self._auntification()
        if data is None:
            print("Game server is not available!")
            return None
        else:
            return data

    def make_move(self, position):
        try:
            url = 'http://localhost:5000/make_move'
            data = {'player_id': self.player_id, 'position': position}
            response = requests.post(url, json=data)
            match response.status_code:
                case 200:
                    print("Move successful!")
                    return dict(response.json())
                case 205:
                    print(dict(response.json())['message'])
                    print("RESTARTING GAME!")
                    return dict(response.json())['message']
                case 403:
                    print(f'It is not your turn!')
                    return None
                case 404:
                    print(f'You are not in a game or session ended!')
                    self.session = False
                    return None
                case 400:
                    print(f'Invalid move!')
                    return None
                case _:
                    print(f'Failed to update.')
                    self.session = False
                    return None
        except Exception as e:
            print(f'Error on connecting to remote application.\n{e}.')
            self.session = False
            return None

    def display_board(self):
        print(f"-------------------------------\nYOUR SIGN: {self.your_sign}\nNOW TURN OF {self.current_player}\n"
              f"--------------------------------")
        print(f"SCORE\nYOU {self.your_score} VS {self.opponent_score} OPPONENT\n-------------------------------")

        self.board.display()
        print("----------------------------")

    def update(self):
        data = self._get_data()
        if data is not None:
            self.current_player = data['current_player']
            self.board.board = data['board']
            self.your_score = data['your_score']
            self.opponent_score = data['opponent_score']
            self.your_sign = data['you']
            self.session = True
        else:
            print("Session ended!")
            self.session = False

    def display_leaderboard(self):
        try:
            response = requests.get('http://127.0.0.1:8000/leaderboard')
            if response.status_code == 200:
                leaderboard = list(response.json())
                if len(leaderboard) != 0:
                    index = 1
                    for value in leaderboard:
                        if value[0] == self.player_id:
                            print(f"{index}) YOU: {value[1]}")
                        else:
                            print(f"{index}) Player {value[0]}: {value[1]}")
            else:
                print("Something went wrong while getting leaderboard!")
        except Exception as e:
            print("Do not connected to leaderboard server!")

    def _get_data(self):
        try:
            url = 'http://localhost:5000/get_game_state'
            data = {'player_id': self.player_id}
            response = requests.post(url, json=data)
            match response.status_code:
                case 200:
                    return dict(response.json())
                case 404:
                    print(f'You are not in a game or session ended!')
                    self.session = False
                    return None
                case _:
                    print(f'Failed to update.')
                    self.session = False
                    return None
        except Exception as e:
            print(f'Error on connecting to remote application.\n.')
            self.session = False
            return None

    def _auntification(self):
        try:
            url = 'http://127.0.0.1:5000/join_game'
            data = {'player_id': self.player_id}
            response = requests.post(url, json=data)
            return response
        except Exception as e:
            print(f'Error on connecting to remote application.\n.')
            self.session = False
            return None