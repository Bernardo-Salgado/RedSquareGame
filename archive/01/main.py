import pygame
import sys
from menu import Menu
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

                # Directly use the game.state as it is now a list of tuples: [((x, y), (width, height)), ...]
                board_state = game.state  # This is already in the correct format

                # Solve the puzzle using the BFS solver
                solution_moves = bfs_solver(board_state)

                for move in solution_moves:
                    piece_index, new_position = move  # Unpack the move tuple
                    current_position, size = board_state[piece_index]  # Get the current position and size

                    # Determine the direction of movement
                    direction = game.get_move_direction(current_position, new_position)  # Use the current position

                    # Move the block using the new position and direction
                    current_position, block_size = board_state[piece_index]  # Get the current position and size
                    moved = game.move_block((current_position, block_size), direction)  # Pass the position, size, and direction
                    if moved:
                        game.draw()  # Redraw the game state
                        pygame.display.flip()  # Update the display
                        pygame.time.delay(500)  # Delay for visual effect

            elif menu_action is None:
                pass

        menu.draw()

if __name__ == "__main__":
    main()
