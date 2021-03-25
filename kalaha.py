import sys

import algorithm
import game_state
import moves


def print_game_state(gamestate):

    print(" ")
    print("             Current game state: ")
    print(f"    {gamestate.player2_kalaha}")
    print(f"Player 2:    {gamestate.player2_board}")
    print(f"             {gamestate.player1_board}      Player 1:")
    print(f"                                        {gamestate.player1_kalaha}")


def check_if_goal_state(gamestate):

    if all(i == 0 for i in gamestate.player1_board) or all(
        j == 0 for j in gamestate.player2_board
    ):
        return True

    else:
        return False


def main():

    playing = True
    game = game_state.GameState()
    raw_input = input("Welcome to a dumb implementation of Kalaha. Are you ready? y/n ")

    if raw_input.lower() == "y":
        print_game_state(game)

        while playing:

            # AIs turn
            best_move = algorithm.minimax(game, 3, float("-inf"), float("inf"), True)[1]
            moves.move(game, "player 1", best_move, True)
            print("AI-Rian made his move!")
            print_game_state(game)

            if check_if_goal_state(game):
                moves.distribute_remaining(game)
                playing = False
                break

            while game.go_again:
                print("AI-Rian is allowed to go again.")
                game.go_again = False
                best_move = algorithm.minimax(
                    game, 7, float("-inf"), float("inf"), True
                )[1]
                moves.move(game, "player 1", best_move, True)
                print("AI-Rian made his move!")
                print_game_state(game)

            # Players turn
            raw_input = int(input("player 2s turn (0, 1, 2, 3, 4, 5) "))

            if raw_input in range(6):
                moves.move(game, "player 2", raw_input, False)
                print_game_state(game)
                if check_if_goal_state(game):
                    moves.distribute_remaining(game)
                    playing = False
                    break

            else:
                print("\nTry again: Please insert a number between 0 and 5")

        if game.player1_kalaha > game.player2_kalaha:
            print("The Winner is:   Player 1!!!")

        elif game.player1_kalaha < game.player2_kalaha:
            print("The Winner is:   Player 2!!!")

        else:
            print("We got a draw!")

        print(f"Score: [P2] {game.player2_kalaha}:{game.player1_kalaha} [P1]")

    else:
        sys.exit()


if __name__ == "__main__":

    main()
