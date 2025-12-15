# Manages algorithm selection, integration, and comparison
# contains Easy, Medium, and Hard modes

import random
import time 
from Minimax import Minimax
from AlphaBeta import AlphaBeta 
from HeuristicEvaluator import evaluate, evaluate_distance_to_center, evaluate_freedom

class AIController:
    
    def __init__(self, depth_limit=3): 
        # --- 1. EASY MODE (Minimax + H1 @ Depth 1) ---
        self.easy_bot = Minimax(depth=1, heuristic_func=evaluate) 
        
        # --- 2. MEDIUM MODE (AlphaBeta + H1 + H2 @ Depth 3) ---
        self.medium_bot = AlphaBeta(depth=3, heuristic_func=self.heuristic_medium) 

        # --- 3. HARD MODE (AlphaBeta + H1 + H2 + H3 @ Depth 4) ---
        self.hard_bot = AlphaBeta(depth=4, heuristic_func=self.heuristic_hard) 

    # --- Heuristic Combinations ---

    def heuristic_medium(self, board_grid, player):
        """Medium: Pattern (H1) + Center (H2)"""
        h1 = evaluate(board_grid, player)
        h2 = evaluate_distance_to_center(board_grid, player)
        return h1 + h2

    def heuristic_hard(self, board_grid, player):
        """Hard: Pattern (H1) + Center (H2) + Freedom (H3)"""
        h1 = evaluate(board_grid, player) 
        h2 = evaluate_distance_to_center(board_grid, player)
        h3 = evaluate_freedom(board_grid, player)
        return (h1 * 1.5) + h2 + h3

    # --- Main Selection Logic ---

    def select_best_move(self, board, mode):
        print(f"--- AI Thinking: {mode} ---")
        start_time = time.time()
        move = None
        nodes_count = 0
        
        # 1. EASY (Blunder Factor Added)
        if mode == "Minimax_H1":
            # 30% Chance to make a mistake (Human-like beginner behavior)
            if random.random() < 0.3:
                candidates = board.get_possible_moves()
                if candidates:
                    print(">> Oops! AI made a blunder (Easy Mode).")
                    move = random.choice(candidates)
                    nodes_count = 0 # No search done
            
            # 70% Chance to play the best move
            if move is None: 
                self.easy_bot.nodes_explored = 0
                move = self.easy_bot.find_best_move(board)
                nodes_count = self.easy_bot.nodes_explored

        # 2. MEDIUM
        elif mode == "AlphaBeta_H2": 
            self.medium_bot.nodes_explored = 0
            self.medium_bot.pruning_count = 0
            move = self.medium_bot.find_best_move(board)
            nodes_count = self.medium_bot.nodes_explored

        # 3. HARD
        elif mode == "AlphaBeta_Combined":
            self.hard_bot.nodes_explored = 0
            self.hard_bot.pruning_count = 0
            move = self.hard_bot.find_best_move(board)
            nodes_count = self.hard_bot.nodes_explored
            
        else:
            print(f"Error: Invalid Mode ({mode})")
            return None, 0, 0 

        # --- Performance Reporting ---
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Stats -> Time: {elapsed_time:.4f}s | Nodes: {nodes_count} | Move: {move}")
        
        return move, elapsed_time, nodes_count