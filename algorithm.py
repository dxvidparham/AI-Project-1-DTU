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


def evaluate(gamestate):

    sumStones = gamestate.player1_kalaha - gamestate.player2_kalaha

    # sumEmptyPits = len(gamestate.player1_board)-np.count_nonzero(gamestate.player1_board)
    # decision_factor = sumEmptyPits*0.1+sumStones
    
    return sumStones


def get_valid_moves(gamestate, player):

    valid_moves = []
    if player == "player 1":
        for bowl in range(len(gamestate.player1_board)):
            if gamestate.player1_board[bowl] != 0:
                valid_moves.append(bowl)

    else:
        for bowl in range(len(gamestate.player2_board)):
            if gamestate.player2_board[bowl] != 0:
                valid_moves.append(bowl)
    return valid_moves


def max_search(gamestate, depth, alpha, beta, best_move=None):
    max_value = float("-inf")
    for bowl in get_valid_moves(gamestate, "player 1"):
        tmp_gamestate = copy.deepcopy(gamestate)
        moves.move(tmp_gamestate, "player 1", bowl)
        if kalaha.check_if_goal_state(tmp_gamestate):
            tmp_gamestate.player2_kalaha += sum(tmp_gamestate.player2_board) # evaluate that remaining stones will go to opponent
        if tmp_gamestate.go_again:
            evaluation = minimax(tmp_gamestate, depth - 1, alpha, beta, True)[0]
        else:
            evaluation = minimax(tmp_gamestate, depth - 1, alpha, beta, False)[0]
        max_value = max(max_value, evaluation)
        alpha = max(alpha, max_value)
        if alpha >= beta:
            break
        elif max_value == evaluation:
            best_move = bowl
    return max_value, best_move


def min_search(gamestate, depth, alpha, beta, best_move=None):
    min_value = float("inf")
    for bowl in get_valid_moves(gamestate, "player 2"):
        tmp_gamestate = copy.deepcopy(gamestate)
        moves.move(tmp_gamestate, "player 2", bowl)
        if kalaha.check_if_goal_state(tmp_gamestate):
            tmp_gamestate.player2_kalaha += sum(tmp_gamestate.player2_board) # evaluate that remaining stones will go to opponent
        if tmp_gamestate.go_again:
            evaluation = minimax(tmp_gamestate, depth - 1, alpha, beta, False)[0]
        else:
            evaluation = minimax(tmp_gamestate, depth - 1, alpha, beta, True)[0]
        # append array
        min_value = min(min_value, evaluation)
        beta = min(beta, min_value)
        if beta <= alpha:
            break
        elif min_value == evaluation:
            best_move = bowl
    # scale array
    # evaluate best move
    return min_value, best_move


def minimax(gamestate, depth, alpha, beta, maximizing_player):

    if depth == 0 or kalaha.check_if_goal_state(gamestate):
        return evaluate(gamestate), gamestate

    if maximizing_player:
        return max_search(gamestate, depth, alpha, beta)

    else:
        return min_search(gamestate, depth, alpha, beta)
