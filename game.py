import pygame
import random
import os
import time

# Initialize game
pygame.init()

# Set up the Screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Catch The Fruits")

#color
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

# Game variables
basket_width = 100
basket_height = 50
basket_x = screen_width // 2 - basket_width // 2
basket_y = screen_height - basket_height - 20
basket_speed = 10

fruit_width = 50
fruit_height = 50
fruit_speed = 5

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
    # Draw the basket image
    screen.blit(basket_image, (x, y))

def display_fruit_points(x, y, fruit_img):
    points = fruit_points[fruit_files[fruit_images.index(fruit_img)]]
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"+{points}", True, BLACK)

    # Adjust x position if too close to right edge
    text_x = min(x + fruit_width + 5, screen_width - text.get_width() - 5)
    # If fruit is near right edge, show points on left side
    if x > screen_width - fruit_width - 30:
        text_x = x - text.get_width() - 5

    screen.blit(text, (text_x, y))
    
def display_score(score):
    # Both "Score:" and number in smaller font
    label_font = pygame.font.Font("PressStart2P-Regular.ttf", 16)
    score_font = pygame.font.Font("PressStart2P-Regular.ttf", 16)

    label = label_font.render("Score:", True, BLACK)
    number = score_font.render(str(score), True, BLACK)

    # Position "Score:" and the number with more spacing
    screen.blit(label, (10, 100))  # "Score:" at (10, 100)
    screen.blit(number, (120, 100))  # Number moved further to the right

def display_high_score(high_score):
    label_font = pygame.font.Font("PressStart2P-Regular.ttf", 16)
    score_font = pygame.font.Font("PressStart2P-Regular.ttf", 16)

    label = label_font.render("Highest Score:", True, BLACK)
    number = score_font.render(str(high_score), True, BLACK)

    # Calculate the width of the label to properly position the number
    label_width = label.get_width()

    # Position "Highest Score:" and the number below the current score
    screen.blit(label, (10, 150))
    screen.blit(number, (10 + label_width + 20, 150))  # 20 pixels spacing between label and number

def draw_start_button():
    button_width = 200
    button_height = 50
    spacing = 20
    
    total_width = button_width * 3 + spacing * 2
    
    start_x = screen_width // 2 - total_width // 2
    group_start_x = screen_width // 2 - total_width // 2
    button_y = screen_height // 2 - button_height // 2

    pygame.draw.rect(screen, (0, 200, 0), [group_start_x, button_y, button_width, button_height])  # Green
    font = pygame.font.Font("PressStart2P-Regular.ttf", 20)
    text = font.render("Start Game", True, BLACK)
    text_rect = text.get_rect(center=(group_start_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)
    return pygame.Rect(start_x, button_y, button_width, button_height)
   
    # Help Button
def draw_help_button():
    button_width = 200
    button_height = 50
    spacing = 20 

    total_width = button_width * 3 + spacing * 2

    group_start_x = screen_width // 2 - total_width // 2

    button_x = group_start_x + button_width + spacing
    button_y = screen_height // 2 - button_height // 2
    

    pygame.draw.rect(screen, (0, 100, 255), [button_x, button_y, button_width, button_height])  # Blue
    font = pygame.font.Font("PressStart2P-Regular.ttf", 20)
    text = font.render("Help", True, BLACK)
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)
    return pygame.Rect(button_x, button_y, button_width, button_height)    
  
    # Help Screen
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
    button_width = 200
    button_height = 50
    spacing = 20 

    total_width = button_width * 3 + spacing * 2

    group_start_x = screen_width // 2 - total_width // 2

    
    button_y = screen_height // 2 - button_height // 2
    button_x = group_start_x + (button_width + spacing) * 2

    pygame.draw.rect(screen, (200, 0, 0), [button_x, button_y, button_width, button_height])  # Red
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
    # Set button dimensions and position (top-right corner)
    button_width = 100  # Increased size for usability
    button_height = 50
    button_x = screen_width - button_width - 10  # 10px padding from right edge
    button_y = 10  # 10px padding from top edge
    
    # Create a Rect for collision detection
    pause_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    
    # Draw the button
    pygame.draw.rect(screen, RED, pause_rect)
    
    # Display "Pause" when the game is running, and "Resume" when paused
    font = pygame.font.Font(None, 30)
    text_str = "Resume" if paused else "Pause"
    text = font.render(text_str, True, BLACK)
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)
    
    return pause_rect

def toggle_pause():
    """Toggle the paused state of the game."""
    global paused
    paused = not paused
# --- END PAUSE BUTTON CODE ---

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
    # Display the "Game over" message
    font = pygame.font.Font("PressStart2P-Regular.ttf", 30)
    text = font.render("Game over", True, BLACK)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - 100))
    
    # Draw the restart button
    restart_button_rect = draw_restart_button()
    menu_button_rect = return_to_menu_button()
    pygame.display.update()
    
    # Wait for the player to click the restart button
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    waiting = False
                    # Reset any necessary game variables (e.g., score, basket position)
                    global score, basket_x
                    score = 0
                    basket_x = screen_width // 2 - basket_width // 2
                    # Restart the game loop
                    game_loop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button_rect.collidepoint(event.pos):
                    main()
        clock.tick(60)

    
def game_loop():
    global score
    global basket_x
    global high_score

    fruit_x = random.randint(0, screen_width - fruit_width)
    fruit_y = -fruit_height
    fruit_img = random.choice(fruit_images)
    splatter_positions = []  # List to store splatter positions
    missed_fruits = 0  # Counter for missed fruits

    running = True
    while running:
        screen.blit(background_image, (0, 0))

         #Always draw the pause button and get its Rect for click detection
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

            # keep the basket within the screen bounds
            if basket_x < 0:
                basket_x = 0
            elif basket_x > screen_width - basket_width:
                basket_x = screen_width - basket_width

            fruit_y += fruit_speed

        # check if the fruit collides with the basket
        if fruit_y + fruit_height > basket_y and basket_x < fruit_x + fruit_width < basket_x + basket_width:
            score += fruit_points[fruit_files[fruit_images.index(fruit_img)]]
            if score > high_score:  
             high_score = score
            fruit_x = random.randint(0, screen_width - fruit_width)
            fruit_y = -fruit_height
            fruit_img = random.choice(fruit_images)

        # Check if the fruit is missed
        if fruit_y > screen_height:
            splatter_positions.append((fruit_x, screen_height - fruit_height, time.time()))  # Add timestamp
            fruit_x = random.randint(0, screen_width - fruit_width)
            fruit_y = -fruit_height
            fruit_img = random.choice(fruit_images)
            missed_fruits += 1  # Increment missed fruits counter

        draw_basket(basket_x, basket_y)
        screen.blit(fruit_img, (fruit_x, fruit_y))
        display_fruit_points(fruit_x, fruit_y, fruit_img)
        display_score(score)
        display_high_score(high_score)

        # Draw splatters and remove old ones
        current_time = time.time()
        splatter_positions = [
            (x, y, t) for (x, y, t) in splatter_positions if current_time - t < 0.5
        ]

        for x, y, _ in splatter_positions:
            screen.blit(splatter_image, (x, y))

        # End game if two fruits are missed
        if missed_fruits >= 3:
            game_over()
            running = False

        pygame.display.update()
        clock.tick(60)

def main(): 
    waiting = True      
    while waiting:
        screen.blit(background_image, (0, 0))

        font = pygame.font.Font("PressStart2P-Regular.ttf", 20)
        welcome_text = font.render("Welcome to the Catch The Fruits Game", True, BLACK)
        welcome_rect = welcome_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
        screen.blit(welcome_text, welcome_rect)

        start_button_rect = draw_start_button()
        help_button_rect = draw_help_button()
        exit_button_rect = draw_exit_button()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if start_button_rect.collidepoint(mouse_pos):
                    waiting = False
                    game_loop()
                if help_button_rect.collidepoint(mouse_pos):
                    help_screen()
                if exit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()

        pygame.display.update()
        clock.tick(60)


main()

