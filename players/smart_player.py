# Made by Kai and Stephanie

from players.MancalaAI import MancalaAI

class SmartPlayer(MancalaAI):
    def get_move(self, board):
        valid_moves = board.get_valid_moves()
        if not valid_moves:
            return None
        stones_in_play = sum(board.board[1:7]) + sum(board.board[8:14])
        depth = 12 if stones_in_play <= 16 else 8
        _, best_move = self._minimax(board.clone(), depth, float('-inf'), float('inf'), self.player_num)
        return best_move if best_move is not None else valid_moves[0]

    def _minimax(self, board, depth, alpha, beta, root_player):
        if depth == 0 or board.is_game_over():
            return self._evaluate(board, root_player), None
        maximizing = board.player_num == root_player
        moves = self._ordered_moves(board)
        best_move = moves[0][0]
        best_val = float('-inf') if maximizing else float('inf')
        for move, test_board in moves:
            score, _ = self._minimax(test_board, depth - 1, alpha, beta, root_player)
            if (maximizing and score > best_val) or (not maximizing and score < best_val):
                best_val, best_move = score, move
            alpha, beta = (max(alpha, best_val), beta) if maximizing else (alpha, min(beta, best_val))
            if alpha >= beta:
                break
        return best_val, best_move

    def _ordered_moves(self, board):
        scored = [(tb.player_num == board.player_num, mv, tb)
                  for mv in board.get_valid_moves()
                  for tb in [board.get_test_board(mv)]]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [(mv, tb) for (_, mv, tb) in scored]

    def _evaluate(self, board, root_player):
        my_idx, opp_idx = (0, 7) if root_player == 2 else (7, 0)
        my_pits = board.board[1:7] if root_player == 1 else board.board[8:14]
        opp_pits = board.board[8:14] if root_player == 1 else board.board[1:7]
        if board.is_game_over():
            p1_final = board.board[7] + sum(board.board[1:7])
            p2_final = board.board[0] + sum(board.board[8:14])
            my_final, opp_final = (p1_final, p2_final) if root_player == 1 else (p2_final, p1_final)
            return (my_final - opp_final) * 1000
        store_diff = board.board[my_idx] - board.board[opp_idx]
        side_diff = sum(my_pits) - sum(opp_pits)
        threat = sum(mv for ov, mv in zip(opp_pits, my_pits[::-1]) if ov == 0 and mv > 0)
        return store_diff * 2 + side_diff * 0.5 - threat * 3.25