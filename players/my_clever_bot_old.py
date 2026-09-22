###
# MyCleverBot
# by: Eli
# assisted by: Bonsai:27b
# using: Cline agent
###
from players.MancalaAI import MancalaAI
class MyCleverBotOld(MancalaAI):
    def get_move(self, game_board_state):
        my_player_mancala_index, opponent_player_mancala_index, my_pit_starting_index, highest_score_so_far, best_move_selection, valid_move_options = (7, 0, 1, -1, game_board_state.get_valid_moves()[0], game_board_state.get_valid_moves()) if self.player_num == 1 else (0, 7, 8, -1, game_board_state.get_valid_moves()[0], game_board_state.get_valid_moves())
        for candidate_move_number in valid_move_options:
            evaluated_move_score = ((game_board_state.get_test_board(candidate_move_number)).board[my_player_mancala_index] - (game_board_state.get_test_board(candidate_move_number)).board[opponent_player_mancala_index]) * 10
            if (game_board_state.get_test_board(candidate_move_number)).player_num == self.player_num: evaluated_move_score += 100
            evaluated_move_score = ((game_board_state.get_test_board(candidate_move_number)).board[my_player_mancala_index] - (game_board_state.get_test_board(candidate_move_number)).board[opponent_player_mancala_index]) * 10
            if (game_board_state.get_test_board(candidate_move_number)).player_num == game_board_state.player_num: evaluated_move_score += 100
            evaluated_move_score += (evaluated_move_score + (self._detect_capture((game_board_state.get_test_board(candidate_move_number)), game_board_state, my_pit_starting_index) * 3) + self._score_pit_balance((game_board_state.get_test_board(candidate_move_number)), my_pit_starting_index))
            if (game_board_state.get_test_board(candidate_move_number)).get_valid_moves(): evaluated_move_score -= max((self._score_board_from_ai_perspective((game_board_state.get_test_board(candidate_move_number)).get_test_board(opponent_candidate_move), (game_board_state.get_test_board(candidate_move_number)), (1+(((game_board_state.get_test_board(candidate_move_number)).player_num-1)*7)), self.player_num, my_player_mancala_index, opponent_player_mancala_index) for opponent_candidate_move in (game_board_state.get_test_board(candidate_move_number)).get_valid_moves()), default=0)
            if evaluated_move_score > highest_score_so_far: highest_score_so_far, best_move_selection = evaluated_move_score, candidate_move_number
        return best_move_selection
    def _detect_capture(self, nested_test_board, original_board_state, my_pit_starting_index):
        for pit_position_index in range(6): 
            if nested_test_board.board[(my_pit_starting_index + pit_position_index)] == 0 and original_board_state.board[(my_pit_starting_index + pit_position_index)] > 0 and original_board_state.board[((my_pit_starting_index + pit_position_index) + 7 if (my_pit_starting_index + pit_position_index) < 7 else (my_pit_starting_index + pit_position_index) - 7)] > 0: return 1
        return 0
    def _score_pit_balance(self, nested_test_board, my_pit_starting_index):
        if 2<=(sum(1 for pit_position_index in range(6) if nested_test_board.board[my_pit_starting_index+pit_position_index] == 0))<=3: return (sum(1 for pit_position_index in range(6) if nested_test_board.board[my_pit_starting_index+pit_position_index] == 0))*2
        if (sum(1 for pit_position_index in range(6) if nested_test_board.board[my_pit_starting_index+pit_position_index] == 1))>=3: return (sum(1 for pit_position_index in range(6) if nested_test_board.board[my_pit_starting_index+pit_position_index] == 1))*1.5
        return 0
    def _score_board_from_ai_perspective(self, nested_test_board, original_board_state, my_pit_starting_index, ai_player_num, my_player_mancala_index, opponent_player_mancala_index):
        evaluated_move_score = (nested_test_board.board[my_player_mancala_index] - nested_test_board.board[opponent_player_mancala_index]) * 10
        if nested_test_board.player_num == original_board_state.player_num: evaluated_move_score += 100
        evaluated_move_score += (self._detect_capture(nested_test_board, original_board_state, my_pit_starting_index) * 3) + self._score_pit_balance(nested_test_board, my_pit_starting_index)
        for pit_position_index in range(6):
            if nested_test_board.board[(1+pit_position_index)] == 0 and nested_test_board.board[((1+pit_position_index) + 7 if (1+pit_position_index) < 7 else (1+pit_position_index) - 7)] > 0 and ai_player_num == 1: evaluated_move_score -= 3*nested_test_board.board[((1+pit_position_index) + 7 if (1+pit_position_index) < 7 else (1+pit_position_index) - 7)]
            if nested_test_board.board[((1+pit_position_index) + 7 if (1+pit_position_index) < 7 else (1+pit_position_index) - 7)] == 0 and nested_test_board.board[(1+pit_position_index)] > 0 and ai_player_num == 2: evaluated_move_score -= 3*nested_test_board.board[(1+pit_position_index)]
        return evaluated_move_score