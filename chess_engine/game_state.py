from chess_engine.move import Move


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

    def undo_move(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.source_row][move.source_col] = move.piece_moved
            self.board[move.destination_row][move.destination_col] = move.piece_captured
            self.isWhiteToMove = not self.isWhiteToMove
