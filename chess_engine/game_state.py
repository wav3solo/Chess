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

        self.player_in_check = False
        self.checks = []
        self.pins = []

        self.whites_king_position = (7, 4)
        self.blacks_king_position = (0, 4)

        self.move_log = []

    def make_move(self, move):
        self.board[move.source_row][move.source_col] = "--"
        self.board[move.destination_row][move.destination_col] = move.piece_moved

        # updating kings position
        if move.piece_moved == "wK":
            self.whites_king_position = (move.destination_row, move.destination_col)
        elif move.piece_moved == "bK":
            self.blacks_king_position = (move.destination_row, move.destination_col)

        self.move_log.append(move)

        self.isWhiteToMove = not self.isWhiteToMove

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            print("Undoing the latest move: " + move.get_chess_notation())

            self.board[move.source_row][move.source_col] = move.piece_moved
            self.board[move.destination_row][move.destination_col] = move.piece_captured

            # updating kings position
            if move.piece_moved == "wK":
                self.whites_king_position = (move.source_row, move.source_col)
            elif move.piece_moved == "bK":
                self.blacks_king_position = (move.source_row, move.source_col)

            self.isWhiteToMove = not self.isWhiteToMove
