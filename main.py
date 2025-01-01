import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
FPS = 30
GRAVITY = 0.25
FLAP_POWER = -4
PIPE_SPEED = -4
PIPE_GAP = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Doge Dash')

# Load and resize assets
background = pygame.image.load('assets/background.jpg')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
dark_background = pygame.image.load('assets/darkbg.jpg')
dark_background = pygame.transform.scale(dark_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

bird = pygame.image.load('assets/doge-removebg-preview.png')
bird = pygame.transform.scale(bird, (45, 40))
pipe_surface = pygame.image.load('assets/pipe.png')
pipe_surface = pygame.transform.scale(pipe_surface, (50, 300))
cloud_surface = pygame.image.load('assets/clouds-removebg-preview.png')
cloud_surface = pygame.transform.scale(cloud_surface, (60, 40))
heart_image = pygame.image.load('assets/heart-removebg-preview.png')
heart_image = pygame.transform.scale(heart_image, (36, 36))
game_over_image = pygame.image.load('assets/game_over2-removebg-preview.png')
game_over_image = pygame.transform.scale(game_over_image, (300, 100))

# Fonts
font = pygame.font.Font('assets/Silkscreen-Regular.ttf', 48)
title_font = pygame.font.Font('assets\FlappyBirdy.ttf',175)
title_font2= pygame.font.Font('assets\FlappyBirdy.ttf',75)
button_font = pygame.font.Font('assets/Silkscreen-Regular.ttf', 36)
score_font = pygame.font.Font('assets/Silkscreen-Regular.ttf', 30)

clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()


# Bird settings
bird_x = 50
bird_y = 200
bird_y_velocity = 0

# Pipe settings
pipe_list = []
pipe_height = [200, 300, 400]

# Lives and Score
lives = 3
score = 0
final_score = 0  

dark_mode = False
cloud_list = []
cloud_spawn_time = 0


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(SCREEN_WIDTH, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(SCREEN_WIDTH, random_pipe_pos - PIPE_GAP))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx += PIPE_SPEED
    return [pipe for pipe in pipes if pipe.right > 0]

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= SCREEN_HEIGHT:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    bird_rect = bird.get_rect(topleft=(bird_x, bird_y))
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    return False

def get_pipe_y_ranges(pipes):
    ranges = []
    for pipe in pipes:
        if pipe.bottom >= SCREEN_HEIGHT:
            ranges.append((pipe.top, pipe.bottom))
        else:
            ranges.append((pipe.bottom - PIPE_GAP, pipe.bottom))
    return ranges

def create_cloud(pipes):
    pipe_y_ranges = get_pipe_y_ranges(pipes)
    while True:
        cloud_y_positions = [50, 100, 150, 200, 250]
        random_cloud_pos = random.choice(cloud_y_positions)
        
        # Check if the chosen position overlaps with any pipe y-ranges
        overlap = False
        for y_range in pipe_y_ranges:
            if y_range[0] < random_cloud_pos < y_range[1] or y_range[0] < random_cloud_pos + cloud_surface.get_height() < y_range[1]:
                overlap = True
                break
        
        if not overlap:
            break
    
    cloud = cloud_surface.get_rect(midtop=(SCREEN_WIDTH, random_cloud_pos))
    return cloud


def move_clouds(clouds):
    for cloud in clouds:
        cloud.centerx += PIPE_SPEED
    return [cloud for cloud in clouds if cloud.right > 0]

def draw_clouds(clouds):
    for cloud in clouds:
        screen.blit(cloud_surface, cloud)

def check_cloud_collision(clouds):
    bird_rect = bird.get_rect(topleft=(bird_x, bird_y))
    for cloud in clouds:
        if bird_rect.colliderect(cloud):
            return True
    return False

def draw_hearts(lives):
    for i in range(lives):
        screen.blit(heart_image, (10 + i * 40, 10))

def draw_score():
    if lives > 0:
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        score_text = score_font.render(f'Score: {elapsed_time}', True, WHITE if dark_mode else BLACK)
    else:
        score_text = score_font.render(f'Score: {final_score}', True, WHITE if dark_mode else BLACK)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 10))

def game_over_screen(final_score):  
    screen.blit(game_over_image, (SCREEN_WIDTH // 2 - game_over_image.get_width() // 2, SCREEN_HEIGHT // 4))

    score_text = score_font.render(f'Score: {final_score}', True, BLACK)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 4 + game_over_image.get_height() + 10))

    restart_button = button_font.render("Restart", True, BLACK)
    quit_button = button_font.render("Quit", True, BLACK)
    

    gap = 75
    button_spacing = 50
    restart_y_position = SCREEN_HEIGHT // 4 + game_over_image.get_height() + gap
    quit_y_position = restart_y_position + button_spacing

    restart_rect = restart_button.get_rect(center=(SCREEN_WIDTH // 2, restart_y_position))
    quit_rect = quit_button.get_rect(center=(SCREEN_WIDTH // 2, quit_y_position))

    screen.blit(restart_button, restart_rect)
    screen.blit(quit_button, quit_rect)

    pygame.display.update()

    return restart_rect, quit_rect

def reset_game():
    global bird_y, bird_y_velocity, pipe_list, pipe_spawn_time, lives, score, final_score, start_time
    bird_y = 200
    bird_y_velocity = 0
    pipe_list = []
    pipe_spawn_time = 0
    lives = 3
    score = 0
    final_score = 0  
    start_time = pygame.time.get_ticks()

def welcome_screen():
    title = title_font.render('Doge Dash', True, WHITE if dark_mode else BLACK)
    play_button = title_font2.render('Play', True, WHITE if dark_mode else BLACK)
    dark_mode_button_text = 'Light Mode' if dark_mode else 'Dark Mode'
    dark_mode_button = title_font2.render(dark_mode_button_text, True,  BLACK)

    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    play_button_rect = play_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    dark_mode_button_rect = dark_mode_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 75))  # Increased spacing

    screen.blit(title, title_rect)
    screen.blit(play_button, play_button_rect)
    screen.blit(dark_mode_button, dark_mode_button_rect)

    pygame.display.update()

    return play_button_rect, dark_mode_button_rect


# MAIN GAME LOOP
running = True
pipe_spawn_time = 0
score = 0
final_score = 0
game_over = False  # Flag to indicate if the game is over
welcome = True

while running:
    if welcome:
        screen.blit(background if not dark_mode else dark_background, (0, 0))
        play_button_rect, dark_mode_button_rect = welcome_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    welcome = False
                    start_time = pygame.time.get_ticks()
                elif dark_mode_button_rect.collidepoint(event.pos):
                    dark_mode = not dark_mode

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    welcome = False
                    start_time = pygame.time.get_ticks()
    else:
        screen.blit(background if not dark_mode else dark_background, (0, 0))

        if game_over:
            restart_rect, quit_rect = game_over_screen(final_score)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_rect.collidepoint(event.pos):
                        reset_game()
                        game_over = False
                    elif quit_rect.collidepoint(event.pos):
                        running = False
                        pygame.quit()
                        sys.exit()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird_y_velocity = FLAP_POWER

            if lives > 0:
                bird_y_velocity += GRAVITY
                bird_y += bird_y_velocity

                if check_collision(pipe_list) or bird_y < 0 or bird_y >= SCREEN_HEIGHT - bird.get_height() or (dark_mode and check_cloud_collision(cloud_list)):
                    lives -= 1
                    if lives == 0:
                        final_score = (pygame.time.get_ticks() - start_time) // 1000
                        game_over = True

                    bird_y = 200
                    bird_y_velocity = 0
                    pipe_list = []
                    pipe_spawn_time = 0
                    cloud_list = []
                    cloud_spawn_time = 0

                if pipe_spawn_time == 0:
                    pipe_list.extend(create_pipe())
                pipe_spawn_time += 1
                if pipe_spawn_time == 90:
                    pipe_spawn_time = 0

                pipe_list = move_pipes(pipe_list)

                passed_pipe = False
                for pipe in pipe_list:
                    if not passed_pipe and bird_x > pipe.centerx and pipe.centerx + PIPE_SPEED < bird_x:
                        passed_pipe = True
                if passed_pipe:
                    score += 1

                if dark_mode:
                    if cloud_spawn_time == 0:
                        cloud_list.append(create_cloud(pipe_list))
                    cloud_spawn_time += 1
                    if cloud_spawn_time == 180:
                        cloud_spawn_time = 0
                    cloud_list = move_clouds(cloud_list)
                    draw_clouds(cloud_list)

                screen.blit(bird, (bird_x, bird_y))
                draw_pipes(pipe_list)
                draw_hearts(lives)
                draw_score()
            else:
                restart_rect, quit_rect = game_over_screen(final_score)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()