import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512
MAX_FPS = 15
BOARD_DIMENSIONS = 8
SQ_SIZE = WIDTH // BOARD_DIMENSIONS
PIECES = ["wR", "wN", "wB", "wQ", "wK", "wP", "bR", "bN", "bB", "bQ", "bK", "bP"]
IMAGES = {}


def load_images():
    for piece in PIECES:
        IMAGES[piece] = p.image.load("images/" + piece + ".png")


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

    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Chess")

    clock = p.time.Clock()

    gs = ChessEngine.GameState()

    load_images()

    running = True
    square_selected = ()
    player_clicks = []
    while running:
        keys = p.key.get_pressed()
        for e in p.event.get():
            if (e.type == p.QUIT) or (keys[p.K_ESCAPE]):
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if square_selected == (row, col):
                    square_selected = ()
                    player_clicks = []
                else:
                    square_selected = (row, col)
                    player_clicks.append(square_selected)
                if len(player_clicks) == 2:
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    gs.make_move(move)
                    print(move.get_chess_notation())
                    square_selected = ()
                    player_clicks = []

        draw_game_state(screen, gs)

        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
