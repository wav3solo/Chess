import pygame as p
from chess_engine.move import Move
from chess_engine.game_rules import GameRules


class ChessUI:
    def __init__(self, game_state):

        self.game_state = game_state

        self.screen = None
        self.width = self.height = 512
        self.max_fps = 15

        self.board_dimension = 8
        self.square_size = self.width // self.board_dimension

        self.pieces = ["wR", "wN", "wB", "wQ", "wK", "wP", "bR", "bN", "bB", "bQ", "bK", "bP"]

        self.images = {}
        self.sounds = {}

        p.init()
        p.mixer.init()
        self.screen = p.display.set_mode((self.width, self.height))
        p.display.set_caption("Chess")

        self.game_rules = GameRules(game_state)

        self.square_selected = ()
        self.player_clicks = []
        self.valid_moves = self.game_rules.get_valid_moves()

        self.move = None
        self.move_made = False

        self.undoing_move = False

    def load_resources(self):
        for piece in self.pieces:
            self.images[piece] = p.image.load("images/" + piece + ".png")

        self.sounds["move"] = p.mixer.Sound("sounds/move.mp3")
        self.sounds["capture"] = p.mixer.Sound("sounds/capture.mp3")
        self.sounds["check"] = p.mixer.Sound("sounds/check.mp3")
        self.sounds["checkmate"] = p.mixer.Sound("sounds/checkmate.mp3")

    def draw_game_state(self):
        self.draw_board(self.screen)
        self.draw_pieces(self.screen, self.game_state.board)

    def draw_board(self, screen):
        colors = [p.Color("#e8d6b4"), p.Color("#b18a67")]
        for c in range(self.board_dimension):
            for r in range(self.board_dimension):
                color = colors[((r + c) % 2)]
                p.draw.rect(screen, color,
                            p.Rect(c * self.square_size, r * self.square_size, self.square_size, self.square_size))

    def draw_pieces(self, screen, board):
        for r in range(self.board_dimension):
            for c in range(self.board_dimension):
                piece = board[r][c]
                if piece != "--":
                    screen.blit(self.images[piece],
                                p.Rect(c * self.square_size, r * self.square_size, self.square_size, self.square_size))

    def handle_events(self):
        for e in p.event.get():
            if e.type == p.QUIT:
                exit()
            elif e.type == p.KEYDOWN:
                if e.key == p.K_LEFT or e.key == p.K_SPACE:
                    if len(self.game_state.move_log) != 0:
                        self.sounds["move"].play()

                        print("Undoing the latest move: " + self.game_state.move_log[-1].get_chess_notation())
                        self.game_state.undo_move()
                        self.game_state.print_move_rights()

                        self.undoing_move = True
                        self.move_made = True
                elif e.key == p.K_q or e.key == p.K_ESCAPE:
                    exit()
                elif e.key == p.K_s:
                    self.save_pgn_to_file(self.game_state.checkmate)
                elif e.key == p.K_r:
                    self.game_state.game_title = input("Please, provide a new game title: ")
                elif e.key == p.K_DOWN:
                    self.game_state.reset_position()
                    self.valid_moves = self.game_rules.get_valid_moves()

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // self.square_size
                row = location[1] // self.square_size

                if self.square_selected == (row, col):
                    self.square_selected = ()
                    self.player_clicks = []
                else:
                    self.square_selected = (row, col)
                    self.player_clicks.append(self.square_selected)

                if len(self.player_clicks) == 2:
                    move = Move(self.player_clicks[0], self.player_clicks[1], self.game_state)
                    if move in self.valid_moves:
                        self.game_state.make_move(move)
                        self.move = move
                        self.move_made = True

                        self.square_selected = ()
                        self.player_clicks = []
                    else:
                        self.player_clicks = [self.square_selected]

        if self.move_made:
            self.valid_moves = self.game_rules.get_valid_moves()
            self.game_state.checkmate = True if len(self.valid_moves) == 0 else False
            self.move_made = False

            if not self.undoing_move:
                # adding a move into the pgn move log
                if not self.game_state.is_white_to_move:  # it was white's move
                    self.game_state.pgn_move_number += 1
                    self.game_state.pgn_move_log += str(self.game_state.pgn_move_number) + ". " + \
                                                    self.move.get_chess_notation() + " "
                    print("White's move is: " + self.move.get_chess_notation())
                else:  # it was black's move
                    self.game_state.pgn_move_log += self.move.get_chess_notation() + " "

                    print("Black's move is: " + self.move.get_chess_notation())

                if self.game_state.checkmate:
                    self.sounds["checkmate"].play()
                    if not self.game_state.is_white_to_move:
                        print("Checkmate! Game lasted for " +
                              str(self.game_state.pgn_move_number) + " moves and white won!")
                    else:
                        print("Checkmate! Game lasted for " +
                              str(self.game_state.pgn_move_number) + " moves and black won!")
                    print("The game unfolded as follows:")
                    print(self.game_state.pgn_move_log)
                    self.save_pgn_to_file(True)
                else:
                    self.game_state.print_move_rights()

                if self.game_state.player_in_check:
                    self.sounds["check"].play()
                elif self.move.piece_captured == "--":
                    self.sounds["move"].play()
                else:
                    self.sounds["capture"].play()
            else:
                moves = self.game_state.pgn_move_log.strip().split()
                moves = moves[:-2] if self.game_state.is_white_to_move else moves[:-1]
                self.game_state.pgn_move_number -= 1 if self.game_state.is_white_to_move else 0
                if moves:
                    self.game_state.pgn_move_log = " ".join(moves).rstrip() + " "
                else:
                    self.game_state.pgn_move_log = ""
                self.undoing_move = False

    def save_pgn_to_file(self, ended):
        with open('game_archive/' + self.game_state.game_title, 'w') as file:
            if ended:
                file.write(self.game_state.pgn_move_log)
            else:
                file.write(self.game_state.pgn_move_log + "*")
