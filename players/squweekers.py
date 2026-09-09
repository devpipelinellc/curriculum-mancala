# welcome to the Destroyer
import logging
from players.MancalaAI import MancalaAI
import random


class Squweekers(MancalaAI):
    logging.basicConfig(filename='squweekers.log', encoding='utf-8', level=logging.DEBUG)

    def get_move(self, board):
        my_mancala_idx = 0 if self.player_num == 2 else 7
        valid_moves = board.get_valid_moves()
        max_score = -1
        max_score_move = -1


        if self.player_num == 1:
            stones = board.get_stones()
            number_of_stones_in_pit = board.board[my_mancala_idx]

            if sum(stones[0:7]) == 24 and sum(stones[8:14]) == 24:
                return 1
            else:
                for move in valid_moves:
                    test_board = board.get_test_board(move)
                    go_again = 0
                    if test_board.player_num == self.player_num:
                        go_again = 30
                    score = go_again + (test_board.board[my_mancala_idx] - number_of_stones_in_pit)
                    if score > max_score:
                        max_score = score
                        max_score_move = move

                return max_score_move

        if self.player_num == 2:
            stones = board.get_stones()
            number_of_stones_in_pit = board.board[my_mancala_idx]
            move_list = []
            for move in valid_moves:
                test_board = board.get_test_board(move)

                if stones[7] <= 2 and stones[0] < 1:
                    if test_board.player_num == self.player_num:
                        return move
                elif stones[7] <= 2 and stones[0] == 1:
                    return valid_moves[-1]
                else:
                    go_again = 0
                    if test_board.player_num == self.player_num:
                        go_again = 10
                    elif test_board.player_num != self.player_num and number_of_stones_in_pit <= 1:
                        return valid_moves[-1]
                    
                    score = go_again + (test_board.board[my_mancala_idx] - number_of_stones_in_pit)

                    if score > max_score:
                        max_score = score
                        max_score_move = move


            return max_score_move