# Alpha-Beta Pruning logic
import math

class AlphaBeta:
    def __init__(self, depth, heuristic_func=None):
        self.depth = depth
        self.heuristic_func = heuristic_func
        self.ai_player = None 
        # Statistics
        self.nodes_explored = 0 # <--- ADD THIS LINE for stats tracking
        self.pruning_count = 0 # <--- ADD THIS LINE for counting pruned nodes

    def find_best_move(self, board):
        """
        Starts the Alpha-Beta Pruning search.
        """
        self.ai_player = board.current_player
        
        # Reset counters
        self.nodes_explored = 0
        self.pruning_count = 0
        
        # Initialize Alpha (-infinity) and Beta (+infinity)
        alpha = -math.inf
        beta = math.inf
        
        # Start maximizing
        _, best_move = self._alphabeta(board, self.depth, alpha, beta, True)
        return best_move

    def _alphabeta(self, board, depth, alpha, beta, is_maximizing):
        # Count this node
        self.nodes_explored += 1 # <--- ADD THIS LINE for stats tracking
        
        # 1. Base Case: Terminal State or Max Depth
        if depth == 0 or board.is_terminal():
            return self._evaluate_state(board), None

        possible_moves = board.get_possible_moves()
        
        if not possible_moves:
            return 0, None

        best_move = possible_moves[0] 

        if is_maximizing:
            max_eval = -math.inf
            for r, c in possible_moves:
                board.make_move(r, c)
                
                # Recurse
                eval_score, _ = self._alphabeta(board, depth - 1, alpha, beta, False)
                
                board.undo_move(r, c)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (r, c)
                
                # Update Alpha
                alpha = max(alpha, eval_score)
                
                # Prune (Cutoff)
                if beta <= alpha:
                    self.pruning_count += 1
                    break 
                    
            return max_eval, best_move

        else: # Minimizing step
            min_eval = math.inf
            for r, c in possible_moves:
                board.make_move(r, c)
                
                eval_score, _ = self._alphabeta(board, depth - 1, alpha, beta, True)
                
                board.undo_move(r, c)

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (r, c)
                
                # Update Beta
                beta = min(beta, eval_score)
                
                # Prune (Cutoff)
                if beta <= alpha:
                    self.pruning_count += 1 # <--- ADD THIS LINE for counting pruned nodes
                    break 
                    
            return min_eval, best_move

    def _evaluate_state(self, board):
        """Helper to calculate score (Same as Minimax)."""
        if self.heuristic_func:
            return self.heuristic_func(board.board, self.ai_player)

        if board.is_terminal():
            winner = "O" if board.current_player == "X" else "X"
            if not board.is_full(): 
                if winner == self.ai_player:
                    return 1000000 
                else:
                    return -1000000
        return 0
