from collections import deque
from game import Game, Block
import pygame
import sys
import heapq
from end import EndMenu

cols, rows = 5, 4 # Grid size

class Solver:
    def __init__(self, game):
        self.game = game
        self.initial_state = game.state
        # Define goal positions for the red block
        self.target_positions = [(3, 1), (4, 1), (3, 2), (4, 2)]


    # Perform BFS to find the shortest path to the goal state
    def bfs(self):
        # Initialize with the initial state as the starting path
        initial_state_tuple = self.state_to_tuple(self.initial_state) # Tuple structure ((grid_x1, grid_y1, size_x1, size_y1),...,(grid_xn, grid_yn, size_xn, size_yn))
        initial_path = [self.initial_state]

        # Early check if the initial state is the goal
        if self.is_goal_state(self.initial_state):
            print("Goal reached with 0 moves.")
            return []

        visited = set([initial_state_tuple]) # Set initial state as visited
        queue = deque([(self.initial_state, initial_path)]) # Queue stores state and path

        while queue:
            # Take current state and the path
            current_state, path = queue.popleft()
            # Check possible moves for each block
            for block in current_state:
                for direction in ['left', 'right', 'up', 'down']:
                    new_state = self.move_block(block, direction, current_state)
                    # Checks the move
                    if new_state:
                        state_tuple = self.state_to_tuple(new_state)
                        # Checks if visited
                        if state_tuple not in visited:
                            visited.add(state_tuple)
                            new_path = path + [new_state]
                            # Checks the win status
                            if self.is_goal_state(new_state):
                                # Prints solution step by step
                                self.print_solution(new_path)
                                print(f"Solution found in {len(new_path) - 1} moves")
                                # Animates solution step by step
                                self.animate_solution(new_path)
                                return new_path
                            # Adds new state and the path to the queue
                            queue.append((new_state, new_path))
        print("No solution found.")
        return []


    # Perform DFS to find the shortest path to the goal state with a depth limit
    def dfs(self, max_depth=6):
        # Initialize with the initial state as the starting path
        initial_state_tuple = self.state_to_tuple(self.initial_state)
        initial_path = [self.initial_state]

        # Early check if the initial state is the goal
        if self.is_goal_state(self.initial_state):
            print("Goal reached with 0 moves.")
            return []

        visited = set([initial_state_tuple])  # Set initial state as visited
        stack = [(self.initial_state, initial_path, 0)]  # Stack stores state, path, and current depth

        while stack:
            # Take current state, path and depth
            current_state, path, depth = stack.pop()
            # If the current depth exceeds the max depth, skip further exploration
            if depth >= max_depth:
                continue
            # Check possible moves for each block
            for block in current_state:
                for direction in ['left', 'right', 'up', 'down']:
                    new_state = self.move_block(block, direction, current_state)
                    # Checks the move
                    if new_state:
                        state_tuple = self.state_to_tuple(new_state)
                        # Checks if visited
                        if state_tuple not in visited:
                            visited.add(state_tuple)
                            new_path = path + [new_state]
                            # Checks the win status
                            if self.is_goal_state(new_state):
                                # Prints solution step by step
                                self.print_solution(new_path)
                                print(f"Solution found in {len(new_path) - 1} moves")
                                # Animates solution step by step
                                self.animate_solution(new_path)
                                return new_path

                            # Adds new state, path, and incremented depth to the stack
                            stack.append((new_state, new_path, depth + 1))

        print("No solution found.")
        return []


    # Perform Iterative Deepening Search (IDS) to find the shortest path to the goal state
    def ids(self):
        max_depth = 0
        while True:
            print(f"Starting DFS with depth limit: {max_depth}")
            solution = self.dfs(max_depth)
            if solution:
                return solution
            max_depth += 1


    # Perform greedy search to find the shortest path to the goal state
    def greedy_search(self):
        # Initialize with the initial state as the starting path
        initial_state_tuple = self.state_to_tuple(self.initial_state)
        initial_path = [self.initial_state]

        # Early check if the initial state is the goal
        if self.is_goal_state(self.initial_state):
            print("Goal reached with 0 moves.")
            return []

        # Priority queue stores states and their heuristic values
        prior_queue = []
        heapq.heappush(prior_queue, (self.heuristic(self.initial_state), self.initial_state, initial_path))

        visited = set([initial_state_tuple])  # Set initial state as visited

        while prior_queue:
            # Take the state with the lowest heuristic value
            _, current_state, path = heapq.heappop(prior_queue)

            # Check possible moves for each block
            for block in current_state:
                for direction in ['left', 'right', 'up', 'down']:
                    new_state = self.move_block(block, direction, current_state)
                    # Checks the move
                    if new_state:
                        state_tuple = self.state_to_tuple(new_state)
                        # Checks if visited
                        if state_tuple not in visited:
                            visited.add(state_tuple)
                            new_path = path + [new_state]
                            # Checks the win status
                            if self.is_goal_state(new_state):
                                # Prints solution step by step
                                self.print_solution(new_path)
                                print(f"Solution found in {len(new_path) - 1} moves")
                                # Animates solution step by step
                                self.animate_solution(new_path)
                                return new_path
                            # Push the new state and its heuristic value to the priority queue, path as well
                            heapq.heappush(prior_queue, (self.heuristic(new_state), new_state, new_path))

        print("No solution found.")
        return []


    # Perform A* search to find the shortest path to the goal state
    def a_star_search(self):
        # Initialize with the initial state as the starting path
        initial_state_tuple = self.state_to_tuple(self.initial_state)
        initial_path = [self.initial_state]

        # Early check if the initial state is the goal
        if self.is_goal_state(self.initial_state):
            print("Goal reached with 0 moves.")
            return []

        # Priority queue stores states with their f(n) values (f(n), state, path)
        prior_queue = []
        # At the beginning just f(n) = h(n) because g(n) = 0 (cost function)
        heapq.heappush(prior_queue, (self.heuristic(self.initial_state), 0, self.initial_state, initial_path))

        # Set of visited states to avoid reprocessing
        visited = set([initial_state_tuple])

        while prior_queue:
            # Get the state with the lowest f(n)
            f_n, g_n, current_state, path = heapq.heappop(prior_queue)
            # Check possible moves for each block
            for block in current_state:
                for direction in ['left', 'right', 'up', 'down']:
                    new_state = self.move_block(block, direction, current_state)
                    # Check if the move is valid
                    if new_state:
                        state_tuple = self.state_to_tuple(new_state)
                        # If the state hasn't been visited
                        if state_tuple not in visited:
                            visited.add(state_tuple)
                            new_path = path + [new_state]
                            # Check if we've reached the goal state
                            if self.is_goal_state(new_state):
                                # Prints solution step by step
                                self.print_solution(new_path)
                                print(f"Solution found in {len(new_path) - 1} moves")
                                # Animates solution step by step
                                self.animate_solution(new_path)
                                return new_path
                            # Calculate f(n) = g(n) + h(n)
                            g_n_new = g_n + 1  # Each move has a cost of 1
                            f_n_new = g_n_new + self.heuristic(new_state)
                            # Add the new state to the open list with its f(n)
                            heapq.heappush(prior_queue, (f_n_new, g_n_new, new_state, new_path))

        print("No solution found.")
        return []


    def heuristic(self, state):
        # Heuristic: Manhattan distance to the closest goal position for the red block
        red_block = state[0]  # Takes state of the red block (top left block credentials)
        goal_x, goal_y = self.target_positions[0] # Takes the goal credentials (top left credentials)
        # Calculate Manhattan distance between the red block's top-left corner and target position
        distance = abs(red_block.grid_x - goal_x) + abs(red_block.grid_y - goal_y)
        return distance

    def state_to_tuple(self, state):
        # Converts the state to a tuple for hashing and comparison
        return tuple(sorted((block.grid_x, block.grid_y, block.size_x, block.size_y) for block in state))

    def is_goal_state(self, state):
        # Checks if the current state matches the target goal configuration
        red_block = state[0]  # Assuming the first block is the red block
        return all(pos in self.target_positions for pos in red_block.get_positions())

    def move_block(self, block, direction, current_state):
        # Attempts to move a block in the specified direction if valid
        # Clone the block to avoid mutating the original state
        cloned_block = Block(block.grid_x, block.grid_y, block.size_x, block.size_y)
        new_state = [Block(b.grid_x, b.grid_y, b.size_x, b.size_y) for b in current_state]

        # Adjust cloned block's position based on the direction
        if direction == 'left' and cloned_block.grid_x > 0:
            cloned_block.grid_x -= 1
        elif direction == 'right' and cloned_block.grid_x < cols - cloned_block.size_x:
            cloned_block.grid_x += 1
        elif direction == 'up' and cloned_block.grid_y > 0:
            cloned_block.grid_y -= 1
        elif direction == 'down' and cloned_block.grid_y < rows - cloned_block.size_y:
            cloned_block.grid_y += 1
        else:
            return None

        # Replace the original block in new_state with the moved block
        for idx, b in enumerate(new_state):
            if b.grid_x == block.grid_x and b.grid_y == block.grid_y:
                new_state[idx] = cloned_block
                break

        # Return None if there is a collision, otherwise return the new state
        if self.check_collisions(cloned_block, new_state):
            return None

        return new_state

    def check_collisions(self, block, current_state):
        # Checks for collisions between the moving block and others in the state
        occupied_positions = set()
        for b in current_state:
            if b != block:
                occupied_positions.update(b.get_positions())
        # Return True if any position is occupied, else False
        return any(pos in occupied_positions for pos in block.get_positions())

    def print_solution(self, solution_path):
        # Prints each step in the solution path for debugging
        for step, state in enumerate(solution_path):
            print(f"Step {step}:")
            for block in state:
                print(f"Block at ({block.grid_x}, {block.grid_y}) with size ({block.size_x}, {block.size_y})")
            print("-" * 30)

    def animate_solution(self, solution_path):
        # Create an instance of EndMenu with the Game instance
        end_menu = EndMenu(self.game.screen, self.game)  # Pass the Game instance

        # Animates the solution path in the game
        for step, state in enumerate(solution_path):
            self.game.state = state  # Update game state to the current step
            self.game.update()  # Check for win and update game state
            self.game.draw()  # Redraw the screen
            pygame.time.wait(500)  # Wait for 500ms before the next step
            pygame.display.flip()

            # Increment the move count in the Game instance
            if step < len(solution_path) - 1:  # Increment for every move except the last state
                self.game.move_count += 1

        # After the final step, show the end menu
        end_menu.show_end_menu()  # Call the end menu directly
