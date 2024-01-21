import pygame as p
from chess_engine.game_state import GameState
from ches_ui import ChessUI


def main():

    gs = GameState()

    chess_ui = ChessUI(gs)
    chess_ui.load_resources()

    while True:
        chess_ui.handle_events(gs)
        chess_ui.draw_game_state(gs)

        p.time.Clock().tick(chess_ui.max_fps)
        p.display.flip()


if __name__ == "__main__":
    main()
