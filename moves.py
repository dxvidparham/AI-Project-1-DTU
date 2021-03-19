import kalaha


def capture_stones(gamestate, player, position):

    if player == "player 1":

        if gamestate.player2_board[position] != 0:
            gamestate.player1_kalaha += 1 + gamestate.player2_board[position]
            gamestate.player2_board[position] = 0
            return gamestate

        else:
            gamestate.player1_board[position] += 1
            return gamestate

    else:

        if gamestate.player1_board[position] != 0:
            gamestate.player2_kalaha += 1 + gamestate.player1_board[position]
            gamestate.player1_board[position] = 0
            return gamestate

        else:
            gamestate.player2_board[position] += 1
            return gamestate


def distribute_kalaha(gamestate, player, stones_left, origin):
    if player == "player 1":

        if player == origin:

            if stones_left == 1:
                gamestate.player1_kalaha += 1
                # kalaha.print_game_state(gamestate)
                # if not kalaha.check_if_goal_state(gamestate):
                #     print("\nThe last ball ended in the Kalaha. You're allowed to go again.")
                #     position = int(input("player 1s turn (0, 1, 2, 3, 4, 5) "))
                #     move(gamestate, player, position)
                # else:
                #     return gamestate
                return gamestate

            elif stones_left > 1:
                gamestate.player1_kalaha += 1
                position = 5
                player = "player 2"
                return distribute_stone_on_board(gamestate, player, position, stones_left - 1, origin="player 1")

            else:
                return gamestate

        else:
            position = 5
            player = "player 2"
            return distribute_stone_on_board(gamestate, player, position, stones_left, origin="player 1")

    elif player == "player 2":

        if player == origin:

            if stones_left == 1:
                gamestate.player2_kalaha += 1
                # kalaha.print_game_state(gamestate)
                # if not kalaha.check_if_goal_state(gamestate):
                #     print("\nThe last ball ended in the Kalaha. You're allowed to go again.")
                #     position = int(input("player 2s turn (0, 1, 2, 3, 4, 5) "))
                #     move(gamestate, player, position)
                # else:
                #     return gamestate
                return gamestate

            elif stones_left > 1:
                gamestate.player2_kalaha += 1
                position = 0
                player = "player 1"
                return distribute_stone_on_board(gamestate, player, position, stones_left - 1, origin="player 2")

            else:
                return gamestate

        else:
            position = 0
            player = "player 1"
            return distribute_stone_on_board(gamestate, player, position, stones_left, origin="player 2")

    else:
        print("fail")


def distribute_stone_on_board(gamestate, player, position, stones_left, origin):

    if player == "player 1":

        if stones_left == 1 and gamestate.player1_board[position] == 0 and player == origin:
            return capture_stones(gamestate, player, position)

        elif stones_left != 0 and position == 5:
            gamestate.player1_board[position] += 1
            return distribute_kalaha(gamestate, player, stones_left - 1, origin)

        elif stones_left != 0:
            gamestate.player1_board[position] += 1
            return distribute_stone_on_board(gamestate, player, position + 1, stones_left - 1, origin)

        else:
            return gamestate

    else:

        if stones_left == 1 and gamestate.player2_board[position] == 0 and player == origin:
            return capture_stones(gamestate, player, position)

        elif stones_left != 0 and position == 0:
            gamestate.player2_board[position] += 1
            return distribute_kalaha(gamestate, player, stones_left - 1, origin)

        elif stones_left == 1 and position == 5:
            gamestate.player2_board[position] += 1

        elif stones_left > 0 and position < 6:
            gamestate.player2_board[position] += 1
            return distribute_stone_on_board(gamestate, player, position - 1, stones_left - 1, origin)

        else:
            return gamestate


def move(gamestate, player, position):

    while True:
        if player == "player 1" and gamestate.player1_board[position] == 0 or player == "player 2" and gamestate.player2_board[position] == 0:
            position = int(input(f"\nPit {position} is already empty. Please choose another one: \n"))
        else:
            break

    if player == "player 1":

        if position == 5:
            stones_left = gamestate.player1_board[position]
            gamestate.player1_board[position] = 0
            return distribute_kalaha(gamestate, player, stones_left, origin="player 1")

        else:
            stones_left = gamestate.player1_board[position]
            gamestate.player1_board[position] = 0
            position += 1
            return distribute_stone_on_board(gamestate, player, position, stones_left, origin="player 1")

    elif player == "player 2":

        if position == 0:
            stones_left = gamestate.player2_board[position]
            gamestate.player2_board[position] = 0
            return distribute_kalaha(gamestate, player, stones_left, origin="player 2")

        else:
            stones_left = gamestate.player2_board[position]
            gamestate.player2_board[position] = 0
            position -= 1
            return distribute_stone_on_board(gamestate, player, position, stones_left, origin="player 2")

    else:
        return gamestate


def distribute_remaining(gamestate):

    remaining1 = sum(gamestate.player1_board)
    gamestate.player1_kalaha += remaining1
    remaining2 = sum(gamestate.player2_board)
    gamestate.player2_kalaha += remaining2
    print(f"\nRemaining stones added:\nPlayer 1 - {remaining1}\nPlayer 2 - {remaining2}\n")
    return gamestate

