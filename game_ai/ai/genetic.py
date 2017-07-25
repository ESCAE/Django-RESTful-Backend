"""The manipulation file for AI.py."""
from tic_tack import directory


class Game(object):
    """Docstring for Game."""

    def __init__(self):
        """Make a game."""
        self.board = '         '
        self.winner = None
        self.history = []

    def emptysquares(self, board):
        """Find empty spaces."""
        empty = []
        for i in range(9):
            if board[i] == ' ':
                empty.append(i)
        return empty

    def move(self, board, move):
        """Make a move and get the response."""
        self.history.append(self.board)
        next_board = directory(board, move)
        self.board = next_board['board']
        self.winner = next_board['WL']
        # self.board = self.board[:next_board['move']] + 'O' + self.board[next_board['move'] + 1:]
        # if self.winner is True:
        #     return
        # self.history.append(self.board)

    def undo(self):
        """Undo a move."""
        # if len(self.history) > 1:
        #     self.history.pop()
        self.board = self.history.pop()


class Individual(object):
    """."""

    def __init__(self, id, net):
        """."""
        self.id = id
        self.net = net
        self.age = float('-inf')
        self.score = float('-inf')
        self.AGE_MAX = 8
        self.SCORE_MAX = 4298

    def compare_to(self, other):
        """."""
        return Genetic.compare(self, other)

    def evaluate_one(self, b):
        """."""
        pass


class Genetic(object):
    """."""

    def __init__(self):
        """."""
        pass

    def generate_test_boards(self, boards=['         ' for i in range(8)],
                             visited={}, game=None):
        """Make some test boards."""
        boards = boards
        visited = visited
        game = game if game else Game()
        # print('---')
        # print(game.winner)
        emptysquares = game.emptysquares(game.board)
        try:
            if (visited[game.board] or game.winner or game.winner is False or len(emptysquares) <= 1):
                # print(visited[game.board])
                return boards
        except:
            pass

        print(emptysquares)
        try:
            boards[9 - len(emptysquares)] = game.board
        except:
            pass
        #     'right_moves': None
        # })

        visited[game.board] = True

        for move in emptysquares:
            game.move(game.board, move)
            self.generate_test_boards(boards, visited, game)
            game.undo()

        return boards

    def compare(self, a, b):
        """Compare two individual Neurals by age or score."""
        if a.age != b.age:
            return a.age - b.age
        return a.score - b.score

    def compare_descending(self, a, b):
        """."""
        return self.compare(b, a)


def translate():
    """."""
    pass


if __name__ == "__main__":
    test = Genetic()
    print(test.generate_test_boards())
