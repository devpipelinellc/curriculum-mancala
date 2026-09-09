from players.MancalaAI import MancalaAI
class Skinny(MancalaAI):
    move_weights = {
        'new_turn': 10,
        'capture': 8,
    }
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
    def get_score(self,mancala_board,move):
        if self.player_num == 1:
            my_mancala_idx = mancala_board.get_my_mancala_idx(self.player_num) # index of my mancala
            original_mancala = mancala_board.board[my_mancala_idx] #original amount of stones in mancala 
            test_board = mancala_board.get_test_board(move)
            board = mancala_board
            num_stones_pit = test_board.board[my_mancala_idx] #after the move is made
            captured_stones = num_stones_pit - original_mancala
            score = 0
            player_one_cups = [board.board[1],board.board[2],board.board[3],board.board[4],board.board[5],board.board[6]]
            player_two_cups = [board.board[8],board.board[9],board.board[10],board.board[11],board.board[12],board.board[13]]
            after_cups_pone = [test_board.board[1],test_board.board[2],test_board.board[3],test_board.board[4],test_board.board[5],test_board.board[6]]
            after_cups_ptwo = [test_board.board[8],test_board.board[9],test_board.board[10],test_board.board[11],test_board.board[12],test_board.board[13]]
            if test_board.player_num == self.player_num:
                score = (Skinny.move_weights['new_turn'])
                return score
            if captured_stones > 1:
                score = (captured_stones + Skinny.move_weights['capture'])
                return score
            if self.player_num == 1:
                if '' in player_two_cups:
                    for key,cup in enumerate(player_two_cups):
                        if cup == '':
                            if after_cups_ptwo[key] == '':
                                score = 1
                                return score
                        else:
                            return 2  
            if self.player_num != 1:
                if '' in player_one_cups:
                    for key,cup in enumerate(player_one_cups):
                        if cup == '':
                            if after_cups_pone[key] == '':
                                score = 1
                                return score
                        else:
                            return 2
            else:
                return 1
        else:
            my_mancala_idx = mancala_board.get_my_mancala_idx(self.player_num) # index of my mancala
            original_mancala = mancala_board.board[my_mancala_idx] #original amount of stones in mancala 
            test_board = mancala_board.get_test_board(move)
            board = mancala_board
            num_stones_pit = test_board.board[my_mancala_idx] #after the move is made
            captured_stones = num_stones_pit - original_mancala
            score = 0
            player_one_cups = [board.board[1],board.board[2],board.board[3],board.board[4],board.board[5],board.board[6]]
            player_two_cups = [board.board[8],board.board[9],board.board[10],board.board[11],board.board[12],board.board[13]]
            after_cups_pone = [test_board.board[1],test_board.board[2],test_board.board[3],test_board.board[4],test_board.board[5],test_board.board[6]]
            after_cups_ptwo = [test_board.board[8],test_board.board[9],test_board.board[10],test_board.board[11],test_board.board[12],test_board.board[13]]
            if test_board.player_num == self.player_num:
                score = (Skinny.move_weights['new_turn'])
                return score
            if captured_stones > 1:
                score = (captured_stones + Skinny.move_weights['capture'])
                return score
            if self.player_num == 1:
                if '' in player_two_cups:
                    for key,cup in enumerate(player_two_cups):
                        if cup == '':
                            if after_cups_ptwo[key] == '':
                                score = 1
                                return score
                        else:
                            return 2  
            else:
                return 1