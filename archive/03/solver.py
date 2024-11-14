from game import YellowSquare as _YellowSquare, RedSquare as _RedSquare, Board as _Board

class YellowSquare(_YellowSquare):
    def update_position(self, position):
        return YellowSquare(position.x, position.y)

    def __hash__(self):
        return hash(('YellowSquare', self.position))

    @classmethod
    def from_piece(cls, piece):
        return cls(piece.position.x, piece.position.y)


class RedSquare(_RedSquare):
    def update_position(self, position):
        return RedSquare(position.x, position.y)

    def __hash__(self):
        return hash(('RedSquare', self.position))

    @classmethod
    def from_piece(cls, piece):
        return cls(piece.position.x, piece.position.y)
    
# class Board(_Board):
#     def move(self, piece, position):
#         print('pppppppppppiece')
#         print(piece)
#         print('positionnnnnnnnnn')
#         print(position)
#         pieces = tuple(
#             _piece if _piece != piece
#             else piece.update_position(position)
#             for _piece in self.pieces
#         )
#         return Board.from_pieces(pieces)
    
#     def __hash__(self):
#         # Unique identifier for each board configuration
#         return hash(frozenset(self.pieces))

#     def __eq__(self, other):
#         # Check if two boards are equivalent
#         return hash(self) == hash(other)

class Boardd(_Board):
    def move(self, piece, position):
        print('SOOOOLVER')
        pieces = tuple(
            _piece if _piece != piece
            else piece.update_position(position)
            for _piece in self.pieces
        )
        return Boardd.from_pieces(pieces)

    def potential_moves(self):
        moves = []
        empty_positions = self.empty_positions()
        for piece in self.pieces:
            if isinstance(piece, _YellowSquare) or isinstance(piece, _RedSquare):
                for position in piece.possible_moves(empty_positions):
                    moves.append((piece, position))
        return moves

    def __hash__(self):
        return hash(frozenset(self.pieces))

    def __eq__(self, other):
        return hash(self) == hash(other)

    @classmethod
    def from_pieces(cls, pieces: tuple):
        return cls(pieces)

    @classmethod
    def from_board(cls, _board):
        pieces = []
        for piece in _board.pieces:
            # print(piece.position)
            if isinstance(piece, _YellowSquare):
                pieces.append(_YellowSquare.from_piece(piece))
            elif isinstance(piece, _RedSquare):
                pieces.append(_RedSquare.from_piece(piece))
            else:
                raise NotImplementedError("Unknown piece type")
        return cls.from_pieces(tuple(pieces))

    def map_piece(self, piece, _board: _Board):
        # Returns the corresponding piece in _board O(1)
        return _board.pieces[self.pieces.index(piece)]


def bfs_solver(_board: _Board):
    # start_board = _Board([piece for piece in _board.pieces])
    start_board = Boardd.from_board(_board)

    visited_boards = set()
    new_boards = [start_board]
    new_boards_set = {start_board}
    transitions = {}
    board = None

    while new_boards:

        board = new_boards.pop(0)
        new_boards_set.remove(board)

        if board.is_solved:
            break

        for curr_piece in board.pieces:
                    if isinstance(curr_piece, _RedSquare):
                        print(f"CURR: Red Square at {curr_piece.position}")
                    elif isinstance(curr_piece, _YellowSquare):
                        print(f"CURR: Yellow Square at {curr_piece.position}")

        visited_boards.add(board)

        for piece, move in board.potential_moves():
            # print('board.potential_moves(): ')
            # print(board.potential_moves())
            # Log the attempted move with positions
            # piece_type = "RedSquare" if isinstance(piece, _RedSquare) else "YellowSquare"
            # print(f"Attempting to move {piece_type} at {piece.position} to {move}, "
            #       f"possible positions: {piece.possible_moves(board.empty_positions())}")

            # print('RIGHT BEFORE SOLVER*S MOVE')
            new_board = board.move(piece, move)
            # print('RIGHT AFTERRRRRRRRRRRRRRRRRRRRRRRRRRR SOLVER* MOVE')

            # print(f"\nNEEEEEEEEEEEEEEEEEEEEEEW board:")
            # for new_piece in new_board.pieces:
            #         new_piece_type = "RedSquare" if isinstance(new_piece, _RedSquare) else "YellowSquare"
            #         print(f"{new_piece_type} at {new_piece.position}")
            # print(f"\nNEEEEEEEEEEEEEEEEEEEEEEW board:")
            # for new_piece in new_board.pieces:
            #         if isinstance(new_piece, _RedSquare):
            #             print(f"Red Square at {new_piece.position}")
            #         elif isinstance(new_piece, _YellowSquare):
            #             print(f"Yellow Square at {new_piece.position}")
                    

            if new_board not in visited_boards and \
                new_board not in new_boards_set:
                # Log the new board state with positions
                # print(f"New board generated:")
                # for new_piece in new_board.pieces:
                #     new_piece_type = "RedSquare" if isinstance(new_piece, _RedSquare) else "YellowSquare"
                #     print(f"{new_piece_type} at {new_piece.position}")
                
                # piece_type = "RedSquare" if isinstance(piece, _RedSquare) else "YellowSquare"
                # print(f"Move: {piece_type} at {piece.position} -> {move}")
                new_boards.append(new_board)
                new_boards_set.add(new_board)
                transitions[new_board] = (board, board.map_piece(piece, _board), move)

    # Backtrack to construct the solution path
    moves_taken = []
    while board != start_board:
        board, piece, move = transitions[board]
        moves_taken.insert(0, (piece, move))

    print("MMoves found:", moves_taken)
    return moves_taken




















# def explore_states():
#     initial_board = _Board.from_start_position()
#     visited_boards = set()
#     new_boards = {initial_board}

#     while new_boards:
#         board = new_boards.pop()
#         visited_boards.add(board)
#         for piece, move in board.potential_moves():
#             new_board = board.move(piece, move)
#             if new_board not in visited_boards:
#                 new_boards.add(new_board)

#     total_boards = len(visited_boards)
#     solution_boards = sum(board.is_solved for board in visited_boards)
#     print(f"Possible board configurations are {total_boards}, of which {solution_boards} are solutions.")


# if __name__ == '__main__':
#     explore_states()
