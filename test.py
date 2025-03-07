import pygame
import random

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

# Load the basket image
basket_image = pygame.image.load("basket.png")  
basket_image = pygame.transform.scale(basket_image, (basket_width, basket_height))

fruit_width = 50
fruit_height = 50
fruit_speed = 5

score = 0

clock = pygame.time.Clock()

def draw_basket(x, y):
    # Draw the basket image
    screen.blit(basket_image, (x, y))

def draw_fruits(x,y):
    pygame.draw.ellipse(screen, RED, [x,y,fruit_width, fruit_height])

def display_score(score):
    font = pygame.font.SysFont(None, 36)
    text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(text, (10,10))

def draw_start_button():
    button_width = 200
    button_height = 50
    button_x = screen_width // 2 - button_width // 2
    button_y = screen_height // 2 - button_height // 2

    pygame.draw.rect(screen, BLACK, [button_x, button_y, button_width, button_height])
    font = pygame.font.SysFont(None, 48)
    text = font.render("Start Game", True, WHITE)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)
    return pygame.Rect(button_x, button_y, button_width, button_height)
    
def game_over():
    font = pygame.font.SysFont(None, 72)
    text = font.render("Game over", True, BLACK)
    screen.blit(text, (screen_width // 2 - 150, screen_height // 2 - 36))
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    quit()
    
def game_loop():
    global score
    global basket_x

    fruit_x = random.randint(0, screen_width - fruit_width)
    fruit_y = -fruit_height

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check for key presses (moved outside the event loop)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            basket_x -= basket_speed
        if keys[pygame.K_RIGHT]:
            basket_x += basket_speed

        # Keep the basket within the screen bounds
        if basket_x < 0:
            basket_x = 0
        elif basket_x > screen_width - basket_width:
            basket_x = screen_width - basket_width

        fruit_y += fruit_speed

        # Check if the fruit is caught
        if fruit_y + fruit_height > basket_y and basket_x < fruit_x + fruit_width < basket_x + basket_width:
            score += 1
            fruit_x = random.randint(0, screen_width - fruit_width)
            fruit_y = -fruit_height

        draw_basket(basket_x, basket_y)
        draw_fruits(fruit_x, fruit_y)
        display_score(score)

        # Game over if the fruit reaches the bottom
        if fruit_y > screen_height:
            game_over()

        pygame.display.update()
        clock.tick(60)

def main():
    waiting = True
    while waiting:
        screen.fill(WHITE)
        button_rect = draw_start_button()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_rect.collidepoint(mouse_pos):
                    waiting = False
                    game_loop()

        pygame.display.update()
        clock.tick(60)


main()