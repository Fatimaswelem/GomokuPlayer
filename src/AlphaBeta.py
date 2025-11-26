# Alpha-Beta Pruning logic
from HeuristicEvaluator import get_lines, evaluate, evaluate_distance_to_center


class AlphaBeta:

    @staticmethod
    def alphabeta(board, depth: int, alpha: float, beta: float, maximizingPlayer: bool, heuristic_func=None):
        """
        Alpha-Beta Pruning implementation for Gomoku

        Parameters:
        - board: current game state
        - depth: search depth
        - alpha: best value that the maximizing player can guarantee
        - beta: best value that the minimizing player can guarantee
        - maximizingPlayer: True if it's AI's turn (maximizing), False if opponent's turn (minimizing)
        - heuristic_func: evaluation function to use

        Returns:
        - tuple: (evaluation_score, best_move)
        """
        # Default to pattern heuristic if none provided
        if heuristic_func is None:
            heuristic_func = evaluate

        # Terminal state check
        if depth == 0 or AlphaBeta.is_terminal(board):
            return heuristic_func(board, "X"), None

        if maximizingPlayer:
            value = float('-inf')
            possible_moves = AlphaBeta.get_possible_moves(board)
            best_movement = possible_moves[0] if possible_moves else None

            for move in possible_moves:
                new_board = AlphaBeta.make_move(board, move, "X")

                # Recursive call with alpha-beta pruning
                tmp = AlphaBeta.alphabeta(new_board, depth - 1, alpha, beta, False, heuristic_func)[0]

                # Update best value and move
                if tmp > value:
                    value = tmp
                    best_movement = move

                # Update alpha value
                alpha = max(alpha, value)

                # Alpha-beta pruning: if current value is already better than beta,
                # we can stop exploring this branch
                if value >= beta:
                    break  # Beta cutoff

            return value, best_movement

        else:
            value = float('inf')
            possible_moves = AlphaBeta.get_possible_moves(board)
            best_movement = possible_moves[0] if possible_moves else None

            for move in possible_moves:
                new_board = AlphaBeta.make_move(board, move, "O")

                # Recursive call with alpha-beta pruning
                tmp = AlphaBeta.alphabeta(new_board, depth - 1, alpha, beta, True, heuristic_func)[0]

                # Update best value and move
                if tmp < value:
                    value = tmp
                    best_movement = move

                # Update beta value
                beta = min(beta, value)

                # Alpha-beta pruning: if current value is already worse than alpha,
                # we can stop exploring this branch
                if value <= alpha:
                    break  # Alpha cutoff

            return value, best_movement

    @staticmethod
    def is_terminal(board):
        """Check if game is over (win or draw)"""
        # Check if game is over
        lines = get_lines(board)
        for line in lines:
            if "XXXXX" in line or "OOOOO" in line:
                return True

        # Check for draw
        for row in board:
            for cell in row:
                if cell == '_':
                    return False
        return True

    @staticmethod
    def get_possible_moves(board):
        """Get all empty positions"""
        moves = []
        for x in range(len(board)):
            for y in range(len(board[0])):
                if board[x][y] == '_':
                    moves.append((x, y))
        return moves

    @staticmethod
    def make_move(board, move, player):
        """Create new board with move made"""
        import copy
        new_board = copy.deepcopy(board)
        x, y = move[0], move[1]
        new_board[x][y] = player
        return new_board

    @staticmethod
    def get_best_move(board, depth: int, heuristic_func=None):
        """
        Public method to get the best move using Alpha-Beta pruning

        Parameters:
        - board: current game state
        - depth: search depth
        - heuristic_func: evaluation function to use

        Returns:
        - tuple: best move coordinates (x, y)
        """
        # Initialize alpha and beta with worst-case values
        alpha = float('-inf')
        beta = float('inf')

        # Start the search as maximizing player (AI is "X")
        score, best_move = AlphaBeta.alphabeta(board, depth, alpha, beta, True, heuristic_func)
        return best_move
# Alpha-Beta Pruning logic
