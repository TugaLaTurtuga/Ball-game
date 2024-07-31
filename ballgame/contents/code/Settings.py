import pygame as pg
import os
from subprocess import Popen

pg.init()

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Initialize Pygame
clock = pg.time.Clock()

# Colors
BLUE_ISH = (95 + 30, 150 + 30, 255)
BLUE = (95, 150, 255)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
MORE_GREY = (200, 200, 200)
RED = (200, 100, 100)

# Font and Font Size
FONT = pg.font.Font(None, 24)

save_rows_and_cols = 'saves/Ball_game_settings/rows_and_cols.txt'
save_margin_padding_and_line_thickness = 'saves/Ball_game_settings/margin_padding_and_line_thickness.txt'
save_col_row_size = 'saves/Ball_game_settings/col_row_size.txt'
margin_padding_and_line_thickness = [10, 5, 5]
row_and_cols = [5, 7]
col_row_size = [100, 100]

def load_settings():
    global row_and_cols, col_row_size, margin_padding_and_line_thickness
    if os.path.exists(save_rows_and_cols):
        with open(save_rows_and_cols, 'r') as file:
            content = file.read()
            try:
                row_and_cols = list(map(int, content.strip().split(',')))
            except ValueError:
                row_and_cols = [5, 7]  # Default values if there's an error
        with open(save_margin_padding_and_line_thickness, 'r') as file:
            content = file.read()
            try:
                margin_padding_and_line_thickness = list(map(int, content.strip().split(',')))
            except ValueError:
                margin_padding_and_line_thickness = [10, 5, 5]
        with open(save_col_row_size, 'r') as file:
            content = file.read()
            try:
                col_row_size = list(map(int, content.strip().split(',')))
            except ValueError:
                col_row_size = [100, 100]
    else:
        save_settings()

def save_settings():
    with open(save_rows_and_cols, 'w') as file:
        file.write(','.join(map(str, row_and_cols)))
    with open(save_margin_padding_and_line_thickness, 'w') as file:
        file.write(','.join(map(str, margin_padding_and_line_thickness)))
    with open(save_col_row_size, 'w') as file:
        file.write(','.join(map(str, col_row_size)))

load_settings()

def add_col_or_row(col_or_Row_T_F, add_or_remove_T_F):
    global row_and_cols
    if col_or_Row_T_F:
        if add_or_remove_T_F:
            row_and_cols[0] += 1
        else:
            row_and_cols[0] = max(3, row_and_cols[0] - 1)  # Prevent negative values
    else:
        if add_or_remove_T_F:
            row_and_cols[1] += 1
        else:
            row_and_cols[1] = max(3, row_and_cols[1] - 1)  # Prevent negative values
    save_settings()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 310, 310 - 50
# Create the screen
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Ball game settings")

path = 'saves/Ball_game_settings'
def open_file_explorer_or_finder():
    if os.name == 'nt':  # For Windows
        try:
            Popen(f'explorer {path}')
        except Exception as e:
            print(f"Error opening file explorer: {e}")
    elif os.name == 'posix':  # For macOS or Linux
        if 'darwin' in os.uname().sysname.lower():  # macOS
            try:
                Popen(['open', path])
            except Exception as e:
                print(f"Error opening Finder: {e}")
        else:  # Linux
            try:
                Popen(['xdg-open', path])
            except Exception as e:
                print(f"Error opening file manager: {e}")

# Main loop
FPS = 60
key_down = False
s_key_down = 0
running = True
while running:
    done = False
    dt = clock.tick(FPS)
    screen.fill(WHITE)

    mouse_pos = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            key_down = True
            s_key_down = 0
            if event.key == pg.K_UP:
                add_col_or_row(False, True)
            elif event.key == pg.K_DOWN:
                add_col_or_row(False, False)
            elif event.key == pg.K_LEFT:
                add_col_or_row(True, False)
            elif event.key == pg.K_RIGHT:
                add_col_or_row(True, True)
            elif event.key == pg.K_RETURN or event.key == pg.K_f:
                open_file_explorer_or_finder()
            elif event.key == pg.K_s:
                s_key_down = 1
            elif event.key == pg.K_l:
                s_key_down = 2

        elif event.type == pg.KEYUP:
            key_down = False
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect.collidepoint(mouse_pos):
                open_file_explorer_or_finder()

        if key_down and not done:
            done = True
            if s_key_down == 1:
                if col_row_size[0] - 2 > 5:
                    col_row_size[0] -= 2
                    col_row_size[1] = col_row_size[0]
            elif s_key_down == 2:
                col_row_size[0] += 2
                col_row_size[1] = col_row_size[0]
            save_settings()

    # Render the current rows and columns
    text = FONT.render(f"Width: {row_and_cols[0]} Height: {row_and_cols[1]}", True, BLUE)
    text_rect = text.get_rect()
    text_rect.midleft = 10, 10
    screen.blit(text, text_rect)

    # Render the current size
    text = FONT.render(f"Ball size: {col_row_size[0]}", True, BLUE)
    text_rect = text.get_rect()
    text_rect.midright = SCREEN_WIDTH - 10, 10
    screen.blit(text, text_rect)

    # Render the current margin_padding_and_line_thickness
    text = FONT.render(f"Margin: {margin_padding_and_line_thickness[0]}"
                       f" Padding: {margin_padding_and_line_thickness[1]}"
                       f" Line thickness: {margin_padding_and_line_thickness[2]}", True, BLUE)
    text_rect = text.get_rect()
    text_rect.bottom = SCREEN_HEIGHT
    text_rect.centerx = SCREEN_WIDTH - SCREEN_WIDTH / 2
    screen.blit(text, text_rect)

    # Render the start button
    button_text = FONT.render("Open folder", True, WHITE)
    button_rect = button_text.get_rect()
    button_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Determine button color based on hover state
    button_color = BLUE_ISH if button_rect.collidepoint(mouse_pos) else BLUE

    # Draw the button with the determined color
    pg.draw.rect(screen, button_color, button_rect.inflate(20, 10))  # Button background
    screen.blit(button_text, button_rect)

    pg.display.flip()
