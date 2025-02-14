from random import choice
from board import Board, Space, Coordinate


class Pickaxer:

    count = 0

    def __init__(self):
        self.name = f"Pickaxer_{Pickaxer.count}"
        Pickaxer.count += 1
    def evaluate(self, board: Board, color: Space):
        if color == Space.RED:
            opponent = Space.BLUE
        else:
            opponent = Space.RED
        opponent_mineable = (len(board.mineable_by_player(opponent)))
        self_mineable = len(board.mineable_by_player(color))
        opponent_pieces = len(board.find_all(opponent))
        self_pieces = len(board.find_all(color))
        opponent_score = opponent_mineable + opponent_pieces
        self_score = self_mineable + self_pieces
        score = self_score - opponent_score
        return score
    def mine(self, board: Board, color: Space) -> Coordinate:
        print(self.evaluate(board, color))
        mineable = board.mineable_by_player(color)
        
        return choice(tuple(mineable))

    def move(self, board: Board, color: Space) -> tuple[Coordinate, Coordinate] | None:
        pieces = board.find_all(color)
        start = choice(tuple(pieces))
        ends = board.walkable_from_coord(start)
        if len(ends) == 0:
            return None
        return start, choice(tuple(ends))
