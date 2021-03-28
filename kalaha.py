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
import time
from loguru import logger

import algorithm
import game_state
import moves


def print_game_state(gamestate, game_mode):

  if game_mode == "1":

      return f"""
                  Current game state:
          {gamestate.player2_kalaha}
    Player 2:    {gamestate.player2_board}
                  {gamestate.player1_board}      Player 1:
                                              {gamestate.player1_kalaha}"""
  elif game_mode == "2":
      return f"""
                  Current game state:
          {gamestate.player3_kalaha}
    Player 3:    {gamestate.player3_board}
                  {gamestate.player1_board}      Player 1:
                                              {gamestate.player1_kalaha}"""


def check_if_goal_state(gamestate, game_mode):

  if game_mode == "1":
      
      return all(i == 0 for i in gamestate.player1_board) or not any(
          j != 0 for j in gamestate.player2_board
      )
  elif game_mode == "2":

      return all(i == 0 for i in gamestate.player1_board) or not any(
          j != 0 for j in gamestate.player3_board
      )


def player1_turn(game, game_mode):
    # AIs turn
    best_move = algorithm.minimax(game, 3, float("-inf"), float("inf"), True, game_mode)[1]
    moves.move(game, "player 1", best_move, game_mode)

    print(f"Player 1 move: {best_move}\n")
    logger.info(print_game_state(game, game_mode))

    if game.go_again and not check_if_goal_state(game, game_mode):
        print("\nThe last ball ended in the Kalaha. player 1 is allowed to go again.")
        game.go_again = False
        return player1_turn(game, game_mode)


def player2_turn(game, game_mode):
    # Players turn
    try:
        raw_input = int(input("player 2s turn (0, 1, 2, 3, 4, 5) "))
        if raw_input not in range(6):
            raise ValueError
    except ValueError:
        print("\nTry again: Please insert a number between 0 and 5")
        return player2_turn(game, game_mode)

    move = moves.move(game, "player 2", raw_input, game_mode)

    try:

        if check_if_goal_state(game, game_mode):
            raise AttributeError

        move.get("go-again")
        logger.info(print_game_state(game, game_mode))
        print("\nThe last ball ended in the Kalaha. You're allowed to go again.")
        return player2_turn(game, game_mode)

    except AttributeError:
        logger.info(print_game_state(game, game_mode))
        return

def player3_turn(game, game_mode):
    # Second AIs turn
    best_move = algorithm.minimax(game, 4, float("-inf"), float("inf"), False, game_mode)[1]
    moves.move(game, "player 3", best_move, game_mode)

    print(f"Player 3 move: {best_move}\n")
    logger.info(print_game_state(game, game_mode))


    if game.go_again and not check_if_goal_state(game, game_mode):
        print("\nThe last ball ended in the Kalaha. player 3 is allowed to go again.")
        game.go_again = False
        return player3_turn(game, game_mode)


def evaluate_game(game, game_mode):

    moves.distribute_remaining(game, game_mode)

    if game_mode == "1":
      if game.player1_kalaha > game.player2_kalaha:
          print("The Winner is:   Player 1!!!")

      elif game.player1_kalaha < game.player2_kalaha:
          print("The Winner is:   Player 2!!!")

      else:
          print("We got a draw!")

      print(f"Score: [P2] {game.player2_kalaha}:{game.player1_kalaha} [P1]")

    elif game_mode == "2":
      if game.player1_kalaha > game.player3_kalaha:
          print("The Winner is:   Player 1!")

      elif game.player1_kalaha < game.player3_kalaha:
          print("The Winner is:   Player 3!")

      else:
          print("We got a draw!")

      print(f"Score: [P3] {game.player3_kalaha}:{game.player1_kalaha} [P1]")


@logger.catch
def main():

    game = game_state.GameState()
    game_mode = input("Welcome to a dumb implementation of Kalaha. \n 1. player vs AI \n 2. AI vs AI ")
    if game_mode == "1":
        
      raw_input = input("Welcome to a dumb implementation of Kalaha. Are you ready? y/n ")

      if raw_input.lower() == "y":
          logger.info(print_game_state(game, game_mode))

          while True:

              player1_turn(game, game_mode)
              if check_if_goal_state(game, game_mode):
                  break

              player2_turn(game, game_mode)
              if check_if_goal_state(game, game_mode):
                  break

          evaluate_game(game, game_mode)

      else:
          sys.exit()

    elif game_mode == "2":
      raw_input = input("Sit back and watch the AI battle it out. Are you ready? y/n ")

      if raw_input.lower() == "y":
          logger.info(print_game_state(game, game_mode))

          while True:

              player1_turn(game, game_mode)
              if check_if_goal_state(game, game_mode):
                  break

              player3_turn(game, game_mode)
              if check_if_goal_state(game, game_mode):
                  break




          evaluate_game(game, game_mode)

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