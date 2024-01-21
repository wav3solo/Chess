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
