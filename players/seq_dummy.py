from players.MancalaAI import MancalaAI

class SeqDummy(MancalaAI):
   
   def get_move(self, board):
      valid_moves = board.get_valid_moves()

      return sorted(valid_moves)[0] 