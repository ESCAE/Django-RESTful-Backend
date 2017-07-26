"""."""
import time
from random import randint
import datetime


class Spot(object):
    """."""

    def __init__(self, x, y):
        """."""
        self.xpos = x
        self.ypos = y
        self.full = False
        self.owner = False
        self.item = 'O'


class C4Game(object):
    """."""

    def __init__(self, board=None):
        """."""
        if board is None:
            self.board = self.make_board()
        else:
            self.board = board

    def dumb_bot(self):
        """."""
        while True:
            move = randint(0, 6)
            if self.real_move(move):
                break
        return move

    def new_board(self):
        """."""
        output = []
        for x in range(6):
            output.append([])
            for y in range(7):
                new_spot = Spot(x, y)
                new_spot.owner = self.board[x][y].owner
                new_spot.full = self.board[x][y].full
                new_spot.item = self.board[x][y].item
                output[x].append(new_spot)
        return output

    def make_board(self):
        """."""
        board = []
        for x in range(6):
            new_list = []
            board.append(new_list)
            for y in range(7):
                new_spot = Spot(x, y)
                board[x].append(new_spot)
        return board

    def print_board(self):
        """."""
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
        """."""
        count = 0
        while True:
            if self.board[count][xpos].owner:
                return count - 1
            if count == 5:
                return count
            count += 1

    def move(self, pos, player):
        """."""
        ypos = self.get_pos(pos)
        self.board[ypos][pos].full = True
        self.board[ypos][pos].owner = player

    def winner(self, xpos, ypos, player):
        """."""
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
                if self.board[ypos - (s + 1)][xpos - (s + 1)].owner == player and (ypos - (s + 1)) >= 0 and (xpos - (s + 1)):
                    count_1 += 1
                else:
                    break
            except IndexError:
                break
        for d in range(3):
            try:
                if self.board[ypos + (d + 1)][xpos - (d + 1)].owner == player and (xpos - (d + 1)):
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
                if self.board[ypos][xpos - (g + 1)].owner == player and (xpos - (g + 1)) >= 0:
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
                if self.board[ypos - (j + 1)][xpos].owner == player and (ypos - (j + 1)) >= 0:
                    count_4 += 1
                else:
                    break
            except IndexError:
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
            return True
        if count_2 >= 3:
            return True
        if count_3 >= 3:
            return True
        if count_4 >= 3:
            return True

    def real_move(self, pos):
        """."""
        return(not self.board[0][pos].full)

    def game(self):
        """."""
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
                else:
                    curr_move = input('Input move:')
                    curr_move = int(curr_move)
                    # curr_move = self.dumb_bot()
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

    def greedy_bot(self):
        """."""
        count = 0
        wins = []
        time = datetime.datetime.now()
        for a in range(7):
            count += 1
            self.print_board()
            wins.append(0)
            print(a)
            if self.real_move(a):
                board_1 = self.new_board()
                game_1 = C4Game(board_1)
                game_1.move(a, 'B')
                if game_1.winner(game_1.get_pos(a), a, 'B'):
                    return a
                self.print_board()
                for b in range(7):
                    count += 1
                    if self.real_move(b):
                        board_2 = game_1.new_board()
                        game_2 = C4Game(board_2)
                        game_2.move(b, 'R')
                        if game_2.winner(game_2.get_pos(b), b, 'R'):
                            if b == a:
                                wins[a] = float('-inf')
                            else:
                                return b
                        # game_1.print_board()
                        for c in range(7):
                            count += 1
                            if self.real_move(c):
                                board_3 = game_2.new_board()
                                game_3 = C4Game(board_3)
                                game_3.move(c, 'B')
                                if game_3.winner(game_3.get_pos(c), c, 'B'):
                                    wins[a] += 1
                                    game_3.print_board()
                                    print('hi')
                                    break
                                # game_2.print_board()
                                for d in range(7):
                                    count += 1
                                    if self.real_move(d):
                                        board_4 = game_3.new_board()
                                        game_4 = C4Game(board_4)
                                        game_4.move(d, 'R')
                                        if game_4.winner(game_4.get_pos(d), d, 'R'):
                                            wins[a] -= 1
                                            break
                                        for e in range(7):
                                            count += 1
                                            if self.real_move(e):
                                                board_5 = game_4.new_board()
                                                game_5 = C4Game(board_5)
                                                game_5.move(e, 'B')
                                                if game_5.winner(game_5.get_pos(e), e, 'B'):
                                                    wins[a] += 1
                                                    game_5.print_board()
                                                    print('cake')
                                                    break
                                                # for f in range(7):
                                                #     count += 1
                                                #     if self.real_move(f):
                                                #         board_6 = game_5.new_board()
                                                #         game_6 = C4Game(board_6)
                                                #         game_6.move(f, 'R')
                                                #         if game_6.winner(game_6.get_pos(f), f, 'R'):
                                                #             wins[a] -= 1
                                                #             break
                                                        # game_5.print_board()
                                                        # for g in range(7):
                                                        #     count += 1
                                                        #     if self.real_move(g):
                                                        #         board_7 = game_6.new_board()
                                                        #         game_7 = C4Game(board_7)
                                                        #         game_7.move(g, 'B')
                                                        #         if game_7.winner(game_7.get_pos(g), g, 'B'):
                                                        #             wins[a] += 1
                                                        #             break
                                                                # game_6.print_board()
                                                                # for h in range(7):
                                                                #     count += 1
                                                                #     if self.real_move(h):
                                                                #         board_8 = game_7.new_board()
                                                                #         game_8 = C4Game(board_8)
                                                                #         game_8.move(h, 'R')
                                                                #         if game_8.winner(game_8.get_pos(h), h, 'R'):
                                                                #             wins[a] -= 1
                                                                #             break
                                                                        # for i in range(7):
                                                                        #     count += 1
                                                                        #     if self.real_move(i):
                                                                        #         board_9 = game_8.new_board()
                                                                        #         game_9 = C4Game(board_9)
                                                                        #         game_9.move(i, 'B')
                                                                        #         if game_9.winner(game_9.get_pos(i), i, 'B'):
                                                                        #             wins[a] += 1
                                                                        #             break
                                                                        #         game_8.print_board()
                                                                        #         for j in range(7):
                                                                        #             count += 1
                                                                        #             if self.real_move(j):
                                                                        #                 board_10 = game_9.new_board()
                                                                        #                 game_10 = C4Game(board_10)
                                                                        #                 game_10.move(j, 'R')
                                                                        #                 if game_10.winner(game_10.get_pos(j), f, 'R'):
                                                                        #                     wins[a] -= 1
                                                                        #                     break
        move = 0
        curr_max = float('-inf')
        print(count)
        print(wins)
        for pos in range(7):
            if wins[pos] >= curr_max:
                curr_max = wins[pos]
                move = pos
        complete = datetime.datetime.now()
        print(complete - time)

        return move


new = C4Game()
# print(new.greedy_bot())
new.game()