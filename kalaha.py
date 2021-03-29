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

import sys
from time import sleep
from loguru import logger

import algorithm2
import algorithm
import game_state
import moves


def print_game_state(gamestate):

    return f"""
                 Current game state:
        {gamestate.player2_kalaha}
   Player 2:    {gamestate.player2_board}
                {gamestate.player1_board}      Player 1:
                                            {gamestate.player1_kalaha}"""


def check_if_goal_state(gamestate):
    return all(i == 0 for i in gamestate.player1_board) or not any(
        j != 0 for j in gamestate.player2_board
    )


def ai_turn(game, player, depth):

    if player == "player 1":
        best_move = algorithm.minimax(game, depth, float("-inf"), float("inf"), True)[1]

    else:
        best_move = algorithm.minimax(game, depth, float("-inf"), float("inf"), False)[1]

    moves.move(game, player, best_move)
    print(f"{player} made his move: {best_move}")
    logger.info(print_game_state(game))
    sleep(2)

    if game.go_again and not check_if_goal_state(game):
        print(f"\nThe last ball ended in the Kalaha. {player} is allowed to go again.")
        game.go_again = False
        return ai_turn(game, player, depth)


def player_turn(game, player):

    try:
        raw_input = int(input(f"{player}s turn (0, 1, 2, 3, 4, 5) "))
        if raw_input not in range(6):
            raise ValueError
    except ValueError:
        print("\nTry again: Please insert a number between 0 and 5")
        return player_turn(game, player)

    move = moves.move(game, player, raw_input)

    try:

        if check_if_goal_state(game):
            raise AttributeError

        if game.go_again:
            game.go_again = False
            logger.info(print_game_state(game))
            print("\nThe last ball ended in the Kalaha. You're allowed to go again.")
            return player_turn(game, player)

    except AttributeError:
        logger.info(print_game_state(game))
        return


def evaluate_game(game):

    moves.distribute_remaining(game)

    if game.player1_kalaha > game.player2_kalaha:
        print("The Winner is:   Player 1!!!")

    elif game.player1_kalaha < game.player2_kalaha:
        print("The Winner is:   Player 2!!!")

    else:
        print("We got a draw!")

    print(f"Score: [P2] {game.player2_kalaha}:{game.player1_kalaha} [P1]")


@logger.catch
def main():

    game = game_state.GameState()
    raw_input = input("Welcome to a dumb implementation of Kalaha. Are you ready? y/n ")

    if raw_input.lower() == "y":

        game_mode = int(input("What game mode would you like? 1: ai vs. ai, 2: player vs. ai, 3: ai vs. player? (1, 2, 3)"))

        if game_mode == 1:

            logger.info(print_game_state(game))
            while True:
                ai_turn(game, "player 1", depth=4)
                if check_if_goal_state(game):
                    break
                ai_turn(game, "player 2", depth=4)
                if check_if_goal_state(game):
                    break
            evaluate_game(game)

        elif game_mode == 2:

            logger.info(print_game_state(game))
            while True:
                player_turn(game, "player 1")
                if check_if_goal_state(game):
                    break
                ai_turn(game, "player 2", depth=4)
                if check_if_goal_state(game):
                    break
            evaluate_game(game)

        elif game_mode == 3:

            logger.info(print_game_state(game))
            while True:
                ai_turn(game, "player 1", depth=4)
                if check_if_goal_state(game):
                    break
                player_turn(game, "player 2")
                if check_if_goal_state(game):
                    break
            evaluate_game(game)

        else:
            sys.exit()

    else:
        sys.exit()


if __name__ == "__main__":
    raw_input = input("Do you want to log this session? y/n ")
    if raw_input.lower() == "y":
        logger.debug(
            "Initialize logger. Files can be found in the /logfiles/ directory"
        )
        logger.add(
            "./logfiles/file_{time}.log",
            colorize=True,
            format="<green>{time}</green> <level>{message}</level>",
            backtrace=True,
            diagnose=True,
        )

    main()
