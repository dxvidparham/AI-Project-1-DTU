class GameState:
    def __init__(self, stone_cnt=4):

        self.player1_kalaha = 0
        self.player2_kalaha = 0
        self.player2_board = [stone_cnt for _ in range(6)]
        self.player1_board = [stone_cnt for _ in range(6)]
