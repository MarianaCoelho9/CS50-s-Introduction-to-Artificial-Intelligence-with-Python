"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    total_X=0
    total_O=0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j]==X:
                 total_X+=1
            if board[i][j]==O:
                 total_O+=1
    if total_X==total_O:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions=[]
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j]==EMPTY:
                actions.append((i,j))
    
    return actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if not action in actions(board):
        raise ("Action not possible")
    
    result_board= copy.deepcopy(board)
    result_board[action[0]][action[1]]=player(board)

    return result_board




def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        #Horizontal win
        if board[i][0]==board[i][1]==board[i][2]:
            return board[i][0]
    for j in range(len(board[0])):
        #vertical win
        if board[0][j]==board[1][j]==board[2][j]:
            return board[0][j]
     
    #Diagnal win   
    if board[0][0]==board[1][1]==board[2][2]:
        return board[0][0]
    
    if board[2][0]==board[1][1]==board[0][2]:
        return board[2][0]

    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if (not any(None in subl for subl in board)) or winner(board)==X or winner(board)==O:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board)==X:
        return 1
    if winner(board)==O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board) is True:
        return None
    
    if player(board)==X:
        max=-999999999999999
        optimal_action=[]
        aux=0
        for action in actions(board):
            aux=min_value(result(board, action))
            if aux>max:
                max=aux
                optimal_action=action
    else:
        min=+999999999999999
        optimal_action=[]
        aux=0
        for action in actions(board):
            aux=max_value(result(board, action))
            print('a', aux)
            if aux<min:
                min=aux
                optimal_action=action
    
    return optimal_action


def max_value (board):
    v=-999999999999999
    if terminal(board) is True:
        return utility(board)
    for action in actions(board):
        v=max(v, min_value(result(board, action)))
    return v

def min_value (board):
    v=+ 999999999999999
    if terminal(board) is True:
        return utility(board)
    for action in actions(board):
        v=min(v, max_value(result(board, action)))
    return v

        
