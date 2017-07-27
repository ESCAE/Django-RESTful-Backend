from random import randint


#def make_board(board):
  #  mid_line = '------\n'
    #output = ''
   # for x in range(9):
     #   if board[x] not in ['X', 'O']:
        #    output += ' '
        #else:
          #  output += board[x]
        #if x in [2, 5]:
          #  output += '\n'
            #output += mid_line
        #elif x != 8:
          #  output += '|'
   # print(output)


def check_move(board, move):
    if board[move] == ' ':
        return True
    return False


def winner(board, player):
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


def directory(board, move):
    board_list = []
    for x in board:
        board_list.append(x)
    board_dic = new_board(board_list, move)
    if board_dic['WL'] is not None:
        return board_dic
    board_list = []
    for x in board_dic['board']:
        board_list.append(x)
    greedy_move = greedy_bot(board_list)
    board_dic = new_board(board_list, greedy_move ,'O')
    return board_dic


def new_board_bot(board, move, chariter='X'):
    output = []
    for x in board:
        output.append(x)
    output[move] = chariter
    return output

def greedy_bot(board, my_bot = 'O'):
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
    while True:
        move = randint(0, 8)
        if board[move] == ' ':
            break
    return move


#def play_game():
    #board = [' ', ' ', ' ', ' ', ' ',  ' ', ' ',  ' ',  ' ']
    #player = randint(1, 2)
    #want_bot = 'Y'
    #move = ''
    #if want_bot == 'Y':
        #want_bot = True
    #else:
        #want_bot = False
    #turn = 0
    #while True:
        #turn += 1
        #if want_bot and player == 1:
            #while True:
                #output = 'It is player ' + str(player) + ' turn enter a move'
                #move = input(output)
                #if check_move(board, int(move)):
                    #break
                #print('Move is not vaild, please enter a vaild move ')
        #else:
            #move = greedy_bot(board)
        #if player == 1:
            #board[int(move)] = 'X'
        #else:
            #board[int(move)] = 'O'
        #if player == 1:
            #if winner(board, 'X'):
                #make_board(board)
                #output = 'player ' + str(player) + ' has won'
                #print(output)
                #break
        #else:
            #if winner(board, 'O'):
                #make_board(board)
                #output = 'player ' + str(player) + ' has won'
                #print(output)
                #break

        #make_board(board)
        #print('\n')
        #if player == 1:
            #player = 2
        #else:
            #player = 1
        #if turn == 9:
            #print('It is a tie, nobody wins')
            #break

