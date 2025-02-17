from random import choice
from board import Board, Space, Coordinate


class Pickaxer:

    count = 0

    def __init__(self):
        self.name = f"Pickaxer_{Pickaxer.count}"
        Pickaxer.count += 1
    def get_opponent(self, color):
        if color == Space.RED:
            opponent = Space.BLUE
        else:
            opponent = Space.RED
        return opponent
    def evaluate(self, board: Board, color: Space):
        opponent = self.get_opponent(color)
        opponent_mineable = (len(board.mineable_by_player(opponent)))
        self_mineable = len(board.mineable_by_player(color))
        opponent_pieces = len(board.find_all(opponent))
        self_pieces = len(board.find_all(color))
        opponent_score = opponent_mineable + opponent_pieces
        self_score = self_mineable + self_pieces
        score = self_score - opponent_score
        return score
    def clairvoyance(self, board: Board, color: Space):
        projected_board = board
        if projected_board.mineable_by_player(color) == 0:
            print("i have seen the future!!!")
            return 0
        for i in projected_board.mineable_by_player(color):
            projected_board[i] = (
            Space.EMPTY
            if projected_board.count_elements(color) == projected_board.miner_count
            else color
        )
            for v in projected_board.find_all(color):
                for z in projected_board.walkable_from_coord(v):
                    projected_board[v] = Space.EMPTY
                    projected_board[z] = color
                    print("iterated")
                    return(self.clairvoyance(projected_board, self.get_opponent(color)))
                    
                

    def mine(self, board: Board, color: Space) -> Coordinate:
        print(self.evaluate(board, color))
        print(self.clairvoyance(board, color))
        mineable = board.mineable_by_player(color)
        return choice(tuple(mineable))

    def move(self, board: Board, color: Space) -> tuple[Coordinate, Coordinate] | None:
        pieces = board.find_all(color)
        start = choice(tuple(pieces))
        ends = board.walkable_from_coord(start)
        if len(ends) == 0:
            return None
        return start, choice(tuple(ends))
