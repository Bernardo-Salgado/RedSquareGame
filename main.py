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
    pygame.display.set_caption("Klotski Game")

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
                # UNCOMMENT A SPECIFIC SOLVER

                # Run the BFS solver to find the solution path
                solver.track_solver(solver.bfs, 'BFS')

                # Run the DFS solver to find the solution path
                
                # max_depth = 29
                # solver.track_solver(lambda: solver.dfs(max_depth), 'DFS')

                # Run the IDS solver to find the solution path
                #solver.track_solver(solver.ids, 'IDS')

                # Run the greedy solver to find the solution path with different heuristics
                # solver.track_solver(lambda: solver.greedy_search(solver.manhattan), 'Greedy Search with Manhattan')
                # solver.track_solver(lambda: solver.greedy_search(solver.euclidean), 'Greedy Search with Euclidian')
                # solver.track_solver(lambda: solver.greedy_search(solver.chebyshev), 'Greedy Search with Chebyshev')

                # Run A* solver to find the solution path with different heuristics
                # solver.track_solver(lambda: solver.a_star_search(solver.manhattan), 'A* Search with Manhattan')
                # solver.track_solver(lambda: solver.a_star_search(solver.euclidean), 'A* Search with Euclidian')
                # solver.track_solver(lambda: solver.a_star_search(solver.chebyshev), 'A* Search with Chebyshev')
            
            elif menu_action == "DFS":

                # Get the current board size from the menu
                cols, rows = menu.board_sizes[menu.current_board_size_index]
                game = Game(cols, rows)  # Pass the selected board size to the Game instance

                menu.show_solving_message()  # Show the solving window

                # Initialize the game and the solver
                solver = Solver(game)

                # Retrieve the DFS depth entered by the user from the menu
                # max_depth = menu.get_dfs_depth()

                ##PROLLY UNCOMMENT THIS -->
                # # Check if the input is a valid integer
                # if max_depth is not None and isinstance(max_depth, int):
                #     # Run the DFS solver with the given max depth
                #     solver.track_solver(lambda: solver.dfs(max_depth), 'DFS')
                # else:
                #     # Optionally, display a message if the depth is invalid
                #     print("Invalid depth input!")
                ##PROLLY UNCOMMENT THIS^^


            #     print("HEEEEEEEEEEEEEEELP")
            # # elif menu_action.isdigit():
            #     cols, rows = menu.board_sizes[menu.current_board_size_index]
            #     game = Game(cols, rows)  # Pass the selected board size to the Game instance

            #     menu.show_solving_message() # Solving window

            #     # Initialize the game and the solver
            #     solver = Solver(game)

            #     max_depth = menu.get_dfs_depth()
            #     solver.track_solver(lambda: solver.dfs(max_depth), 'DFS')

            # elif menu_action == "IDS":
            #     cols, rows = menu.board_sizes[menu.current_board_size_index]
            #     game = Game(cols, rows)  # Pass the selected board size to the Game instance

            #     menu.show_solving_message() # Solving window

            #     # Initialize the game and the solver
            #     solver = Solver(game)

            #     # Run the IDS solver to find the solution path
            #     solver.track_solver(solver.ids, 'IDS')

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

            elif menu_action == "A* with Euclidian":
                cols, rows = menu.board_sizes[menu.current_board_size_index]
                game = Game(cols, rows)  # Pass the selected board size to the Game instance

                menu.show_solving_message() # Solving window

                # Initialize the game and the solver
                solver = Solver(game)

                # Run A* solver to find the solution path with different heuristics
                solver.track_solver(lambda: solver.a_star_search(solver.euclidian), 'A* with Euclidian')

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