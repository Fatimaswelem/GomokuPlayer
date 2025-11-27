# Manages algorithm selection, integration, and comparison
import random
import time  # Required for performance tracking
from Minimax import Minimax
from AlphaBeta import AlphaBeta 
from HeuristicEvaluator import evaluate, evaluate_distance_to_center

class AIController:
    def __init__(self, depth_limit=3):
        self.depth_limit = depth_limit

        # --- Initialize Algorithms ---
        # We ensure every algorithm instance allows us to access its internal stats later
        self.minimax_basic = Minimax(depth_limit, heuristic_func=None)
        self.alphabeta_basic = AlphaBeta(depth_limit, heuristic_func=None)
        self.minimax_h1 = Minimax(depth_limit, heuristic_func=evaluate)
        self.minimax_h2 = Minimax(depth_limit, heuristic_func=evaluate_distance_to_center)
        self.alphabeta_h1 = AlphaBeta(depth_limit, heuristic_func=evaluate)

    def get_greedy_move(self, board, heuristic_func):
        """Modes 1 & 2: Greedy Search (1 step lookahead)."""
        nodes_explored = 0 # Stat tracking
        best_score = float('-inf')
        best_move = None
        
        legal_moves = board.get_possible_moves()
        if not legal_moves: return None
        random.shuffle(legal_moves)

        for r, c in legal_moves:
            nodes_explored += 1 # Count every move evaluated
            
            board.make_move(r, c)
            player_who_just_moved = "O" if board.current_player == "X" else "X"
            score = heuristic_func(board.board, player_who_just_moved)
            board.undo_move(r, c)
            
            if score > best_score:
                best_score = score
                best_move = (r, c)
        
        # Return move AND stats (tuple for internal use, though select_best_move handles unwrapping)
        return best_move, nodes_explored

    def select_best_move(self, board, mode):
        """
        Executes the logic for the 6 modes AND tracks performance stats.
        """
        print(f"--- AI Turn: {mode} ---")
        start_time = time.time()
        
        move = None
        nodes_count = 0
        algorithm_used = mode

        # --- MODE 1 & 2: Greedy ---
        if mode == "Heuristic_1_Only":
            move, nodes_count = self.get_greedy_move(board, evaluate)
        elif mode == "Heuristic_2_Only":
            move, nodes_count = self.get_greedy_move(board, evaluate_distance_to_center)

        # --- MODE 3: Minimax Basic ---
        elif mode == "Minimax_Basic":
            self.minimax_basic.nodes_explored = 0 # Reset counter
            move = self.minimax_basic.find_best_move(board)
            nodes_count = self.minimax_basic.nodes_explored

        # --- MODE 4: AlphaBeta Basic ---
        elif mode == "AlphaBeta_Basic":
            self.alphabeta_basic.nodes_explored = 0 # Reset counter
            self.alphabeta_basic.pruning_count = 0  # Reset pruning
            move = self.alphabeta_basic.find_best_move(board)
            nodes_count = self.alphabeta_basic.nodes_explored
            # Note: You can also print pruning_count if needed

        # --- MODE 5: Minimax H1 ---
        elif mode == "Minimax_H1":
            self.minimax_h1.nodes_explored = 0
            move = self.minimax_h1.find_best_move(board)
            nodes_count = self.minimax_h1.nodes_explored

        # --- MODE 6: Minimax H2 ---
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