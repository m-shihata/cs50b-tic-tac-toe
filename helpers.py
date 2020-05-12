from math import inf
from random import choice


def score(game, turn, count):

    # declare variables
    g = game
    t = -turn

    # is
    for i in range(3):
        if g[i][0] == g[i][1] == g[i][2] == t:
            return t

    # js
    for j in range(3):
        if g[0][j] == g[1][j] == g[2][j] == t:
            return t        

    # Diags
    if (g[0][0] == g[1][1] == g[2][2] == t) or (g[0][2] == g[1][1] == g[2][0] == t):
        return t

    # Tie
    elif count == 9:
        return 0

    # continue
    else:
        return None


def av_moves(game):

    moves = []

    for i in range(3):
        for j in range(3):
            if game[i][j] == 0:
                moves.append((i, j))

    return moves


def minimax(game, turn, count):

    # Base case to return if game is over 
    s = score(game, turn, count) 
    if s != None:
        return s 

    value = 0

    # X turn
    if turn is 1:
        value = -inf
        for move in av_moves(game):

            # Make a virtual move for X
            game[move[0]][move[1]] = turn
            count += 1
            turn *= -1

            # Recruse to get the value
            value = max(value, minimax(game, turn, count)) 

            # Undo the move
            game[move[0]][move[1]] = 0
            count -= 1
            turn *= -1

    # O turn
    else:
        value = inf
        for move in av_moves(game):

            # Make a virtual move for O
            game[move[0]][move[1]] = turn           
            count += 1
            turn *= -1

            # Recruse to get the value
            value = min(value, minimax(game, turn, count))
    
            # Undo the move 
            game[move[0]][move[1]] = 0
            count -= 1
            turn *= -1

    # Return index value
    return value


def scores(game, turn, count):

    # Scores of every a vailable move
    s = [[None, None, None], [None, None, None], [None, None, None]]

    # Try and error solution
    for i in range(3):

        for j in range(3):

            # check if the move is availble
            if (i, j) in av_moves(game):

                # Play the current move 
                game[i][j] = turn
                count += 1
                turn *= -1

                # Record this move score    
                s[i][j] = minimax(game, turn, count)  

                # Undo the last move for a new round   
                game[i][j] = 0
                count -= 1 
                turn *= -1

    return s 


def best_move(game, turn, count):

    # Best moves
    moves = []

    # To avoid taking so much time in first move 
    if count == 0:
        
        for i in range(3):
            for j in range(3):
                moves.append((i, j))

        return choice(moves)

    # Score for each available move
    s = scores(game, turn, count)

    # Winning moves
    for i in range(3):
        for j in range(3):
                
                # X turn
                if turn == 1:
                    if s[i][j] == 1:
                        moves.append((i, j))
                    
                # O turn
                elif turn == -1:
                    if s[i][j] == -1:
                        moves.append((i, j))
    
    # Return a random winning move
    if moves:
        return choice(moves)

    # Tie moves
    for i in range(3):
        for j in range(3):
            if s[i][j] == 0:
                moves.append((i, j))

    # Return a random tie move
    if moves:
        return choice(moves)

    # Losing moves
    for i in range(3):
        for j in range(3):
            # If X turn play first available move with score 1
            if turn == 1:
                if s[i][j] == -1:
                    moves.append((i, j))

            # If O turn play any available move with score -1
            elif turn == -1:
                if s[i][j] == 1:
                    moves.append((i, j))

    # Return a random losing move
    return choice(moves)