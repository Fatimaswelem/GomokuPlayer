import pygame
import sys

pygame.init()
current_page='Start'
#input entry
text_en = ''

active = False

WIDTH, HEIGHT = 600, 600
# -----

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gomoku Grid")


BLACK = (0, 0, 0)
BOARD_COLOR = (200, 170, 120)
WHITE=(255, 255, 255)
num_text = int(text_en) if text_en != '' else 15
ROWS = COLS = num_text + 1
CELL_SIZE = WIDTH // COLS
def draw_grid():
    screen.fill(BOARD_COLOR)
    num_text = int(text_en) if text_en != '' else 15
    ROWS = COLS = num_text + 1
    global CELL_SIZE
    CELL_SIZE = WIDTH // COLS
    for row in range(ROWS):
        y = CELL_SIZE // 2 + row * CELL_SIZE
        pygame.draw.line(screen, BLACK,
                         (CELL_SIZE // 2, y),
                         (WIDTH - CELL_SIZE // 2, y),
                         2)


    for col in range(COLS):
        x = CELL_SIZE // 2 + col * CELL_SIZE
        pygame.draw.line(screen, BLACK,
                         (x, CELL_SIZE // 2),
                         (x, HEIGHT - CELL_SIZE // 2),
                         2)



def Start_Menue():
    screen.fill(BOARD_COLOR)


    #-------START BUTTON-------
    button_rect = pygame.Rect(175,450, 300, 60)
    pygame.draw.rect(screen, BOARD_COLOR, button_rect)
    font = pygame.font.SysFont("Arial", 32)
    text = font.render("Click To Start", True, (255, 255, 255))
    screen.blit(text, (button_rect.x + 50, button_rect.y + 10))
    #-------LEVEL CHOICE-------
    font = pygame.font.SysFont("Arial", 32)
    text = font.render("Level", True, (255, 255, 255))
    screen.blit(text, (20,135))
    #-------EASY BUTTON-------
    button_Easy = pygame.Rect(140,125, 130, 60)
    mouse_over = button_Easy.collidepoint(pygame.mouse.get_pos())
    color = WHITE if mouse_over else (70, 130, 180)
    pygame.draw.rect(screen, color, button_Easy)
    font = pygame.font.SysFont("Arial", 32)
    text = font.render("Easy", True, BLACK)
    screen.blit(text, (button_Easy.x +25, button_Easy.y + 10))
    #-------MEDIUM BUTTON-------
    button_Medium = pygame.Rect(290,125, 130, 60)
    mouse_over = button_Medium.collidepoint(pygame.mouse.get_pos())
    color = WHITE if mouse_over else (70, 130, 180)
    pygame.draw.rect(screen, color, button_Medium)
    font = pygame.font.SysFont("Arial", 32)
    text = font.render("Medium", True, BLACK)
    screen.blit(text, (button_Medium.x + 25, button_Medium.y + 10))
    #-------HARD BUTTON-------
    button_Hard = pygame.Rect(440,125, 130, 60)
    mouse_over = button_Hard.collidepoint(pygame.mouse.get_pos())
    color = WHITE if mouse_over else (70, 130, 180)
    pygame.draw.rect(screen, color, button_Hard)
    font = pygame.font.SysFont("Arial", 32)
    text = font.render("Hard", True, BLACK)
    screen.blit(text, (button_Hard.x +25, button_Hard.y + 10))

    #-------BOARD SIZE-------
    font = pygame.font.SysFont("Arial", 32)
    text = font.render("Board Size", True, (255, 255, 255))
    screen.blit(text, (20,300))


    #------ُENTRY--------
    box = pygame.Rect(175, 300, 300, 40)
    mouse_over = box.collidepoint(pygame.mouse.get_pos())

    color = WHITE if mouse_over else (70, 130, 180)
    pygame.draw.rect(screen, color, box, 2)
    screen.blit(font.render(text_en, True, (255,255,255)), (box.x+5, box.y+5))


    return {'button_rect':button_rect,'box':box}
def draw_piece(row, col, color):

    x = CELL_SIZE//2 + col * CELL_SIZE
    y = CELL_SIZE//2 + row * CELL_SIZE
    pygame.draw.circle(screen, color, (x, y), CELL_SIZE//3)
def get_cell_from_pos(x_p,y_p):
    col = round((x_p- CELL_SIZE // 2) / CELL_SIZE)
    row = round((y_p - CELL_SIZE // 2) / CELL_SIZE)
    draw_piece(row, col, WHITE)
    if 0 <= col < COLS and 0 <= row < ROWS:
        return row, col
    else:
        return None, None

button =Start_Menue()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if current_page == "Start":
            button =Start_Menue()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button['button_rect'].collidepoint(event.pos):
                    current_page = "Game"
                    draw_grid()
        if event.type == pygame.MOUSEBUTTONDOWN:
            active = button['box'].collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and active:
            if event.key == pygame.K_BACKSPACE:
                text_en = text_en[:-1]
            else: text_en += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            get_cell_from_pos(x,y)



    pygame.display.update()
