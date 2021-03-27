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


def player1_turn(game):
    # AIs turn
    best_move = algorithm.minimax(game, 8, float("-inf"), float("inf"), True)[1]
    moves.move(game, "player 1", best_move)
    print(f"AI-Rian made his move! {best_move}")
    logger.info(print_game_state(game))
    sleep(2)

    if game.go_again and not check_if_goal_state(game):
        print("\nThe last ball ended in the Kalaha. player 1 is allowed to go again.")
        game.go_again = False
        return player1_turn(game)


def player2_turn(game):
    # Players turn
    try:
        raw_input = int(input("player 2s turn (0, 1, 2, 3, 4, 5) "))
        if raw_input not in range(6):
            raise ValueError
    except ValueError:
        print("\nTry again: Please insert a number between 0 and 5")
        return player2_turn(game)

    move = moves.move(game, "player 2", raw_input)

  
    try:

        if check_if_goal_state(game):
            raise AttributeError

        move.get("go-again")
        logger.info(print_game_state(game))
        print("\nThe last ball ended in the Kalaha. You're allowed to go again.")
        return player2_turn(game)

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
        logger.info(print_game_state(game))

        while True:

            player1_turn(game)
            if check_if_goal_state(game):
                break

            player2_turn(game)
            if check_if_goal_state(game):
                break

        evaluate_game(game)

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
