import time
from content.gameinstance import GameInstance


def input_int(input_comment, error_message, allowed_numbers):
    num = None
    while num is None or num not in allowed_numbers:
        try:
            num = int(input(input_comment))
        except:
            print(error_message)
    return num


def start_game():
    print("Welcome to the TicTacToe!\n--------------------------------------------------")
    id_of_player = input_int("What is your id: ", "Only numbers are allowed", range(1, 999999))
    print("Trying to connect to server...")
    return id_of_player


def connect_to_server():
    data = gameinstance.start()
    if data is None:
        exit(1)
    status_of_connection = data.status_code
    match status_of_connection:
        case 202:
            print("You were connected to the existing session!")
        case 201:
            print("You created session, waiting for opponent...")
        case 403:
            print("Your opponent connected!")
    return status_of_connection


def create_match():
    status_of_connection = None
    while status_of_connection != 202 and status_of_connection != 403:
        status_of_connection = connect_to_server()
        time.sleep(1)
    print("Starting game!")


def match():
    state_of_input = 0
    while gameinstance.session:
        time.sleep(1)
        gameinstance.update()

        if gameinstance.current_player == gameinstance.your_sign and state_of_input != 2:
            state_of_input = 1
        elif gameinstance.current_player != gameinstance.your_sign and state_of_input != 2:
            state_of_input = 0

        match state_of_input:
            case 1:
                gameinstance.display_board()
                print("Now is your turn. Loading...")
                time.sleep(2)
                gameinstance.update()
                if gameinstance.current_player == gameinstance.your_sign:
                    gameinstance.display_board()
                    print("1) Make a move\n"
                          "2) Watch leaderboard\n"
                          "3) Exit game")
                    option = input_int("\nEnter your choice: ", "Try again! Only numbers 1-3 are allowed!", [1, 2, 3])
                    if option == 1:
                        option = input_int("\nChoose cell: ", "Try again! Only numbers 1-9 are allowed!", range(1, 10))
                        gameinstance.make_move(option - 1)
                    elif option == 3:
                        break
                    else:
                        state_of_input = 2
                else:
                    print("Game ended.\nRESTARTING OF GAME!")
            case 0:
                gameinstance.display_board()
                print("Waiting for opponent move!\n")
            case 2:
                print("\n-------LEADERBOARD---------\n")
                gameinstance.display_leaderboard()
                print("\n------------END------------\n\n1) Return back\n")
                input_int("\nEnter your choice: ", "Try again! Only number 1 is allowed!", [1])
                state_of_input = 0
    print("GAME ENDED!\nThank you for playing!")


id_of_player = start_game()
gameinstance = GameInstance(player_id=int(id_of_player))
create_match()
gameinstance.session = True
gameinstance.update()
match()
