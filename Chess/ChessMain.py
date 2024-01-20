import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512
MAX_FPS = 15
BOARD_DIMENSIONS = 8
SQ_SIZE = WIDTH // BOARD_DIMENSIONS
PIECES = ["wR", "wN", "wB", "wQ", "wK", "wP", "bR", "bN", "bB", "bQ", "bK", "bP"]
IMAGES = {}
SOUNDS = {}


def load_resources():
    for piece in PIECES:
        IMAGES[piece] = p.image.load("images/" + piece + ".png")

    SOUNDS["move"] = p.mixer.Sound("sounds/move.mp3")
    SOUNDS["capture"] = p.mixer.Sound("sounds/capture.mp3")


def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)


def draw_board(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for c in range(BOARD_DIMENSIONS):
        for r in range(BOARD_DIMENSIONS):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for r in range(BOARD_DIMENSIONS):
        for c in range(BOARD_DIMENSIONS):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    p.mixer.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Chess")
    clock = p.time.Clock()
    gs = ChessEngine.GameState()
    load_resources()
    valid_moves = gs.get_valid_moves()

    move_made = False
    running = True
    square_selected = ()
    player_clicks = []

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.KEYDOWN:
                if e.key == p.K_LEFT:
                    gs.undo_move()
                    move_made = True
                elif e.key == p.K_q or e.key == p.K_ESCAPE:
                    running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                mouse_buttons = p.mouse.get_pressed()
                if mouse_buttons[0]:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE

                    if (player_clicks == [] and gs.board[row][col] != "--") or (not (player_clicks == [])):
                        square_selected = (row, col)
                        player_clicks.append(square_selected)

                    if len(player_clicks) == 2:
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                        if move in valid_moves:
                            gs.make_move(move)
                            if move.piece_captured == "--":
                                SOUNDS["move"].play()
                            else:
                                SOUNDS["capture"].play()
                            move_made = True

                        square_selected = ()
                        player_clicks = []
                if mouse_buttons[2]:
                    square_selected = ()
                    player_clicks = []

                if mouse_buttons[1]:
                    gs.undo_move()
                    move_made = True

        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

        draw_game_state(screen, gs)

        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
