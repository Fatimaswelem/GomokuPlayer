# Game board and move logic
class Board:
    def __init__(self, size=15):
        self.size = size
        self.board = [["." for _ in range(size)] for _ in range(size)]

    def put_in_position(self, row, col, player):

        if 0 <= row < self.size and 0 <= col < self.size:
            if self.board[row][col] == '.':
                self.board[row][col] = player
                return True
        return False

    def count_in_direction(self, x, y, dx, dy, player):

        count = 0
        while 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == player:
            count += 1
            x += dx
            y += dy
        return count

    def check_winner(self, x, y):

        player = self.board[x][y]
        if player == ".":
            return False
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            total = (
                self.count_in_direction(x, y, dx, dy, player)
                + self.count_in_direction(x, y, -dx, -dy, player) - 1
            )
            if total >= 5:
                return True
        return False

    def is_full(self):

        for row in self.board:
            if '.' in row:
                return False
        return True