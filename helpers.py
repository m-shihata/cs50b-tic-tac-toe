from math import inf
from copy import deepcopy


def Score(game, turn, count):

    # declare variables
    g = game
    t = -turn

    # rows
    if (g[0][0] == g[0][1] == g[0][2] == t) or (g[1][0] == g[1][1] == g[1][2] == t) or (g[2][0] == g[2][1] == g[2][2] == t):
        return t

    # cols
    elif (g[0][0] == g[1][0] == g[2][0] == t) or (g[0][1] == g[1][1] == g[2][1] == t) or (g[0][2] == g[1][2] == g[2][2] == t):
        return t        

    # diags
    elif (g[0][0] == g[1][1] == g[2][2] == t) or (g[0][2] == g[1][1] == g[2][0] == t):
        return t

    # tie
    elif count == 9:
        return 0

    # continue
    else:
        return None


def available_moves(game):

    moves = []

    for row in range(3):
        for col in range(3):
            if game[row][col] == 0:
                moves.append((row, col))

    return moves


def minimax(game, turn, count):

    # Base case to return if game is over 
    if Score(game, turn, count) != None:
        return Score(game, turn, count)  

    # Available moves
    moves = available_moves(game)
    value = 0

    # X turn
    if turn is 1:
        value = -inf
        for move in moves:

            game[move[0]][move[1]] = turn
            count += 1
            turn *= -1

            value = max(value, minimax(game, turn, count)) 

            game[move[0]][move[1]] = 0
            count -= 1
            turn *= -1

    # O turn
    else:
        value = inf
        for move in moves:

            game[move[0]][move[1]] = turn           
            count += 1
            turn *= -1

            value = min(value, minimax(game, turn, count))
    
            game[move[0]][move[1]] = 0
            count -= 1
            turn *= -1

    # Return index value
    return value


def Scores(game, turn, count):

    # available moves
    moves = available_moves(game)

    # Scores of every a vailable move
    scores = [[None, None, None], [None, None, None], [None, None, None]]

    # Try and error solution
    for row in range(3):

        for col in range(3):

            # check if the move is availble
            if (row, col) in moves:

                # Play the current move 
                game[row][col] = turn
                count += 1
                turn *= -1

                # Record this move score    
                scores[row][col] = minimax(game, turn, count)  

                # Undo the last move for a new round   
                game[row][col] = 0
                count -= 1 
                turn *= -1

    return scores  


def Best_move(game, turn, count):

    # Available moves
    moves = available_moves(game)

    # Score for each available move
    scores = Scores(game, turn, count)

    # Iterage over every score to decide which fits more 
    for row in range(3):

        for col in range(3):
            
            if (row, col) in moves:
                
                # If X turn play first available move with score 1
                if turn == 1:
                    if scores[row][col] == 1:
                        return (row, col)

                # If O turn play any available move with score -1
                elif turn == -1:
                    if scores[row][col] == -1:
                        return (row, col)

    # If all scores iterated and no one return win move return a tie move 
    for row in range(3):
        for col in range(3):
            if scores[row][col] == 0:
                return (row, col)            