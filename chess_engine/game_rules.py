from chess_engine.move import Move


class GameRules:
    def __init__(self, game_state):
        self.game_state = game_state
        self.move_functions = {"P": self.get_pawn_moves, "R": self.get_rook_moves, "N": self.get_knight_moves,
                               "B": self.get_bishop_moves, "Q": self.get_queen_moves, "K": self.get_king_moves}

    def get_valid_moves(self):
        return self.get_possible_moves()

    def get_possible_moves(self):
        moves = []

        for r in range(len(self.game_state.board)):
            for c in range(len(self.game_state.board[r])):
                turn = self.game_state.board[r][c][0]
                if (turn == "w" and self.game_state.isWhiteToMove) or (turn == "b" and not self.game_state.isWhiteToMove):
                    piece = self.game_state.board[r][c][1]
                    self.move_functions[piece](r, c, moves)

        return moves

    def get_pawn_moves(self, r, c, moves):
        if self.game_state.isWhiteToMove:
            if self.game_state.board[r - 1][c] == "--":
                moves.append(Move((r, c), (r - 1, c), self.game_state.board))
                if r == 6 and self.game_state.board[r - 2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.game_state.board))

            if c - 1 >= 0:
                if self.game_state.board[r - 1][c - 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c - 1), self.game_state.board))

            if c + 1 <= 7:
                if self.game_state.board[r - 1][c + 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c + 1), self.game_state.board))

        else:
            if self.game_state.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.game_state.board))
                if r == 1 and self.game_state.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.game_state.board))

            if c - 1 >= 0:
                if self.game_state.board[r + 1][c - 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c - 1), self.game_state.board))

            if c + 1 <= 7:
                if self.game_state.board[r + 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.game_state.board))

    def get_linear_moves(self, r, c, moves, directions, move_range):
        enemy_color = "b" if self.game_state.isWhiteToMove else "w"
        for d in directions:
            for i in range(1, (move_range + 1)):
                destination_row = r + d[0] * i
                destination_col = c + d[1] * i
                if 0 <= destination_row < 8 and 0 <= destination_col < 8:
                    destination_square = self.game_state.board[destination_row][destination_col]
                    if destination_square == "--":
                        moves.append(Move((r, c), (destination_row, destination_col), self.game_state.board))
                    elif destination_square[0] == enemy_color:
                        moves.append(Move((r, c), (destination_row, destination_col), self.game_state.board))
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
        ally_color = "w" if self.game_state.isWhiteToMove else "b"

        for m in knight_moves:
            destination_row = r + m[0]
            destination_col = c + m[1]
            if 0 <= destination_row < 8 and 0 <= destination_col < 8:
                destination_square = self.game_state.board[destination_row][destination_col]
                if destination_square[0] != ally_color:
                    moves.append(Move((r, c), (destination_row, destination_col), self.game_state.board))

    def get_bishop_moves(self, r, c, moves):
        directions = ((1, 1), (-1, -1), (1, -1), (-1, 1))
        self.get_linear_moves(r, c, moves, directions, 7)

    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)

    def get_king_moves(self, r, c, moves):
        directions = ((0, -1), (-1, 0), (0, 1), (1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1))
        self.get_linear_moves(r, c, moves, directions, 1)
