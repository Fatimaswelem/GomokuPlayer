# Basic Minimax logic
from HeuristicEvaluator import get_lines, evaluate, evaluate_distance_to_center

class Minimax:

    @staticmethod
    def minimax(board, depth: int, maximizingPlayer: bool, heuristic_func=None):
        # Default to pattern heuristic if none provided
        if heuristic_func is None:
            heuristic_func = evaluate
        
        # Terminal state check
        if depth == 0 or Minimax.is_terminal(board):
            return heuristic_func(board, "X"), None

        if maximizingPlayer:
            value = float('-inf')
            possible_moves = Minimax.get_possible_moves(board)
            best_movement = possible_moves[0] if possible_moves else None
            
            for move in possible_moves:
                new_board = Minimax.make_move(board, move, "X")
              
                tmp = Minimax.minimax(new_board, depth-1, False, heuristic_func)[0]
                
                if tmp > value:
                    value = tmp
                    best_movement = move
                    
            return value, best_movement

        else:
            value = float('inf')
            possible_moves = Minimax.get_possible_moves(board)
            best_movement = possible_moves[0] if possible_moves else None
            
            for move in possible_moves:
                new_board = Minimax.make_move(board, move, "O")
              
                tmp = Minimax.minimax(new_board, depth-1, True, heuristic_func)[0]
                
                if tmp < value:
                    value = tmp
                    best_movement = move
                    
            return value, best_movement

    @staticmethod
    def is_terminal(board):
        # Check if game is over
        lines = get_lines(board)
        for line in lines:
            if "XXXXX" in line or "OOOOO" in line:
                return True
        
        # Check for draw
        for row in board:
            for cell in row:
                if cell == '_':
                    return False
        return True

    @staticmethod
    def get_possible_moves(board):
        """Get all empty positions"""
        moves = []
        for x in range(len(board)):
            for y in range(len(board[0])):
                if board[x][y] == '_':
                    moves.append((x, y))
        return moves

    @staticmethod
    def make_move(board, move, player):
        """Create new board with move made"""
        import copy
        new_board = copy.deepcopy(board)
        x, y = move[0], move[1]
        new_board[x][y] = player
        return new_board