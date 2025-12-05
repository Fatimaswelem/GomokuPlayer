# HeuristicEvaluator.py

# Two different evaluation functions
# GOMOKU HEURISTIC EVALUATION FUNCTION_1 (Pattern Scoring)

# Constants must match Board.py
AI = "X"
OP = "O"
EMPTY = "."  # Changed: Was "_"

PATTERN_SCORES = {
    # --- AI (Maximizing) Patterns ---
    "XXXXX": 100000000,        # Win
    ".XXXX.": 100000,          # Open four (Guaranteed win next turn)
    "XX.XX": 10000,            # Split four
    "X.XXX": 10000,
    "XXX.X": 10000,
    "OXXXX.": 10000,           # Closed four (Threat)
    ".XXXXO": 10000,
    ".XXX.": 5000,             # Open three
    "OXXX.": 500,              # Closed three
    ".XXXO": 500,
    ".XX.X.": 200,             # Split three
    ".X.XX.": 200,
    ".XX.": 200,               # Open two
    "OXX.": 50,                # Closed two
    ".XXO": 50,

    # --- Opponent (Minimizing) Patterns ---
    # We punish these heavily so Minimax avoids them
    "OOOOO": -1500000000,      # Lose
    ".OOOO.": -1500000,         # Opponent Open four
    "OO.OO": -150000,
    "O.OOO": -150000,
    "OOO.O": -150000,
    "XOOOO.": -150000,          # Opponent Closed four
    ".OOOOX": -150000,
    ".OOO.": -55000,            # Opponent Open three
    "XOOO.": -5500,             # Opponent Closed three
    ".OOOX": -5500,
    ".OO.O.": -2500,
    ".O.OO.": -2500,
    ".OO.": -2500,              # Opponent Open two
    "XOO.": -50,                # Opponent Closed two
    ".OOX": -50,
}

# Extract rows, columns, diagonals as strings
def get_lines(board):
    """
    Extracts all horizontal, vertical, and diagonal lines from the board 
    where a 5-in-a-row can potentially be found.
    """
    # Important: 'board' here must be the 2D list, not the Board object
    n = len(board)
    lines = []

    # Rows
    for row in board:
        lines.append("".join(row))

    # Columns
    for col in range(n):
        col_str = "".join(board[row][col] for row in range(n))
        lines.append(col_str)

    # --- Diagonals ---
    # Top-left to bottom-right
    for r in range(n):
        x, y = r, 0
        diag = []
        while x < n and y < n:
            diag.append(board[x][y])
            x += 1
            y += 1
        if len(diag) >= 5:
            lines.append("".join(diag))

    for c in range(1, n):
        x, y = 0, c
        diag = []
        while x < n and y < n:
            diag.append(board[x][y])
            x += 1
            y += 1
        if len(diag) >= 5:
            lines.append("".join(diag))

    # Top-right to bottom-left
    for r in range(n):
        x, y = r, n - 1
        diag = []
        while x < n and y >= 0:
            diag.append(board[x][y])
            x += 1
            y -= 1
        if len(diag) >= 5:
            lines.append("".join(diag))

    for c in range(n - 2, -1, -1):
        x, y = 0, c
        diag = []
        while x < n and y >= 0:
            diag.append(board[x][y])
            x += 1
            y -= 1
        if len(diag) >= 5:
            lines.append("".join(diag))

    return lines


# Evaluate Patterns in a Single Line
def evaluate_line(line, player):
    """Calculates the score for a single line based on patterns."""
    score = 0
    # Note: 'opp' is not used here but is defined implicitly in the logic below
    
    for pattern, value in PATTERN_SCORES.items():
        if player == AI: # If we are 'X' (the default perspective)
            if pattern in line:
                score += value
        else: # If we are 'O', we need to flip the pattern logic
            # Flip X/O in the pattern key to match the current 'O' perspective
            flipped_pattern = pattern.replace("X", "TEMP").replace("O", "X").replace("TEMP", "O")
            if flipped_pattern in line:
                score += value

    return score


# Main Evaluation Function (Heuristic 1)
def evaluate(board, player=AI):
    """H1: Calculates the total score based on patterns (Tactical)."""
    score = 0
    lines = get_lines(board)

    for line in lines:
        score += evaluate_line(line, player)

        # Immediate Win/Loss Detection override
        # (This helps Minimax see terminal states clearly)
        if "XXXXX" in line:
            return 1000000000 if player == "X" else -1000000000
        if "OOOOO" in line:
            return 1000000000 if player == "O" else -1000000000

    return score


# GOMOKU DISTANCE-TO-CENTER HEURISTIC EVALUATION FUNCTION_2

def distance_score(r, c, n):
    """Calculates a positional score based on distance to the center."""
    center = (n - 1) / 2.0

    # Manhattan distance from center
    dist = abs(r - center) + abs(c - center)

    # Normalize so center has highest score
    max_dist = center * 2
    return int((max_dist - dist) * 10)  # scale up

# Evaluate whole board based on piece positions
def evaluate_distance_to_center(board, player=AI):
    """H2: Calculates the total score based on positional advantage (Strategic)."""
    n = len(board)
    score = 0
    opponent = OP if player == AI else AI

    for r in range(n):
        for c in range(n):
            cell = board[r][c]

            if cell == player:
                score += distance_score(r, c, n)

            elif cell == opponent:
                # We subtract score for opponent's good positions
                score -= distance_score(r, c, n) * 2  

    return score


# =========================================================================
# === NEW COMBINED HEURISTICS FOR MEDIUM AND HARD MODE ===
# =========================================================================

def combined_heuristic_medium(board, player):
    """
    Medium Mode Heuristic: H1 (Pattern) + H2 (Center). 
    Balanced tactical and strategic evaluation.
    """
    # H1: Pattern Score (Tactical)
    score_h1 = evaluate(board, player) 
    
    # H2: Distance to Center Score (Strategic)
    score_h2 = evaluate_distance_to_center(board, player) 
    
    return score_h1 + score_h2

def combined_heuristic_hard(board, player):
    """
    Hard Mode Heuristic: H1 (Aggressive Pattern) + H2 (Center). (2:1 Ratio)
    Increasing H1 weight to make it more tactical and offensive.
    """
    
    # H1: Pattern Score (Tactical)
    score_h1 = evaluate(board, player) 
    
    # H2: Distance to Center Score (Strategic)
    score_h2 = evaluate_distance_to_center(board, player) 
    # double weight 
    H1_WEIGHT = 2.0 
    
    return (score_h1 * H1_WEIGHT) + score_h2

if __name__ == "__main__":
    # --- Example Usage (Assuming an 8x8 Board) ---
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', 'O', '.', '.', '.', '.', '.', '.'],
        ['.', '.', 'O', '.', '.', '.', '.', '.'],
        ['.', 'X', '.', 'O', '.', '.', '.', '.'],
        ['.', '.', 'X', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', 'X', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]

    print(f"--- Player X's Perspective ---")
    print(f"H1 (Pattern Score): {evaluate(board, player='X')}")
    print(f"H2 (Distance Score): {evaluate_distance_to_center(board, player='X')}")
    print(f"Combined (Medium) Score: {combined_heuristic_medium(board, player='X')}")
    print(f"Combined (Medium) Score: {combined_heuristic_hard(board, player='X')}")
