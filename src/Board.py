# Game board and move logic
# Game board and move logic - AI CONTROLLER COMPATIBLE VERSION
class Board:
    def __init__(self, size=15):
        self.size = size
        self.board = [["." for _ in range(size)] for _ in range(size)]
        self.current_player = "X"  # Track whose turn it is (X goes first)
        self.last_move = None      # Track the last move for efficient win checking

    def get_possible_moves(self):
        """Returns a list of (row, col) tuples for all empty spots."""
        moves = []
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == ".":
                    moves.append((r, c))
        return moves

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
            self.board[row][col] = '.'
            # Toggle player back
            self.current_player = "O" if self.current_player == "X" else "X"
            self.last_move = None # (Optional: handling strictly not needed for Minimax recursion but good practice)

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

    # --- Mohammed's Original Helper Logic (Slightly Adapted) ---

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
            
            if count >= 5:
                return True
        return False

    def is_full(self):
        for row in self.board:
            if '.' in row:
                return False
        return True