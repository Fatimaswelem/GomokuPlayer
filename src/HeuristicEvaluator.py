# Two different evaluation functions

# GOMOKU HEURISTIC EVALUATION FUNCTION_1

AI = "X"
OP = "O"
EMPTY = "_"

PATTERN_SCORES = {

    "XXXXX": 100000000,          
    "_XXXX_": 100000,       # Open four
    "XX_XX": 10000,
    "X_XXX": 10000,
    "XXX_X": 10000,        
    "XX_XX": 10000,
    "X_XXX": 10000,
    "OXXXX_": 10000,        # Closed four
    "_XXXXO": 10000,
    "_XXX_": 5000,          # Open three
    "OXXX_": 500,           # Closed three
    "_XXXO": 500,
    "_XX_X_": 200,
    "_X_XX_": 200,
    "_XX_": 200,            # Open two
    "OXX_": 50,             # Closed two
    "_XXO": 50,


    "OOOOO": -100000000,     # lose
    "_OOOO_": -100000,       # Open four
    "OO_OO": -10000,
    "O_OOO": -10000,
    "OOO_O": -10000,        
    "XOOOO_": -10000,        # Closed four
    "_OOOOX": -10000,
    "_OOO_": -5000,          # Open three
    "XOOO_": -500,           # Closed three
    "_OOOX": -500,
    "_OO_O_": -200,
    "_O_OO_": -200,
    "_OO_": -200,            # Open two
    "XOO_": -50,             # Closed two
    "_OOX": -50,

}

# Extract rows, columns, diagonals as strings

def get_lines(board):
    n = len(board)
    lines = []

    for row in board:
        lines.append("".join(row))

    for col in range(n):
        col_str = "".join(board[row][col] for row in range(n))
        lines.append(col_str)

    # --- Diagonals ---
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


#valuate Patterns in a Single Line

def evaluate_line(line, player):
    score = 0
    opp = OP if player == AI else AI

    # AI patterns
    for pattern, value in PATTERN_SCORES.items():
        if player == "X":
            if pattern in line:
                score += value
        else:
            pattern_player = pattern.replace("X", player)
            if pattern_player in line:
                score += value

    # Opponent patterns (negative score)
    for pattern, value in PATTERN_SCORES.items():
        opp_pattern = pattern.replace("X", opp)
        if opp_pattern in line:
            score -= value * 1

    return score



# Main Evaluation Function

def evaluate(board, player=AI):
    score = 0
    lines = get_lines(board)

    for line in lines:
        score += evaluate_line(line, player)

        # win detection
        if "XXXXX" in line:
            if player == AI:
                return 1000000000
            else:
                return -1000000000

    return score

# # GOMOKU  DISTANCE-TO-CENTER HEURISTIC EVALUATION FUNCTION_2

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
                score -= distance_score(r, c, n) * 1.2  

    return score

# Example usage:
# --- Example Usage (Assuming an 8x8 Board) ---
board = [
    ['_', '_', '_', '_', '_', '_', '_', '_'],
    ['_', 'O', '_', '_', '_', '_', '_', '_'],
    ['_', '_', 'O', '_', '_', '_', '_', '_'],
    ['_', 'X', '_', 'O', '_', '_', '_', '_'],
    ['_', '_', 'X', '_', '_', '_', '_', '_'],
    ['_', '_', '_', '_', '_', '_', '_', '_'],
    ['_', '_', '_', '_', 'X', '_', '_', '_'],
    ['_', '_', '_', '_', '_', '_', '_', '_']
]
print(f"Pattern Score: {evaluate(board)}")
print(f"Distance Score: {evaluate_distance_to_center(board)}")