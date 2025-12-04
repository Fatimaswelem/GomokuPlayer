# Board.py

# Game board and move logic - AI CONTROLLER COMPATIBLE VERSION
class Board:
    def __init__(self, size=15):
        self.size = size
        self.board = [["." for _ in range(size)] for _ in range(size)]
        self.current_player = "X"  # Track whose turn it is (X goes first)
        self.last_move = None      # Track the last move for efficient win checking

    def get_possible_moves(self):
        """
        FIXED: Returns a limited list of (row, col) tuples of empty spots 
        near existing pieces to reduce the branching factor (Candidate Moves).
        """
        if not self.last_move:
            center = self.size // 2
            return [(center, center)]

        return self._get_candidate_moves(search_radius=2)


    def _get_all_pieces(self):
        """Helper: Gets coordinates of all placed pieces."""
        pieces = []
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] != ".":
                    pieces.append((r, c))
        return pieces

    def _get_candidate_moves(self, search_radius):
        """Generates a limited list of promising moves (empty spots near placed pieces)."""
        candidate_moves = set()
        
        pieces = self._get_all_pieces()
        
        for r_piece, c_piece in pieces:
            for dr in range(-search_radius, search_radius + 1):
                for dc in range(-search_radius, search_radius + 1):
                    r_move, c_move = r_piece + dr, c_piece + dc
                    
                    if (0 <= r_move < self.size and 
                        0 <= c_move < self.size and 
                        self.board[r_move][c_move] == '.'):
                        
                        candidate_moves.add((r_move, c_move))
                        
        return list(candidate_moves)



    def make_move(self, row, col):
        """Places the current player's piece and toggles the turn."""
        if 0 <= row < self.size and 0 <= col < self.size:
            if self.board[row][col] == '.':
                self.board[row][col] = self.current_player
                self.last_move = (row, col)
                # Toggle player
                self.current_player = "O" if self.current_player == "X" else "X"
                return True
        return False

    def undo_move(self, row, col):
        """Removes a piece and toggles the turn back. ESSENTIAL FOR AI."""
        if 0 <= row < self.size and 0 <= col < self.size:
            if self.board[row][col] != '.': 
                
                self.current_player = "O" if self.current_player == "X" else "X"
                
                self.board[row][col] = '.'
                return True
        return False

    def is_terminal(self):
        """Checks if the game is over (Win or Draw)."""
        # If no moves have been made, game is not over
        if not self.last_move:
            return False
            
        # Check if the LAST move won the game
        # We check the player who Just moved (the previous player)
        prev_player = "O" if self.current_player == "X" else "X"
        r, c = self.last_move
        
        if self.check_winner(r, c, prev_player):
            return True
            
        if self.is_full():
            return True
            
        return False

    # --- Mohammed's Original Helper Logic (Win Checking) ---

    def count_in_direction(self, x, y, dx, dy, player):
        count = 0
        # Look forward
        cx, cy = x + dx, y + dy
        while 0 <= cx < self.size and 0 <= cy < self.size and self.board[cx][cy] == player:
            count += 1
            cx += dx
            cy += dy
        return count

    def check_winner(self, x, y, player):
        """Checks if the specific move at (x,y) by 'player' caused a win."""
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            # Check strictly 5 in a row
            count = 1  # The piece itself
            count += self.count_in_direction(x, y, dx, dy, player)
            count += self.count_in_direction(x, y, -dx, -dy, player)
            
            if count == 5:
                return True
        return False

    def is_full(self):
        for row in self.board:
            if '.' in row:
                return False
        return True
