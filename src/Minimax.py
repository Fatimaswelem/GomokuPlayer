# Basic Minimax logic

import math

class Minimax:
    def __init__(self, depth, heuristic_func=None):
        self.depth = depth
        self.heuristic_func = heuristic_func
        self.ai_player = None 
        # Statistics
        self.nodes_explored = 0 # <--- ADD THIS LINE for counting explored nodes

    def find_best_move(self, board):
        """
        Starts the Minimax search.
        """
        # Capture who the AI is (the player whose turn it is at the start)
        self.ai_player = board.current_player
        
        # Reset counters for this search
        self.nodes_explored = 0
        
        # Start maximizing for the AI
        _, best_move = self._minimax(board, self.depth, True)
        return best_move

    def _minimax(self, board, depth, is_maximizing):
        # Count this node
        self.nodes_explored += 1 # <--- ADD THIS LINE for counting explored nodes
        
        # 1. Base Case: Terminal State or Max Depth reached
        if depth == 0 or board.is_terminal():
            return self._evaluate_state(board), None

        possible_moves = board.get_possible_moves()
        
        if not possible_moves:
            return 0, None

        best_move = possible_moves[0] # Default fallback

        if is_maximizing:
            max_eval = -math.inf
            for r, c in possible_moves:
                board.make_move(r, c)
                
                # Recurse
                eval_score, _ = self._minimax(board, depth - 1, False)
                
                board.undo_move(r, c)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (r, c)
            return max_eval, best_move

        else: # Minimizing step
            min_eval = math.inf
            for r, c in possible_moves:
                board.make_move(r, c)
                
                # Recurse
                eval_score, _ = self._minimax(board, depth - 1, True)
                
                board.undo_move(r, c)

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (r, c)
            return min_eval, best_move

    def _evaluate_state(self, board):
        """
        Helper to calculate the score of the board.
        Handles both 'Basic Mode' (Win/Loss only) and 'Heuristic Mode'.
        """
        # CASE 1: Heuristic Function is provided
        if self.heuristic_func:
            return self.heuristic_func(board.board, self.ai_player)

        # CASE 2: Basic Mode / No Heuristic
        if board.is_terminal():
            # Check who won based on the current player state
            winner = "O" if board.current_player == "X" else "X"
            
            if not board.is_full(): # If not full, someone won
                if winner == self.ai_player:
                    return 1000000 # AI Won
                else:
                    return -1000000 # AI Lost
            
        return 0