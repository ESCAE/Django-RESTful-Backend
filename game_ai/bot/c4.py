import time
from random import randint
class spot(object):
    def __init__(self, x , y):
        self.xpos = x
        self.ypos = y
        self.full = False
        self.owner = False
        self.item = 'O'

class c4Game(object):

    def dumb_bot(self):
        while True:
            move = randint(0,6)
            if self.real_move(move):
                break
        return move

    def new_board()

    def make_board(self):
        board = []
        for x in range(6):
            new_list = []
            board.append(new_list)
            for y in range(7):
                new_spot = spot(x, y)
                board[x].append(new_spot)
        return board



    def __init__(self, board = None):
        if board is None:
            self.board = self.make_board()
        else:
            self.board = board

    def print_board(self):
        board_build = ''
        for x in range(6):
            for y in range(7):
                if self.board[x][y].owner is not False:
                    board_build += self.board[x][y].owner
                else:
                    board_build += 'O'
            board_build += '\n'
        print(board_build)

    def get_pos(self, xpos):
        curr = xpos
        count = 0
        while True:
            if self.board[count][xpos].owner:
                return count -1
            if count == 5:
                return count
            count += 1

    def move(self, pos, player):
        ypos = self.get_pos(pos)
        self.board[ypos][pos].full = True
        self.board[ypos][pos].owner = player

    def winner(self,xpos, ypos, player):
        print(xpos)
        print(ypos)
        count_1 = 0
        count_2 = 0
        count_3 = 0
        count_4 = 0
        for a in range(3):
            try:
                if self.board[ypos + (a + 1)][xpos + (a + 1)].owner == player:
                    count_1 += 1
                else:
                    break
            except IndexError:
                break
        for s in range(3):
            try:
                if self.board[ypos - (s + 1)][xpos - (s + 1)].owner == player and (ypos - (s+1)) >= 0 and (xpos - (s+1)):
                    count_1 += 1
                else:
                    break
            except IndexError:
                break
        for d in range(3):
            try:
                if self.board[ypos + (d + 1)][xpos - (d + 1)].owner == player and (xpos - (d+1)):
                    count_2 += 1
                else:
                    break
            except IndexError:
                break
        for f in range(3):
            try:
                if self.board[ypos - (f + 1)][xpos + (f + 1)].owner == player:
                    count_2 += 1
                else:
                    break
            except IndexError:
                break
        for g in range(3):
            try:
                if self.board[ypos][xpos - (g + 1)].owner == player and (xpos -(g + 1)) >= 0:
                    count_3 += 1
                else:
                    break
            except IndexError:
                break
        for h in range(3):
            try:
                if self.board[ypos][xpos + (h + 1)].owner == player:
                    count_3 += 1
                else:
                    break
            except IndexError:
                break
        for j in range(3):
            try:
                if self.board[ypos - (j + 1)][xpos].owner == player and (ypos- (j+1)) >= 0:
                    count_4 += 1
                else:
                    break
            except IndexError:
                print(j)
                break
        for k in range(3):
            try:
                if self.board[ypos + (k + 1)][xpos].owner == player:
                    count_4 += 1
                else:
                    break
            except IndexError:
                break
        if count_1 >= 3:
            print('count is 1')
            return True
        if count_2 >= 3:
            print('count is 2')
            return True
        if count_3 >= 3:
            print('count is 3')
            return True
        if count_4 >= 3:
            print('count is 4')
            return True

    def real_move(self, pos):
        return(not self.board[0][pos].full)

    def game(self):
        print('Lets start the game')
        print('Making board ')
        time.sleep(1)
        print('Done')
        palyer1 = 'R'
        palyer2 = 'B'
        turn = 1
        while True:
            print('It is player ' + str(turn) + ' turn')
            while True:
                if turn == 1:
                    curr_move = input('Input move:')
                    curr_move = int(curr_move)
                #print(curr_move)
                else:
                    curr_move = self.dumb_bot()
                if self.real_move(curr_move):
                    break
                print ('move is not vaild')
            other_spot = self.get_pos(curr_move)
            if turn == 1:
                self.move(curr_move, palyer1)
            else:
                self.move(curr_move, palyer2)
            if turn == 1:
                if self.winner(curr_move, other_spot, palyer1):
                    self.print_board()
                    print('Player 1 has won')
                    break
            else:
                if self.winner(curr_move, other_spot, palyer2):
                    self.print_board()
                    print('Player 2 has won')
                    break
            if turn == 1:
                turn = 2
            else:
                turn = 1
            self.print_board()






new = c4Game()
new.game()
