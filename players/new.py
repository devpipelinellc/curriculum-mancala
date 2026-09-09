from players.MancalaAI import MancalaAI

class New(MancalaAI):
    move_weights = {
        'new_turn': 10,
        'capture': 8,
    }
    def get_score(self,mancala_board,move):
        my_mancala_idx = mancala_board.get_my_mancala_idx(self.player_num) # index of my mancala
        original_mancala = mancala_board.board[my_mancala_idx] #original amount of stones in mancala 
        test_board = mancala_board.get_test_board(move)
        board = mancala_board
        num_stones_pit = test_board.board[my_mancala_idx] #after the move is made
        captured_stones = num_stones_pit - original_mancala
        score = 0
        
        if test_board.player_num == self.player_num:
            score = (New.move_weights['new_turn'])
            return score
        if captured_stones > 1:
            score = (captured_stones + New.move_weights['capture'])
            return score
        else:
            return 1 

    def get_move(self, board): #this needs to return 1-6 from Valid moves
        
        valid_moves = board.get_valid_moves() #this will return 1-6 that are valid
        
        return_move = valid_moves[0] #this variable is the one we want to change, this line sets it to default first position

        if len(valid_moves) == 1: # if there is only one available move we can just return that move
            return return_move
        list_scores = []
        list_moves = []
        for move in valid_moves:
           move_score = self.get_score(board,move)
           list_scores.append(move_score)
           list_moves.append(move)
        index = list_scores.index(max(list_scores))
        return list_moves[index]