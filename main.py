import pygame
import sys
from chess_pieces import Pawn, Rook, Knight, Bishop, Queen, King

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
BOARD_SIZE = 8
SQUARE_SIZE = WINDOW_SIZE // BOARD_SIZE
WHITE = (255, 255, 255)
BLACK = (128, 128, 128)
HIGHLIGHT_COLOR = (255, 255, 0, 128)

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Chess Game")

class ChessGame:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.selected_piece = None
        self.current_player = 'white'
        self.initialize_board()

    def initialize_board(self):
        # Initialize pawns
        for x in range(8):
            self.board[1][x] = Pawn('black', (x, 1))
            self.board[6][x] = Pawn('white', (x, 6))

        # Initialize other pieces
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for x, piece_class in enumerate(piece_order):
            self.board[0][x] = piece_class('black', (x, 0))
            self.board[7][x] = piece_class('white', (x, 7))

    def draw_board(self):
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                color = WHITE if (x + y) % 2 == 0 else BLACK
                pygame.draw.rect(screen, color, (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self):
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                piece = self.board[y][x]
                if piece:
                    # Draw piece (simple circle for now)
                    color = WHITE if piece.color == 'white' else BLACK
                    pygame.draw.circle(screen, color, 
                                    (x * SQUARE_SIZE + SQUARE_SIZE // 2,
                                     y * SQUARE_SIZE + SQUARE_SIZE // 2),
                                    SQUARE_SIZE // 3)

    def draw_valid_moves(self, valid_moves):
        for x, y in valid_moves:
            pygame.draw.circle(screen, HIGHLIGHT_COLOR,
                             (x * SQUARE_SIZE + SQUARE_SIZE // 2,
                              y * SQUARE_SIZE + SQUARE_SIZE // 2),
                             SQUARE_SIZE // 6)

    def get_piece_at_pos(self, pos):
        x, y = pos
        return self.board[y][x]

    def move_piece(self, from_pos, to_pos):
        from_x, from_y = from_pos
        to_x, to_y = to_pos
        piece = self.board[from_y][from_x]
        
        if piece:
            piece.position = (to_x, to_y)
            piece.has_moved = True
            self.board[to_y][to_x] = piece
            self.board[from_y][from_x] = None
            self.current_player = 'black' if self.current_player == 'white' else 'white'

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    board_x, board_y = x // SQUARE_SIZE, y // SQUARE_SIZE
                    
                    if self.selected_piece is None:
                        piece = self.get_piece_at_pos((board_x, board_y))
                        if piece and piece.color == self.current_player:
                            self.selected_piece = piece
                    else:
                        valid_moves = self.selected_piece.get_valid_moves(self.board)
                        if (board_x, board_y) in valid_moves:
                            self.move_piece(self.selected_piece.position, (board_x, board_y))
                        self.selected_piece = None

            # Draw everything
            self.draw_board()
            if self.selected_piece:
                self.draw_valid_moves(self.selected_piece.get_valid_moves(self.board))
            self.draw_pieces()
            
            pygame.display.flip()

if __name__ == "__main__":
    game = ChessGame()
    game.run() 