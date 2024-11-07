from game import Game

class Boardd:
    def __init__(self, state):
        self.state = state  # state is now a list of ((x, y), (width, height))

    def move(self, block_index, new_position):
        print(f"Current state before move: {self.state}")
        print(f"MOVE: Moving block {block_index} to new position {new_position}")
        new_state = list(self.state)
        size = new_state[block_index][1]  # Get the size of the block
        new_state[block_index] = (new_position, size)  # Ensure new_position is a tuple
        print(f"New state after move: {new_state}")
        return Boardd(new_state)

    def potential_moves(self):
        moves = []
        empty_positions = self.empty_positions()
        for index, (position, size) in enumerate(self.state):
            possible_moves = self.get_possible_moves(position, size, empty_positions, 4, 5)
            for new_position in possible_moves:
                moves.append((index, new_position))  # Include the block index with the new position
        return moves

    def get_possible_moves(self, position, size, empty_positions, rows, cols):
        # Correctly unpack the position, where position is actually (row, col) and size is (width, height)
        # The position might be wrapped in another tuple (index, (row, col)), so we need to unpack accordingly.
        if isinstance(position, tuple) and len(position) == 2 and isinstance(position[1], tuple):
            _, (row, col) = position  # Unpack (index, (row, col))
        else:
            row, col = position  # Otherwise, just unpack the position as (row, col)

        print(f"Getting possible moves for block at position: ({row}, {col}) with size: {size}")

        possible_moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up

        # Loop over possible movement directions
        for dr, dc in directions:
            print(f"Trying direction: (dr={dr}, dc={dc})")

            # Calculate the new candidate position
            new_row, new_col = row + dr, col + dc
            print(f"New position candidate: ({new_row}, {new_col})")

            # Check if the new position is within the grid boundaries
            if 0 <= new_row < rows and 0 <= new_col < cols:
                print(f"Position ({new_row}, {new_col}) is within grid bounds")

                # Check if the block can actually fit in the new position based on its size
                if dr == 0:  # Horizontal move
                    print(f"Checking horizontal move to position ({new_row}, {new_col})")
                    if (new_row, new_col + size[0] - 1) in empty_positions:
                        print(f"Move valid: the block fits horizontally")
                        possible_moves.append((new_row, new_col))
                elif dc == 0:  # Vertical move
                    print(f"Checking vertical move to position ({new_row}, {new_col})")
                    if (new_row + size[1] - 1, new_col) in empty_positions:
                        print(f"Move valid: the block fits vertically")
                        possible_moves.append((new_row, new_col))

            else:
                print(f"Position ({new_row}, {new_col}) is outside grid bounds")

        print(f"Possible moves for block at position ({row}, {col}): {possible_moves}")
        return possible_moves

    def empty_positions(self):
        occupied_positions = set(self.state)
        all_positions = {(r, c) for r in range(5) for c in range(4)}  # Assuming a 5x4 grid
        return list(all_positions - occupied_positions)

    def __hash__(self):
        return hash(frozenset(self.state))

    def __eq__(self, other):
        return hash(self) == hash(other)

    @classmethod
    def from_board(cls, state):
        return cls(state)  # Directly accept the state

    def is_solved(self):
        # Define the target position for the red block (2x2)
        target_position = (0, (3,1)) # Adjust based on your winning condition

        #DEBUG
        print(f"This is the state: {self.state}")
        print(f"This is the state of red block: {self.state[0][0]}")

        return self.state[0][0] == target_position

def bfs_solver(game_state):
    # Directly use the game_state as it is already in the correct format
    initial_state = game_state  # This should be a list of tuples: [((x, y), (width, height)), ...]
    start_board = Boardd(initial_state)

    visited_boards = set()
    new_boards = [start_board]
    new_boards_set = {start_board}
    transitions = {}
    board = None
    i = 0

    while new_boards:
        board = new_boards.pop(0)
        new_boards_set.remove(board)

        if board.is_solved():
            break

        visited_boards.add(board)

        for block_index in range(len(board.state)):  # Iterate over each block
            for new_position in board.potential_moves():
                print(f"Attempting to move block {block_index} to new position {new_position}")
                new_board = board.move(block_index, new_position)  # Use block_index correctly
                if new_board not in visited_boards and new_board not in new_boards_set:
                    new_boards.append(new_board)
                    new_boards_set.add(new_board)
                    transitions[new_board] = (board, block_index, new_position)

    # Backtrack to construct the solution path
    moves_taken = []
    while board != start_board:
        board, block_index, new_position = transitions[board]
        moves_taken.insert(0, (block_index, new_position))

    print(f"moves taken: {moves_taken}")

    # Now, we create the formatted_moves list using list comprehension
    formatted_moves = [(block_index, new_position) for block_index, (empty_position, new_position) in moves_taken]

    print(f"formatted moves: {formatted_moves}")
    return formatted_moves

