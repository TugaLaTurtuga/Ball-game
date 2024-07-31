import pygame as pg
import os
import random
import colorsys
import save_time

pg.init()

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Initialize Pygame
clock = pg.time.Clock()

# Colors
SCREEN_FILL = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
BLUE = (95, 150, 255)
BLUE_ISH = (95 + 30, 150 + 30, 255)
GREY = (200, 200, 200, 128)

save_rows_and_cols = 'saves/Ball_game_settings/rows_and_cols.txt'
save_margin_padding_and_line_thickness = 'saves/Ball_game_settings/margin_padding_and_line_thickness.txt'
save_col_row_size = 'saves/Ball_game_settings/col_row_size.txt'
margin_padding_and_line_thickness = [10, 5, 5]
margin = margin_padding_and_line_thickness[0]
padding = margin_padding_and_line_thickness[1]
line_thickness = margin_padding_and_line_thickness[2]
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
    if os.path.exists(save_margin_padding_and_line_thickness):
        with open(save_margin_padding_and_line_thickness, 'r') as file:
            content = file.read()
            try:
                margin_padding_and_line_thickness = list(map(int, content.strip().split(',')))
            except ValueError:
                margin_padding_and_line_thickness = [10, 5, 5]
    if os.path.exists(save_col_row_size):
        with open(save_col_row_size, 'r') as file:
            content = file.read()
            try:
                col_row_size = list(map(int, content.strip().split(',')))
            except ValueError:
                col_row_size = [100, 100]

load_settings()

# Screen dimensions #
SCREEN_WIDTH = (
        (margin * 2) +
        (row_and_cols[0] * (col_row_size[0] + 1)) +
        (padding * row_and_cols[0])
)
SCREEN_HEIGHT = (
        (margin * 2) +
        ((row_and_cols[1] + 1) * col_row_size[1]) +
        (padding * (row_and_cols[1] + 1))
)

# Font and Font Size
FONT = pg.font.Font(None, SCREEN_WIDTH // 10)
RESTART_FONT = pg.font.Font(None, 32)

# Create virtual board #
# 0 means nothing the rest means balls class #
Virtual_board = []
current_number = 0
Ball_colors = [None]
rows, cols = row_and_cols

def calculate_time(time):
    if time is not None:
        hours, remainder = divmod(time, 3600)
        minutes, remainder = divmod(remainder, 60)
        seconds = int(remainder)
        hundreds = int((remainder - seconds) * 100)  # Extracting hundredths of a second

        # Format the time as a string with proper handling of fractional seconds
        if hours > 0:
            formatted_time = '{:01.0f}:{:02.0f}:{:02.0f}.{:02.0f}'.format(hours, minutes, seconds, hundreds)
        elif minutes > 0:
            formatted_time = '{:02.0f}:{:02.0f}.{:02.0f}'.format(minutes, seconds, hundreds)
        else:
            formatted_time = '{:02.0f}.{:02.0f}'.format(seconds, hundreds)
        return formatted_time
    else:
        return 'no time has been set'

# Create the screen #
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption(f"Ball game; high score: {calculate_time(save_time.get_high_score(row_and_cols))}")
pg.display.set_icon(pg.image.load('saves/icons/icon.png'))

# Draw the lines #
button_rect = []
def Draw_lines(screen):
    global button_rect
    button_rect = []

    # Initial positions for the lines
    start_pos = [margin + padding, margin + col_row_size[0] + padding * row_and_cols[1]]
    end_pos = [margin + padding, SCREEN_HEIGHT - margin]

    # Draw the initial line
    pg.draw.line(screen, LINE_COLOR, start_pos, end_pos, line_thickness)

    for _ in range(row_and_cols[0]):
        # Calculate the position for the next line
        next_line_x = start_pos[0] + padding + col_row_size[0]

        # Calculate button dimensions
        button_x = start_pos[0] + line_thickness
        button_width = next_line_x - start_pos[0] - line_thickness
        button_y = start_pos[1]
        button_height = end_pos[1] - start_pos[1]
        button_rect.append(pg.Rect(button_x, button_y, button_width, button_height))

        # Draw the next line
        pg.draw.line(screen, LINE_COLOR, (next_line_x, start_pos[1]), (next_line_x, end_pos[1]), line_thickness)

        # Update start_pos and end_pos for the next line
        start_pos[0] = next_line_x
        end_pos[0] = next_line_x

show_numbers = True

def Draw_balls(screen, mouse_x):
    plus_x = line_thickness + col_row_size[0]
    plus_y = col_row_size[0]
    pos = (margin + padding + line_thickness + col_row_size[0] / 2, SCREEN_HEIGHT - margin - col_row_size[0] / 2)
    for col in range(len(Virtual_board)):
        s_pos = pos
        for row in range(len(Virtual_board[col])):
            number = Virtual_board[col][row]
            if number != 0:
                pg.draw.circle(screen, Ball_colors[number], s_pos, col_row_size[0] / 2 - padding)
                s_pos = (s_pos[0], s_pos[1] - plus_y)
            else:
                break
        pos = (pos[0] + plus_x, pos[1])
    # Show selected ball
    if current_number != 0:
        s_pos = (mouse_x, col_row_size[0])
        pg.draw.circle(screen, Ball_colors[current_number], s_pos, col_row_size[0] / 2 - padding)

def Draw_restart_button(screen, mouse):
    button_width = 200
    button_height = 50

    text_color = SCREEN_FILL
    button_x = (SCREEN_WIDTH - button_width) // 2
    button_y = (SCREEN_HEIGHT - button_height) // 2
    restart_rect = pg.Rect(button_x, button_y, button_width, button_height)
    if restart_rect.collidepoint(mouse):
        button_color = BLUE_ISH
    else:
        button_color = BLUE
    # Draw button
    pg.draw.rect(screen, button_color, restart_rect)
    text = RESTART_FONT.render('Restart Game', True, text_color)
    text_rect = text.get_rect(center=restart_rect.center)
    screen.blit(text, text_rect)

    return restart_rect

time = 0
def start_game():
    global Virtual_board, current_number, Ball_colors, Finished, time
    rows, cols = row_and_cols
    Virtual_board = []
    Ball_colors = [None]
    # Initialize the count of each number
    total_cells = rows * cols
    max_number = rows - 1  # This determines the highest number to be used
    max_occurrences = row_and_cols[1]

    # Generate the list of numbers to fill the board
    numbers = []
    for num in range(1, max_number + 1):
        numbers.extend([num] * max_occurrences)

    # Randomize the order of the numbers list
    random.shuffle(numbers)

    # Ensure the numbers list is long enough to fill all rows except the last one
    needed_numbers = (rows - 1) * cols
    if len(numbers) < needed_numbers:
        additional_numbers_needed = needed_numbers - len(numbers)
        numbers.extend([max_number] * additional_numbers_needed)
    numbers = numbers[:needed_numbers]

    # Fill the Virtual_board
    for row in range(rows):
        if row == rows - 1:
            # Last row should be all zeros
            new_row = [0] * cols
        else:
            # Populate the row with numbers
            new_row = numbers[:cols]
            numbers = numbers[cols:]
            random.shuffle(new_row)  # Randomize the order of numbers in the row

        Virtual_board.append(new_row)
        # Generate colors evenly distributed in the HSV color space
        hue = row / row_and_cols[1]  # Hue range [0, 1)
        saturation = 0.6 + random.random() * 0.4  # Saturation range [0.6, 1)
        value = 0.6 + random.random() * 0.4  # Value range [0.6, 1)

        # Convert HSV to RGB
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        rgb = tuple(int(c * 255) for c in rgb)  # Convert to 0-255 range
        if rgb == SCREEN_FILL:  # Change if the background color is the same as rgb
            rgb = (rgb[0] - 10, rgb[1] - 20, rgb[2] - 30)
        Ball_colors.append(rgb)
    time = 0
    Finished = False

# Main loop
FPS = 60
start_game()
Won = False
Finished = False
running = True
while running:
    screen.fill(SCREEN_FILL)
    Draw_lines(screen)
    dt = clock.tick(FPS)

    mouse_x, mouse_y = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not Finished:
                    for btn_number in range(len(button_rect)):
                        rect = button_rect[btn_number]
                        if pg.Rect(rect).collidepoint(mouse_x, mouse_y):
                            print(f'Clicked btn: {btn_number}')
                            if current_number == 0:
                                for balls in range(len(Virtual_board[btn_number]) - 1, -1, -1):
                                    number = Virtual_board[btn_number][balls]
                                    if number != 0:
                                        Virtual_board[btn_number][balls] = 0
                                        current_number = number
                                        print(Virtual_board)
                                        break
                            else:
                                for balls in range(len(Virtual_board[btn_number])):
                                    number = Virtual_board[btn_number][balls]
                                    if number == 0:
                                        Virtual_board[btn_number][balls] = current_number
                                        current_number = 0
                                        print(Virtual_board)
                                        break
                                if current_number == 0:
                                    # Check if player won the game
                                    Won = False
                                    # Check rows for a winning condition
                                    for row in Virtual_board:
                                        if all(value == row[0] for value in row):
                                            Won = True
                                        else:
                                            Won = False
                                            break

                                    # Print result based on winning condition
                                    if Won:
                                        print('Game over')
                                        Finished = True
                                        # save data
                                        save_time.Finish_game(Finished, time, row_and_cols)
                                        pg.display.set_caption(
                                            f"Ball game; high score: {calculate_time(save_time.get_high_score(row_and_cols))}")
                            break
                else:
                    if restart_button and restart_button.collidepoint(mouse_x, mouse_y):
                        start_game()
            # else: # DEBUG
            #    print('THIS IS FOR DEBUGING REMOVE, AFTER')
            #    Virtual_board = [[1, 1, 1, 1], [2, 2, 2, 2], [0, 0, 0, 0]]

    text = FONT.render('Time: ' + calculate_time(time), True, BLUE)
    screen.blit(text, (10, 10))
    Draw_balls(screen, mouse_x)

    # Render the current rows and columns
    text = FONT.render(f"Rows: {row_and_cols[0]}, Cols: {row_and_cols[1]}", True, BLUE)
    text_rect = text.get_rect()
    text_rect.topright = SCREEN_WIDTH - 10, 10
    screen.blit(text, text_rect)

    if not Finished:
        time += dt / 1000
    else:
        # pg.draw.rect(screen, GREY, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 1000)
        restart_button = Draw_restart_button(screen, (mouse_x, mouse_y))

        text = FONT.render(f"High score: {calculate_time(save_time.get_high_score(row_and_cols))}", True, BLUE)
        text_rect = text.get_rect()
        text_rect.bottom = (SCREEN_HEIGHT / 2) - 25 - padding
        text_rect.centerx = SCREEN_WIDTH / 2
        screen.blit(text, text_rect)

        text = FONT.render(f"Time: {calculate_time(time)}", True, BLUE)
        text_rect = text.get_rect()
        text_rect.top = (SCREEN_HEIGHT / 2) + 25 + padding
        text_rect.centerx = SCREEN_WIDTH / 2
        screen.blit(text, text_rect)

    pg.display.flip()

# On Exit
pg.quit()
