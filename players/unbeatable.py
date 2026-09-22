from players.MancalaAI import MancalaAI


class Unbeatable(MancalaAI):
    """Aggressive alpha-beta search with transposition table."""

    WIN = 1_000_000
    DEPTH = 5

    def __init__(self, player_num):
        super().__init__(player_num)
        self._tt = {}

    def get_move(self, board):
        self._tt.clear()
        moves = board.get_valid_moves()
        best, score, alpha = moves[0], -self.WIN, -self.WIN
        for mv, ch in self._ordered(board, moves):
            v = self._search(ch, alpha, self.WIN, 1)
            if v > score:
                score, best = v, mv
            alpha = max(alpha, score)
        return best

    def _ordered(self, board, moves):
        me, mine = board.player_num, 7 if board.player_num == 1 else 0
        r = []
        for m in moves:
            c = board.get_test_board(m)
            r.append((c.player_num == me, c.board[mine] - board.board[mine], m, c))
        r.sort()
        return [(m, c) for _, _, m, c in r]

    def _search(self, board, alpha, beta, depth):
        k = (tuple(board.board), board.player_num, depth)
        if k in self._tt:
            return self._tt[k]
        if board.is_game_over():
            v = self._terminal(board)
        elif depth >= self.DEPTH:
            v = self._heuristic(board)
        else:
            mx = board.player_num == self.player_num
            v = -self.WIN if mx else self.WIN
            for _, c in self._ordered(board, board.get_valid_moves()):
                s = self._search(c, alpha, beta, depth + 1)
                v = max(v, s) if mx else min(v, s)
                if mx:
                    alpha = max(alpha, v)
                else:
                    beta = min(beta, v)
                if alpha >= beta:
                    break
        self._tt[k] = v
        return v

    def _terminal(self, board):
        b = board.clone(); b.collect()
        a = b.board[7 if self.player_num == 1 else 0]
        o = b.board[0 if self.player_num == 1 else 7]
        if a > o: return self.WIN + a
        if a < o: return -self.WIN - o
        return 0

    def _heuristic(self, board):
        s = 1 if self.player_num == 1 else -1
        return s * ((board.board[7] - board.board[0]) +
                     (sum(board.board[1:7]) - sum(board.board[8:14])) // 2)