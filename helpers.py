from math import inf


def Score(board, turn, count):

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


def minimax(game, turn, count):
    
    score = Score(game, turn, count)
    
    if score != None:
        return score
    
    moves = []
    value = 0

    for row in game:
        for col in row:
            if game[row][col] != None:
                moves.append((row, col))

    if turn is 1:
        value = -inf
        for move in moves:
            game[move[0]][move[1]] = 1
            count += 1
            value = max(value, minimax(game, -1, count)) 

    else:
        value = inf
        for move in moves:
            game[move[0]][move[1]] = -1
            count += 1
            value = min(value, minimax(game, 1, count))
    return value