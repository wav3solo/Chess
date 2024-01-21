from Chess.chess_engine.move import Move


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

    def get_linear_moves(self, r, c, moves, directions, move_range):
        enemy_color = "b" if self.isWhiteToMove else "w"
        for d in directions:
            for i in range(1, (move_range + 1)):
                destination_row = r + d[0] * i
                destination_col = c + d[1] * i
                if 0 <= destination_row < 8 and 0 <= destination_col < 8:
                    destination_square = self.board[destination_row][destination_col]
                    if destination_square == "--":
                        moves.append(Move((r, c), (destination_row, destination_col), self.board))
                    elif destination_square[0] == enemy_color:
                        moves.append(Move((r, c), (destination_row, destination_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_rook_moves(self, r, c, moves):
        directions = ((0, -1), (-1, 0), (0, 1), (1, 0))
        self.get_linear_moves(r, c, moves, directions, 7)

    def get_knight_moves(self, r, c, moves):
        knight_moves = ((1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1))
        ally_color = "w" if self.isWhiteToMove else "b"

        for m in knight_moves:
            destination_row = r + m[0]
            destination_col = c + m[1]
            if 0 <= destination_row < 8 and 0 <= destination_col < 8:
                destination_square = self.board[destination_row][destination_col]
                if destination_square[0] != ally_color:
                    moves.append(Move((r, c), (destination_row, destination_col), self.board))

    def get_bishop_moves(self, r, c, moves):
        directions = ((1, 1), (-1, -1), (1, -1), (-1, 1))
        self.get_linear_moves(r, c, moves, directions, 7)

    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)

    def get_king_moves(self, r, c, moves):
        directions = ((0, -1), (-1, 0), (0, 1), (1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1))
        self.get_linear_moves(r, c, moves, directions, 1)
