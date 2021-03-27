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
class GameState:
    def __init__(self, stone_cnt=4):

        self.player1_kalaha = 0
        self.player2_kalaha = 0
        self.player2_board = [stone_cnt for _ in range(6)]
        self.player1_board = [stone_cnt for _ in range(6)]
        self.go_again = False

