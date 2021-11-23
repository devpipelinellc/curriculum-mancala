import random
from players.MancalaAI import MancalaAI

class RandomIdiot(MancalaAI):
   
   def get_move(self, board):
      valid_moves = board.get_valid_moves()

      return random.choice(valid_moves)   