# Game board and move logic - AI CONTROLLER COMPATIBLE

class Board:
    def __init__(self, size=15):
        self.size = size
        self.board = [["." for _ in range(size)] for _ in range(size)]
        self.current_player = "X"
        self.last_move = None

    def get_possible_moves(self):
        """
        Returns candidate moves sorted by potential (Center moves first).
        Radius 1 (Direct neighbors) is used for maximum speed at Depth 4.
        """
        if not self.last_move:
            center = self.size // 2
            return [(center, center)]
        
        # 1. Get all pieces
        occupied = []
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] != ".":
                    occupied.append((r, c))
        
        # 2. Find neighbors (Radius 1 for speed)
        possible = set()
        radius = 1 
        for r, c in occupied:
            for dr in range(-radius, radius + 1):
                for dc in range(-radius, radius + 1):
                    if dr == 0 and dc == 0: continue
                    
                    nr, nc = r + dr, c + dc
                    
                    if 0 <= nr < self.size and 0 <= nc < self.size:
                        if self.board[nr][nc] == ".":
                            possible.add((nr, nc))
                            
        # 3. Sort by distance to center (Crucial for Alpha-Beta pruning efficiency)
        center = self.size // 2
        sorted_moves = sorted(list(possible), key=lambda m: abs(m[0]-center) + abs(m[1]-center))
        
        return sorted_moves

    def make_move(self, row, col):
        if 0 <= row < self.size and 0 <= col < self.size:
            if self.board[row][col] == '.':
                self.board[row][col] = self.current_player
                self.last_move = (row, col)
                self.current_player = "O" if self.current_player == "X" else "X"
                return True
        return False

    def undo_move(self, row, col):
        if 0 <= row < self.size and 0 <= col < self.size:
            if self.board[row][col] != '.':
                self.current_player = "O" if self.current_player == "X" else "X"
                self.board[row][col] = '.'
                # Note: last_move is not strictly reverted for efficiency in search, 
                # but grid/player state is correct.
                return True
        return False

    def is_terminal(self):
        if not self.last_move:
            return False
        
        # Check if the move that just happened caused a win
        prev_player = "O" if self.current_player == "X" else "X"
        r, c = self.last_move
        
        if self.check_winner(r, c, prev_player):
            return True
            
        if self.is_full():
            return True
            
        return False

    def count_in_direction(self, x, y, dx, dy, player):
        count = 0
        cx, cy = x + dx, y + dy
        while 0 <= cx < self.size and 0 <= cy < self.size and self.board[cx][cy] == player:
            count += 1
            cx += dx
            cy += dy
        return count

    def check_winner(self, x, y, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1 
            count += self.count_in_direction(x, y, dx, dy, player)
            count += self.count_in_direction(x, y, -dx, -dy, player)
            
            # RULE IMPLEMENTATION: Exact 5 stones wins. 6+ (Overline) does NOT win.
            if count == 5:
                return True
        return False

    def is_full(self):
        for row in self.board:
            if '.' in row:
                return False
        return True
