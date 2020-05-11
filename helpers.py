from math import inf


def Score(board, turn, count):

    # declare variables
    b = board
    t = -turn

    # rows
    if (b[0][0] == b[0][1] == b[0][2] == t) or (b[1][0] == b[1][1] == b[1][2] == t) or (b[2][0] == b[2][1] == b[2][2] == t):
        return t

    # cols
    elif (b[0][0] == b[1][0] == b[2][0] == t) or (b[0][1] == b[1][1] == b[2][1] == t) or (b[0][2] == b[1][2] == b[2][2] == t):
        return t        

    # diags
    elif (b[0][0] == b[1][1] == b[2][2] == t) or (b[0][2] == b[1][1] == b[2][0] == t):
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

    # In X turn
    if turn is 1:
        value = -inf
        for move in moves:
            game[move[0]][move[1]] = 1
            count += 1
            value = max(value, minimax(game, -1, count)) 

    # In O turn
    else:
        value = inf
        for move in moves:
            game[move[0]][move[1]] = -1
            count += 1
            value = min(value, minimax(game, 1, count))

    # Return index value
    return value


def Scores(moves, game, turn, count):

    # Scores of every a vailable move
    scores = [[None, None, None], [None, None, None], [None, None, None]]

    for row in range(3):
        for col in range(3):

            # check if 
            if (row, col) in moves:

                # Play the move 
                game[row][col] = turn

                # Record this move score    
                scores[row][col] = minimax(game, turn, count)  
    return scores  


def Best_move(game, turn, count):

    # Available moves
    moves = available_moves(game)

    # Score for each available move
    scores = Score(moves, game, turn, count)

    # If X turn play first available move with score 1
    if turn == 1:
        for row in range(3):
            for col in range(3):
                if scores[row][col] == 1:
                    return (row, col)

    # If O turn play any available move with score -1
    elif turn == -1:
        for row in range(3):
            for col in range(3):
                if scores[row][col] == -1:
                    return (row, col)

    # else play any available move with score 0
    for row in range(3):
        for col in range(3):
            if scores[row][col] == 0:
                return (row, col)            