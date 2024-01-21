from chess_engine.move import Move


def is_square_on_board(row, col):
    return (0 <= row < 8) and (0 <= col < 8)


class GameRules:
    def __init__(self, game_state):
        self.game_state = game_state
        self.move_functions = {"P": self.get_pawn_moves, "R": self.get_rook_moves, "N": self.get_knight_moves,
                               "B": self.get_bishop_moves, "Q": self.get_queen_moves, "K": self.get_king_moves}

        # possible move directions
        self.knight_directions = ((1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1))
        self.bishop_directions = ((1, 1), (-1, -1), (1, -1), (-1, 1))
        self.rook_directions = ((0, -1), (-1, 0), (0, 1), (1, 0))

        # first 4 are orthogonal directions, next 4 are diagonal. 4 and 5 are white pawn directions,
        # 6 and 7 are black pawn directions
        self.all_possible_directions = ((0, -1), (-1, 0), (0, 1), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1))

    def get_valid_moves(self):  # returns all valid moves considering checks
        moves = []
        self.game_state.checks, self.game_state.pins, self.game_state.player_in_check = self.check_for_checks_and_pins()

        king_row = self.game_state.whites_king_position[0] if self.game_state.isWhiteToMove \
            else self.game_state.blacks_king_position[0]
        king_col = self.game_state.whites_king_position[1] if self.game_state.isWhiteToMove \
            else self.game_state.blacks_king_position[1]

        if self.game_state.player_in_check:
            if len(self.game_state.checks) == 1:  # only one check (block, capture or move)
                moves = self.get_possible_moves()

                check = self.game_state.checks[0]
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.game_state.board[check_row][check_col]

                valid_squares = []

                if piece_checking[1] == "N":
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        # check[2] and check[3] are check directions
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i)

                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break

                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].piece_moved[1] != "K":
                        if not (moves[i].destination_row, moves[i].destination_col) in valid_squares:
                            moves.remove(moves[i])

            elif len(self.game_state.checks) == 2:  # double check (move the king)
                self.get_king_moves(king_row, king_col, moves)

        else:
            moves = self.get_possible_moves()

        return moves

    def get_possible_moves(self):  # returns all possible moves without looking for checks
        moves = []

        for r in range(len(self.game_state.board)):
            for c in range(len(self.game_state.board[r])):
                piece_color = self.game_state.board[r][c][0]
                if ((piece_color == "w" and self.game_state.isWhiteToMove)
                        or (piece_color == "b" and not self.game_state.isWhiteToMove)):
                    piece = self.game_state.board[r][c][1]
                    self.move_functions[piece](r, c, moves)

        return moves

    # __Generating piece movement_______________________________________________________________________________________

    def get_linear_moves(self, r, c, moves, directions, move_range):
        piece_pinned, pin_direction = self.get_pin_directions(r, c)

        enemy_color = "b" if self.game_state.isWhiteToMove else "w"
        for d in directions:
            for i in range(1, (move_range + 1)):
                destination_row = r + d[0] * i
                destination_col = c + d[1] * i
                if is_square_on_board(destination_row, destination_col):
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        destination_square = self.game_state.board[destination_row][destination_col]
                        if destination_square == "--":
                            moves.append(Move((r, c), (destination_row, destination_col), self.game_state))
                        elif destination_square[0] == enemy_color:
                            moves.append(Move((r, c), (destination_row, destination_col), self.game_state))
                            break
                        else:
                            break
                else:
                    break

    def get_pawn_moves(self, r, c, moves):
        piece_pinned, pin_direction = self.get_pin_directions(r, c)

        if self.game_state.isWhiteToMove:
            if self.game_state.board[r - 1][c] == "--":
                if not piece_pinned or pin_direction == (-1, 0):
                    moves.append(Move((r, c), (r - 1, c), self.game_state))
                    if r == 6 and self.game_state.board[r - 2][c] == "--":
                        moves.append(Move((r, c), (r - 2, c), self.game_state))

            if c - 1 >= 0:
                if not piece_pinned or pin_direction == (-1, -1):
                    if self.game_state.board[r - 1][c - 1][0] == "b":
                        moves.append(Move((r, c), (r - 1, c - 1), self.game_state))

            if c + 1 <= 7:
                if not piece_pinned or pin_direction == (-1, 1):
                    if self.game_state.board[r - 1][c + 1][0] == "b":
                        moves.append(Move((r, c), (r - 1, c + 1), self.game_state))

        else:
            if self.game_state.board[r + 1][c] == "--":
                if not piece_pinned or pin_direction == (1, 0):
                    moves.append(Move((r, c), (r + 1, c), self.game_state))
                    if r == 1 and self.game_state.board[r + 2][c] == "--":
                        moves.append(Move((r, c), (r + 2, c), self.game_state))

            if c - 1 >= 0:
                if not piece_pinned or pin_direction == (1, -1):
                    if self.game_state.board[r + 1][c - 1][0] == "w":
                        moves.append(Move((r, c), (r + 1, c - 1), self.game_state))

            if c + 1 <= 7:
                if not piece_pinned or pin_direction == (1, 1):
                    if self.game_state.board[r + 1][c + 1][0] == "w":
                        moves.append(Move((r, c), (r + 1, c + 1), self.game_state))

    def get_rook_moves(self, r, c, moves):
        directions = self.rook_directions
        self.get_linear_moves(r, c, moves, directions, 7)

    def get_knight_moves(self, r, c, moves):
        piece_pinned, pin_direction = self.get_pin_directions(r, c)

        knight_moves = ((1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1))
        ally_color = "w" if self.game_state.isWhiteToMove else "b"

        for m in knight_moves:
            destination_row = r + m[0]
            destination_col = c + m[1]
            if is_square_on_board(destination_row, destination_col):
                if not piece_pinned:
                    destination_square = self.game_state.board[destination_row][destination_col]
                    if destination_square[0] != ally_color:
                        moves.append(Move((r, c),
                                          (destination_row, destination_col), self.game_state))

    def get_bishop_moves(self, r, c, moves):
        directions = self.bishop_directions
        self.get_linear_moves(r, c, moves, directions, 7)

    def get_queen_moves(self, r, c, moves):
        directions = self.all_possible_directions
        self.get_linear_moves(r, c, moves, directions, 7)

    def get_king_moves(self, r, c, moves):
        directions = self.all_possible_directions
        self.get_linear_moves(r, c, moves, directions, 1)

    # __Checks__________________________________________________________________________________________________________

    def check_for_checks_and_pins(self):
        pins = []
        checks = []
        player_in_check = False

        if self.game_state.isWhiteToMove:
            enemy_color = "b"
            ally_color = "w"
            source_row = self.game_state.whites_king_position[0]
            source_col = self.game_state.whites_king_position[1]
        else:
            enemy_color = "w"
            ally_color = "b"
            source_row = self.game_state.blacks_king_position[0]
            source_col = self.game_state.blacks_king_position[1]

        directions = self.all_possible_directions

        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()
            for i in range(1, 8):
                destination_row = source_row + d[0] * i
                destination_col = source_col + d[1] * i
                if is_square_on_board(destination_row, destination_col):
                    destination_piece = self.game_state.board[destination_row][destination_col]
                    if destination_piece[0] == ally_color:
                        if possible_pin == ():
                            possible_pin = (destination_row, destination_col, d[0], d[1])
                        else:
                            break
                    elif destination_piece[0] == enemy_color:
                        piece_type = destination_piece[1]
                        if (0 <= j <= 3 and piece_type == "R") or \
                                (4 <= j <= 7 and piece_type == "B") or \
                                (i == 1 and piece_type == "P" and ((enemy_color == "w" and 6 <= j <= 7) or
                                                                   (enemy_color == "b" and 4 <= j <= 5))) or \
                                (piece_type == "Q") or \
                                (i == 1 and piece_type == "K"):
                            if possible_pin == ():
                                player_in_check = True
                                checks.append((destination_row, destination_col, d[0], d[1]))
                                break
                            else:
                                pins.append(possible_pin)
                        else:  # there is an enemy piece, but it's not checking the king
                            break
                else:  # square is not on the board
                    break

        knight_moves = self.knight_directions

        for move in knight_moves:
            destination_row = source_row + move[0]
            destination_col = source_col + move[1]
            if is_square_on_board(destination_row, destination_col):
                destination_piece = self.game_state.board[destination_row][destination_col]
                if destination_piece[0] == enemy_color and destination_piece[1] == "N":
                    player_in_check = True
                    checks.append((destination_row, destination_col, move[0], move[1]))

        return checks, pins, player_in_check

    def get_pin_directions(self, r, c):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.game_state.pins) - 1, -1, -1):
            if self.game_state.pins[i][0] == r and self.game_state.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.game_state.pins[i][2], self.game_state.pins[i][3])
                self.game_state.pins.remove(self.game_state.pins[i])
                break
        return piece_pinned, pin_direction
