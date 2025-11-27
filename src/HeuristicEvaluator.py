# Two different evaluation functions
# GOMOKU HEURISTIC EVALUATION FUNCTION_1
# Constants must match Board.py
AI = "X"
OP = "O"
EMPTY = "."  # CHANGED: Was "_"

PATTERN_SCORES = {
    # --- AI (Maximizing) Patterns ---
    "XXXXX": 100000000,      # Win
    ".XXXX.": 100000,        # Open four (Guaranteed win next turn)
    "XX.XX": 10000,          # Split four
    "X.XXX": 10000,
    "XXX.X": 10000,
    "OXXXX.": 10000,         # Closed four (Threat)
    ".XXXXO": 10000,
    ".XXX.": 5000,           # Open three
    "OXXX.": 500,            # Closed three
    ".XXXO": 500,
    ".XX.X.": 200,           # Split three
    ".X.XX.": 200,
    ".XX.": 200,             # Open two
    "OXX.": 50,              # Closed two
    ".XXO": 50,

    # --- Opponent (Minimizing) Patterns ---
    # We punish these heavily so Minimax avoids them
    "OOOOO": -100000000,     # Lose
    ".OOOO.": -100000,       # Opponent Open four
    "OO.OO": -10000,
    "O.OOO": -10000,
    "OOO.O": -10000,
    "XOOOO.": -10000,        # Opponent Closed four
    ".OOOOX": -10000,
    ".OOO.": -5000,          # Opponent Open three
    "XOOO.": -500,           # Opponent Closed three
    ".OOOX": -500,
    ".OO.O.": -200,
    ".O.OO.": -200,
    ".OO.": -200,            # Opponent Open two
    "XOO.": -50,             # Opponent Closed two
    ".OOX": -50,
}

# Extract rows, columns, diagonals as strings
def get_lines(board):
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
    score = 0
    opp = OP if player == AI else AI

    # To simplify pattern matching, we can replace the player's char with 'X'
    # and opponent with 'O' just for the lookup, or duplicte dictionary.
    # The current approach iterates keys and checks based on player.
    
    for pattern, value in PATTERN_SCORES.items():
        if player == AI: # If we are 'X'
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
    center = (n - 1) / 2.0

    # Manhattan distance from center
    dist = abs(r - center) + abs(c - center)

    # Normalize so center has highest score
    max_dist = center * 2
    return int((max_dist - dist) * 10)  # scale up

# Evaluate whole board based on piece positions
def evaluate_distance_to_center(board, player=AI):
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
                score -= distance_score(r, c, n) * 1.2  

    return score

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

if __name__ == "__main__":
    print(f"Pattern Score: {evaluate(board)}")
    print(f"Distance Score: {evaluate_distance_to_center(board)}")