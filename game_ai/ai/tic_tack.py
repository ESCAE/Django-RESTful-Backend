from random import randint
#import NN
def check_move(board, move):
    """makes sure the the move is vaild"""
    if board[move] == ' ':
        return True
    return False
def winner(board, player):
    """checks if there is a win condition"""
    if board[0] == player and board[1] == player and board[2] == player:
        if player == 'X':
            return (True, [0, 1, 2])
        return (False, [0, 1, 2])
    if board[0] == player and board[3] == player and board[6] == player:
        if player == 'X':
            return (True, [0, 3, 6])
        return (False, [0, 3, 6])
    if board[0] == player and board[4] == player and board[8] == player:
        if player == 'X':
            return (True, [0, 4, 8])
        return (False, [0, 4, 8])
    if board[1] == player and board[4] == player and board[7] == player:
        if player == 'X':
            return (True, [1, 4, 7])
        return (False, [1, 4, 7])
    if board[2] == player and board[5] == player and board[8] == player:
        if player == 'X':
            return (True, [2, 5, 8])
        return (False, [2, 5, 8])
    if board[2] == player and board[4] == player and board[6] == player:
        if player == 'X':
            return (True, [2, 4, 6])
        return (False, [2, 4, 6])
    if board[3] == player and board[4] == player and board[5] == player:
        if player == 'X':
            return (True, [3, 4, 5])
        return (False, [3, 4, 5])
    if board[6] == player and board[7] == player and board[8] == player:
        if player == 'X':
            return (True, [6, 7, 8])
        return (False, [6, 7, 8])
    output = (None, -1)
    return output
def new_board(board, move, chariter='X', flag=0):
    """makes a new board for the game"""
    output = []
    output_send = {'board': '', 'move': move, 'WL': None, 'Wline': None}
    output_str = ''
    for x in range(len(board)):
        if x != move:
            output.append(board[x])
            output_str += board[x]
        else:
            output.append(chariter)
            if chariter is 'X' or flag != 0:
                output_str += chariter
            else:
                output_str += board[x]
    output_send['board'] = output_str
    output_send['WL'] = winner(output, chariter)[0]
    output_send['Wline'] = winner(output, chariter)[1]
    return output_send
def directory(board, move, NN=0):
    """middle man for the front end and the NN"""
    board_list = []
    for x in board:
        board_list.append(x)
    board_dic = new_board(board_list, move)
    if board_dic['WL'] is not None:
        return board_dic
    board_list = []
    for x in board_dic['board']:
        board_list.append(x)
    if NN == 0:
        greedy_move = greedy_bot(board_list)
    elif NN == 1:
        greedy_move = dumb_bot(board_list)
    elif NN == 3:
        #greedy_move = NN
        pass
    board_dic = new_board(board_list, greedy_move ,'O')
    return board_dic
def new_board_bot(board, move, chariter='X'):
    """makes a new board for the bot"""
    output = []
    for x in board:
        output.append(x)
    output[move] = chariter
    return output
def greedy_bot(board, my_bot = 'O'):
    """makes a move based the the most wins"""
    wins = []
    count = 0
    if my_bot == 'O':
        my_plyer = 'X'
    else:
        my_plyer = 'O'
    for p in range(len(board)):
        count += 1
        if board[p] == ' ':
            newboard_0 = new_board_bot(board, p, my_bot)
            if winner(newboard_0, my_bot)[0] is False and my_bot == 'O' :
                return p
            elif winner(newboard_0, my_bot)[0] is True and my_bot == 'X' :
                return p
    for a in range(len(board)):
        count += 1
        wins.append(-1)
        if board[a] == ' ':
            wins[a] = 0
            newboard_0 = new_board_bot(board, a, my_bot)
            if winner(newboard_0, my_bot)[0] is False and my_bot == 'O' :
                return a
            elif winner(newboard_0, my_bot)[0] is True and my_bot == 'X' :
                return a
            for s in range(len(board)):
                count += 1
                if newboard_0[s] == ' ':
                    newboard_1 = new_board_bot(newboard_0, s, my_plyer)
                    if winner(newboard_1, my_plyer)[0] is False and my_plyer == 'O' :
                        return s
                    elif winner(newboard_1, my_plyer)[0] is True and my_plyer == 'X' :
                        return s
                    for d in range(len(board)):
                        count += 1
                        if newboard_1[d] == ' ':
                            newboard_2 = new_board_bot(newboard_1, d, my_bot)
                            if winner(newboard_2, my_bot)[0] is False and my_bot == 'O' :
                                wins[a] += 1
                                break
                            elif winner(newboard_2, my_bot)[0] is True and my_bot == 'X' :
                                wins[a] += 1
                                break
                            else:
                                for f in range(len(board)):
                                    count += 1
                                    if newboard_2[f] == ' ':
                                        newboard_3 = new_board_bot(newboard_2, f, my_plyer)
                                        if winner(newboard_3, my_plyer)[0] is False and my_plyer == 'O' :
                                            wins[a] -= 1
                                            break
                                        elif winner(newboard_3, my_plyer)[0] is True and my_plyer == 'X' :
                                            wins[a] -= 1
                                            break
                                        else:
                                            for g in range(len(board)):
                                                count += 1
                                                if newboard_3[g] == ' ':
                                                    newboard_4 = new_board_bot(newboard_3, g, my_bot)
                                                    if winner(newboard_4, my_bot)[0] is False and my_bot == 'O' :
                                                        wins[a] += 1
                                                        break
                                                    elif winner(newboard_4, my_bot)[0] is True and my_bot == 'X' :
                                                        wins[a] += 1
                                                        break
                                                    else:
                                                        for q in range(len(board)):
                                                            if newboard_4[q] == ' ':
                                                                newboard_5 = new_board_bot(newboard_4, q, my_plyer)
                                                                if winner(newboard_5, my_plyer)[0] is False and my_plyer == 'O' :
                                                                    wins[a] -= 1
                                                                    break
                                                                elif winner(newboard_5, my_plyer)[0] is True and my_plyer == 'X' :
                                                                    wins[a] -= 1
                                                                    break
                                                                else:
                                                                    for w in range(len(board)):
                                                                        if newboard_5[w] == ' ':
                                                                            newboard_6 = new_board_bot(newboard_5, w, my_bot)
                                                                            if winner(newboard_6, my_bot)[0] is False and my_bot == 'O' :
                                                                                wins[a] += 1
                                                                                break
                                                                            elif winner(newboard_6, my_bot)[0] is True and my_bot == 'X' :
                                                                                wins[a] += 1
                                                                                break
                                                                            else:
                                                                                for e in range(len(board)):
                                                                                    if newboard_6[e] == ' ':
                                                                                        newboard_7 = new_board_bot(newboard_6, e, my_plyer)
                                                                                        if winner(newboard_7, my_plyer)[0] is False and my_plyer == 'O' :
                                                                                            wins[a] -= 1
                                                                                            break
                                                                                        elif winner(newboard_7, my_plyer)[0] is True and my_plyer == 'X' :
                                                                                            wins[a] -= 1
                                                                                            break
                                                                                        else:
                                                                                            for r in range(len(board)):
                                                                                                if newboard_7[r] ==  ' ':
                                                                                                    newboard_8 = new_board_bot(newboard_7, r, my_bot)
                                                                                                    if winner(newboard_8, my_bot)[0] is False and my_bot == 'O' :
                                                                                                        wins[a] += 1
                                                                                                        break
                                                                                                    elif winner(newboard_8, my_bot)[0] is True and my_bot == 'X' :
                                                                                                        wins[a] += 1
                                                                                                        break
    the_max = float('-inf')
    total = 0
    for x in range(len(wins)):
        if the_max <= wins[x] and check_move(board, x):
            the_max = wins[x]
            total = x
    return total
def dumb_bot(board):
    """makes a random move"""
    while True:
        move = randint(0, 8)
        if board[move] == ' ':
            break
    return move
