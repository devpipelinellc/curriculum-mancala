from players.MancalaAI import MancalaAI

class StoneOvenV2(MancalaAI):

    def get_move(self, board_obj):
        return self.get_best_move(board_obj)[0]


    def get_best_move(self, board, depth = 1):
        valid_moves = board.get_valid_moves()
        my_mancala_idx = 0 if board.player_num == 2 else 7
        number_of_stones_in_my_mancala = board.board[my_mancala_idx]
        max_score = -999
        max_score_move = -1
        for move in valid_moves:
            test_board = board.get_test_board(move)
            number_of_stones_in_pit = test_board.board[my_mancala_idx]
            score = number_of_stones_in_pit - number_of_stones_in_my_mancala
            if test_board.player_num == board.player_num:
                next_move = self.get_best_move(test_board, depth)
                score += next_move[1]
            elif depth > 0:
                opp_move = self.get_best_move(test_board, depth - 1)
                score -= opp_move[1]

            if score > max_score:
                max_score = score
                max_score_move = move
        return [max_score_move, max_score]