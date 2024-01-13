import pygame
import random
import math

pygame.init()

def draw_img():
    global rotated_p1_rect, rotated_p2_rect

    rotated_p1 = pygame.transform.rotate(player_1, p1_angle)
    rotated_p1_rect = rotated_p1.get_rect(center=p1_rect.center)
    WIN.blit(rotated_p1, rotated_p1_rect)

    rotated_p2 = pygame.transform.rotate(player_2, p2_angle)
    rotated_p2_rect = rotated_p2.get_rect(center=p2_rect.center)
    WIN.blit(rotated_p2, rotated_p2_rect)

    WIN.blit(ball, ball_rect)

def player_movement():
    global p1_angle, p2_angle, p1_tilt_time, p2_tilt_time

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and p1_rect.top > 0:
        p1_rect.y -= 10

    elif keys[pygame.K_s] and p1_rect.bottom < HEIGHT:
        p1_rect.y += 10

    if keys[pygame.K_UP] and p2_rect.top > 0:
        p2_rect.y -= 10
        
    elif keys[pygame.K_DOWN] and p2_rect.bottom < HEIGHT:
        p2_rect.y += 10

    # Handle paddle tilting for player 1
    if keys[pygame.K_a] and p1_rect.left > 0:
        p1_angle = 45  
        p1_tilt_time = pygame.time.get_ticks()

    elif keys[pygame.K_d] and p1_rect.right < WIDTH:
        p1_angle = -45  
        p1_tilt_time = pygame.time.get_ticks()

    # Handle paddle tilting for player 2
    if keys[pygame.K_LEFT] and p2_rect.left > 0:
        p2_angle = 45  
        p2_tilt_time = pygame.time.get_ticks()

    elif keys[pygame.K_RIGHT] and p2_rect.right < WIDTH:
        p2_angle = -45  
        p2_tilt_time = pygame.time.get_ticks()

    # Check if it's time to revert paddles to their original positions
    current_time = pygame.time.get_ticks()
    if current_time - p1_tilt_time > 2000:
        p1_angle = 0

    if current_time - p2_tilt_time > 2000:
        p2_angle = 0

def ball_movement():
    global ball_speed, cur_ball_speed, change_ball_speed, start_time

    if pygame.time.get_ticks() - start_time > 2000:
        ball_rect.x += ball_speed[0]
        ball_rect.y += ball_speed[1]

        if ball_rect.top <= 0 or ball_rect.bottom >= HEIGHT:
            ball_speed[1] = -ball_speed[1]

        if ball_rect.colliderect(p1_rect) or ball_rect.colliderect(p2_rect) or ball_rect.colliderect(rotated_p1_rect) or ball_rect.colliderect(rotated_p2_rect):
            ball_speed[0] = -ball_speed[0]
            change_ball_speed += 1
            if change_ball_speed % 10 == 0:
                cur_ball_speed += 1
                ball_speed = [random.choice([-cur_ball_speed, cur_ball_speed]), random.choice([-cur_ball_speed, cur_ball_speed])]

        if ball_rect.left <= 0 or ball_rect.right >= WIDTH:
            ball_rect.center = (WIDTH // 2, HEIGHT // 2)
            ball_speed = [random.choice([-5, 5]), random.choice([-5, 5])]
            change_ball_speed = 0
            cur_ball_speed = 5
            start_time = pygame.time.get_ticks()

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()
FPS = 60

# Game objects
player_1 = pygame.image.load("assets/red.png").convert_alpha()
player_1 = pygame.transform.scale(player_1, (10, 50))
p1_rect = player_1.get_rect(center=(20, HEIGHT // 2))
p1_angle = 0
p1_tilt_time = 0

player_2 = pygame.image.load("assets/blue.png").convert_alpha()
player_2 = pygame.transform.scale(player_2, (10, 50))
p2_rect = player_2.get_rect(center=(WIDTH - 20, HEIGHT // 2))
p2_angle = 0
p2_tilt_time = 0

ball = pygame.image.load("assets/pong-ball.png").convert_alpha()
ball = pygame.transform.scale(ball, (20, 20))
ball_rect = ball.get_rect(center=(WIDTH // 2, HEIGHT // 2))

ball_speed = [random.choice([-5, 5]), random.choice([-5, 5])]
change_ball_speed = 0
cur_ball_speed = 5

start_time = pygame.time.get_ticks()

# Main loop
running = True
while running:

    WIN.fill((0, 0, 0))
    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.size
            WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            player_1 = pygame.transform.scale(player_1, (10, 50))
            p1_rect = player_1.get_rect(center=(20, HEIGHT // 2))
            player_2 = pygame.transform.scale(player_2, (10, 50))
            p2_rect = player_2.get_rect(center=(WIDTH - 20, HEIGHT // 2))

    draw_img()
    player_movement()
    ball_movement()
    pygame.display.update()

pygame.quit()
