import pygame
import sys
from secondversion.menu import Menu  # Import the Menu class
from game import Game, Position  # Assuming your game logic is in game.py
from solver import Boardd
from game import Board
from solver import bfs_solver

def main():
    pygame.init()

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
            
            if menu_action == "solve":
                # Attempt to solve the puzzle
                solution_moves = []  # Initialize to avoid UnboundLocalError
                print("Solving...")

                # Create a Board from the current game state using from_board
                board_state = Boardd.from_board(Game.get_board(game))  # Assuming `game.board` is compatible with Board's from_board
                # board_state = Board.from_start_position()

                # Solve the puzzle with BFS solver
                solution_moves = bfs_solver(board_state)  # Get solution moves as a list of (piece, position) tuples
                print(f"Moves found: {solution_moves}")

                # Execute the solution moves step-by-step
                for move in solution_moves:
                    piece, position = move  # Unpack piece and position from solution move
                    piece_index = game.get_piece_index(piece)  # Obtain index of the piece (if needed for `move_piece`)
                    direction = game.get_move_direction(piece.position, position)  # Determine direction (implement this if needed)

                    # Move the piece and update the game
                    game.move_piece(piece_index, direction)  # Adjust `move_piece` to accept piece_index and direction
                    game.draw()  # Redraw the game state
                    pygame.display.flip()  # Update the display
                    pygame.time.delay(500)  # Delay to visualize the moves


            # elif menu_action == "solve":
            #     # Attempt to solve the puzzle
            #     solution_moves = []  # Initialize to avoid UnboundLocalError
            #     print("Solving...")
            #     solution_moves = bfs_solver(Board.from_board(game.red_square, game.squares))  # Create a Board from the current game state
            #     print(f"Moves found: {solution_moves}")

            #     # Execute the solution moves step-by-step
            #     for move in solution_moves:
            #         piece_index, direction = move
            #         game.move_piece(piece_index, direction)  # Implement move_piece method in Game
            #         game.draw()  # Redraw the game state
            #         pygame.display.flip()  # Update the display
            #         pygame.time.delay(500)  # Delay to visualize the moves
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
