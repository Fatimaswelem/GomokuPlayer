import time
from Board import Board
from Minimax import Minimax
from AlphaBeta import AlphaBeta
from HeuristicEvaluator import evaluate, evaluate_distance_to_center, evaluate_freedom

# --- HEURISTIC COMBINATIONS ---

def h_medium(board_grid, player):
    """H1 + H2 (Pattern + Center)"""
    return evaluate(board_grid, player) + evaluate_distance_to_center(board_grid, player)

def h_hard(board_grid, player):
    """H1 + H2 + H3 (Pattern + Center + Freedom)"""
    h1 = evaluate(board_grid, player)
    h2 = evaluate_distance_to_center(board_grid, player)
    h3 = evaluate_freedom(board_grid, player)
    return (h1 * 1.5) + h2 + h3

# --- TEST SCENARIOS ---
SCENARIOS = {
    "1. Center Opening": [(7, 7)],
    "2. Simple Block": [(7, 7), (6, 6), (7, 8)], 
    "3. Diagonal Threat": [(5, 5), (5, 6), (6, 6), (5, 7), (7, 7)],
    "4. Split Three": [(7, 7), (2, 2), (7, 8), (2, 3), (7, 10)],
    "5. Complex Midgame": [
        (7,7), (7,8), (6,7), (6,6), (8,8), (5,5), (8,6), (9,6),
        (5,8), (4,9), (8,5), (8,4), (9,5), (9,4), (5,6)
    ]
}

# --- ALGORITHM CONFIGURATIONS ---
# Format: ("Name", Class, Depth, Heuristic_Function)
CONFIGS = [
    # 1. NO HEURISTICS (Control Group / "Blind" Search)
    # These bots return 0 for any state that isn't a Win/Loss.
    ("Minimax No-H",       Minimax,   2, None), 
    ("AlphaBeta No-H",     AlphaBeta, 3, None),

    # 2. MINIMAX VARIANTS (Comparing Heuristics on standard search)
    ("Minimax H1+H2",      Minimax,   2, h_medium),
    ("Minimax H1+H2+H3",   Minimax,   2, h_hard),

    # 3. ALPHABETA VARIANTS (Comparing Heuristics on optimized search)
    ("AlphaBeta H1+H2",    AlphaBeta, 3, h_medium),
    ("AlphaBeta H1+H2+H3", AlphaBeta, 4, h_hard),
]

def run_benchmark():
    # Header
    print(f"{'SCENARIO':<20} | {'VARIANT':<20} | {'TIME':<8} | {'NODES':<8} | {'PRUNED':<8} | {'MOVE'}")
    print("=" * 95)

    for scen_name, moves in SCENARIOS.items():
        for name, AlgoClass, depth, h_func in CONFIGS:
            # 1. Setup Board
            board = Board(size=15)
            for r, c in moves:
                board.make_move(r, c)
            
            # 2. Instantiate Bot
            # Passing 'None' as h_func works because your classes handle "if self.heuristic_func:"
            bot = AlgoClass(depth=depth, heuristic_func=h_func)
            
            # 3. Run & Time
            start = time.time()
            try:
                move = bot.find_best_move(board)
                elapsed = time.time() - start
                
                # 4. Gather Stats
                nodes = bot.nodes_explored
                pruned = getattr(bot, 'pruning_count', 0) 
                
                print(f"{scen_name:<20} | {name:<20} | {elapsed:.4f}s  | {nodes:<8} | {pruned:<8} | {move}")
                
            except Exception as e:
                print(f"{scen_name:<20} | {name:<20} | ERROR: {e}")

    print("=" * 95)

if __name__ == "__main__":
    run_benchmark()