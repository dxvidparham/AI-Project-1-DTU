#!/usr/bin/env python3
######################################################################
# Authors:  - Ole Martin Soerensen <s165495>,
#           - Bence Bejczy <s202821>,
#           - Rian Leevinson <s202540>,
#           - David Parham <s202385>
# Course: Introduction to Artificial Intelligence
# Spring 2021
# Technical University of Denmark (DTU)
######################################################################


def capture_stones(gamestate, player, position):

    if player == "player 1":

        if gamestate.player2_board[position] != 0:
            gamestate.player1_kalaha += 1 + gamestate.player2_board[position]
            gamestate.player2_board[position] = 0
        else:
            gamestate.player1_board[position] += 1
    else:

        if gamestate.player1_board[position] != 0:
            gamestate.player2_kalaha += 1 + gamestate.player1_board[position]
            gamestate.player1_board[position] = 0
        else:
            gamestate.player2_board[position] += 1

    return gamestate


def distribute_kalaha(gamestate, player, stones_left, origin):

    if player == "player 1":

        if player == origin:
            if stones_left == 1:
                gamestate.player1_kalaha += 1
                gamestate.go_again = True
                return gamestate

            elif stones_left > 1:
                gamestate.player1_kalaha += 1
                position = 5
                player = "player 2"
                return distribute_stone_on_board(
                    gamestate, player, position, stones_left - 1, "player 1"
                )

            else:
                return gamestate

        else:
            position = 5
            player = "player 2"
            return distribute_stone_on_board(
                gamestate, player, position, stones_left, "player 1"
            )

    elif player == "player 2":

        if player == origin:
            if stones_left == 1:
                gamestate.player2_kalaha += 1
                gamestate.go_again = True
                return {"state": gamestate, "go-again": True}

            elif stones_left > 1:
                gamestate.player2_kalaha += 1
                position = 0
                player = "player 1"
                return distribute_stone_on_board(
                    gamestate, player, position, stones_left - 1, "player 2"
                )

            else:
                return gamestate

        else:
            position = 0
            player = "player 1"
            return distribute_stone_on_board(
                gamestate, player, position, stones_left, "player 2"
            )


def distribute_stone_on_board(gamestate, player, position, stones_left, origin):

    if player == "player 1":

        if (
            stones_left == 1
            and gamestate.player1_board[position] == 0
            and player == origin
        ):
            return capture_stones(gamestate, player, position)

        elif stones_left != 0 and position == 5:
            gamestate.player1_board[position] += 1
            return distribute_kalaha(gamestate, player, stones_left - 1, origin)

        elif stones_left != 0:
            gamestate.player1_board[position] += 1
            return distribute_stone_on_board(
                gamestate, player, position + 1, stones_left - 1, origin
            )

        else:
            return gamestate

    else:

        if (
            stones_left == 1
            and gamestate.player2_board[position] == 0
            and player == origin
        ):
            return capture_stones(gamestate, player, position)

        elif stones_left != 0 and position == 0:
            gamestate.player2_board[position] += 1
            return distribute_kalaha(gamestate, player, stones_left - 1, origin)

        elif stones_left == 1 and position == 5:
            gamestate.player2_board[position] += 1

        elif stones_left > 0 and position < 6:
            gamestate.player2_board[position] += 1
            return distribute_stone_on_board(
                gamestate, player, position - 1, stones_left - 1, origin
            )

        else:
            return gamestate


def valid_move(gamestate, player, position):
    # I guess we can assume that the search algorithm never enters this function.
    # Therefore, this function can be removed when we have two agents play agents
    # each other

    while True:
        try:
            if player != "player 2" or gamestate.player2_board[position] != 0:
                return position
            position = int(
                input(
                    f"\nPit {position} is already empty. Please choose another one: \n"
                )
            )
            if position not in range(6):
                raise IndexError
        except IndexError:
            position = int(
                input("\nTry again: Please insert a number between 0 and 5: ")
            )


def move_player1(gamestate, player, position):
    stones_left = gamestate.player1_board[position]
    if position == 5:
        gamestate.player1_board[position] = 0
        return distribute_kalaha(gamestate, player, stones_left, "player 1")

    else:
        gamestate.player1_board[position] = 0
        position += 1
        return distribute_stone_on_board(
            gamestate, player, position, stones_left, "player 1"
        )


def move_player2(gamestate, player, position):
    stones_left = gamestate.player2_board[position]
    if position == 0:
        gamestate.player2_board[position] = 0
        return distribute_kalaha(gamestate, player, stones_left, "player 2")

    else:
        gamestate.player2_board[position] = 0
        position -= 1
        return distribute_stone_on_board(
            gamestate, player, position, stones_left, "player 2"
        )


def move(gamestate, player, position):
    position = valid_move(gamestate, player, position)

    if player == "player 1":
        return move_player1(gamestate, player, position)

    else:
        return move_player2(gamestate, player, position)


def distribute_remaining(gamestate):
    remaining1 = sum(gamestate.player1_board)
    gamestate.player1_kalaha += remaining1

    remaining2 = sum(gamestate.player2_board)
    gamestate.player2_kalaha += remaining2

    print(
        f"\nRemaining stones added:\nPlayer 1 - {remaining1}\nPlayer 2 - {remaining2}\n"
    )
    return gamestate
