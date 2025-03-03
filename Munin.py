from random import choice
from board import Board, Space, Coordinate
import pickle

class Munin:
    count = 0
    TRANSPOSITION_FILE = "the_time_stone.pkl"
    def __init__(self):
        self.name = f"MUNIN_{Munin.count}"
        Munin.count += 1
        self.depth = 3
        self.transpos_table = self.load_table()
    def get_opponent(self, color):
        if color == Space.RED:
            return Space.BLUE
        else:
            return Space.RED
    def evaluate(self, board: Board, color: Space):
        opponent = self.get_opponent(color)
        projected_board = board.__copy__()
        projected_board.clear_dead(color)
        projected_board.clear_dead(opponent)
        my_pieces = projected_board.count_elements(color)
        opponent_pieces = projected_board.count_elements(opponent)
        return (len(projected_board.mineable_by_player(color)) + my_pieces) - (len(projected_board.mineable_by_player(opponent)) + opponent_pieces)
    def clairvoyance(self, board: Board, color: Space, depth: int, alpha: float, beta: float, maximizing: bool):
        board_hash = hash(board)
        if board_hash in self.transpos_table:
            return self.transpos_table[board_hash]
        if depth == 0 or board.mineable_by_player(color) == 0:
            eval_score = self.evaluate(board,color)
            self.transpos_table[board_hash] = (eval_score, None)
            return eval_score, None
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
            self.transpos_table[board_hash] = (max_eval, best_move)
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
            self.transpos_table[board_hash] = (min_eval,best_move)
            #print("discovered")
            return min_eval, best_move
    def mine(self, board: Board, color: Space) -> Coordinate:
        eval_score, best_move = self.clairvoyance(board, color, self.depth, float('-inf'), float('inf'), True)
        self.save_table()
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
        self.save_table()
        if best_move:
            return best_move
        else:
            return None
    def save_table(self):
        with open(self.TRANSPOSITION_FILE, "wb") as f:
            pickle.dump(self.transpos_table, f)
    def load_table(self):
        try:
            with open(self.TRANSPOSITION_FILE, "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return {}