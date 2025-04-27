import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
FPS = 60
FONT = pygame.font.SysFont(None, 48)
SMALL_FONT = pygame.font.SysFont(None, 32)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)

# Moves
MOVES = ['rock', 'paper', 'scissors']

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")

# Clock
clock = pygame.time.Clock()

# Scores
player_score = 0
cpu_score = 0

# Load and scale images
def load_and_scale(path, scale_factor=0.2):
    image = pygame.image.load(path)
    width = int(image.get_width() * scale_factor)
    height = int(image.get_height() * scale_factor)
    return pygame.transform.scale(image, (width, height))

graphics = {
    'PrePlayer': load_and_scale('Graphics/PrePlayer.png'),
    'PreCPU': load_and_scale('Graphics/PreCPU.png'),
    'RockPlayer': load_and_scale('Graphics/RockPlayer.png'),
    'RockCPU': load_and_scale('Graphics/RockCPU.png'),
    'PaperPlayer': load_and_scale('Graphics/PaperPlayer.png'),
    'PaperCPU': load_and_scale('Graphics/PaperCPU.png'),
    'PlayerScissor': load_and_scale('Graphics/PlayerScissor.png'),
    'CPUScissor': load_and_scale('Graphics/CPUScissor.png')
}

# Load sounds
pre_sound = pygame.mixer.Sound('Sounds/PreSound.mp3')
draw_sound = pygame.mixer.Sound('Sounds/DrawSound.mp3')
shoot_sounds = [
    pygame.mixer.Sound('Sounds/Shoot1.mp3'),
    pygame.mixer.Sound('Sounds/Shoot2.mp3'),
    pygame.mixer.Sound('Sounds/Shoot3.mp3')
]
win_sounds = [
    pygame.mixer.Sound('Sounds/Win1.mp3'),
    pygame.mixer.Sound('Sounds/Win2.mp3'),
    pygame.mixer.Sound('Sounds/Win3.mp3')
]
lose_sounds = [
    pygame.mixer.Sound('Sounds/Lose1.mp3'),
    pygame.mixer.Sound('Sounds/Lose2.mp3'),
    pygame.mixer.Sound('Sounds/Lose3.mp3')
]

# Helper function to render text
def draw_text(text, font, color, surface, x, y, center=True):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Title Screen
def title_screen():
    screen.fill(WHITE)
    draw_text("Rock Paper Scissors", FONT, BLACK, screen, WIDTH//2, HEIGHT//2)
    pygame.display.update()
    pygame.time.delay(4000)

# Hand Animation with bouncing effect
def hand_animation(player_move, cpu_move):
    bounce_offset = [0, -10, 0, 10, 0]
    for word in ["Rock", "Paper", "Scissors"]:
        for offset in bounce_offset:
            screen.fill(WHITE)
            draw_hands('PrePlayer', 'PreCPU', offset)
            draw_text(word, FONT, BLACK, screen, WIDTH//2, HEIGHT//4)
            pygame.display.update()
            pygame.time.delay(100)

    random.choice(shoot_sounds).play()
    screen.fill(WHITE)
    player_key = f"{player_move.capitalize()}Player" if player_move != 'scissors' else "PlayerScissor"
    cpu_key = f"{cpu_move.capitalize()}CPU" if cpu_move != 'scissors' else "CPUScissor"
    draw_hands(player_key, cpu_key, 0)
    draw_text("Shoot!", FONT, BLACK, screen, WIDTH//2, HEIGHT//4)
    pygame.display.update()
    pygame.time.delay(1000)

# Draw hands with optional vertical offset
def draw_hands(player_key, cpu_key, offset=0):
    player_image = graphics[player_key]
    cpu_image = graphics[cpu_key]
    screen.blit(player_image, (WIDTH//4 - player_image.get_width()//2, HEIGHT//2 - player_image.get_height()//2 + offset))
    screen.blit(cpu_image, (WIDTH*3//4 - cpu_image.get_width()//2, HEIGHT//2 - cpu_image.get_height()//2 + offset))

# Draw button
def draw_button(text, rect, color, surface):
    pygame.draw.rect(surface, color, rect)
    draw_text(text, SMALL_FONT, BLACK, surface, rect.centerx, rect.centery)

# Determine winner
def determine_winner(player, cpu):
    if player == cpu:
        return 'draw'
    elif (player == 'rock' and cpu == 'scissors') or (player == 'paper' and cpu == 'rock') or (player == 'scissors' and cpu == 'paper'):
        return 'player'
    else:
        return 'cpu'

# Main game loop
def game_loop():
    global player_score, cpu_score

    button_width = 120
    button_height = 40
    button_spacing = 20
    total_height = button_height * 3 + button_spacing * 2
    start_y = (HEIGHT - total_height) // 2

    buttons = {
        'rock': pygame.Rect(WIDTH//2 - button_width//2, start_y, button_width, button_height),
        'paper': pygame.Rect(WIDTH//2 - button_width//2, start_y + button_height + button_spacing, button_width, button_height),
        'scissors': pygame.Rect(WIDTH//2 - button_width//2, start_y + (button_height + button_spacing) * 2, button_width, button_height)
    }

    running = True
    while running:
        screen.fill(WHITE)

        # Display Scores
        draw_text(f"Player: {player_score}", SMALL_FONT, BLACK, screen, WIDTH//4, HEIGHT - 30)
        draw_text(f"CPU: {cpu_score}", SMALL_FONT, BLACK, screen, WIDTH*3//4, HEIGHT - 30)

        # Display prompt
        draw_text("What's your move?", FONT, BLACK, screen, WIDTH//2, 50)

        # Draw buttons
        for move, rect in buttons.items():
            draw_button(move.capitalize(), rect, GRAY, screen)

        pygame.display.update()

        player_move = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for move, rect in buttons.items():
                    if rect.collidepoint(mx, my):
                        player_move = move

        if player_move:
            pre_sound.play()
            cpu_move = random.choice(MOVES)
            hand_animation(player_move, cpu_move)

            winner = determine_winner(player_move, cpu_move)

            screen.fill(WHITE)
            player_key = f"{player_move.capitalize()}Player" if player_move != 'scissors' else "PlayerScissor"
            cpu_key = f"{cpu_move.capitalize()}CPU" if cpu_move != 'scissors' else "CPUScissor"
            draw_hands(player_key, cpu_key, 0)

            if winner == 'draw':
                draw_sound.play()
                result_text = "Draw!"
            elif winner == 'player':
                random.choice(win_sounds).play()
                result_text = f"{player_move.capitalize()} beats {cpu_move.capitalize()}; You Win!"
                player_score += 1
            else:
                random.choice(lose_sounds).play()
                result_text = f"{cpu_move.capitalize()} beats {player_move.capitalize()}; You Lose!"
                cpu_score += 1

            draw_text(result_text, SMALL_FONT, BLACK, screen, WIDTH//2, 50)

            # Display Scores
            draw_text(f"Player: {player_score}", SMALL_FONT, BLACK, screen, WIDTH//4, HEIGHT - 30)
            draw_text(f"CPU: {cpu_score}", SMALL_FONT, BLACK, screen, WIDTH*3//4, HEIGHT - 30)

            pygame.display.update()
            pygame.time.delay(2000)

# Main
if __name__ == "__main__":
    title_screen()
    game_loop()
