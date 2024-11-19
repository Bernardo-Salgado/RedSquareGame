# import pygame
# import sys
# from menu import Menu  # Import the Menu class
# from game import Game  # Assuming your game logic is in game.py

# def main():
#     pygame.init()

#     # Set window dimensions
#     screen_width, screen_height = 1536, 864
#     screen = pygame.display.set_mode((screen_width, screen_height))
#     pygame.display.set_caption("Klotski Game")

#     menu = Menu(screen)
#     game = Game()  # Initialize the game, but do not run it yet

#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#             # Handle menu events
#             menu_action = menu.handle_event(event)
#             if menu_action == "start":
#                 # Start the game
#                 while True:
#                     game.update()
#                     game.draw()
#                     for event in pygame.event.get():
#                         if event.type == pygame.QUIT:
#                             pygame.quit()
#                             sys.exit()
#                         game.handle_event(event)
#             elif menu_action is None:
#                 pass  # No action taken in the menu

#         menu.draw()  # Draw the menu

# if __name__ == "__main__":
#     main()

####################################################################################

import pygame
import sys
from menu import Menu  # Import the Menu class
from game import Game  # Assuming your game logic is in game.py
from game import Board
from solver import bfs_solver

def main():
    pygame.init()

# <Michal> [initialising mixer for playing audio]------------------------------------
    # Initialize the mixer
    pygame.mixer.init()

# </Michal> -------------------------------------------------------------

    # Set window dimensions
    screen_width, screen_height = 1536, 864
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Klotski Game")

    menu = Menu(screen)
    game = Game()  # Initialize the game, but do not run it yet

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle menu events
            menu_action = menu.handle_event(event)
            if menu_action == "start":
                # Start the game
                while True:
                    game.update()
                    game.draw()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        game.handle_event(event)
            elif menu_action == "solve":
                # Attempt to solve the puzzle
                solution_moves = []  # Initialize to avoid UnboundLocalError
                print("Solving...")
                solution_moves = bfs_solver(Board.from_game(game.red_square, game.squares))  # Create a Board from the current game state
                print(f"Moves found: {solution_moves}")

                # Execute the solution moves step-by-step
                for move in solution_moves:
                    piece_index, direction = move
                    game.move_piece(piece_index, direction)  # Implement move_piece method in Game
                    game.draw()  # Redraw the game state
                    pygame.display.flip()  # Update the display
                    pygame.time.delay(500)  # Delay to visualize the moves
                # try:
                #     print("Solving...")
                #     solution_moves = bfs_solver(Board.from_game(game.red_square, game.squares))  # Create a Board from the current game state
                #     print(f"Moves found: {solution_moves}")

                #     # Execute the solution moves step-by-step
                #     for move in solution_moves:
                #         piece_index, direction = move
                #         game.move_piece(piece_index, direction)  # Implement move_piece method in Game
                #         game.draw()  # Redraw the game state
                #         pygame.display.flip()  # Update the display
                #         pygame.time.delay(500)  # Delay to visualize the moves
                # except Exception as e:
                #     print(f"An error occurred: {e}")
            elif menu_action is None:
                pass  # No action taken in the menu

        menu.draw()  # Draw the menu

if __name__ == "__main__":
    main()
