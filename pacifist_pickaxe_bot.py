from random import choice
from board import Board, Space, Coordinate

class Pacifist_Pickaxer:
    count = 0

    def __init__(self):
        self.name = f"Pickaxer_{Pacifist_Pickaxer.count}"
        Pacifist_Pickaxer.count += 1
        self.depth = 3
    def get_opponent(self, color):
        if color == Space.RED:
            return Space.BLUE
        else:
            return Space.RED
    def evaluate(self, board: Board, color: Space):
        opponent = self.get_opponent(color)
        projected_board = board.__copy__()
        my_pieces = projected_board.count_elements(color)
        opponent_pieces = projected_board.count_elements(opponent)
        return (len(projected_board.mineable_by_player(color)) + my_pieces) - (len(projected_board.mineable_by_player(opponent)) + opponent_pieces)
    def clairvoyance(self, board: Board, color: Space, depth: int, alpha: float, beta: float, maximizing: bool):
        if depth == 0 or board.mineable_by_player(color) == 0:
            return self.evaluate(board, color), None
        best_move = None
        if maximizing:
            max_eval = float('-inf')
            for move in board.mineable_by_player(color):
                projected_board = board.__copy__()
                if projected_board.count_elements(color) < projected_board.miner_count:
                    projected_board[move] = color 
                else:
                    projected_board[move] = Space.EMPTY
                eval_score, loc = self.clairvoyance(projected_board, self.get_opponent(color), depth-1, alpha, beta, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in board.mineable_by_player(self.get_opponent(color)):
                projected_board = board.__copy__()
                
                if projected_board.count_elements(self.get_opponent(color)) < projected_board.miner_count: 
                    projected_board[move] = self.get_opponent(color) 
                else:
                    projected_board[move] = Space.EMPTY
                eval_score, loc = self.clairvoyance(projected_board, color, depth-1, alpha, beta, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move
    def mine(self, board: Board, color: Space) -> Coordinate:
        eval_score, best_move = self.clairvoyance(board, color, self.depth, float('-inf'), float('inf'), True)
        if best_move:
            return best_move
        else:
            return choice(tuple(board.mineable_by_player(color)))
    def move(self, board: Board, color: Space) -> tuple[Coordinate, Coordinate] | None:
        pieces = board.find_all(color)
        best_move = None
        max_eval = float('-inf')
        for piece in pieces:
            for move in board.walkable_from_coord(piece):
                projected_board = board.__copy__()
                projected_board[piece] = Space.EMPTY
                projected_board[move] = color
                eval_score = self.evaluate(projected_board, color)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (piece, move)
        if best_move:
            return best_move
        else:
            return None
