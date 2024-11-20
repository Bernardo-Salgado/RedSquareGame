# [4/5 SOLVER.PY]

from collections import deque
from game import Game, Block
import pygame
import sys
import random
import heapq
from end import EndMenu
import time
import psutil
import os
import gc

class Solver:
    def __init__(self, game):
        self.game = game
        self.initial_state = game.state

        # Define goal positions for the red block
        self.cols = game.cols  # Use cols from the Game instance
        self.rows = game.rows  # Use rows from the Game instance
        self.target_positions = game.target_positions  # Use target_positions from the Game instance

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
                for direction in ['right', 'left', 'up', 'down']:
                    # Move current block
                    new_state = self.move_block(block, direction, current_state)
                    # Checks the move possibility
                    if new_state:
                        state_tuple = self.state_to_tuple(new_state)
                        # Checks if visited
                        if state_tuple not in visited:
                            visited.add(state_tuple)
                            new_path = path + [new_state]
                            # Checks the win status
                            if self.is_goal_state(new_state):
                                # Return a solution path
                                return new_path
                            # Adds new state and the path to the queue
                            queue.append((new_state, new_path))
        print("No solution found.")
        return []

    # Perform DFS to find the shortest path to the goal state with a depth limit
    def dfs(self, max_depth=6):
        # Initialize with the initial state as the starting path
        initial_path = [self.initial_state]

        # Early check if the initial state is the goal
        if self.is_goal_state(self.initial_state):
            print("Goal reached with 0 moves.")
            return []

        # Local visited set, stores states and their depth
        visited = {}

        # Stack stores state, path, current depth
        stack = [(self.initial_state, initial_path, 0)]

        while stack:
            # Take current state, path, depth
            current_state, path, depth = stack.pop()

            # If current depth exceeds max_depth, stop further exploration
            if depth >= max_depth:
                continue

            # Convert current state to tuple for comparison
            state_tuple = self.state_to_tuple(current_state)

            # Check if the state was visited at a shallower or equal depth, meaning we don't need to explore it again because there will not be a solution in that state
            if state_tuple in visited and visited[state_tuple] <= depth:
                continue  # Ignore this state

            # Mark the state as visited at the current depth
            visited[state_tuple] = depth

            # Check possible moves for each block
            for block in current_state:
                for direction in ['left', 'right', 'up', 'down']:
                    new_state = self.move_block(block, direction, current_state)

                    # If the move is valid
                    if new_state:
                        new_state_tuple = self.state_to_tuple(new_state)

                        # If the new state has not been visited or the new state appears on the shallower depth then in previous cases, it can be solution found on deeper levels
                        if new_state_tuple not in visited or visited[new_state_tuple] > depth + 1:
                            new_path = path + [new_state]

                            # If the goal is reached
                            if self.is_goal_state(new_state):
                                return new_path  # Return solution path

                            # Push new state to the stack with updated path and depth
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
    def greedy_search(self, heuristic):
        # Initialize with the initial state as the starting path
        initial_state_tuple = self.state_to_tuple(self.initial_state)
        initial_path = [self.initial_state]

        # Early check if the initial state is the goal
        if self.is_goal_state(self.initial_state):
            print("Goal reached with 0 moves.")
            return []

        # Priority queue stores states and their heuristic values
        prior_queue = []
        heapq.heappush(prior_queue, (heuristic(self.initial_state), self.initial_state, initial_path))

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
                                # Return a solution path
                                return new_path
                            # Push the new state and its heuristic value to the priority queue, path as well
                            heapq.heappush(prior_queue, (heuristic(new_state), new_state, new_path))
        print("No solution found.")
        return []


    # Perform A* search to find the shortest path to the goal state
    def a_star_search(self, heuristic):
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
        heapq.heappush(prior_queue, (heuristic(self.initial_state), 0, self.initial_state, initial_path))

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
                                # Return a solution path
                                return new_path
                            # Calculate f(n) = g(n) + h(n)
                            g_n_new = g_n + 1  # Each move has a cost of 1
                            f_n_new = g_n_new + heuristic(new_state)
                            # Add the new state to the open list with its f(n)
                            heapq.heappush(prior_queue, (f_n_new, g_n_new, new_state, new_path))
        print("No solution found.")
        return []

    def manhattan(self, state):
        # Heuristic: Manhattan Distance
        red_block = state[0]  # Takes state of the red block (top left block credentials)
        goal_x, goal_y = self.target_positions[0] # Takes the goal credentials (top left credentials)
        # Calculate Manhattan distance between the red block's top-left corner and target position
        distance = abs(red_block.grid_x - goal_x) + abs(red_block.grid_y - goal_y)
        return distance

    def euclidean(self, state):
        # Heuristic: Euclidean Distance
        red_block = state[0]  # Takes state of the red block (top left block credentials)
        goal_x, goal_y = self.target_positions[0]  # Takes the goal position (top-left credentials)
        # Calculate Euclidean distance between the red block's top-left corner and the target position
        distance = ((red_block.grid_x - goal_x) ** 2 + (red_block.grid_y - goal_y) ** 2) ** 0.5
        return distance

    def chebyshev(self, state):
        # Heuristic: Chebyshev Distance
        red_block = state[0] # Takes state of the red block (top left block credentials)
        goal_x, goal_y = self.target_positions[0]   # Takes the goal position (top-left credentials)
        # Calculate the Chebyshev distance between the red block and the goal position
        distance = max(abs(red_block.grid_x - goal_x), abs(red_block.grid_y - goal_y))
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
        elif direction == 'right' and cloned_block.grid_x < self.cols - cloned_block.size_x:
            cloned_block.grid_x += 1
        elif direction == 'up' and cloned_block.grid_y > 0:
            cloned_block.grid_y -= 1
        elif direction == 'down' and cloned_block.grid_y < self.rows - cloned_block.size_y:
            cloned_block.grid_y += 1
        else:
            return None

        # Replace the original block in new_state with the moved block
        for idx, b in enumerate(new_state):
            if b.grid_x == block.grid_x and b.grid_y == block.grid_y:
                new_state[idx] = cloned_block

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
            self.game.draw()  # Redraw the screen
            self.game.update()  # Check for win and update game state
            pygame.time.wait(250)  # Wait before the next step
            pygame.display.flip()

            # Increment the move count in the Game instance
            if step < len(solution_path) - 1:  # Increment for every move except the last state
                self.game.move_count += 1

                # Play sounds based on the block index
                for block in state:
                    block_index = self.game.state.index(block)
                    if block_index == 0:  # If it's the first block (2x2)
                        sound_to_play = random.choice(self.game.sick_quack_sounds)
                    else:  # For blocks with index > 0
                        sound_to_play = random.choice(self.game.quack_sounds)

                    # Play the selected sound
                    sound_to_play.play()
                    # Play a random swirl sound
                    random.choice(self.game.swirl_sounds).play()

        # After the final step, show the end menu
        end_menu.show_end_menu()  # Call the end menu directly
        # Reset the current state to the initial state
        self.game.reset()

    def track_solver(self, solver_type, solver_name, *solver_args):
        print(f"Starting {solver_name}...")

        #Collect garbage to avoid negative memory usage
        gc.collect()

        # Start time and memory tracking
        start_time = time.time()
        process = psutil.Process(os.getpid())
        start_memory = process.memory_info().rss

        # Run the solver and capture the solution
        solution = solver_type(*solver_args)

        # Calculate elapsed time and memory usage
        elapsed_time = time.time() - start_time
        end_memory = process.memory_info().rss  # Memory usage after execution
        memory_used = (end_memory - start_memory) / 1024  # Convert to KB

        # Print solution step by step
        self.print_solution(solution)

        # Output results
        print(f"{solver_name} completed in {elapsed_time:.4f} seconds.")
        print(f"{solver_name} used {memory_used:.4f} KB during execution.")
        print(f"Solution found in {len(solution) - 1} moves.")

        # Animate solution step by step
        self.animate_solution(solution)
