from util import deep_copy_list

class InvalidMoveException(Exception):
   pass

class MancalaBoard:
   #
   # This class implements a Mancala board, encapsulating
   # the board and the methods to operate on the board.
   # The board is represented by a single numerical list of 14 elements
   # the indexes of which are labeled below:
   #
   # Player 1:
   # ╔═══════════════════════════════════════════════════╗
   # ║ ┌────┐ ┌─1─┐ ┌─2─┐ ┌─3─┐ ┌─4─┐ ┌─5─┐ ┌─6─┐ ┌────┐ ║
   # ║ │    │ │[6]│ │[5]│ │[4]│ │[3]│ │[2]│ │[1]│ │    │ ║
   # ║ │    │ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ │    │ ║
   # ║ │[7] │                                     │[0] │ ║
   # ║ │    │ ┌─6─┐ ┌─5─┐ ┌─4─┐ ┌─3─┐ ┌─2─┐ ┌─1─┐ │    │ ║
   # ║ │    │ │[8]│ │[9]│ │[10] │[11] │[12] │[13] │    │ ║
   # ║ └────┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └────┘ ║
   # ╚═══════════════════════════════════════════════════╝
   #                                         Player 2:
   def __init__(self, player_num = 1, init_board = None, moves_list = None):
      if not init_board:
         self.board = [0] + [4]*6 + [0] + [4]*6
      else:
         self.board = init_board[::]
      self.player_num = player_num
      if not moves_list:
         self.__moves = [ [], [] ] 
      else:
         self.__moves = moves_list.copy()
      self.player_1 = ''
      self.player_2 = ''

   def set_player_names(self, player_1 = '', player_2 = ''):
      self.player_1 = player_1
      self.player_2 = player_2
   
   def get_stones(self):
      return self.board

   def is_game_over(self):
      return sum(self.board[1:7]) == 0 or sum(self.board[8:14]) == 0
   
   def collect(self):
      p1_count = sum(self.board[1:8])
      p2_count = self.board[0] + sum(self.board[8:14])
      self.board = [0] * 14
      self.board[7] = p1_count
      self.board[0] = p2_count

   #
   # Returns 0 if the game is not yet over
   # Returns -1 if the game ends in a tie
   # Returns 1 if Player 1 wins
   # Returns 2 if Player 2 wins
   #
   def get_winner(self):
      if not self.is_game_over():
         return 0
      elif self.board[0] > self.board[7]:
         return 2
      elif self.board[7] > self.board[0]:
         return 1
      return -1

   def is_valid_move(self, move_num):
      if 1 <= move_num <= 6:
         idx = self.get_index_from_move(move_num)
         return self.board[idx] > 0
      return False
   
   def get_index_from_move(self, move_num):
      # print(f"Index of move {move_num} for Player {self.player_num} is {(7 * (self.player_num)) - move_num}")
      return (7 * (self.player_num)) - move_num

   def __str__(self):
      p1_moves = f"{''.join([str(s) for s in self.__moves[0]]):54}"
      p2_moves = f"{''.join([str(s) for s in self.__moves[1]]):54}"
      player_2_label = f'Player 2: {self.player_2}'
      player_2_str = f'{player_2_label:>53}'

      player_1_marker = ''
      player_2_marker = ''

      if self.player_num == 1:
         player_1_marker = f'<----- Player 1'
      else:
         player_2_marker = f'<----- Player 2'
      disp = [str(n) if n > 0 else '' for n in self.board]
      return f'''
Move History
┌───┬────────────────────────────────────────────────────────┐
│ 1 │ {p1_moves} │
├───┼────────────────────────────────────────────────────────┤
│ 2 │ {p2_moves} │
└───┴────────────────────────────────────────────────────────┘



Player 1: {self.player_1}
╔═══════════════════════════════════════════════════╗
║ ┌────┐ ┌─1─┐ ┌─2─┐ ┌─3─┐ ┌─4─┐ ┌─5─┐ ┌─6─┐ ┌────┐ ║
║ │    │ │{disp[6]:^3}│ │{disp[5]:^3}│ │{disp[4]:^3}│ │{disp[3]:^3}│ │{disp[2]:^3}│ │{disp[1]:^3}│ │    │ ║ {player_1_marker}
║ │    │ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ │    │ ║
║ │ {disp[7]:>2} │                                     │ {disp[0]:>2} │ ║
║ │    │ ┌─6─┐ ┌─5─┐ ┌─4─┐ ┌─3─┐ ┌─2─┐ ┌─1─┐ │    │ ║
║ │    │ │{disp[8]:^3}│ │{disp[9]:^3}│ │{disp[10]:^3}│ │{disp[11]:^3}│ │{disp[12]:^3}│ │{disp[13]:^3}│ │    │ ║ {player_2_marker}
║ └────┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └────┘ ║
╚═══════════════════════════════════════════════════╝
{player_2_str}
'''

   def get_string_list(self):
      return self.__str__().split('\n')

   def get_moves(self):
      return self.__moves

   def make_move(self, move_num):
      if not self.is_valid_move(move_num):
         raise InvalidMoveException(f'Move {move_num} is invalid for Player {self.player_num}')

      self.__moves[self.player_num - 1].append(move_num)
      idx = self.get_index_from_move(move_num)
      num_stones = self.board[idx]
      self.board[idx] = 0
      while num_stones > 0:
         idx = (idx + 1) % 14
         # Skip the other player's Mancala
         if self.player_num == 2 and idx == 7:
            idx += 1
         elif self.player_num == 1 and idx == 0:
            idx += 1
         self.board[idx] = self.board[idx] + 1
         num_stones -= 1

      my_mancala_index = 7 if self.player_num == 1 else 0
      opposite_index = 14 - idx
      # print(f"Ended on Index: {idx}")
      # Where did we end?
      if self.board[idx] == 1 and idx != my_mancala_index and self.index_on_my_side(idx) and self.board[opposite_index] > 0:
         # We ended in a blank space on our side AND 
         # there are stones on the opposite side
         # Get the opposite pieces
         total_count = self.board[idx] + self.board[opposite_index]
         self.board[idx] = 0
         self.board[opposite_index] = 0
         self.board[my_mancala_index] += total_count
         self.__moves[self.player_num - 1].append('°')
         self.switch_player()
      elif idx == my_mancala_index:
         # Don't switch the player
         self.__moves[self.player_num - 1].append('_')
      else:
         # We didn't end in our own Mancala
         # So, switch the player for next turn
         self.__moves[self.player_num - 1].append(' ')
         self.switch_player()
      
      return self

   def switch_player(self):
      # print("Switching Players!!")
      self.player_num = (self.player_num % 2) + 1
      
   def index_on_my_side(self, idx):
      if self.player_num == 1 and (1 <= idx <= 6):
         return True
      elif self.player_num == 2 and (8 <= idx <= 13):
         return True
      return False

   #
   # Gets a list of all valid moves for the current player
   def get_valid_moves(self):
      valid_moves = []
      idx = 1 + ((self.player_num - 1) * 7)
      for i in range(6):
         # print(f'{idx + i} = {self.board[idx + i]}')
         if self.board[idx + i] > 0:
            valid_moves.append(6 - i)
      
      return valid_moves[::-1]

   def clone(self):
      return MancalaBoard(self.player_num, self.board.copy(), deep_copy_list(self.__moves))

   # 
   # Returns a copy of the current board with the move_num move made
   def get_test_board(self, move_num, player_num = None):
      if player_num == None:
         player_num = self.player_num
      
      if not self.is_valid_move(move_num, player_num):
         raise InvalidMoveException(f'Move {move_num} is invalid for Player {player_num}')
   
      test_board = MancalaBoard(player_num, self.board.copy(), deep_copy_list(self.__moves))
      return test_board.make_move(move_num, player_num)

   # def print_test(self, move_num):
   #    print(f'Player {self.player_num} moves {move_num}')
   #    self.make_move(move_num)
   #    print(self)
   #    print(self.get_valid_moves())
   #    print()

# board = MancalaBoard(moves_list = [ [3,2,4,2], [1,2,1,3] ])

# print(board)
# try:
#    moves = [4,3,1,5,6,3,1]
#    for m in moves:
#       board.print_test(m)
# except InvalidMoveException as e:
#    print(e)

# print(board.get_string_list())

# board_copy = board.clone()

# moves = board_copy.get_moves()
# print(moves)

# print(board.get_valid_moves())