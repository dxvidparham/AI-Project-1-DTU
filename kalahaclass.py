import sys


class Kalaha():

    def __init__(self):

        self.player1_kalaha = 0
        self.player2_kalaha = 0
        self.player1_board = [4, 4, 4, 4, 4, 4]
        self.player2_board = [4, 4, 4, 4, 4, 4]

    def print_game_state(self):

        print(self.player1_kalaha, self.player1_board)
        print(" ", self.player2_board, self.player2_kalaha)

    def check_if_goal_state(self):

        if all(i == 0 for i in self.player1_board) or all(j == 0 for j in self.player2_board):
            return True
        else:
            return False

    def capture_stones(self, player, position):

        if player == "player 1":
            self.player1_kalaha += 1 + self.player2_board[position]
            self.player2_board[position] = 0

        else:
            self.player2_kalaha += 1 + self.player1_board[position]
            self.player1_board[position] = 0

    def distribute_kalaha(self, player, stones_left, skip_kalaha):

        if player == "player 1" and skip_kalaha == 2:
            self.player1_kalaha += 1
            if stones_left == 1:
                print("player 1 go again")
            else:
                position = 0
                player = "player 2"
                return self.distribute_stone_on_board(player, position, stones_left - 1, skip_kalaha)
        elif player == "player 2" and skip_kalaha == 1:
            self.player2_kalaha += 1
            if stones_left == 1:
                print("player 2 go again")
            else:
                position = 5
                player = "player 1"
                return self.distribute_stone_on_board(player, position, stones_left - 1, skip_kalaha)
        elif player == "player 1" and skip_kalaha == 1:
            position = 0
            player = "player 2"
            return self.distribute_stone_on_board(player, position, stones_left, skip_kalaha)
        else:
            position = 5
            player = "player 1"
            return self.distribute_stone_on_board(player, position, stones_left, skip_kalaha)

    def distribute_stone_on_board(self, player, position, stones_left, skip_kalaha):

        if player == "player 1":

            if stones_left == 1 and self.player1_board[position] == 0:
                return self.capture_stones(player, position)
            elif stones_left != 0 and position == 0:
                self.player1_board[position] += 1
                return self.distribute_kalaha(player, stones_left - 1, skip_kalaha)
            elif stones_left != 0:
                self.player1_board[position] += 1
                return self.distribute_stone_on_board(player, position - 1, stones_left - 1, skip_kalaha)
            else:
                pass

        else:

            if stones_left == 1 and self.player2_board[position] == 0:
                return self.capture_stones(player, position)
            elif stones_left != 0 and position == 5:
                self.player2_board[position] += 1
                return self.distribute_kalaha(player, stones_left - 1, skip_kalaha)
            elif stones_left > 0 and position < 5:
                self.player2_board[position] += 1
                return self.distribute_stone_on_board(player, position + 1, stones_left - 1, skip_kalaha)
            else:
                pass

    def move(self, player, position, skip_kalaha):

        if player == "player 1" and self.player1_board[position] == 0 or player == "player 2" and self.player2_board[position] == 0:
            print("illegal move")

        else:
            if player == "player 1" and position > 0:
                stones_left = self.player1_board[position]
                self.player1_board[position] = 0
                position -= 1
                self.distribute_stone_on_board(player, position, stones_left, skip_kalaha)

            elif player == "player 1" and position == 0:
                stones_left = self.player1_board[position]
                self.player1_board[position] = 0
                self.distribute_kalaha(player, stones_left, skip_kalaha)

            elif player == "player 2" and position == 5:
                stones_left = self.player2_board[position]
                self.player2_board[position] = 0
                self.distribute_kalaha(player, stones_left, skip_kalaha)

            else:
                stones_left = self.player2_board[position]
                self.player2_board[position] = 0
                position += 1
                self.distribute_stone_on_board(player, position, stones_left, skip_kalaha)

def main():

    game = Kalaha()
    playing = True
    raw_input = input("Welcome to a dumb implementation of Kalaha. Are you ready? y/n ")
    if raw_input == "y":

        while playing:
            raw_input = int(input("player 1s turn (0, 1, 2, 3, 4, 5) "))
            game.move("player 1", raw_input, 2)
            game.print_game_state()
            if game.check_if_goal_state():
                playing = False
                break
            raw_input = int(input("player 2s turn (0, 1, 2, 3, 4, 5) "))
            game.move("player 2", raw_input, 1)
            game.print_game_state()
            if game.check_if_goal_state():
                playing = False
                break


if __name__ == "__main__":

    main()
