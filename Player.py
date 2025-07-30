from random import randint
import numpy as np
import sys
import copy
from operator import itemgetter
import random
class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
             
    def actions(self, board):
            valid_moves = []
            for col in range(7):
                for row in range(5,-1,-1):
                    if board[row][col] == 0:
                        valid_moves.append([row, col])
                        break
            return valid_moves          
    
    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        

        values = []

        def find_best_move(board, depth, alpha, beta, current_player, opponent_player):
            for row, col in self.actions(board):
                board[row][col] = current_player
                alpha = max(alpha, minimize(board,alpha, beta,depth + 1 ,current_player, opponent_player))
                values.append((alpha, col))
                board[row][col] = 0
            max_value = (max(values,key=itemgetter(1))[0]) 
            for item in values:
                if max_value in item:
                    max_index = item[1]
                    break
            return max_index

        def minimize(board, alpha, beta, depth, current_player, opponent_player):
            valid_moves = self.actions(board)
            if depth == 4 or not valid_moves:
                return self.evaluation_function(board)
            for row, col in valid_moves:
                board[row][col] = opponent_player
                result = maximize(board, alpha, beta, depth + 1, current_player, opponent_player)
                beta = min(beta, result)
                board[row][col] = 0
                if beta <= alpha:
                    return beta
            return beta

        def maximize(board, alpha, beta, depth, current_player, opponent_player):
            valid_moves = self.actions(board)
            if depth == 4 or not valid_moves:
                return self.evaluation_function(board)
            for row, col in valid_moves:
                board[row][col] = current_player
                result = minimize(board, alpha, beta, depth + 1, current_player, opponent_player)
                alpha = max(alpha, result)
                board[row][col] = 0
                if alpha >= beta:
                    return alpha
            return alpha

        try:
            current_player = self.player_number
            if current_player == 1:
                opponent_player = 2
            else:
                opponent_player = 1
            return find_best_move(board, 0, -sys.maxsize, sys.maxsize, current_player, opponent_player)
        except Exception as e:
            raise NotImplementedError("Oops! I'm not sure what to do.")

        
    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        def actions(board):
            act_list=[]
            for i in range(len(board[0])):
                if 0 in board[:,i]:
                    act_list.append(i)
            return act_list
        
        def result(board,act):
            temp_board=copy.deepcopy(board)
            for i in range(board.shape[0]-1,-1,-1):
                if temp_board[i][act]==0:
                    temp_board[i][act]=self.player_number
                    return temp_board
                
        def max_value(board,depth,alpha,beta):
            print('max',depth)
            if depth==3:
                return self.evaluation_function(board),board
            v=-sys.maxsize
            res_board=None
            for act in actions(board):
                v_temp,bb=chance_node(result(board,act),depth+1,alpha,beta)
                if v_temp>v:
                    v=v_temp
                    res_board=bb
                
                if v>=beta:
                    return v,res_board
                
            return v,res_board
        
        def chance_node(board,depth,alpha,beta):
            print('min',depth)
            if depth==3:
                return self.evaluation_function(board),board
            v=sys.maxsize
            probab=1/7
            res_board=None
            for act in actions(board):
                v1,res_board=max_value(result(board,act),depth+1,alpha,beta)
                v+=v1*probab
    
            return int(v),res_board
        try:
            v,r=max_value(board,0,-sys.maxsize,sys.maxsize)    
            for j in range(6):
                for k in range(7):
                    if board[j][k]!=r[j][k]:
                        return k
        
        except Exception as e:
            raise NotImplementedError('Whoops I don\'t know what to do')
        

    def player_count(self,row,player_number):
        count_row=0
        c=0
        for j in range(len(row)):
            if row[j]==player_number:
                c+=1 
            else:
                count_row+=max(count_row,c)
                c=0
        count_row=max(count_row,c)
        return count_row
    
    def eval_count_values(self, board, num, player_num):
        numberofwins = 0 
        player_win_str = '{0}' * num 
        player_win_str = player_win_str.format(player_num)
        to_str = lambda a: ''.join(a.astype(str))

        def checking_horizontal(b):
            count = 0
            for row in b:
                if player_win_str in to_str(row):
                    count += to_str(row).count(player_win_str) 
            return count

        def checking_verticle(b):
            return checking_horizontal(b.T)

        def checking_diagonal(b):
            count = 0 
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                root_diag = np.diagonal(op_board, offset=0).astype(int)
                if player_win_str in to_str(root_diag):
                    count += to_str(root_diag).count(player_win_str) 

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(int))
                        if player_win_str in diag:
                            count += diag.count(player_win_str) 
            return count 
        numberofwins = checking_horizontal(board) + checking_verticle(board) + checking_diagonal(board) 
        return numberofwins

    

    def evaluation_function(self, board):
        """
        Given the current stat of the board, return the scalar value that 
        represents the evaluation function for the current player
       
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The utility value for the current board
        """
        res_eval = 0
        player = self.player_number
        if (player == 1): 
            opponent = 2
        else: 
            opponent = 1
        res_eval = self.eval_count_values( board, 4, player) * 100
        res_eval += self.eval_count_values( board, 3, player) * 10
        res_eval += self.eval_count_values( board, 2, player) * 1

        res_eval -= self.eval_count_values( board, 4, opponent) * 95 
        res_eval -= self.eval_count_values( board, 3, opponent) * 10 
        res_eval -= self.eval_count_values( board, 2, opponent) * 1

        return (res_eval)
        
class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)

class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move
