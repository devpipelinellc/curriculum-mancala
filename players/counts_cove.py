from players.MancalaAI import MancalaAI

# counts_cove
# by: Jake Egbert
# assisted by: deepseek-v4.1-flash
# using: Cline Agent


class CountsCove(MancalaAI):

    MANCALA_STONE = 1
    EXTRA_TURN = 6
    CAPTURED_STONE = 2

    def get_move(self, board):
        my_mancala_idx = board.get_my_mancala_idx(self.player_num)
        stones_before = board.board[my_mancala_idx]

        best_score = None
        best_move = None
        for move in board.get_valid_moves():
            score = self.score_move(board, move, my_mancala_idx, stones_before)
            if best_score is None or score > best_score:
                best_score = score
                best_move = move
        return best_move

    def score_move(self, board, move, my_mancala_idx, stones_before):
        test_board = board.get_test_board(move)
        banked = test_board.board[my_mancala_idx] - stones_before
        score = banked * self.MANCALA_STONE

        if test_board.player_num == self.player_num:
            score += self.EXTRA_TURN
            score += self.best_follow_up(test_board, my_mancala_idx)
        elif banked > 0:
            score += banked * (self.CAPTURED_STONE - self.MANCALA_STONE)

        return score

    def best_follow_up(self, board, my_mancala_idx):
        stones_before = board.board[my_mancala_idx]
        best = 0
        for move in board.get_valid_moves():
            after = board.get_test_board(move)
            banked = after.board[my_mancala_idx] - stones_before
            value = banked * self.CAPTURED_STONE
            if after.player_num == self.player_num:
                value += self.EXTRA_TURN
            if value > best:
                best = value
        return best
