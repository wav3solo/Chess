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

    def make_move(self, move):
        self.board[move.source_row][move.source_col] = "--"
        self.board[move.destination_row][move.destination_col] = move.piece_moved

        self.moveLog.append(move)

        self.isWhiteToMove = not self.isWhiteToMove


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

    def get_chess_notation(self):
        return (self.get_rank_file(self.source_row, self.source_col)
                + self.get_rank_file(self.destination_row, self.destination_col))

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
