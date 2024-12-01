import pygame
import random
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

PIPE_WIDTH = 40
PIPE_GAP = 100
pipe_list = []

bird_width = 25
bird_height = 25
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0
gravity = 0.5
flap_strength = -10
bird_rect = pygame.Rect(50, bird_y, bird_width, bird_height)

HIGH_SCORE_FILE = "highscore.txt"


def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, 'r') as file:
            return int(file.read().strip())
    else:
        return 0


def save_high_score(score):
    with open(HIGH_SCORE_FILE, 'w') as file:
        file.write(str(score))


def game_loop():
    global bird_y, bird_velocity, pipe_list, bird_rect, gravity, score, high_score, no_game_over, score_plus

    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    bird_rect.y = bird_y
    pipe_list = []
    score = 0
    game_over = False
    cheat_menu = False
    unlimited_fly = False
    no_gravity = False
    pipe_speed = 3
    no_game_over = False
    score_plus = False

    clock = pygame.time.Clock()
    high_score = load_high_score()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if bird_rect.top > 0:
                        bird_velocity = flap_strength
                if event.key == pygame.K_c:
                    cheat_menu = not cheat_menu
                if cheat_menu:
                    if event.key == pygame.K_u:
                        unlimited_fly = not unlimited_fly
                    elif event.key == pygame.K_g:
                        no_gravity = not no_gravity
                    elif event.key == pygame.K_p:
                        pipe_speed += 9999
                    elif event.key == pygame.K_m:
                        pipe_speed = max(1, pipe_speed - 1)
                    elif event.key == pygame.K_l:
                        pipe_speed = 3  # Reset Pipe Speed
                    elif event.key == pygame.K_o:
                        no_game_over = not no_game_over
                    elif event.key == pygame.K_i:
                        score_plus = not score_plus

        if unlimited_fly:
            bird_velocity = 0
        if no_gravity:
            gravity = 0
        else:
            gravity = 0.5

        if not unlimited_fly:
            bird_velocity += gravity
        bird_y += bird_velocity
        bird_rect.y = bird_y

        if bird_rect.top < 0:
            bird_rect.top = 0
        if bird_rect.bottom > SCREEN_HEIGHT:
            bird_rect.bottom = SCREEN_HEIGHT

        if len(pipe_list) == 0 or pipe_list[-1][0].x < SCREEN_WIDTH - 300:
            pipe_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
            upper_pipe = pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, pipe_height)
            lower_pipe = pygame.Rect(SCREEN_WIDTH, pipe_height + PIPE_GAP, PIPE_WIDTH,
                                     SCREEN_HEIGHT - pipe_height - PIPE_GAP)
            pipe_list.append([upper_pipe, lower_pipe])

        for pipe in pipe_list:
            pipe[0].x -= pipe_speed
            pipe[1].x -= pipe_speed

        for pipe in pipe_list[:]:
            if pipe[0].x + PIPE_WIDTH < 0:
                pipe_list.remove(pipe)
                score += 9999999999 if score_plus else 1

        if not no_game_over:
            for pipe in pipe_list:
                if bird_rect.colliderect(pipe[0]) or bird_rect.colliderect(pipe[1]):
                    game_over = True

        screen.fill(WHITE)

        for pipe in pipe_list:
            pygame.draw.rect(screen, GREEN, pipe[0])
            pygame.draw.rect(screen, GREEN, pipe[1])

        pygame.draw.rect(screen, BLUE, bird_rect)

        if game_over:
            font = pygame.font.SysFont('Arial', 36)
            text = font.render("Game Over", True, RED)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2,
                               SCREEN_HEIGHT // 2 - text.get_height() // 2))
            if score > high_score:
                high_score = score
                save_high_score(high_score)

        font = pygame.font.SysFont('Arial', 24)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        high_score_text = font.render(f"Highscore: {high_score}", True, YELLOW)
        screen.blit(score_text, (20, 20))
        screen.blit(high_score_text, (SCREEN_WIDTH - high_score_text.get_width() - 20, 20))

        if cheat_menu:
            cheat_font = pygame.font.SysFont('Arial', 24)
            cheat_texts = [
                "Cheat Menu (Press 'C' to toggle):",
                f"Unlimited Fly: {'ON' if unlimited_fly else 'OFF'} (Press 'U')",
                f"Gravity: {'OFF' if no_gravity else 'ON'} (Press 'G')",
                f"Pipe Speed: {pipe_speed} (Press 'P' to increase high increase, 'M' to decrease, 'L' to reset)",
                f"No Game Over: {'ON' if no_game_over else 'OFF'} (Press 'O')",
                f"Score Cheat: {'ON' if score_plus else 'OFF'} (Press 'I')"
            ]
            for idx, text in enumerate(cheat_texts):
                cheat_text = cheat_font.render(text, True, (0, 0, 0))
                screen.blit(cheat_text, (SCREEN_WIDTH // 2 - cheat_text.get_width() // 2, 100 + idx * 40))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    game_loop()
