"""The manipulation file for AI.py."""
from tic_tack import directory

class Game(object):
    """docstring for Game"""
    def __init__(self, board, winner, empty_squares,):
        self.board = 
        self.winner = 
        self.empty_squares = 



class Individual(object):
    """."""
    def __init__(self, id, net):
        self.id = id
        self.net = net
        self.age = float('-inf')
        self.score = float('-inf')
        self.AGE_MAX = 8
        self.SCORE_MAX = 4298

    def compare_to(self, other):
        return Genetic.compare(self, other)

    def evaluate_one(self, b):
        pass

class Genetic(object):
    """."""

    def __init__(self):
        pass

    def generate_test_boards(self, boards, visited, game):
        boards = boards or [[], [], [], [], [], [], [], [], []]
        visited = visited or {{}}
        # game = game or new Ttt.Game()
        pass

    def compare(self, a, b):
        """Compare two individual Neurals by age or score."""
        if a.age != b.age:
            return a.age - b.age
        return a.score - b.score

    def compare_descending(self, a, b):
        return self.compare(b, a)


if __name__ == "__main__":
    print((directory('         ', 4)))
