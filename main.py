# [1/5 MAIN.PY]

import pygame
import sys
from menu import Menu
from game import Game
from solver import Solver

def main():
    pygame.init()

    pygame.mixer.init()    # Initialize the mixer
    screen_width, screen_height = 1920, 1080
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Red Duck Game")

    menu = Menu(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            menu_action = menu.handle_event(event)
            if menu_action == "start":
                # Get the current board size from the menu
                cols, rows = menu.board_sizes[menu.current_board_size_index]
                game = Game(cols, rows)  # Pass the selected board size to the Game instance
                # Run the game (player solver)
                game.run()

            elif menu_action == "BFS":
                # Get the current board size from the menu
                cols, rows = menu.board_sizes[menu.current_board_size_index]
                game = Game(cols, rows)  # Pass the selected board size to the Game instance

                menu.show_solving_message() # Solving window

                # Initialize the game and the solver
                solver = Solver(game)

                # Run the BFS solver to find the solution path
                solver.track_solver(solver.bfs, 'BFS')

            elif menu_action == "IDS":

                # Get the current board size from the menu
                cols, rows = menu.board_sizes[menu.current_board_size_index]
                game = Game(cols, rows)  # Pass the selected board size to the Game instance

                menu.show_solving_message()  # Show the solving window

                # Initialize the game and the solver
                solver = Solver(game)

                # Run the IDS solver to find the solution path
                solver.track_solver(solver.ids, 'IDS')


            elif menu_action == "Greedy Search with Manhattan":
                cols, rows = menu.board_sizes[menu.current_board_size_index]
                game = Game(cols, rows)  # Pass the selected board size to the Game instance

                menu.show_solving_message() # Solving window

                # Initialize the game and the solver
                solver = Solver(game)

                # Run the greedy solver to find the solution path with different heuristics
                solver.track_solver(lambda: solver.greedy_search(solver.manhattan), 'Greedy Search with Manhattan')

            elif menu_action == "Greedy Search with Euclidean":
                cols, rows = menu.board_sizes[menu.current_board_size_index]
                game = Game(cols, rows)  # Pass the selected board size to the Game instance

                menu.show_solving_message() # Solving window

                # Initialize the game and the solver
                solver = Solver(game)

                # Run the greedy solver to find the solution path with different heuristics
                solver.track_solver(lambda: solver.greedy_search(solver.euclidean), 'Greedy Search with Euclidian')

            elif menu_action == "Greedy Search with Chebyshev":
                cols, rows = menu.board_sizes[menu.current_board_size_index]
                game = Game(cols, rows)  # Pass the selected board size to the Game instance

                menu.show_solving_message() # Solving window

                # Initialize the game and the solver
                solver = Solver(game)

                # Run the greedy solver to find the solution path with different heuristics
                solver.track_solver(lambda: solver.greedy_search(solver.chebyshev), 'Greedy Search with Chebyshev')

            elif menu_action == "A* with Manhattan":
                cols, rows = menu.board_sizes[menu.current_board_size_index]
                game = Game(cols, rows)  # Pass the selected board size to the Game instance

                menu.show_solving_message() # Solving window

                # Initialize the game and the solver
                solver = Solver(game)

                # Run A* solver to find the solution path with different heuristics
                solver.track_solver(lambda: solver.a_star_search(solver.manhattan), 'A* with Manhattan')

            elif menu_action == "A* with Euclidean":
                cols, rows = menu.board_sizes[menu.current_board_size_index]
                game = Game(cols, rows)  # Pass the selected board size to the Game instance

                menu.show_solving_message() # Solving window

                # Initialize the game and the solver
                solver = Solver(game)

                # Run A* solver to find the solution path with different heuristics
                solver.track_solver(lambda: solver.a_star_search(solver.euclidean), 'A* with Euclidian')

            elif menu_action == "A* with Chebyshev":
                cols, rows = menu.board_sizes[menu.current_board_size_index]
                game = Game(cols, rows)  # Pass the selected board size to the Game instance

                menu.show_solving_message() # Solving window

                # Initialize the game and the solver
                solver = Solver(game)

                # Run A* solver to find the solution path with different heuristics
                solver.track_solver(lambda: solver.a_star_search(solver.chebyshev), 'A* with Chebyshev')

            elif menu_action is None:
                pass

        menu.draw()

if __name__ == "__main__":
    main()