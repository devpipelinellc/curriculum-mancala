from players.MancalaAI import MancalaAI

###
# cline_a_nator_2
# by: MollyKate Adams
# assisted by: cline:cline-free/solar-pro4 
# using: Cline agent
###


class ClineANator2(MancalaAI):

    def get_move(self, board):
        best = None
        best_val = -1
        my_mancala = board.get_my_mancala_idx(self.player_num)
        start_mancala = board.board[my_mancala]
        for move in board.get_valid_moves():
            future = board.get_test_board(move)
            future_mancala = future.board[my_mancala]
            val = future_mancala - start_mancala
            if future.player_num == self.player_num:
                val += 24
            if val > best_val:
                best_val = val
                best = move
        return best
