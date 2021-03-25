import copy

import game_state
import kalaha
import moves


def evaluate(gamestate):

    return gamestate.player1_kalaha - gamestate.player2_kalaha


def get_valid_moves(gamestate, player):

    valid_moves = []
    if player == "player 1":
        for bowl in range(len(gamestate.player1_board)):
            if gamestate.player1_board[bowl] != 0:
                valid_moves.append(bowl)
        return valid_moves

    else:
        for bowl in range(len(gamestate.player2_board)):
            if gamestate.player2_board[bowl] != 0:
                valid_moves.append(bowl)
        return valid_moves


def minimax(gamestate, depth, alpha, beta, maximizing_player):

    if depth == 0 or kalaha.check_if_goal_state(gamestate):
        return evaluate(gamestate), gamestate

    if maximizing_player:
        max_value = float("-inf")
        best_move = None
        for bowl in get_valid_moves(gamestate, "player 1"):
            tmp_gamestate = copy.deepcopy(gamestate)
            moves.move(tmp_gamestate, "player 1", bowl, True)
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

    else:
        min_value = float("inf")
        best_move = None
        for bowl in get_valid_moves(gamestate, "player 2"):
            tmp_gamestate = copy.deepcopy(gamestate)
            moves.move(tmp_gamestate, "player 2", bowl, True)
            if tmp_gamestate.go_again:
                evaluation = minimax(tmp_gamestate, depth - 1, alpha, beta, False)[0]
            else:
                evaluation = minimax(tmp_gamestate, depth - 1, alpha, beta, True)[0]
            min_value = min(min_value, evaluation)
            beta = min(beta, min_value)
            if beta <= alpha:
                break
            elif min_value == evaluation:
                best_move = bowl
        return min_value, best_move
