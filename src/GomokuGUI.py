# GomokuGUI.py

import pygame
import sys
import threading 
from Board import Board
from AIController import AIController

# --- CONFIGURATION ---
WIDTH = 600
HEADER_HEIGHT = 50 
HEIGHT = WIDTH + HEADER_HEIGHT 

BOARD_COLOR = (200, 170, 120)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)      
GREEN = (0, 150, 0)    

# --- COLORS ---
HEADER_COLOR = (50, 50, 50)   
POPUP_BG = (197, 154, 99)     
BTN_SHADOW = (40, 40, 40)     
COLOR_EASY = (60, 180, 75)    
COLOR_MED = (255, 215, 0)     
COLOR_HARD = (220, 60, 60)    

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gomoku - AI Project")

class GomokuGUI:
    def __init__(self):
        self.current_page = 'Start'
        self.text_en = '15' 
        self.active = False
        self.board = None
        self.ai = None
        self.selected_mode = None 
        self.cell_size = 0
        self.cols = 15
        self.game_over = False
        self.winner_text = ""
        self.winner_color = BLACK
        self.ai_thinking = False 

    def init_game(self):
        try:
            size = int(self.text_en)
        except ValueError:
            size = 15
        self.cols = size
        self.cell_size = WIDTH // (self.cols + 1)
        self.board = Board(size=size)
        self.ai = AIController(depth_limit=2) 
        self.game_over = False
        self.winner_text = ""
        self.ai_thinking = False 

    def draw_button_3d(self, rect, color, text_surf):
        shadow_rect = pygame.Rect(rect.x + 4, rect.y + 4, rect.width, rect.height)
        pygame.draw.rect(screen, BTN_SHADOW, shadow_rect, border_radius=8)
        pygame.draw.rect(screen, color, rect, border_radius=8)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    def draw_grid(self):
        screen.fill(BOARD_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, (0, 0, WIDTH, HEADER_HEIGHT))

        if self.ai_thinking:
            font = pygame.font.SysFont("Segoe UI", 24, bold=True) 
            text_surf = font.render("AI is Thinking...", True, WHITE)
            text_rect = text_surf.get_rect(center=(WIDTH // 2, HEADER_HEIGHT // 2))
            screen.blit(text_surf, text_rect)
        
        for i in range(self.cols):
            x_pos = self.cell_size + i * self.cell_size
            y_pos = HEADER_HEIGHT + self.cell_size + i * self.cell_size
            pygame.draw.line(screen, BLACK, (x_pos, HEADER_HEIGHT + self.cell_size), (x_pos, HEIGHT - self.cell_size), 2)
            pygame.draw.line(screen, BLACK, (self.cell_size, y_pos), (WIDTH - self.cell_size, y_pos), 2)
        
        if self.board:
            for r in range(self.board.size):
                for c in range(self.board.size):
                    piece = self.board.board[r][c]
                    if piece != ".":
                        color = BLACK if piece == "X" else WHITE
                        x = self.cell_size + c * self.cell_size 
                        y = HEADER_HEIGHT + self.cell_size + r * self.cell_size 
                        pygame.draw.circle(screen, color, (x, y), self.cell_size // 2.2)

        back_rect = pygame.Rect(10, 10, 80, 30)
        mouse_pos = pygame.mouse.get_pos()
        b_color = (255, 100, 100) if back_rect.collidepoint(mouse_pos) else (200, 50, 50)
        pygame.draw.rect(screen, b_color, back_rect, border_radius=5)
        font_small = pygame.font.SysFont("Arial", 18)
        text_surf = font_small.render("MENU", True, WHITE)
        text_rect = text_surf.get_rect(center=back_rect.center)
        screen.blit(text_surf, text_rect)

        if self.game_over:
            font = pygame.font.SysFont("Segoe UI", 30, bold=True) 
            dummy_txt = font.render(self.winner_text, True, BLACK)
            text_rect = dummy_txt.get_rect(center=(WIDTH//2, HEIGHT//2))
            bg_rect = text_rect.inflate(60, 40)
            pygame.draw.rect(screen, POPUP_BG, bg_rect, border_radius=20)
            main_surf = font.render(self.winner_text, True, self.winner_color)
            screen.blit(main_surf, text_rect)
            
        return back_rect

    def ai_play_thread(self):
        move, elapsed_time, nodes_count = self.ai.select_best_move(self.board, self.selected_mode)
        print("-" * 30)
        print(f"AI Search Finished ({self.selected_mode})")
        print(f"Time Taken: {elapsed_time:.3f} seconds") 
        print(f"Nodes Explored: {nodes_count}")
        print("-" * 30)

        if move:
            self.board.make_move(move[0], move[1])
            print(f"AI moved: {move}")
            
            # Logic Fix: Check Win FIRST, then Draw
            # Because a winning move on the last spot is a WIN, not a DRAW.
            if self.board.check_winner(move[0], move[1], "O"): # O is AI
                self.game_over = True
                self.winner_text = "YOU LOST :( "
                self.winner_color = RED
            elif self.board.is_full():
                self.game_over = True
                self.winner_text = "DRAW -_-"
                self.winner_color = BLACK
        else:
            self.game_over = True
            self.winner_text = "DRAW -_-"
            self.winner_color = BLACK
            
        self.ai_thinking = False

    def start_menu(self):
        screen.fill(BOARD_COLOR)
        font_large = pygame.font.SysFont("Arial", 32)
        mouse_pos = pygame.mouse.get_pos()
        
        start_rect = pygame.Rect(175, 450, 300, 60)
        start_bg = (0, 180, 0) if self.selected_mode else BOARD_COLOR
        text_color = WHITE if self.selected_mode else (100, 100, 100)
        start_surf = font_large.render("Click To Start", True, text_color)
        
        if self.selected_mode:
            self.draw_button_3d(start_rect, start_bg, start_surf)
        else:
            pygame.draw.rect(screen, (150, 140, 120), start_rect, border_radius=8)
            text_rect = start_surf.get_rect(center=start_rect.center)
            screen.blit(start_surf, text_rect)

        text = font_large.render("Level", True, WHITE)
        screen.blit(text, (20, 135))
        text = font_large.render("Board Size", True, WHITE)
        screen.blit(text, (20, 300))

        # Easy (Green)
        btn_easy = pygame.Rect(140, 125, 130, 60)
        color = COLOR_EASY
        if self.selected_mode == "Minimax_H1" or btn_easy.collidepoint(mouse_pos): color = WHITE
        txt_col = BLACK if color == WHITE else WHITE
        easy_surf = font_large.render("Easy", True, txt_col)
        self.draw_button_3d(btn_easy, color, easy_surf)

        # Medium (Yellow)
        btn_medium = pygame.Rect(290, 125, 130, 60)
        color = COLOR_MED
        if self.selected_mode == "AlphaBeta_H2" or btn_medium.collidepoint(mouse_pos): color = WHITE
        txt_col = BLACK 
        med_surf = font_large.render("Medium", True, txt_col)
        self.draw_button_3d(btn_medium, color, med_surf)

        # Hard (Red)
        btn_hard = pygame.Rect(440, 125, 130, 60)
        color = COLOR_HARD
        if self.selected_mode == "AlphaBeta_Combined" or btn_hard.collidepoint(mouse_pos): color = WHITE
        txt_col = BLACK if color == WHITE else WHITE
        hard_surf = font_large.render("Hard", True, txt_col)
        self.draw_button_3d(btn_hard, color, hard_surf)

        box = pygame.Rect(250, 295, 100, 45)
        color = WHITE if box.collidepoint(mouse_pos) or self.active else (70, 130, 180)
        pygame.draw.rect(screen, color, box, border_radius=5)
        pygame.draw.rect(screen, BLACK, box, 2, border_radius=5)
        txt_color = BLACK if color == WHITE else WHITE
        screen.blit(font_large.render(self.text_en, True, txt_color), (box.x+30, box.y+5))

        return {'start': start_rect, 'easy': btn_easy, 'medium': btn_medium, 'hard': btn_hard, 'box': box}

    def start_game(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

                if self.current_page == "Start":
                    buttons = self.start_menu()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if buttons['start'].collidepoint(event.pos):
                            if self.selected_mode: self.init_game(); self.current_page = "Game"
                        if buttons['easy'].collidepoint(event.pos): self.selected_mode = "Minimax_H1"
                        elif buttons['medium'].collidepoint(event.pos): self.selected_mode = "AlphaBeta_H2"
                        elif buttons['hard'].collidepoint(event.pos): self.selected_mode = "AlphaBeta_Combined"
                        if buttons['box'].collidepoint(event.pos): self.active = True
                        else: self.active = False
                    if event.type == pygame.KEYDOWN and self.active:
                        if event.key == pygame.K_BACKSPACE: self.text_en = self.text_en[:-1]
                        else:
                            if event.unicode.isdigit(): self.text_en += event.unicode

                elif self.current_page == "Game":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        back_btn = self.draw_grid() 
                        if back_btn.collidepoint(event.pos):
                            self.current_page = "Start"; self.board = None; self.selected_mode = None; self.ai_thinking = False; continue 

                        if not self.game_over and not self.ai_thinking:
                            if self.board.current_player == "X":
                                x_mouse, y_mouse = event.pos
                                if y_mouse < HEADER_HEIGHT: continue
                                c = round((x_mouse - self.cell_size) / self.cell_size)
                                r = round((y_mouse - HEADER_HEIGHT - self.cell_size) / self.cell_size)

                                if 0 <= r < self.board.size and 0 <= c < self.board.size:
                                    if self.board.make_move(r, c):
                                        print(f"Human moved: {r}, {c}")
                                        # Win/Draw check for Human
                                        if self.board.check_winner(r, c, "X"):
                                            self.game_over = True
                                            self.winner_text = "YOU WON :)"
                                            self.winner_color = GREEN
                                        elif self.board.is_full():
                                            self.game_over = True
                                            self.winner_text = "DRAW -_-"
                                            self.winner_color = BLACK
                                            
                                        if not self.game_over:
                                            self.ai_thinking = True 
                                            ai_thread = threading.Thread(target=self.ai_play_thread)
                                            ai_thread.start()
            if self.current_page == "Game": self.draw_grid()
            elif self.current_page == "Start": self.start_menu() 
            pygame.display.update(); clock.tick(30)
