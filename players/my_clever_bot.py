###
# MyCleverBot
# by: Eli
# assisted by: Bonsai:27b
# using: Cline agent
###
from players.MancalaAI import MancalaAI
class MyCleverBot(MancalaAI):
    def get_move(self, board):
        moves = board.get_valid_moves()
        if not moves: return 1
        my_mancala, opp_mancala, my_pit_start = (7, 0, 1) if self.player_num == 1 else (0, 7, 8)
        best_score, best_move = -1, moves[0]
        for move in moves:
            test = board.get_test_board(move)
            score = (test.board[my_mancala] - test.board[opp_mancala]) * 10
            if test.player_num == self.player_num: score += 100
            score += self._detect_capture(test, board, my_pit_start) * 3
            score += self._score_pit_balance(test, my_pit_start)
            if test.get_valid_moves(): score -= self._evaluate_opponent(test)
            if score > best_score: best_score, best_move = score, move
        return best_move
    def _detect_capture(self, test, original, my_pit_start):
        for i in range(6):
            if test.board[my_pit_start+i] == 0 and original.board[my_pit_start+i] > 0 and original.board[((my_pit_start+i)+7 if my_pit_start+i < 7 else my_pit_start+i-7)] > 0: return 1
        return 0
    def _score_pit_balance(self, test, my_pit_start):
        e = sum(1 for i in range(6) if test.board[my_pit_start+i] == 0)
        s = sum(1 for i in range(6) if test.board[my_pit_start+i] == 1)
        if 2 <= e <= 3: return e * 2
        if s >= 3: return s * 1.5
        return 0
    def _evaluate_opponent(self, test):
        opp_pit = 1 + ((test.player_num - 1) * 7)
        ai = self.player_num
        my_mancala = 7 if ai == 1 else 0
        opp_mancala = 7 if test.player_num == 1 else 0
        return max((self._score_board_from_ai_perspective(test.get_test_board(om), test, opp_pit, ai, my_mancala, opp_mancala) for om in test.get_valid_moves()), default=0)
    def _score_board_from_ai_perspective(self, test, original, my_pit_start, ai_player_num, my_mancala, opp_mancala):
        score = (test.board[my_mancala] - test.board[opp_mancala]) * 10
        if test.player_num == original.player_num: score += 100
        score += self._detect_capture(test, original, my_pit_start) * 3
        score += self._score_pit_balance(test, my_pit_start)
        for i in range(6):
            first = 1 + i
            second = first + 7 if first < 7 else first - 7
            if test.board[first] == 0 and test.board[second] > 0 and ai_player_num == 1: score -= 3 * test.board[second]
            if test.board[second] == 0 and test.board[first] > 0 and ai_player_num == 2: score -= 3 * test.board[first]
        return score