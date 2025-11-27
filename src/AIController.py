# Manages algorithm selection, integration, and comparison
import random
import time
from Minimax import Minimax
from AlphaBeta import AlphaBeta 
from HeuristicEvaluator import evaluate, evaluate_distance_to_center

class AIController:
    def __init__(self, depth_limit=3):
        self.depth_limit = depth_limit

        # --- Initialize Algorithms ---
        
        # 1. Minimax + Heuristic 1 (Pattern)
        self.minimax_h1 = Minimax(depth_limit, heuristic_func=evaluate)
        
        # 2. AlphaBeta + Heuristic 2 (Center Distance) - You asked for this specifically
        self.alphabeta_h2 = AlphaBeta(depth_limit, heuristic_func=evaluate_distance_to_center)

        # 3. NEW: AlphaBeta + Combined (H1 + H2)
        # We pass the 'combined_heuristic' method defined below
        self.alphabeta_combined = AlphaBeta(depth_limit, heuristic_func=self.combined_heuristic)

        # (Keep the others for your other modes if needed)
        self.minimax_basic = Minimax(depth_limit, heuristic_func=None)
        self.alphabeta_basic = AlphaBeta(depth_limit, heuristic_func=None)
        self.minimax_h2 = Minimax(depth_limit, heuristic_func=evaluate_distance_to_center)
        self.alphabeta_h1 = AlphaBeta(depth_limit, heuristic_func=evaluate)

    def combined_heuristic(self, board_grid, player):
        """
        Calculates the sum of H1 and H2.
        H1 handles tactical threats (High scores).
        H2 handles positional advantage (Low scores).
        """
        score_h1 = evaluate(board_grid, player)
        score_h2 = evaluate_distance_to_center(board_grid, player)
        
        # Simply adding them works as a perfect tie-breaker logic
        return score_h1 + score_h2

    def get_greedy_move(self, board, heuristic_func):
        """Modes 1 & 2: Greedy Search (1 step lookahead)."""
        nodes_explored = 0 
        best_score = float('-inf')
        best_move = None
        
        legal_moves = board.get_possible_moves()
        if not legal_moves: return None, 0
        random.shuffle(legal_moves)

        for r, c in legal_moves:
            nodes_explored += 1
            board.make_move(r, c)
            player_who_just_moved = "O" if board.current_player == "X" else "X"
            
            # Use the heuristic function passed in
            score = heuristic_func(board.board, player_who_just_moved)
            
            board.undo_move(r, c)
            
            if score > best_score:
                best_score = score
                best_move = (r, c)
        
        return best_move, nodes_explored

    def select_best_move(self, board, mode):
        """
        Executes the logic for the modes AND tracks performance stats.
        """
        print(f"--- AI Turn: {mode} ---")
        start_time = time.time()
        
        move = None
        nodes_count = 0

        # --- MODE 1: Minimax + H1 ---
        if mode == "Minimax_H1":
            self.minimax_h1.nodes_explored = 0
            move = self.minimax_h1.find_best_move(board)
            nodes_count = self.minimax_h1.nodes_explored

        # --- MODE 2: AlphaBeta + H2 ---
        elif mode == "AlphaBeta_H2":
            self.alphabeta_h2.nodes_explored = 0
            move = self.alphabeta_h2.find_best_move(board)
            nodes_count = self.alphabeta_h2.nodes_explored

        # --- MODE 3: AlphaBeta + Combined (H1 & H2) ---
        elif mode == "AlphaBeta_Combined":
            self.alphabeta_combined.nodes_explored = 0
            move = self.alphabeta_combined.find_best_move(board)
            nodes_count = self.alphabeta_combined.nodes_explored

        # --- OTHER EXISTING MODES (Keep these for your GUI buttons) ---
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

        else:
            print(f"Error: Invalid Mode ({mode})")
            return None

        # --- Performance Reporting ---
        end_time = time.time()
        duration = end_time - start_time
        print(f"Stats -> Time: {duration:.4f}s | Nodes Explored: {nodes_count} | Move: {move}")
        
        return move