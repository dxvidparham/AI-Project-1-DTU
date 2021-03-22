import sys

from loguru import logger

import algorithm
import game_state
import moves


def get_game_state(gamestate):

    game_state = f"""
                         Current game state:
                {gamestate.player2_kalaha}
            Player 2:    {gamestate.player2_board}
                         {gamestate.player1_board}       Player 1:
                                                    {gamestate.player1_kalaha}
    """

    return game_state


def check_if_goal_state(gamestate):

    if all(i == 0 for i in gamestate.player1_board) or all(
        j == 0 for j in gamestate.player2_board
    ):
        return True

    else:
        return False


def player1_turn(game):
    best_move = algorithm.minimax(game, 3, True)[1]
    try:
        x = moves.move(game, "player 1", best_move).get("go_again", False)
    except AttributeError:
        moves.move(game, "player 1", best_move)
        x = False

    print("I made my move!!!!")
    logger.info(get_game_state(game))

    if check_if_goal_state(game):
        moves.distribute_remaining(game)

    elif x:
        print("\nThe last ball ended in the Kalaha. You're allowed to go again.")
        return player1_turn(game)


def player2_turn(game):
    try:
        raw_input = int(input("player 2s turn (0, 1, 2, 3, 4, 5) "))
    except ValueError:
        print("\nTry again: Please insert a number between 0 and 5")
        return player2_turn(game)

    if raw_input in range(6):
        try:
            x = moves.move(game, "player 2", raw_input).get("go_again", False)
        except AttributeError:
            moves.move(game, "player 2", raw_input)
            x = False

        logger.info(get_game_state(game))

        if check_if_goal_state(game):
            moves.distribute_remaining(game)

        elif x:
            print("\nThe last ball ended in the Kalaha. You're allowed to go again.")
            return player2_turn(game)

    else:
        print("\nTry again: Please insert a number between 0 and 5")
        return player2_turn(game)


@logger.catch
def main():

    game = game_state.GameState()
    raw_input = input("Welcome to a dumb implementation of Kalaha. Are you ready? y/n ")
    if raw_input.lower() == "y":
        logger.info(get_game_state(game))

        while True:

            player1_turn(game)
            if check_if_goal_state(game):
                break

            player2_turn(game)
            if check_if_goal_state(game):
                break

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
    # the logfiles folder needs to be created for the logger to work
    logger.debug("That's it, beautiful and simple logging!")
    logger.add(
        "logfiles/file_{time}.log",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    )
    main()
