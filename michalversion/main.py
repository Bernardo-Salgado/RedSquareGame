import pygame
import sys
from secondversion.menu import Menu
from game import Game
from solver import Boardd
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

            elif menu_action == "solve":
                print("Solving...")

                # Assuming game is an instance of Game and game.state is a list of tuples
                board_state = game.state  # Directly use the state if it's already in the correct format
                solution_moves = bfs_solver(board_state)
                print(f"Moves found: {solution_moves}")

                for move in solution_moves:
                    piece, position = move
                    piece_index = game.get_piece_index(piece)  # You may need to implement this method
                    direction = game.get_move_direction(piece.position, position)  # Implement this method

                    game.move_block(piece_index, direction)  # Adjust this if necessary
                    game.draw()
                    pygame.display.flip()
                    pygame.time.delay(500)

            elif menu_action is None:
                pass

        menu.draw()

if __name__ == "__main__":
    main()
