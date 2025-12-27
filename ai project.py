import pygame
import sys
import math
import numpy as np

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700
LINE_WIDTH, SQUARE_SIZE = 10, 200
CIRCLE_RADIUS, CIRCLE_WIDTH, CROSS_WIDTH, SPACE = 60, 15, 25, 55
BG_COLOR, LINE_COLOR = (230, 190, 230), (200, 150, 220)
CIRCLE_COLOR, CROSS_COLOR, TEXT_COLOR = (255, 255, 255), (255, 255, 255), (255, 255, 255)
BUTTON_COLOR, HOVER_COLOR = (180, 100, 200), (150, 80, 180)
WIN_BG, LOSE_BG, DRAW_BG = (255, 200, 255), (200, 150, 230), (240, 180, 240)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - AI with Minimax")
board = np.zeros((3, 3))

# Fonts - using better font families with fallbacks
try:
    font = pygame.font.SysFont('segoeui,arial', 36)
    small_font = pygame.font.SysFont('segoeui,arial', 24)
    title_font = pygame.font.SysFont('segoeui,arial', 90, bold=True)
    subtitle_font = pygame.font.SysFont('segoeui,arial', 32)
    button_font = pygame.font.SysFont('segoeui,arial', 26)
    info_font = pygame.font.SysFont('segoeui,arial', 20)
except:
    font = pygame.font.SysFont('Arial', 36)
    small_font = pygame.font.SysFont('Arial', 24)
    title_font = pygame.font.SysFont('Arial', 90, bold=True)
    subtitle_font = pygame.font.SysFont('Arial', 32)
    button_font = pygame.font.SysFont('Arial', 26)
    info_font = pygame.font.SysFont('Arial', 20)

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect, self.text = pygame.Rect(x, y, w, h), text
        self.color, self.hover_color = BUTTON_COLOR, HOVER_COLOR
    
    def draw(self):
        color = self.hover_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        text_surf = button_font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def is_clicked(self, pos, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(pos)

reset_button = Button(WIDTH//2 - 100, HEIGHT - 35, 200, 30, "Reset Game")
play_again_button = Button(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50, "Play Again")

def draw_lines():
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT-100), LINE_WIDTH)

def draw_figures():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 1:
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), CIRCLE_RADIUS, CIRCLE_WIDTH)

def check_win(player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)): 
            pygame.draw.line(screen, (255, 255, 255), (15, i * SQUARE_SIZE + SQUARE_SIZE // 2), (WIDTH - 15, i * SQUARE_SIZE + SQUARE_SIZE // 2), LINE_WIDTH)
            return True
        if all(board[j][i] == player for j in range(3)):
            pygame.draw.line(screen, (255, 255, 255), (i * SQUARE_SIZE + SQUARE_SIZE // 2, 15), (i * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 185), LINE_WIDTH)
            return True
    if all(board[i][i] == player for i in range(3)):
        pygame.draw.line(screen, (255, 255, 255), (15, 15), (WIDTH - 15, HEIGHT - 185), LINE_WIDTH)
        return True
    if all(board[i][2-i] == player for i in range(3)):
        pygame.draw.line(screen, (255, 255, 255), (15, HEIGHT - 185), (WIDTH - 15, 15), LINE_WIDTH)
        return True
    return False

def is_board_full():
    return not any(board[i][j] == 0 for i in range(3) for j in range(3))

def minimax(b, depth, maximizing):
    if check_win_minimax(2): return 1
    if check_win_minimax(1): return -1
    if is_board_full(): return 0
    scores = []
    for i in range(3):
        for j in range(3):
            if b[i][j] == 0:
                b[i][j] = 2 if maximizing else 1
                scores.append(minimax(b, depth + 1, not maximizing))
                b[i][j] = 0
    return max(scores) if maximizing else min(scores)

def check_win_minimax(p):
    for i in range(3):
        if all(board[i][j] == p for j in range(3)) or all(board[j][i] == p for j in range(3)): return True
    return all(board[i][i] == p for i in range(3)) or all(board[i][2-i] == p for i in range(3))

def best_move():
    best_score, move = -math.inf, (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = 2
                score = minimax(board, 0, False)
                board[i][j] = 0
                if score > best_score: best_score, move = score, (i, j)
    if move != (-1, -1): board[move[0]][move[1]] = 2
    return move != (-1, -1)

def draw_status(player_turn, game_over):
    pygame.draw.rect(screen, (210, 170, 220), pygame.Rect(0, HEIGHT-100, WIDTH, 100))
    if not game_over:
        text = "Your Turn (X)" if player_turn == 1 else "AI Thinking..."
        text_surf = font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT-55))
        screen.blit(text_surf, text_rect)
    info_surf = info_font.render("Algorithm: Minimax (Perfect AI)", True, (255, 255, 255))
    screen.blit(info_surf, (WIDTH//2 - info_surf.get_width()//2, HEIGHT-90))

def draw_end_screen(winner):
    bg, text, subtitle = (WIN_BG, "YOU WON!", "Congratulations! You beat the AI!") if winner == 1 else (LOSE_BG, "YOU LOST!", "The AI wins this round!") if winner == 2 else (DRAW_BG, "DRAW!", "It's a tie! Well played!")
    screen.fill(bg)
    title_surf = title_font.render(text, True, TEXT_COLOR)
    title_rect = title_surf.get_rect(center=(WIDTH//2, HEIGHT//3))
    screen.blit(title_surf, title_rect)
    subtitle_surf = subtitle_font.render(subtitle, True, TEXT_COLOR)
    subtitle_rect = subtitle_surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 30))
    screen.blit(subtitle_surf, subtitle_rect)
    play_again_button.draw()

def reset_game():
    global board, player, game_over, winner, show_end_screen
    board, player, game_over, winner, show_end_screen = np.zeros((3, 3)), 1, False, 0, False
    screen.fill(BG_COLOR)
    draw_lines()
    reset_button.draw()
    draw_status(player, game_over)
    pygame.display.update()

def main():
    global player, game_over, winner, show_end_screen
    player, game_over, winner, show_end_screen = 1, False, 0, False
    draw_lines()
    reset_button.draw()
    draw_status(player, game_over)
    pygame.display.update()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if show_end_screen:
                if play_again_button.is_clicked(mouse_pos, event): reset_game()
            else:
                if reset_button.is_clicked(mouse_pos, event): reset_game(); continue
                if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player == 1:
                    row, col = event.pos[1] // SQUARE_SIZE, event.pos[0] // SQUARE_SIZE
                    if row < 3 and col < 3 and board[row][col] == 0:
                        board[row][col] = player
                        draw_figures()
                        if check_win(player) or is_board_full():
                            game_over, winner = True, player if check_win(player) else 0
                            pygame.display.update()
                            pygame.time.wait(1000)
                            show_end_screen = True
                            draw_end_screen(winner)
                        else:
                            player = 2
                        draw_status(player, game_over)
                        pygame.display.update()
        
        if not game_over and player == 2 and not show_end_screen:
            pygame.time.wait(500)
            if best_move():
                draw_figures()
                if check_win(2) or is_board_full():
                    game_over, winner = True, 2 if check_win(2) else 0
                    pygame.display.update()
                    pygame.time.wait(1000)
                    show_end_screen = True
                    draw_end_screen(winner)
                else:
                    player = 1
                draw_status(player, game_over)
                pygame.display.update()
        
        (play_again_button if show_end_screen else reset_button).draw()
        pygame.display.update()

if __name__ == "__main__": main()