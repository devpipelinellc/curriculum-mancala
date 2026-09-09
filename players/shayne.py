from players.MancalaAI import MancalaAI

class Shayne(MancalaAI):

    # def check_for_steals(self, board):
    #     valid_moves = board.get_valid_moves()
    #     my_mancala_idx = 0 if self.player_num == 2 else 7
    #     number_of_stones_in_my_mancala = board.board[my_mancala_idx]
    #     stones = board.get_stones()
    #     my_stones = stones[1:7:-1] if self.player_num == 2 else stones[8::-1]
    #     max_score_move = -1
    #     for move in valid_moves:
    #         if my_stones[move] < move:
    #             test_board = board.get_test_board(move)
    #             number_of_stones_in_pit = test_board.board[my_mancala_idx]
    #             # new_stones_in_mancala = number_of_stones_in_pit + number_of_stones_in_my_mancala
    #             if number_of_stones_in_pit > number_of_stones_in_my_mancala:
    #                 max_score_move = move
    #         else:
    #             return max_score_move
    #     return max_score_move

#  ║ ┌────┐ ┌─1─┐ ┌─2─┐ ┌─3─┐ ┌─4─┐ ┌─5─┐ ┌─6─┐ ┌────┐ ║
   # ║ │    │ │[6]│ │[5]│ │[4]│ │[3]│ │[2]│ │[1]│ │    │ ║
   # ║ │    │ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ │    │ ║
   # ║ │[7] │                                     │[0] │ ║
   # ║ │    │ ┌─6─┐ ┌─5─┐ ┌─4─┐ ┌─3─┐ ┌─2─┐ ┌─1─┐ │    │ ║
   # ║ │    │ │[8]│ │[9]│ │[10] │[11] │[12] │[13] │    │ ║
   # ║ └────┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └────┘ ║
        
    def check_for_go_again(self, board_obj):
        # index_move = {
        #     1: 6,
        #     2: 5,
        #     3: 4,
        #     4: 3, 
        #     5: 2,
        #     6: 1,
        #     8: 6,
        #     9: 5,
        #     10: 4,
        #     11: 3,
        #     12: 2,
        #     13: 1
        # }
        # valid_moves = board_obj.get_valid_moves()
        # stones = board_obj.get_stones()
        # my_stones = stones[1:7:-1] if self.player_num == 2 else stones[8::-1]
        # max_score_move = -1
        # for move in valid_moves:
        #     if my_stones[move] == move:
        #         max_score_move = move
        # return max_score_move
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
    
    def check_stone_count(self, board_obj):
        stones = board_obj.get_stones()
        max_num_stones = max(stones)
        return max_num_stones
        
   
    def get_move(self, board):

        # steals = self.check_for_steals(board)
        go_again = self.check_for_go_again(board)
        stones = self.check_stone_count(board)
        # if steals > 0:
        #     return steals
        if go_again > 0:
            return go_again
        else:
            return stones

# Check for steals
# Check for go again
# Check for steals
# Select the space with the most stones from left to right