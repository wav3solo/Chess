import pygame as p
from chess_engine.move import Move


class ChessUI:
    def __init__(self, gs):
        self.screen = None
        self.width = self.height = 512
        self.max_fps = 15
        self.board_dimension = 8
        self.square_size = self.width // self.board_dimension
        self.pieces = ["wR", "wN", "wB", "wQ", "wK", "wP", "bR", "bN", "bB", "bQ", "bK", "bP"]
        self.images = {}
        self.sounds = {}

        self.square_selected = ()
        self.player_clicks = []
        self.valid_moves = gs.get_valid_moves()
        self.move_made = False

        p.init()
        p.mixer.init()
        self.screen = p.display.set_mode((self.width, self.height))
        p.display.set_caption("Chess")

    def load_resources(self):
        for piece in self.pieces:
            self.images[piece] = p.image.load("images/" + piece + ".png")

        self.sounds["move"] = p.mixer.Sound("sounds/move.mp3")
        self.sounds["capture"] = p.mixer.Sound("sounds/capture.mp3")

    def draw_game_state(self, gs):
        self.draw_board(self.screen)
        self.draw_pieces(self.screen, gs.board)

    def draw_board(self, screen):
        colors = [p.Color("white"), p.Color("gray")]
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

    def handle_events(self, gs):
        for e in p.event.get():
            if e.type == p.QUIT:
                exit()
            elif e.type == p.KEYDOWN:
                if e.key == p.K_LEFT:
                    gs.undo_move()
                    self.move_made = True
                elif e.key == p.K_q or e.key == p.K_ESCAPE:
                    exit()

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // self.square_size
                row = location[1] // self.square_size

                if self.square_selected == (row, col):
                    square_selected = ()
                    self.player_clicks = []
                else:
                    square_selected = (row, col)
                    self.player_clicks.append(square_selected)

                if len(self.player_clicks) == 2:
                    move = Move(self.player_clicks[0], self.player_clicks[1], gs.board)
                    if move in self.valid_moves:
                        gs.make_move(move)
                        self.sounds["move"].play() if move.piece_captured == "--" else self.sounds["capture"].play()

                        self.move_made = True
                        self.square_selected = ()
                        self.player_clicks = []
                    else:
                        self.player_clicks = [square_selected]

        if self.move_made:
            self.valid_moves = gs.get_valid_moves()
            self.move_made = False
