import pygame
import sys
from menu import Menu
from game import Game
from solver import Solver

def main():
    pygame.init()

    pygame.mixer.init()    # Initialize the mixer

    # screen_width, screen_height = 1536, 864
    screen_width, screen_height = 1920, 1080
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Klotski Game")

    menu = Menu(screen)
    # game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            menu_action = menu.handle_event(event)
            if menu_action == "start":
                # Run the game (player solver)
                game.run()

            elif menu_action == "solve":
                # Initialize the game and the solver
                solver = Solver(game)
                # UNCOMMENT A SPECIFIC SOLVER

                # Run the BFS solver to find the solution path
                # solver.track_solver(solver.bfs, 'BFS')

                # Run the DFS solver to find the solution path
                max_depth = 10
                # solver.track_solver(lambda: solver.dfs(max_depth), 'DFS')

                # Run the IDS solver to find the solution path
                solver.track_solver(solver.ids, 'IDS')

                # Run the greedy solver to find the solution path with different heuristics
                # solver.track_solver(lambda: solver.greedy_search(solver.manhattan), 'Greedy Search with Manhattan')
                # solver.track_solver(lambda: solver.greedy_search(solver.euclidean), 'Greedy Search with Euclidian')
                # solver.track_solver(lambda: solver.greedy_search(solver.chebyshev), 'Greedy Search with Chybyshev')

                # Run A* solver to find the solution path with different heuristics
                # solver.track_solver(lambda: solver.a_star_search(solver.manhattan), 'A* with Manhattan')
                # solver.track_solver(lambda: solver.a_star_search(solver.euclidean), 'A* Search with Euclidian')
                # solver.track_solver(lambda: solver.a_star_search(solver.chebyshev), 'A* Search with Chybyshev')

            elif menu_action is None:
                pass

        menu.draw()

if __name__ == "__main__":
    main()