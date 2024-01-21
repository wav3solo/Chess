class Move:
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}

    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    pieces_to_chess_notation = {"wP": "", "bP": "", "wR": "R", "bR": "R", "wN": "N", "bN": "N", "wB": "B", "bB": "B",
                                "wQ": "Q", "bQ": "Q", "wK": "K", "bK": "K"}

    def __init__(self, source_square, destination_square, game_state):
        self.game_state = game_state
        self.source_row = source_square[0]
        self.source_col = source_square[1]
        self.destination_row = destination_square[0]
        self.destination_col = destination_square[1]
        self.piece_moved = game_state.board[self.source_row][self.source_col]
        self.piece_captured = game_state.board[self.destination_row][self.destination_col]
        self.move_id = self.source_row * 1000 + self.source_col * 100 + self.destination_row * 10 + self.destination_col

    def get_chess_notation(self):
        is_capture = self.piece_captured != "--"
        is_check = self.game_state.player_in_check
        destination_in_chess_notation = self.get_rank_file(self.destination_row, self.destination_col)

        chess_notation = self.pieces_to_chess_notation[self.piece_moved]

        if is_capture:
            if self.piece_moved[1] == "P":
                chess_notation += self.cols_to_files[self.source_col]
            chess_notation += "x"

        chess_notation += destination_in_chess_notation

        if is_check:
            chess_notation += "+"

        return chess_notation

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
