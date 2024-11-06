import pygame
import sys
from secondversion.menu import Menu
from game import Game, Position
from solver import Boardd
from game import Board
from solver import bfs_solver


def main():
    pygame.init()

    screen_width, screen_height = 1536, 864
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Klotski Game")

    menu = Menu(screen)
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            menu_action = menu.handle_event(event)
            if menu_action == "start":
                while True:
                    game.update()
                    game.draw()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        game.handle_event(event)

            if menu_action == "solve":
                solution_moves = []
                print("Solving...")

                board_state = Boardd.from_board(Game.get_board(game))

                solution_moves = bfs_solver(board_state)
                print(f"Moves found: {solution_moves}")

                for move in solution_moves:
                    piece, position = move
                    piece_index = game.get_piece_index(piece)
                    direction = game.get_move_direction(piece.position, position)

                    game.move_piece(piece_index, direction)
                    game.draw()
                    pygame.display.flip()
                    pygame.time.delay(500)

            elif menu_action is None:
                pass

        menu.draw()


if __name__ == "__main__":
    main()
