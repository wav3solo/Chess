class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.isWhiteToMove = True
        self.hasWhiteCastled = False
        self.hasBlackCastled = False
        self.moveLog = []
        self.move_functions = {"P": self.get_pawn_moves, "R": self.get_rook_moves, "N": self.get_knight_moves,
                               "B": self.get_bishop_moves, "Q": self.get_queen_moves, "K": self.get_king_moves}

    def make_move(self, move):
        self.board[move.source_row][move.source_col] = "--"
        self.board[move.destination_row][move.destination_col] = move.piece_moved

        self.moveLog.append(move)

        self.isWhiteToMove = not self.isWhiteToMove

    def undo_move(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.source_row][move.source_col] = move.piece_moved
            self.board[move.destination_row][move.destination_col] = move.piece_captured
            self.isWhiteToMove = not self.isWhiteToMove

    def get_valid_moves(self):
        return self.get_possible_moves()

    def get_possible_moves(self):
        moves = []

        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.isWhiteToMove) or (turn == "b" and not self.isWhiteToMove):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r, c, moves)

        return moves

    def get_pawn_moves(self, r, c, moves):
        if self.isWhiteToMove:
            if self.board[r - 1][c] == "--":
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.board))

            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))

            if c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:
            if self.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))

            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))

            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def get_rook_moves(self, r, c, moves):
        pass

    def get_knight_moves(self, r, c, moves):
        pass

    def get_bishop_moves(self, r, c, moves):
        pass

    def get_queen_moves(self, r, c, moves):
        pass

    def get_king_moves(self, r, c, moves):
        pass


class Move:
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}

    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, source_square, destination_square, board):
        self.source_row = source_square[0]
        self.source_col = source_square[1]
        self.destination_row = destination_square[0]
        self.destination_col = destination_square[1]
        self.piece_moved = board[self.source_row][self.source_col]
        self.piece_captured = board[self.destination_row][self.destination_col]
        self.move_id = self.source_row * 1000 + self.source_col * 100 + self.destination_row * 10 + self.destination_col

    def get_chess_notation(self):
        return (self.get_rank_file(self.source_row, self.source_col)
                + self.get_rank_file(self.destination_row, self.destination_col))

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
