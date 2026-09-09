from players.MancalaAI import MancalaAI

class EasyPeasy(MancalaAI):

   def get_move(self, board_obj):
      valid_moves = board_obj.get_valid_moves()
      my_mancala_idx = 0 if self.player_num == 2 else 7
      number_of_stones_in_my_mancala = board_obj.board[my_mancala_idx]
      max_score = -1
      max_score_move = -1
      for move in valid_moves:
         test_board = board_obj.get_test_board(move)
         number_of_stones_in_pit = test_board.board[my_mancala_idx]
         new_stones_in_mancala = number_of_stones_in_pit - number_of_stones_in_my_mancala
         does_this_move_let_me_go_again = 0
         if test_board.player_num == self.player_num:
            does_this_move_let_me_go_again = 4
         score = does_this_move_let_me_go_again + new_stones_in_mancala
         if score > max_score:
            max_score = score
            max_score_move = move
      # Return a number from 1-6
      return max_score_move

