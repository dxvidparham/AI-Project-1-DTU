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

import copy
import numpy as np

import kalaha
import moves


def evaluate(gamestate, game_mode):

    if game_mode == "1":

      if kalaha.check_if_goal_state(gamestate, game_mode):
          gamestate.player2_kalaha += sum(gamestate.player2_board)
          gamestate.player1_kalaha += sum(gamestate.player1_board)

      sumstones = gamestate.player1_kalaha - gamestate.player2_kalaha
    elif game_mode == "2":
      if kalaha.check_if_goal_state(gamestate, game_mode):
          gamestate.player3_kalaha += sum(gamestate.player3_board)
          gamestate.player1_kalaha += sum(gamestate.player1_board)

      sumstones = gamestate.player1_kalaha - gamestate.player3_kalaha
    # sumEmptyPits = len(gamestate.player1_board)-np.count_nonzero(gamestate.player1_board)
    # decision_factor = sumEmptyPits*0.1+sumStones
    
    return sumstones


def get_valid_moves(gamestate, player, game_mode):

    valid_moves = []
    if player == "player 1":
        for bowl in range(len(gamestate.player1_board)):
            if gamestate.player1_board[bowl] != 0:
                valid_moves.append(bowl)

    elif player == "player 2":
        for bowl in range(len(gamestate.player2_board)):
            if gamestate.player2_board[bowl] != 0:
                valid_moves.append(bowl)

    else:
        for bowl in range(len(gamestate.player3_board)):
            if gamestate.player3_board[bowl] != 0:
                valid_moves.append(bowl)
    return valid_moves


def max_search(gamestate, depth, alpha, beta, game_mode, best_move=None):
    max_value = float("-inf")
    if game_mode == "1":
 
      for bowl in get_valid_moves(gamestate, "player 1", game_mode):
          tmp_gamestate = copy.deepcopy(gamestate)
          moves.move(tmp_gamestate, "player 1", bowl, game_mode)
          if tmp_gamestate.go_again:
              evaluation = minimax(tmp_gamestate, depth - 1, alpha, beta, True, game_mode)[0]
          else:
              evaluation = minimax(tmp_gamestate, depth - 1, alpha, beta, False, game_mode)[0]
          max_value = max(max_value, evaluation)
          alpha = max(alpha, max_value)
          if alpha >= beta:
              break
          elif max_value == evaluation:
              best_move = bowl

    elif game_mode == "2":
      max_value = float("-inf")
      for bowl in get_valid_moves(gamestate, "player 1", game_mode):
          tmp_gamestate = copy.deepcopy(gamestate)
          moves.move(tmp_gamestate, "player 1", bowl, game_mode)
          if tmp_gamestate.go_again:
              evaluation = minimax(tmp_gamestate, depth - 1, alpha, beta, True, game_mode)[0]
          else:
              evaluation = minimax(tmp_gamestate, depth - 1, alpha, beta, False, game_mode)[0]
          max_value = max(max_value, evaluation)
          alpha = max(alpha, max_value)
          if alpha >= beta:
              break
          elif max_value == evaluation:
              best_move = bowl
    return max_value, best_move


def min_search(gamestate, depth, alpha, beta, game_mode, best_move=None):
  min_value = float("inf")
  if game_mode == "1":
      

      for bowl in get_valid_moves(gamestate, "player 2", game_mode):
          tmp_gamestate = copy.deepcopy(gamestate)
          moves.move(tmp_gamestate, "player 2", bowl, game_mode)
          if tmp_gamestate.go_again:
              evaluation = minimax(tmp_gamestate, depth - 1, alpha, beta, False, game_mode)[0]
          else:
              evaluation = minimax(tmp_gamestate, depth - 1, alpha, beta, True, game_mode)[0]
          min_value = min(min_value, evaluation)
          beta = min(beta, min_value)
          if beta <= alpha:
              break
          elif min_value == evaluation:
              best_move = bowl

  elif game_mode == "2":
      min_value = float("inf")
      for bowl in get_valid_moves(gamestate, "player 3", game_mode):
          tmp_gamestate = copy.deepcopy(gamestate)
          moves.move(tmp_gamestate, "player 3", bowl, game_mode)
          if tmp_gamestate.go_again:
              evaluation = minimax(tmp_gamestate, depth - 1, alpha, beta, False, game_mode)[0]
          else:
              evaluation = minimax(tmp_gamestate, depth - 1, alpha, beta, True, game_mode)[0]
          min_value = min(min_value, evaluation)
          beta = min(beta, min_value)
          if beta <= alpha:
              break
          elif min_value == evaluation:
              best_move = bowl
  return min_value, best_move


def minimax(gamestate, depth, alpha, beta, maximizing_player, game_mode):

    if depth == 0 or kalaha.check_if_goal_state(gamestate, game_mode):
        return evaluate(gamestate, game_mode), gamestate

    if maximizing_player:
        return max_search(gamestate, depth, alpha, game_mode, beta )

    else:
        return min_search(gamestate, depth, alpha, game_mode, beta)