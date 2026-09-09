import os

# Mancala board consists of six "pots" on each side of the board and
# two "pots" on the ends of the board.
# The data structure for the game board will be a list:
# [0, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4]
# The first value (index 0) is the number of stones in Player 1's end pit
# The next six digits are Player 2's side pots
# The following value (index 7) is the number of stones in Player 2's end pit
# The next six digits are Player 1's side pots

def load_player_files():
   ignore_files = [
      "__pycache__",
      "__init__.py",
      "MancalaAI.py"
   ]
   players_list = os.listdir('./players')
   output_list = []
   for player in players_list:
      if player not in ignore_files:
         # Strip the '.py' from the end of the file name
         output_list.append(player.split('.')[0])
   return output_list

def get_printable_name(filename):
   return filename.title().replace('_', ' ')

def get_class_name(filename):
   return filename.title().replace('_', '')

def printable_players(file_list):
   output = []
   for player in file_list:
      # Title case the player file name and replace '_' with a space ' '
      output.append(get_printable_name(player))
   return output

def deep_copy_list(lst):
   return [value[::] for value in lst]