import pygame
import sys
import math
import numpy as np

# Initialize pygame
pygame.init()

# Constants
WIDTH = 600
HEIGHT = 700
LINE_WIDTH = 10
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (52, 152, 219)
HOVER_COLOR = (41, 128, 185)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - AI with Minimax")
screen.fill(BG_COLOR)

# Initialize board
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# Font
font = pygame.font.SysFont('Arial', 40)
small_font = pygame.font.SysFont('Arial', 30)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = BUTTON_COLOR
        self.hover_color = HOVER_COLOR
        self.current_color = self.color
        
    def draw(self):
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)
        text_surf = small_font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        if self.rect.collidepoint(pos):
            self.current_color = self.hover_color
            return True
        else:
            self.current_color = self.color
            return False
            
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pos):
                return True
        return False

# Create buttons
reset_button = Button(WIDTH//2 - 100, HEIGHT - 80, 200, 50, "Reset Game")

def draw_lines():
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT-100), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT-100), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                # Draw X
                pygame.draw.line(screen, CROSS_COLOR, 
                                (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                                CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                CROSS_WIDTH)
            elif board[row][col] == 2:
                # Draw O
                pygame.draw.circle(screen, CIRCLE_COLOR,
                                  (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                  CIRCLE_RADIUS, CIRCLE_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True

def check_win(player):
    # Vertical win
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player)
            return True
    
    # Horizontal win
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            return True
    
    # Asc diagonal win
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_diagonal(player)
        return True
    
    # Desc diagonal win
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_desc_diagonal(player)
        return True
    
    return False

def draw_vertical_winning_line(col, player):
    color = CROSS_COLOR if player == 1 else CIRCLE_COLOR
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2
    pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 185), LINE_WIDTH)

def draw_horizontal_winning_line(row, player):
    color = CROSS_COLOR if player == 1 else CIRCLE_COLOR
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2
    pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), LINE_WIDTH)

def draw_asc_diagonal(player):
    color = CROSS_COLOR if player == 1 else CIRCLE_COLOR
    pygame.draw.line(screen, color, (15, HEIGHT - 185), (WIDTH - 15, 15), LINE_WIDTH)

def draw_desc_diagonal(player):
    color = CROSS_COLOR if player == 1 else CIRCLE_COLOR
    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 185), LINE_WIDTH)

# MINIMAX ALGORITHM IMPLEMENTATION
def minimax(board, depth, is_maximizing):
    # Check terminal states
    if check_win_minimax(2):  # AI wins
        return 1
    elif check_win_minimax(1):  # Human wins
        return -1
    elif is_board_full():  # Draw
        return 0
   ########################################################################## 
    if is_maximizing:
        best_score = -math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 2
                    score = minimax(board, depth + 1, False)
                    board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 1
                    score = minimax(board, depth + 1, True)
                    board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

def check_win_minimax(player):
    # Check all win conditions
    # Horizontal
    for row in range(3):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    # Vertical
    for col in range(3):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    # Diagonals
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False
####################################################################
def best_move():
    best_score = -math.inf
    move = (-1, -1)
    
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                
                if score > best_score:
                    best_score = score
                    move = (row, col)
    
    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False

def draw_status(player_turn, game_over, winner):
    # Draw status area
    status_rect = pygame.Rect(0, HEIGHT-100, WIDTH, 100)
    pygame.draw.rect(screen, (40, 40, 40), status_rect)
    
    if game_over:
        if winner == 1:
            text = "You Win! (Impossible with perfect Minimax!)"
            color = (255, 100, 100)
        elif winner == 2:
            text = "AI Wins!"
            color = (100, 200, 255)
        else:
            text = "Game Draw!"
            color = (200, 200, 200)
    else:
        if player_turn == 1:
            text = "Your Turn (X)"
            color = (255, 255, 100)
        else:
            text = "AI Thinking..."
            color = (100, 255, 100)
    
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT-50))
    screen.blit(text_surf, text_rect)
    
    # Draw algorithm info
    algo_text = "Algorithm: Minimax (Perfect AI)"
    algo_surf = small_font.render(algo_text, True, (200, 200, 200))
    screen.blit(algo_surf, (10, HEIGHT-90))

def reset_game():
    global board, player, game_over, winner
    board = np.zeros((BOARD_ROWS, BOARD_COLS))
    player = 1  # Human starts first
    game_over = False
    winner = 0
    screen.fill(BG_COLOR)
    draw_lines()
    reset_button.draw()
    draw_status(player, game_over, winner)
    pygame.display.update()

# Main game loop
def main():
    global player, game_over, winner
    
    player = 1  # Human is 1, AI is 2
    game_over = False
    winner = 0
    
    draw_lines()
    reset_button.draw()
    draw_status(player, game_over, winner)
    pygame.display.update()
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Check button hover
            reset_button.check_hover(mouse_pos)
            
            # Check button click
            if reset_button.is_clicked(mouse_pos, event):
                reset_game()
                continue
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player == 1:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE
                
                if clicked_row < 3 and clicked_col < 3:
                    if available_square(clicked_row, clicked_col):
                        mark_square(clicked_row, clicked_col, player)
                        draw_figures()
                        
                        if check_win(player):
                            game_over = True
                            winner = player
                        elif is_board_full():
                            game_over = True
                            winner = 0
                        else:
                            player = 2  # Switch to AI
                        
                        draw_status(player, game_over, winner)
                        pygame.display.update()
                        
                        # AI move
                        if not game_over and player == 2:
                            pygame.time.wait(500)  # Small delay for AI "thinking"
                            if best_move():
                                draw_figures()
                                
                                if check_win(2):
                                    game_over = True
                                    winner = 2
                                elif is_board_full():
                                    game_over = True
                                    winner = 0
                                else:
                                    player = 1  # Switch back to human
                            
                            draw_status(player, game_over, winner)
                            pygame.display.update()
        
        # Redraw button for hover effect
        reset_button.draw()
        pygame.display.update()

if __name__ == "__main__":
    main()