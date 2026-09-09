from players.MancalaAI import MancalaAI

class Mimancalaplayer(MancalaAI):

    def get_move(self, board):
        valid_moves = board.get_valid_moves()
        my_mancala_idx = 0 if self.player_num == 2 else 7
        opp_mancala_idx = 7 if self.player_num == 2 else 0
        max_diff = -100
        max_diff_move = -1
        for move in valid_moves:
            diff = self.get_move_r(move, board, my_mancala_idx, opp_mancala_idx)
            if diff > max_diff:
                max_diff = diff
                max_diff_move = move
        return max_diff_move

    def get_move_r(self, move, board, my_mancala_idx, opp_mancala_idx):
        test_board = board.get_test_board(move)
        if test_board.player_num == self.player_num:
            valid_moves = test_board.get_valid_moves()
            max_diff = -1
            for next_move in valid_moves:
                diff = self.get_move_r(next_move, test_board, my_mancala_idx, opp_mancala_idx)
                if diff > max_diff:
                    max_diff = diff
            return max_diff
        else:
            number_of_stones_in_pit = test_board.board[my_mancala_idx]
            score = number_of_stones_in_pit
            opp_valid_moves = test_board.get_valid_moves()
            max_opp_score = -1
            for move in opp_valid_moves:
                opp_score = self.get_opp_move_r(move, test_board, opp_mancala_idx)
                if opp_score > max_opp_score:
                    max_opp_score = opp_score
            return score - max_opp_score

    def get_opp_move_r(self,move, board, opp_mancala_idx):
        test_board = board.get_test_board(move)
        if test_board.player_num != self.player_num:
            max_score = -1
            valid_moves = test_board.get_valid_moves()
            for next_move in valid_moves:
                score = self.get_opp_move_r(next_move, test_board, opp_mancala_idx)
                if score > max_score:
                    max_score = score
            return max_score
        else:
            number_of_stones_in_pit = test_board.board[opp_mancala_idx]
            score = number_of_stones_in_pit
            return score