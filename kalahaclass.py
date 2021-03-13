import sys


class Kalaha():

    def __init__(self):

        self.player1_kalaha = 0
        self.player2_kalaha = 0
        self.player1_board = [4, 4, 4, 4, 4, 4]
        self.player2_board = [4, 4, 4, 4, 4, 4]
        self.player1_move_count = 0
        self.player2_move_count = 0
        self.playing = True

    def print_game_state(self):
        print(" ")
        print(f"    {self.player2_kalaha}")
        print(f"Player 2:    {self.player2_board}")
        print(f"             {self.player1_board}      Player 1:")
        print(f"                                        {self.player1_kalaha}")


    def check_if_goal_state(self):

        if all(i == 0 for i in self.player1_board) or all(j == 0 for j in self.player2_board):
            return True
        else:
            return False

    def capture_stones(self, player, position):
        if player == "player 1":
            if self.player2_board[position] != 0:
                self.player1_kalaha += 1 + self.player2_board[position]
                self.player2_board[position] = 0
            else:
                self.player1_board[position] += 1

        else:
            if self.player1_board[position] != 0:
                self.player2_kalaha += 1 + self.player1_board[position]
                self.player1_board[position] = 0
            else:
                self.player2_board[position] += 1

    def distribute_kalaha(self, player, stones_left, skip_kalaha, origin):
        if player == "player 1":
            if player == origin:
                if stones_left == 1:
                    if self.check_if_goal_state():
                        self.playing = False
                    else:
                        self.player1_kalaha += 1
                        self.print_game_state()
                        print("\nThe last ball endet in the Kalaha. You're allowed to go again.")
                        position = int(input("player 1s turn (0, 1, 2, 3, 4, 5) "))
                        self.move(player, position, 2, origin=player)

                elif stones_left > 1:
                    self.player1_kalaha += 1
                    position = 5
                    player = "player 2"
                    return self.distribute_stone_on_board(player, position, stones_left - 1, skip_kalaha, origin="player 1")

                else:
                    pass

            else:
                if stones_left == 1:
                    if self.check_if_goal_state():
                        self.playing = False
                    else:
                        self.print_game_state()
                        print("\nThe last ball endet in the Kalaha. You're allowed to go again.")
                        position = int(input("player 1s turn (0, 1, 2, 3, 4, 5) "))
                        self.move(player, position, 2, origin=player)

                else:
                    position = 5
                    player = "player 2"
                    return self.distribute_stone_on_board(player, position, stones_left, skip_kalaha, origin="player 1")

        elif player == "player 2":
            if player == origin:
                if stones_left == 1:
                    if self.check_if_goal_state():
                        self.playing = False
                    else:
                        self.player2_kalaha += 1
                        self.print_game_state()
                        print("\nThe last ball endet in the Kalaha. You're allowed to go again.")
                        position = int(input("player 2s turn (0, 1, 2, 3, 4, 5) "))
                        self.move(player, position, 1, origin=player)
                elif stones_left > 1:
                    self.player2_kalaha += 1
                    position = 0
                    player = "player 1"
                    return self.distribute_stone_on_board(player, position, stones_left - 1, skip_kalaha, origin="player 2")
                else:
                    pass

            else:
                if stones_left == 1:
                    if self.check_if_goal_state():
                        self.playing = False
                    else:
                        self.print_game_state()
                        print("\nThe last ball endet in the Kalaha. You're allowed to go again.")
                        position = int(input("player 2s turn (0, 1, 2, 3, 4, 5) "))
                        self.move(player, position, 1, origin=player)
                else:
                    position = 0
                    player = "player 1"
                    return self.distribute_stone_on_board(player, position, stones_left, skip_kalaha, origin="player 2")
        else:
            print("fail")


    def distribute_stone_on_board(self, player, position, stones_left, skip_kalaha, origin):

        if player == "player 1":
            if stones_left == 1 and self.player1_board[position] == 0 and player == origin:
                return self.capture_stones(player, position)
            elif stones_left != 0 and position == 5:
                self.player1_board[position] += 1
                return self.distribute_kalaha(player, stones_left - 1, skip_kalaha, origin)
            elif stones_left != 0:
                self.player1_board[position] += 1
                return self.distribute_stone_on_board(player, position + 1, stones_left - 1, skip_kalaha, origin)
            else:
                pass

        else:

            if stones_left == 1 and self.player2_board[position] == 0 and player == origin:
                return self.capture_stones(player, position)

            elif stones_left != 0 and position == 0:
                self.player2_board[position] += 1
                return self.distribute_kalaha(player, stones_left - 1, skip_kalaha, origin)

            elif stones_left == 1 and position == 5:
                self.player2_board[position] += 1

            elif stones_left > 0 and position < 6:
                self.player2_board[position] += 1
                return self.distribute_stone_on_board(player, position - 1, stones_left - 1, skip_kalaha, origin)

            else:
                pass

    def move(self, player, position, skip_kalaha, origin):

        while True:
            if player == "player 1" and self.player1_board[position] == 0 or player == "player 2" and self.player2_board[position] == 0:
                position = int(input(f"\nPit {position} is already empty. Please choose another one: \n"))
            else:
                break

        if player == "player 1":
            self.player1_move_count += 1

            if position == 5:
                stones_left = self.player1_board[position]
                self.player1_board[position] = 0
                self.distribute_kalaha(player, stones_left, skip_kalaha, origin)

            else:
                stones_left = self.player1_board[position]
                self.player1_board[position] = 0
                position += 1
                self.distribute_stone_on_board(player, position, stones_left, skip_kalaha, origin)

        elif player == "player 2":
            self.player2_move_count += 1

            if position == 0:
                stones_left = self.player2_board[position]
                self.player2_board[position] = 0
                self.distribute_kalaha(player, stones_left, skip_kalaha, origin)

            else:
                stones_left = self.player2_board[position]
                self.player2_board[position] = 0
                position -= 1
                self.distribute_stone_on_board(player, position, stones_left, skip_kalaha, origin)


def main():

    game = Kalaha()
    raw_input = input("Welcome to a dumb implementation of Kalaha. Are you ready? y/n ")
    if raw_input.lower() == "y":
        game.print_game_state()
        while game.playing:

            raw_input = int(input("player 1s turn (0, 1, 2, 3, 4, 5) "))
            if raw_input in range(6):

                game.move("player 1", raw_input, 2, origin="player 1")
                game.print_game_state()
                if game.check_if_goal_state():
                    game.playing = False
                    break

            raw_input = int(input("player 2s turn (0, 1, 2, 3, 4, 5) "))
            if raw_input in range(6):

                game.move("player 2", raw_input, 1, origin="player 2")
                game.print_game_state()
                if game.check_if_goal_state():
                    game.playing = False
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
        print(f"Moves played by Player 1: {game.player1_move_count}")

if __name__ == "__main__":

    main()
