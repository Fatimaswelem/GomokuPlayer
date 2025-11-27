# Basic Minimax logic
import math

class Minimax:
    def __init__(self, depth, heuristic_func=None):
        self.depth = depth
        self.heuristic_func = heuristic_func
        self.ai_player = None # Will store who the AI is (X or O)

    def find_best_move(self, board):
        """
        Starts the Minimax search.
        board: The Board object (must support make_move, undo_move, etc.)
        """
        # Capture who the AI is (the player whose turn it is at the start)
        self.ai_player = board.current_player
        
        # Start maximizing for the AI
        _, best_move = self._minimax(board, self.depth, True)
        return best_move

    def _minimax(self, board, depth, is_maximizing):
        # 1. Base Case: Terminal State or Max Depth reached
        if depth == 0 or board.is_terminal():
            return self._evaluate_state(board), None

        # 2. Get all legal moves from the Board class
        possible_moves = board.get_possible_moves()
        
        # If no moves available (draw/full), return 0
        if not possible_moves:
            return 0, None

        best_move = possible_moves[0] # Default fallback

        if is_maximizing:
            max_eval = -math.inf
            for r, c in possible_moves:
                # A. Make Move
                board.make_move(r, c)
                
                # B. Recurse (Switch to minimizing step)
                eval_score, _ = self._minimax(board, depth - 1, False)
                
                # C. Undo Move (Backtrack) - Crucial for speed
                board.undo_move(r, c)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (r, c)
            return max_eval, best_move

        else: # Minimizing step (Opponent's turn)
            min_eval = math.inf
            for r, c in possible_moves:
                board.make_move(r, c)
                
                # Recurse (Switch to maximizing step)
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
        # CASE 1: Heuristic Function is provided (Modes 5 & 6)
        if self.heuristic_func:
            # We evaluate the board grid from the perspective of the AI player
            # heuristic_func expects (board_grid, player_symbol)
            return self.heuristic_func(board.board, self.ai_player)

        # CASE 2: Basic Mode / No Heuristic (Mode 3)
        # If no heuristic, we only score if the game is actually over.
        if board.is_terminal():
            # Check who won. 
            # Note: board.check_winner usually checks the LAST move.
            # If is_terminal is true, someone just won or it's a draw.
            
            # Since we don't have easy access to 'who won' without re-checking logic,
            # we can infer:
            # If it was Maximizing's turn to play but it's terminal, 
            # the PREVIOUS player (Minimizing) made the winning move.
            
            # However, simpler logic for Basic Minimax:
            # If the board shows AI won -> +infinity
            # If the board shows Opponent won -> -infinity
            # We can use the HeuristicEvaluator's built-in win check logic manually 
            # or rely on board state.
            
            # Let's assume a simple fallback score if terminal:
            # We need to know if the LAST move won the game.
            # The Board class tracks 'current_player'.
            # If 'current_player' is X, then O just moved.
            winner = "O" if board.current_player == "X" else "X"
            
            if not board.is_full(): # If not full, someone won
                if winner == self.ai_player:
                    return 1000000 # AI Won
                else:
                    return -1000000 # AI Lost
            
            return 0 # Draw
            
        return 0 # Not terminal, no heuristic -> Score is 0