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

import kalaha
import moves


def evaluate(gamestate, game_mode):

    if game_mode == "1":
        if kalaha.check_if_goal_state(gamestate, game_mode):
            gamestate.player2_kalaha += sum(gamestate.player2_board)
            gamestate.player1_kalaha += sum(gamestate.player1_board)

        evaluation = gamestate.player1_kalaha - gamestate.player2_kalaha

    elif game_mode == "2":
        if kalaha.check_if_goal_state(gamestate, game_mode):
            gamestate.player3_kalaha += sum(gamestate.player3_board)
            gamestate.player1_kalaha += sum(gamestate.player1_board)

        evaluation = gamestate.player1_kalaha - gamestate.player3_kalaha

    return evaluation


def get_valid_moves(gamestate, player):

    valid_moves = []
    if player == "player 1":
        for bowl in range(len(gamestate.player1_board)):
            if gamestate.player1_board[bowl] != 0:
                valid_moves.append(bowl)

    elif player == "player 2":
        for bowl in range(len(gamestate.player2_board)):
            if gamestate.player2_board[bowl] != 0:
                valid_moves.append(bowl)

    elif player == "player 3":
        for bowl in range(len(gamestate.player3_board)):
            if gamestate.player3_board[bowl] != 0:
                valid_moves.append(bowl)
    return valid_moves


def max_search(gamestate, depth, alpha, beta, game_mode, best_move=None):
    max_value = float("-inf")
    # player 1 is always the maximizing player
    for bowl in get_valid_moves(gamestate, "player 1"):
        tmp_gamestate = copy.deepcopy(gamestate)
        moves.move(tmp_gamestate, "player 1", bowl, game_mode)
        if tmp_gamestate.go_again:
            evaluation = minimax(
                tmp_gamestate, depth - 1, alpha, beta, True, game_mode
            )[0]
        else:
            evaluation = minimax(
                tmp_gamestate, depth - 1, alpha, beta, False, game_mode
            )[0]
        max_value = max(max_value, evaluation)
        alpha = max(alpha, max_value)
        if alpha >= beta:
            break
        elif max_value == evaluation:
            best_move = bowl

    return max_value, best_move


def min_search(gamestate, depth, alpha, beta, game_mode, best_move=None):
    # based on game mode, the minimizing player is switched
    player = {"1": "player 2", "2": "player 3"}
    min_value = float("inf")
    for bowl in get_valid_moves(gamestate, player.get(game_mode)):
        tmp_gamestate = copy.deepcopy(gamestate)
        moves.move(tmp_gamestate, player.get(game_mode), bowl, game_mode)
        if tmp_gamestate.go_again:
            evaluation = minimax(
                tmp_gamestate, depth - 1, alpha, beta, False, game_mode
            )[0]
        else:
            evaluation = minimax(
                tmp_gamestate, depth - 1, alpha, beta, True, game_mode
            )[0]
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
        return max_search(gamestate, depth, alpha, beta, game_mode)

    else:
        return min_search(gamestate, depth, alpha, beta, game_mode)