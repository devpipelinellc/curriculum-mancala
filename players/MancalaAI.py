# This is the parent class to any AI that is playing this
# version of Mancala.
# As the parent class, it stores the player's number 
# in the attribute 'player_num'. This will be either 1 or 2, 
# indicating whether the AI is playing as Player 1 or Player 2
class MancalaAI:
   def __init__(self, player_num):
      self.player_num = player_num

   # Your subclass AI will override the get_move function
   # You will need to analyze the 'board', which is an instance of
   # the MancalaBoard.
   # Your function will need to return a valid move as an integer
   # between 1 and 6.
   def get_move(self, board):
      return None
   