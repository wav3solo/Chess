import pygame as p
from chess_engine.game_state import GameState
from ches_ui import ChessUI


def main():
    game_state = GameState()

    chess_ui = ChessUI(game_state)
    chess_ui.load_resources()

    while True:

        chess_ui.handle_events(game_state)
        chess_ui.draw_game_state(game_state)

        p.time.Clock().tick(chess_ui.max_fps)
        p.display.flip()


if __name__ == "__main__":
    main()
