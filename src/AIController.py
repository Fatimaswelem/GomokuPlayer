# AIController.py

# Manages algorithm selection, integration, and comparison
import random
import time 
from Minimax import Minimax
from AlphaBeta import AlphaBeta 
from HeuristicEvaluator import (
    evaluate,                   # H2
    evaluate_distance_to_center,# H2
    combined_heuristic_medium,  #  H1 + H2 
    combined_heuristic_hard     #  H1 + H2 + H3 
)

class AIController:
    
    def __init__(self, depth_limit=2):
        self.depth_limit = depth_limit

        # --- Initialize Algorithms ---
        
        # 1. Easy Mode: Minimax + H1 @ Depth 2
        self.minimax_h1 = Minimax(1, heuristic_func=evaluate) 
        
        #  2. Medium Mode: AlphaBeta + H_Medium (H1 + H2) @ Depth 2
        # (Uses the original name 'alphabeta_h1' for compatibility with select_best_move)
        self.alphabeta_h1 = AlphaBeta(2, heuristic_func=combined_heuristic_medium) 

        # 3. Hard Mode: AlphaBeta + H_Hard (H1 + H2 + H3 )
        # (Uses the original name 'alphabeta_combined')
        self.alphabeta_combined = AlphaBeta(2, heuristic_func=combined_heuristic_hard) 
        
        
        # --- Other Optional Modes (Keeping the user's original definitions) ---
        self.minimax_basic = Minimax(self.depth_limit, heuristic_func=None)
        self.alphabeta_basic = AlphaBeta(self.depth_limit, heuristic_func=None)
        self.minimax_h2 = Minimax(self.depth_limit, heuristic_func=evaluate_distance_to_center)
        self.alphabeta_h2 = AlphaBeta(self.depth_limit, heuristic_func=evaluate_distance_to_center)

    def get_greedy_move(self, board, heuristic_func):
        """Finds the best move at depth 1 (Greedy)."""
        best_score = -float('inf')
        best_move = None
        nodes_count = 0
        
        possible_moves = board.get_possible_moves()
        random.shuffle(possible_moves)

        for r, c in possible_moves:
            nodes_count += 1
            board.make_move(r, c)
            
            # The player whose turn it WAS when the move was made
            eval_player = "O" if board.current_player == "X" else "X" 
            score = heuristic_func(board.board, eval_player) 
            
            board.undo_move(r, c)
            
            if score > best_score:
                best_score = score
                best_move = (r, c)
                
        return best_move, nodes_count


    def select_best_move(self, board, mode):
        """
        Selects the best move, tracks performance, and returns results.
        """
        
        start_time = time.time()
        move = None
        nodes_count = 0
        
        # --- Minimax H1 (Easy) ---
        if mode == "Minimax_H1":
            self.minimax_h1.nodes_explored = 0
            move = self.minimax_h1.find_best_move(board)
            nodes_count = self.minimax_h1.nodes_explored

        #  AlphaBeta H2 (MEDIUM Mode - Now uses H1 + H2 heuristic)
        elif mode == "AlphaBeta_H2": 
            # This uses the agent self.alphabeta_h1 which is now set to H_Medium
            self.alphabeta_h1.nodes_explored = 0
            self.alphabeta_h1.pruning_count = 0
            move = self.alphabeta_h1.find_best_move(board)
            nodes_count = self.alphabeta_h1.nodes_explored

        #  AlphaBeta Combined (HARD Mode - Now uses H1 + H2 + H3 Enhanced heuristic)
        elif mode == "AlphaBeta_Combined":
            # This uses the agent self.alphabeta_combined which is now set to H_Hard
            self.alphabeta_combined.nodes_explored = 0
            self.alphabeta_combined.pruning_count = 0
            move = self.alphabeta_combined.find_best_move(board)
            nodes_count = self.alphabeta_combined.nodes_explored
        
        # --- Optional Modes ---
        elif mode == "Heuristic_1_Only":
            move, nodes_count = self.get_greedy_move(board, evaluate)
        elif mode == "Heuristic_2_Only":
            move, nodes_count = self.get_greedy_move(board, evaluate_distance_to_center)
        elif mode == "Minimax_Basic":
            self.minimax_basic.nodes_explored = 0
            move = self.minimax_basic.find_best_move(board)
            nodes_count = self.minimax_basic.nodes_explored
        elif mode == "AlphaBeta_Basic":
            self.alphabeta_basic.nodes_explored = 0
            move = self.alphabeta_basic.find_best_move(board)
            nodes_count = self.alphabeta_basic.nodes_explored
        elif mode == "Minimax_H2":
            self.minimax_h2.nodes_explored = 0
            move = self.minimax_h2.find_best_move(board)
            nodes_count = self.minimax_h2.nodes_explored
        elif mode == "AlphaBeta_H1":
            # This block relies on the user's original setup where alphabeta_h1 was H1 only
            # Since alphabeta_h1 is now H_Medium, this mode will also use H_Medium (H1+H2)
            self.alphabeta_h1.nodes_explored = 0 
            move = self.alphabeta_h1.find_best_move(board)
            nodes_count = self.alphabeta_h1.nodes_explored
            
        else:
            print(f"Error: Invalid Mode ({mode})")
            return None, 0.0, 0 

        # --- Performance Reporting ---
        end_time = time.time()
        elapsed_time = end_time - start_time
        return move, elapsed_time, nodes_count
