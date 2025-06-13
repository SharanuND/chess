import pygame

class ChessPiece:
    def __init__(self, color, position):
        self.color = color  # 'white' or 'black'
        self.position = position  # (x, y) coordinates
        self.has_moved = False

    def get_valid_moves(self, board):
        pass

class Pawn(ChessPiece):
    def get_valid_moves(self, board):
        moves = []
        direction = -1 if self.color == 'white' else 1
        x, y = self.position

        # Forward move
        if 0 <= y + direction < 8 and board[y + direction][x] is None:
            moves.append((x, y + direction))
            # Initial two-square move
            if not self.has_moved and 0 <= y + 2*direction < 8 and board[y + 2*direction][x] is None:
                moves.append((x, y + 2*direction))

        # Capture moves
        for dx in [-1, 1]:
            if 0 <= x + dx < 8 and 0 <= y + direction < 8:
                piece = board[y + direction][x + dx]
                if piece and piece.color != self.color:
                    moves.append((x + dx, y + direction))

        return moves

class Rook(ChessPiece):
    def get_valid_moves(self, board):
        moves = []
        x, y = self.position
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in directions:
            current_x, current_y = x + dx, y + dy
            while 0 <= current_x < 8 and 0 <= current_y < 8:
                piece = board[current_y][current_x]
                if piece is None:
                    moves.append((current_x, current_y))
                elif piece.color != self.color:
                    moves.append((current_x, current_y))
                    break
                else:
                    break
                current_x += dx
                current_y += dy

        return moves

class Knight(ChessPiece):
    def get_valid_moves(self, board):
        moves = []
        x, y = self.position
        possible_moves = [
            (x+2, y+1), (x+2, y-1), (x-2, y+1), (x-2, y-1),
            (x+1, y+2), (x+1, y-2), (x-1, y+2), (x-1, y-2)
        ]

        for move_x, move_y in possible_moves:
            if 0 <= move_x < 8 and 0 <= move_y < 8:
                piece = board[move_y][move_x]
                if piece is None or piece.color != self.color:
                    moves.append((move_x, move_y))

        return moves

class Bishop(ChessPiece):
    def get_valid_moves(self, board):
        moves = []
        x, y = self.position
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            current_x, current_y = x + dx, y + dy
            while 0 <= current_x < 8 and 0 <= current_y < 8:
                piece = board[current_y][current_x]
                if piece is None:
                    moves.append((current_x, current_y))
                elif piece.color != self.color:
                    moves.append((current_x, current_y))
                    break
                else:
                    break
                current_x += dx
                current_y += dy

        return moves

class Queen(ChessPiece):
    def get_valid_moves(self, board):
        moves = []
        x, y = self.position
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),  # Rook moves
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Bishop moves
        ]

        for dx, dy in directions:
            current_x, current_y = x + dx, y + dy
            while 0 <= current_x < 8 and 0 <= current_y < 8:
                piece = board[current_y][current_x]
                if piece is None:
                    moves.append((current_x, current_y))
                elif piece.color != self.color:
                    moves.append((current_x, current_y))
                    break
                else:
                    break
                current_x += dx
                current_y += dy

        return moves

class King(ChessPiece):
    def get_valid_moves(self, board):
        moves = []
        x, y = self.position
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                piece = board[new_y][new_x]
                if piece is None or piece.color != self.color:
                    moves.append((new_x, new_y))

        return moves 