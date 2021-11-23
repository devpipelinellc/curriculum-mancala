from players.MancalaAI import MancalaAI

class EasyPeasy(MancalaAI):
   
   def get_move(self, board):
      valid_moves = board.get_valid_moves()
      my_mancala_idx = 0 if self.player_num == 2 else 7
      max_score = -1
      max_score_move = -1
      for move in valid_moves:
         test_board = board.get_test_board(move)
         number_of_stones_in_pit = board.board[my_mancala_idx]
         go_again = 0
         if test_board.player_num == self.player_num:
            go_again = 100
         score = go_again + number_of_stones_in_pit
         if score > max_score:
            max_score = score
            max_score_move = move

      return max_score_move