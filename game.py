import pygame
import random
import os
import time

# Initialize game
pygame.init()

# Set up the Screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Catch The Fruits")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game variables
basket_width = 100
basket_height = 50
basket_x = screen_width // 2 - basket_width // 2
basket_y = screen_height - basket_height - 20
basket_speed = 10

fruit_width = 50
fruit_height = 50
fruit_speed = 5  # Default fruit speed (Normal Mode)

# Load the background image
background_image = pygame.image.load("Background.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Load the basket image
basket_image = pygame.image.load("Assets/basket.png")
basket_image = pygame.transform.scale(basket_image, (basket_width, basket_height))

# Load the splatter image
splatter_image = pygame.image.load("Splatter.png")
splatter_image = pygame.transform.scale(splatter_image, (fruit_width, fruit_height))

# Load the fruits
fruit_files = [
    "watermelon.png",
    "strawberry.png",
    "lemon.png",
    "grapes.png",
    "cherries.png",
    "bananas.png",
    "apple.png"
]
fruit_images = []
for file in fruit_files:
    path = os.path.join("Assets", file)
    img = pygame.image.load(path)
    img = pygame.transform.scale(img, (fruit_width, fruit_height))
    fruit_images.append(img)

fruit_points = {
    "watermelon.png": 5,
    "strawberry.png": 3,
    "lemon.png": 2,
    "grapes.png": 4,
    "cherries.png": 1,
    "bananas.png": 3,
    "apple.png": 6
}

score = 0
high_score = 0

clock = pygame.time.Clock()

def draw_basket(x, y):
    screen.blit(basket_image, (x, y))

def display_fruit_points(x, y, fruit_img):
    points = fruit_points[fruit_files[fruit_images.index(fruit_img)]]
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"+{points}", True, BLACK)
    text_x = min(x + fruit_width + 5, screen_width - text.get_width() - 5)
    if x > screen_width - fruit_width - 30:
        text_x = x - text.get_width() - 5
    screen.blit(text, (text_x, y))
    
def display_score(score):
    label_font = pygame.font.Font("PressStart2P-Regular.ttf", 16)
    score_font = pygame.font.Font("PressStart2P-Regular.ttf", 16)
    label = label_font.render("Score:", True, BLACK)
    number = score_font.render(str(score), True, BLACK)
    screen.blit(label, (10, 100))
    screen.blit(number, (120, 100))

def display_high_score(high_score):
    label_font = pygame.font.Font("PressStart2P-Regular.ttf", 16)
    score_font = pygame.font.Font("PressStart2P-Regular.ttf", 16)
    label = label_font.render("Highest Score:", True, BLACK)
    number = score_font.render(str(high_score), True, BLACK)
    label_width = label.get_width()
    screen.blit(label, (10, 150))
    screen.blit(number, (10 + label_width + 20, 150))

def draw_start_button():
    # Draws the "Start Game" button (used only in the original main menu)
    button_width = 200
    button_height = 50
    spacing = 20
    total_width = button_width * 3 + spacing * 2
    start_x = screen_width // 2 - total_width // 2
    button_y = screen_height // 2 - button_height // 2
    pygame.draw.rect(screen, (0, 200, 0), [start_x, button_y, button_width, button_height])
    font = pygame.font.Font("PressStart2P-Regular.ttf", 20)
    text = font.render("Start Game", True, BLACK)
    text_rect = text.get_rect(center=(start_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)
    return pygame.Rect(start_x, button_y, button_width, button_height)

def draw_help_button():
    # Draws the "Help" button (used only in the original main menu)
    button_width = 200
    button_height = 50
    spacing = 20
    total_width = button_width * 3 + spacing * 2
    group_start_x = screen_width // 2 - total_width // 2
    button_x = group_start_x + button_width + spacing
    button_y = screen_height // 2 - button_height // 2
    pygame.draw.rect(screen, (0, 100, 255), [button_x, button_y, button_width, button_height])
    font = pygame.font.Font("PressStart2P-Regular.ttf", 20)
    text = font.render("Help", True, BLACK)
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)
    return pygame.Rect(button_x, button_y, button_width, button_height)

def help_screen():
    help_waiting = True
    help_text = [
        "Help Page:",
        "",
        "Use the arrow keys LEFT and RIGHT to move the basket.",
        "",
        "Collect as many items as you can.",
        "",
        "Click anywhere or press ESC to return."
    ]
    font = pygame.font.Font("PressStart2P-Regular.ttf", 13)
    start_y = 100
    line_spacing = 50
    while help_waiting:
        screen.fill(WHITE)
        for i, line in enumerate(help_text):
            text_surface = font.render(line, True, BLACK)
            text_rect = text_surface.get_rect(center=(screen_width // 2, start_y + i * line_spacing))
            screen.blit(text_surface, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                help_waiting = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                help_waiting = False
        pygame.display.update()
        clock.tick(60)

def draw_exit_button():
    # Draws the "Exit Game" button (used only in the original main menu)
    button_width = 200
    button_height = 50
    spacing = 20
    total_width = button_width * 3 + spacing * 2
    group_start_x = screen_width // 2 - total_width // 2
    button_y = screen_height // 2 - button_height // 2
    button_x = group_start_x + (button_width + spacing) * 2
    pygame.draw.rect(screen, (200, 0, 0), [button_x, button_y, button_width, button_height])
    font = pygame.font.Font("PressStart2P-Regular.ttf", 20)
    text = font.render("Exit Game", True, BLACK)
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)
    return pygame.Rect(button_x, button_y, button_width, button_height)

def draw_restart_button():
    button_width = 250
    button_height = 50
    button_x = screen_width // 2 - button_width // 2
    button_y = screen_height // 2 + 75  
    pygame.draw.rect(screen, (255, 165, 0), [button_x, button_y, button_width, button_height])
    font = pygame.font.Font("PressStart2P-Regular.ttf", 20)
    text = font.render("Restart Game", True, WHITE)
    text_rect = text.get_rect(center=(screen_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)
    return pygame.Rect(button_x, button_y, button_width, button_height)

paused = False

def draw_pause_button():
    button_width = 100
    button_height = 50
    button_x = screen_width - button_width - 10
    button_y = 10
    pause_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, RED, pause_rect)
    font = pygame.font.Font(None, 30)
    text_str = "Resume" if paused else "Pause"
    text = font.render(text_str, True, BLACK)
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)
    return pause_rect

def toggle_pause():
    global paused
    paused = not paused

def return_to_menu_button():
    button_width = 250
    button_height = 50
    spacing = 20
    total_width = button_width * 3 + spacing * 2
    group_start_x = screen_width // 2 - total_width // 2
    button_x = group_start_x + button_width + spacing
    button_y = screen_height // 2 - button_height // 2  
    pygame.draw.rect(screen, (255, 165, 0), [button_x, button_y, button_width, button_height])
    font = pygame.font.Font("PressStart2P-Regular.ttf", 18)
    text = font.render("Return To Menu", True, WHITE)
    text_rect = text.get_rect(center=(screen_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)
    return pygame.Rect(button_x, button_y, button_width, button_height)

def game_over():
    global high_score
    font = pygame.font.Font("PressStart2P-Regular.ttf", 30)
    text = font.render("Game over", True, BLACK)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - 100))
    restart_button_rect = draw_restart_button()
    menu_button_rect = return_to_menu_button()
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    waiting = False
                    global score, basket_x
                    score = 0
                    basket_x = screen_width // 2 - basket_width // 2
                    game_loop()
                if menu_button_rect.collidepoint(event.pos):
                    main()
        clock.tick(60)

def game_loop():
    global score, basket_x, high_score
    fruit_x = random.randint(0, screen_width - fruit_width)
    fruit_y = -fruit_height
    fruit_img = random.choice(fruit_images)
    splatter_positions = []
    missed_fruits = 0
    running = True
    while running:
        screen.blit(background_image, (0, 0))
        pause_button_rect = draw_pause_button()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button_rect.collidepoint(event.pos):
                    toggle_pause()
        if not paused:            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                basket_x -= basket_speed
            if keys[pygame.K_RIGHT]:
                basket_x += basket_speed
            if basket_x < 0:
                basket_x = 0
            elif basket_x > screen_width - basket_width:
                basket_x = screen_width - basket_width
            fruit_y += fruit_speed
        if fruit_y + fruit_height > basket_y and basket_x < fruit_x + fruit_width < basket_x + basket_width:
            score += fruit_points[fruit_files[fruit_images.index(fruit_img)]]
            if score > high_score:
                high_score = score
            fruit_x = random.randint(0, screen_width - fruit_width)
            fruit_y = -fruit_height
            fruit_img = random.choice(fruit_images)
        if fruit_y > screen_height:
            splatter_positions.append((fruit_x, screen_height - fruit_height, time.time()))
            fruit_x = random.randint(0, screen_width - fruit_width)
            fruit_y = -fruit_height
            fruit_img = random.choice(fruit_images)
            missed_fruits += 1
        draw_basket(basket_x, basket_y)
        screen.blit(fruit_img, (fruit_x, fruit_y))
        display_fruit_points(fruit_x, fruit_y, fruit_img)
        display_score(score)
        display_high_score(high_score)
        current_time = time.time()
        splatter_positions = [(x, y, t) for (x, y, t) in splatter_positions if current_time - t < 0.5]
        for x, y, _ in splatter_positions:
            screen.blit(splatter_image, (x, y))
        if missed_fruits >= 3:
            game_over()
            running = False
        pygame.display.update()
        clock.tick(60)

# -New functions for main menu with Game mode buttonn and mode selection submenu 

def draw_main_menu_buttons():
    """
    Draws four buttons on the main menu:
    "Start Game", "Game Mode", "Help", and "Exit Game"
    arranged in a 2x2 grid.
    """
    button_width = 200
    button_height = 50
    spacing_x = 20
    spacing_y = 20
    total_width = button_width * 2 + spacing_x
    total_height = button_height * 2 + spacing_y
    start_x = screen_width // 2 - total_width // 2
    start_y = screen_height // 2 - total_height // 2

    start_game_rect = pygame.Rect(start_x, start_y, button_width, button_height)
    game_mode_rect = pygame.Rect(start_x + button_width + spacing_x, start_y, button_width, button_height)
    help_rect = pygame.Rect(start_x, start_y + button_height + spacing_y, button_width, button_height)
    exit_rect = pygame.Rect(start_x + button_width + spacing_x, start_y + button_height + spacing_y, button_width, button_height)

    pygame.draw.rect(screen, (0, 200, 0), start_game_rect)      # Green: Start Game
    pygame.draw.rect(screen, (200, 200, 0), game_mode_rect)       # Yellow: Game Mode
    pygame.draw.rect(screen, (0, 100, 255), help_rect)            # Blue: Help
    pygame.draw.rect(screen, (200, 0, 0), exit_rect)              # Red: Exit Game

    font = pygame.font.Font("PressStart2P-Regular.ttf", 20)
    start_text = font.render("Start Game", True, BLACK)
    mode_text = font.render("Game Mode", True, BLACK)
    help_text = font.render("Help", True, BLACK)
    exit_text = font.render("Exit Game", True, BLACK)

    screen.blit(start_text, start_text.get_rect(center=start_game_rect.center))
    screen.blit(mode_text, mode_text.get_rect(center=game_mode_rect.center))
    screen.blit(help_text, help_text.get_rect(center=help_rect.center))
    screen.blit(exit_text, exit_text.get_rect(center=exit_rect.center))

    return start_game_rect, game_mode_rect, help_rect, exit_rect

def mode_menu():
    """
    Mode selection submenu.
    Allows the player to choose between:
      - Normal Mode (fruit_speed = 5)
      - Hard Mode (fruit_speed = 10)
    """
    waiting = True
    while waiting:
        screen.blit(background_image, (0, 0))
        font = pygame.font.Font("PressStart2P-Regular.ttf", 20)
        title_text = font.render("Select Game Mode", True, BLACK)
        title_rect = title_text.get_rect(center=(screen_width//2, screen_height//2 - 100))
        screen.blit(title_text, title_rect)

        button_width = 200
        button_height = 50
        spacing = 20
        total_width = button_width * 2 + spacing
        start_x = screen_width // 2 - total_width // 2
        button_y = screen_height // 2 + 50

        normal_rect = pygame.Rect(start_x, button_y, button_width, button_height)
        hard_rect = pygame.Rect(start_x + button_width + spacing, button_y, button_width, button_height)

        pygame.draw.rect(screen, (0, 200, 0), normal_rect)  # Green for Normal Mode
        pygame.draw.rect(screen, (200, 0, 0), hard_rect)     # Red for Hard Mode

        normal_text = font.render("Normal Mode", True, BLACK)
        hard_text = font.render("Hard Mode", True, BLACK)
        screen.blit(normal_text, normal_text.get_rect(center=normal_rect.center))
        screen.blit(hard_text, hard_text.get_rect(center=hard_rect.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if normal_rect.collidepoint(pos):
                    global fruit_speed
                    fruit_speed = 5
                    waiting = False
                    game_loop()
                elif hard_rect.collidepoint(pos):
                    fruit_speed = 10
                    waiting = False
                    game_loop()
        pygame.display.update()
        clock.tick(60)

def main():
    """
    Main menu with four buttons:
    "Start Game", "Game Mode", "Help", and "Exit Game".
    """
    waiting = True
    while waiting:
        screen.blit(background_image, (0, 0))
        font = pygame.font.Font("PressStart2P-Regular.ttf", 20)
        title_text = font.render("Welcome to the Catch The Fruits Game", True, BLACK)
        title_rect = title_text.get_rect(center=(screen_width//2, screen_height//2 - 150))
        screen.blit(title_text, title_rect)

        start_game_rect, game_mode_rect, help_rect, exit_rect = draw_main_menu_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if start_game_rect.collidepoint(pos):
                    waiting = False
                    game_loop()
                elif game_mode_rect.collidepoint(pos):
                    mode_menu()
                    waiting = False
                elif help_rect.collidepoint(pos):
                    help_screen()
                elif exit_rect.collidepoint(pos):
                    pygame.quit()
                    quit()

        pygame.display.update()
        clock.tick(60)

main()
