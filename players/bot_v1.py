from players.MancalaAI import MancalaAI

SEARCH_DEPTH = 4


def evaluate_board(board, player_num):
    """Score board from player_num's view: own total (store + pits) minus opponent's."""
    stones = board.get_stones()
    if player_num == 1:
        my_total = stones[7] + sum(stones[1:7])
        opponent_total = stones[0] + sum(stones[8:14])
    else:
        my_total = stones[0] + sum(stones[8:14])
        opponent_total = stones[7] + sum(stones[1:7])
    return my_total - opponent_total


def _minimax(board, depth, my_player):
    """Best score (from my_player's view) reachable from board within depth."""
    if depth == 0 or board.is_game_over():
        return evaluate_board(board, my_player)
    child_scores = [
        _minimax(board.get_test_board(move), depth - 1, my_player)
        for move in board.get_valid_moves()
    ]
    if board.player_num == my_player:
        return max(child_scores)
    return min(child_scores)


class BotV1(MancalaAI):
    def get_move(self, board):
        """Return the move (1-6) that maximizes my store advantage.

        Runs a depth-limited minimax search from the perspective of the current
        player. Extra turns are handled naturally because each recursion
        maximizes or minimizes according to whose turn the resulting board
        belongs to. Ties keep the first valid move found.
        """
        my_player = board.player_num
        best_move = board.get_valid_moves()[0]
        best_score = float('-inf')
        for move in board.get_valid_moves():
            child_board = board.get_test_board(move)
            score = _minimax(child_board, SEARCH_DEPTH - 1, my_player)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move