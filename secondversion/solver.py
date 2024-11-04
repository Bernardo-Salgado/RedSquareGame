"""
    Solves the Klotski puzzle
"""

from game import YellowSquare as _YellowSquare, RedSquare as _RedSquare, Board as _Board


class YellowSquare(_YellowSquare):
    # def update_position(self, position):
    #     return YellowSquare(position[0], position[1])  # Assuming position is a tuple

    def update_position(self, position):
        self.grid_x, self.grid_y = position
        # Update rect attributes if needed, then return self
        return self


    def __hash__(self):
        return hash(('YELLOW', (self.grid_x, self.grid_y)))  # Changed to use grid_x and grid_y

    # In solver.py, inside YellowSquare class
    @classmethod
    def from_square(cls, square):
        # Assuming square has size and color attributes
        return cls(square.grid_x, square.grid_y, size=square.size, color=square.color)



class RedSquare(_RedSquare):
    # def update_position(self, position):
    #     return RedSquare(position[0], position[1])  # Assuming position is a tuple

    def update_position(self, position):
        self.grid_x, self.grid_y = position
        # Update rect attributes if needed, then return self
        return self


    def __hash__(self):
        return hash(('RED', (self.grid_x, self.grid_y)))  # Changed to use grid_x and grid_y

    @classmethod
    def from_square(cls, square):
        return cls(square.grid_x, square.grid_y)


class Board(_Board):
    def __init__(self, red_square, yellow_squares):
        self.red_square = red_square
        self.yellow_squares = yellow_squares  # Add yellow squares to the Board
        self.squares = [red_square] + yellow_squares  # Combine for easy access

    # def move(self, piece, position):
    #     if isinstance(piece, YellowSquare):
    #         pieces = list(self.yellow_squares)
    #         index = pieces.index(piece)
    #         pieces[index] = piece.update_position(position)
    #         return Board(self.red_square, pieces)

    #     elif isinstance(piece, RedSquare):
    #         # Update red square position
    #         return Board(piece.update_position(position), self.yellow_squares)

    #     raise NotImplementedError("Piece type not handled.")

    # def move(self, piece, position):
    #     # Update position and create a new board with updated pieces
    #     pieces = tuple(
    #         _piece if _piece != piece else piece.update_position(position)
    #         for _piece in [self.red_square] + self.yellow_squares
    #     )
    #     return Board.from_pieces(pieces)

    def move(self, piece, position):
        # Initialize an empty list to store updated pieces
        pieces = []

        # Iterate through each piece in the board
        for _piece in [self.red_square] + self.yellow_squares:
            if _piece == piece:
                # Update the position of the piece being moved
                pieces.append(piece.update_position(position))
            else:
                # Keep the other pieces unchanged
                pieces.append(_piece)
        

        if isinstance(pieces[0], _RedSquare):

            red_square = pieces[0]
            print(f"Red Square Position: ({red_square.grid_x}, {red_square.grid_y})")
        # print(pieces[0])

        # Iterate over all pieces to print positions of yellow squares
        for idx, piece in enumerate(pieces):
            if isinstance(piece, _YellowSquare):
                print(f"Yellow Square {idx} Position: ({piece.grid_x}, {piece.grid_y})")

        print('---------------------')

        # Convert the list to a tuple and return a new Board instance
        return Board.from_pieces(tuple(pieces))

    # def move(self, piece, position):
    #     # Initialize an empty list to store updated pieces
    #     pieces = []

    #     # Iterate through each piece in the board
    #     for _piece in [self.red_square] + self.yellow_squares:
    #         if _piece == piece:
    #             # Update the position of the piece being moved
    #             updated_piece = piece.update_position(position)
    #             if updated_piece is not None:
    #                 pieces.append(updated_piece)  # Append the updated piece
    #             else:
    #                 print("Invalid move: Position not allowed.")  # Handle invalid move
    #                 return self  # Return the original board state
    #         else:
    #             # Keep the other pieces unchanged
    #             pieces.append(_piece)

    #     # Print the current positions of the red and yellow squares
    #     if isinstance(pieces[0], _RedSquare):
    #         red_square = pieces[0]
    #         print(f"Red Square Position: ({red_square.grid_x}, {red_square.grid_y})")

    #     # Iterate over all pieces to print positions of yellow squares
    #     for idx, _piece in enumerate(pieces):
    #         if isinstance(_piece, _YellowSquare):
    #             print(f"Yellow Square {idx} Position: ({_piece.grid_x}, {_piece.grid_y})")

    #     print('---------------------')

    #     # Convert the list to a tuple and return a new Board instance
    #     return Board.from_pieces(tuple(pieces))


    @classmethod
    def from_pieces(cls, pieces):
        # Separate red square and yellow squares

        # print([type(p) for p in pieces if isinstance(p, _RedSquare)])  # Debugging line to check the contents of pieces
        # print([type(p) for p in pieces ])  # Debugging line to check the contents of pieces
        # print([p for p in pieces if isinstance(p, _RedSquare)])  # Debugging line to check the contents of pieces
        # print([p for p in pieces if isinstance(p, _YellowSquare)])  # Debugging line to check the contents of pieces
        # print([p for p in pieces if isinstance(p, None)])  # Debugging line to check the contents of pieces
        # for p in pieces:
        #     print(type(p), p.__class__.__module__)
        # print ("------------------------------------------------------")
        



        red_square = next(p for p in pieces if isinstance(p, _RedSquare))
        yellow_squares = [p for p in pieces if isinstance(p, _YellowSquare)]
        return cls(red_square, yellow_squares)


    def potential_moves(self):
        moves = []
        empty_positions = self.empty_positions()
        for piece in [self.red_square] + self.yellow_squares:
            for position in piece.possible_moves(empty_positions):  # You'll need to implement this method
                moves.append((piece, position))
        return moves

    def __hash__(self):
        return hash((self.red_square, tuple(self.yellow_squares)))

    def __eq__(self, other):
        return (self.red_square, tuple(self.yellow_squares)) == (other.red_square, tuple(other.yellow_squares))

    # @classmethod
    # def from_board(cls, _board):
    #     """Create a Board instance from another board instance."""
    #     print("FROOOOOOOOOOOM BOOOOAAAAAAAAAAAAAARD:\n")
    #     red_square = _board.red_square  # Directly access red_square
    #     print(red_square)
    #     yellow_squares = _board.yellow_squares  # Directly access yellow_squares
    #     print(yellow_squares)
    #     print(_board)
    #     return cls(red_square, yellow_squares)  # Create new Board instance

    @classmethod
    def from_board(cls, _board):
        """Create a Board instance from another board instance."""
        # print("FROOOOOOOOOOOM BOOOOAAAAAAAAAAAAAARD:\n")
    
        # Access and print the red square
        red_square = _board.red_square  
        # print(f"Red Square Position: ({red_square.grid_x}, {red_square.grid_y})")
    
        # Access and print the yellow squares
        yellow_squares = _board.yellow_squares  
        # for idx, yellow_square in enumerate(yellow_squares):
            # print(f"Yellow Square {idx + 1} Position: ({yellow_square.grid_x}, {yellow_square.grid_y})")
        
        # board = _board.squares
        # print(board)
        # for a, b, c in enumerate(board):
        #     print(a)
        #     print(b)
        #     print(c)
        #     print('--------------------')
        return cls(red_square, yellow_squares)  # Create new Board instance





def bfs_solver(_board: _Board):
    start_board = Board.from_board(_board)  # Use the new from_board method
    visited_boards = set()

    new_boards = [start_board]
    new_boards_set = {start_board}
    transitions = {}
    board = None
    while new_boards:
        board = new_boards.pop(0)  # Explore the first element

        if board.is_solved:
            # Found the solution
            break

        # Mark as visited
        visited_boards.add(board)
        for piece, move in board.potential_moves():
            new_board = board.move(piece, move)
            if new_board not in visited_boards and new_board not in new_boards_set:
                new_boards.append(new_board)
                new_boards_set.add(new_board)

                transitions[new_board] = (board, piece, move)

    moves_taken = []
    while board != start_board:
        board, piece, move = transitions[board]
        moves_taken.insert(0, (piece, move))
    return moves_taken


def explore_states():
    # Used for exploration and analysis
    initial_board = Board.from_board(_Board.from_start_position())

    visited_boards = set()
    new_boards = {initial_board}

    while new_boards:
        board = new_boards.pop()
        visited_boards.add(board)
        for piece, move in board.potential_moves():
            new_board = board.move(piece, move)
            if new_board not in visited_boards:
                new_boards.add(new_board)

    total_boards = len(visited_boards)
    solution_boards = sum(board.is_solved for board in visited_boards)
    print(f"Possible board configurations are {total_boards}, of which {solution_boards} are solutions.")


if __name__ == '__main__':
    explore_states()