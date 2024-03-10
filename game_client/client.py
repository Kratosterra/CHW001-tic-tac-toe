import time
from content.gameinstance import GameInstance

print("Welcome to the TicTacToe!\n--------------------------------------------------")

id_of_player = None
while id_of_player is None:
    try:
        id_of_player = int(input("Enter your id: "))
    except:
        print("Try again! Only numbers are allowed!")

print("Trying to connect to server...")

gameinstance = GameInstance(player_id=int(id_of_player))

status_of_connection = None

while status_of_connection != 202 and status_of_connection != 403:
    data = gameinstance.start()
    if data is None:
        print("Cant't connect to server! End of the game!")
        exit(1)
    status_of_connection = data.status_code
    match status_of_connection:
        case 202:
            print("You were connected to the existing session!")
        case 201:
            print("You created session, waiting for opponent...")
        case 403:
            print("Your opponent connected!")
    time.sleep(1)

print("Starting game!")
gameinstance.session = True
gameinstance.update()

state_of_input = 0
while gameinstance.session != False:
    if gameinstance.current_player == gameinstance.your_sign and state_of_input != 2:
        state_of_input = 1
    elif gameinstance.current_player != gameinstance.your_sign and state_of_input != 2:
        state_of_input = 0

    match state_of_input:
        case 1:
            gameinstance.display_board()
            print("1) Make a move\n"
                  "2) Watch leaderboard\n"
                  "3) Exit game")
            option = None
            while option is None or option not in [1, 2, 3]:
                try:
                    option = int(input("\nEnter your choice: "))
                except:
                    print("Try again! Only numbers 1-2 are allowed!")

            if option == 1:
                option = None
                while option is None or option not in range(1, 10):
                    try:
                        option = int(input("\nChoose cell: "))
                    except:
                        print("Try again! Only numbers 1-9 are allowed!")
                gameinstance.make_move(option-1)
            elif option == 3:
                print("Exiting game!")
                break
            else:
                state_of_input = 2

            gameinstance.update()
        case 0:
            gameinstance.display_board()
            print("Waiting for opponent move!\n")
            time.sleep(1)
            gameinstance.update()
        case 2:
            print("\n-------LEADERBOARD---------\n")
            gameinstance.display_leaderboard()
            print("\n------------END------------\n\n1) Return back\n")
            option = None
            while option is None or option != 1:
                try:
                    option = int(input("\nEnter your choice: "))
                except:
                    print("Try again! Only number 1 is allowed!")
            state_of_input = 0
            gameinstance.update()

print("GAME ENDED!\nThank you for playing!")