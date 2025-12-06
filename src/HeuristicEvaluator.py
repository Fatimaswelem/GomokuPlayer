# HeuristicEvaluator.py

AI = "X"
OP = "O"
EMPTY = "." 

PATTERN_SCORES = {
    # --- AI (Maximizing) Patterns ---
    "XXXXX": 100000000,        
    ".XXXX.": 100000,          
    "XX.XX": 10000,            
    "X.XXX": 10000,
    "XXX.X": 10000,
    "OXXXX.": 10000,           
    ".XXXXO": 10000,
    ".XXX.": 5000,             
    "OXXX.": 500,              
    ".XXXO": 500,
    ".XX.X.": 200,             
    ".X.XX.": 200,
    ".XX.": 200,               
    "OXX.": 50,                
    ".XXO": 50,

    # --- Opponent (Minimizing) Patterns ---
    "OOOOO": -1500000000,      
    ".OOOO.": -1500000,         
    "OO.OO": -150000,
    "O.OOO": -150000,
    "OOO.O": -150000,
    "XOOOO.": -150000,          
    ".OOOOX": -150000,
    ".OOO.": -55000,            
    "XOOO.": -5500,             
    ".OOOX": -5500,
    ".OO.O.": -2500,
    ".O.OO.": -2500,
    ".OO.": -2500,              
    "XOO.": -50,                
    ".OOX": -50,
}

def get_lines(board):
    n = len(board)
    lines = []
    # Rows
    for row in board:
        lines.append("".join(row))
    # Columns
    for col in range(n):
        col_str = "".join(board[row][col] for row in range(n))
        lines.append(col_str)
    # Diagonals
    for r in range(n):
        x, y = r, 0
        diag = []
        while x < n and y < n:
            diag.append(board[x][y])
            x += 1; y += 1
        if len(diag) >= 5: lines.append("".join(diag))
    for c in range(1, n):
        x, y = 0, c
        diag = []
        while x < n and y < n:
            diag.append(board[x][y])
            x += 1; y += 1
        if len(diag) >= 5: lines.append("".join(diag))
    for r in range(n):
        x, y = r, n - 1
        diag = []
        while x < n and y >= 0:
            diag.append(board[x][y])
            x += 1; y -= 1
        if len(diag) >= 5: lines.append("".join(diag))
    for c in range(n - 2, -1, -1):
        x, y = 0, c
        diag = []
        while x < n and y >= 0:
            diag.append(board[x][y])
            x += 1; y -= 1
        if len(diag) >= 5: lines.append("".join(diag))
    return lines

def evaluate_line(line, player):
    score = 0
    for pattern, value in PATTERN_SCORES.items():
        if player == AI:
            if pattern in line: score += value
        else:
            # Flip Logic for opponent
            flipped = pattern.replace("X", "T").replace("O", "X").replace("T", "O")
            if flipped in line: score += value
    return score

# H1: Pattern Evaluation
def evaluate(board, player=AI):
    score = 0
    lines = get_lines(board)
    for line in lines:
        score += evaluate_line(line, player)
        
        # WIN DETECTION (EXACT 5 RULE)
        # We ensure it's not 6 (Overline)
        if "XXXXX" in line and "XXXXXX" not in line:
            return 1000000000 if player == "X" else -1000000000
        if "OOOOO" in line and "OOOOOO" not in line:
            return 1000000000 if player == "O" else -1000000000
            
    return score

# H2: Distance Evaluation
def distance_score(r, c, n):
    center = (n - 1) / 2.0
    dist = abs(r - center) + abs(c - center)
    max_dist = center * 2
    return int((max_dist - dist) * 10)

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
                score -= distance_score(r, c, n) * 2  
    return score

# H3: Freedom/Mobility Evaluation
def evaluate_freedom(board, player):
    n = len(board)
    score = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for r in range(n):
        for c in range(n):
            if board[r][c] == player:
                for dr, dc in directions:
                    # Check forward
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and board[nr][nc] == ".":
                        score += 5
                    # Check backward
                    pr, pc = r - dr, c - dc
                    if 0 <= pr < n and 0 <= pc < n and board[pr][pc] == ".":
                        score += 5
    return score

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
    print(f"H3 (Freedom Score): {evaluate_freedom(board, player='X')}")
