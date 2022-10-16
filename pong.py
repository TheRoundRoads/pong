from classes import Paddle, Ball
from random import choice, uniform

import pygame

pygame.init()
pygame.mixer.init()

PATH = "C:\\Users\\micha\\PycharmProjects\\pythonProject\\Games\\pong"

FPS = 10
WIDTH = 1920 // 2
HEIGHT = 1080 // 2

COLOUR = (255, 255, 255)  # white
FAINT = (150, 150, 150)
FONT_TYPE = f"{PATH}\\arcade-normal.ttf"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
state = "start"  # "play" and "end
background = pygame.Surface((WIDTH, HEIGHT))

PADDLE_WIDTH = 15
PADDLE_HEIGHT = 80
paddle1 = Paddle(0, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle2 = Paddle(WIDTH - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
RADIUS = 15
ballVel = [0, 0]
ball = Ball(WIDTH // 2 - RADIUS // 2, HEIGHT // 2 - RADIUS // 2, RADIUS)

velocity = 4
ball_start_vel = 2.2
max_speed = 25
inc_factor = 1.15

WIN_POINTS = 3

hit_sound = pygame.mixer.Sound(f"{PATH}\\paddle.ogg")
score_sound = pygame.mixer.Sound(f"{PATH}\\score.ogg")


def drawFont(text, size, location, colour=COLOUR):
    font = pygame.font.Font(FONT_TYPE, size)
    word = font.render(text, True, colour)
    word_rect = word.get_rect(center=location)
    screen.blit(word, word_rect)


def collide(body1, body2):  # Standard AABB collision
    if (body1.x < body2.x + body2.width and
            body1.x + body1.width > body2.x and
            body1.y < body2.y + body2.height and
            body1.y + body1.height > body2.y):
        return True
    return False


def redrawGameWindow():
    screen.blit(background, (0, 0))
    if state == "start":
        drawFont("PONG", 100, (WIDTH // 2, 200))

        drawFont("Press 'Enter' to play!", 30, (WIDTH // 2, HEIGHT // 2 + 100))

    if state in ["play", "ready"]:
        drawFont("PONG", 50, (WIDTH//2, 50))
        drawFont(f"First to {WIN_POINTS} wins!", 20, (WIDTH//2, 100))
        drawFont(str(P1_SCORE), 200, (WIDTH // 4, HEIGHT // 2), colour=FAINT)
        drawFont(str(P2_SCORE), 200, (3 * WIDTH // 4, HEIGHT // 2), colour=FAINT)
        pygame.draw.rect(screen, COLOUR, (paddle1.x, paddle1.y, paddle1.width, paddle1.height))
        pygame.draw.rect(screen, COLOUR, (paddle2.x, paddle2.y, paddle2.width, paddle2.height))
        pygame.draw.rect(screen, COLOUR, (ball.x, ball.y, ball.width, ball.height))

    if state == "win":
        drawFont(f'WINNER:', 30, (WIDTH//2, HEIGHT//2 - 150))
        drawFont(f'{WINNER}', 150, (WIDTH // 2, HEIGHT // 2 - 20))
        drawFont(f'Final Score: {P1_SCORE}-{P2_SCORE}', 40, (WIDTH//2, HEIGHT//2 + 100))
        drawFont("Press 'Enter' to replay!", 30, (WIDTH//2, HEIGHT//2 + 200))

    pygame.display.update()

start = False
P1_SCORE = 0
P2_SCORE = 0
prev_winner = ""
run = True
while run:
    pygame.time.delay(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Start when enter is pressed
    if state == "start":
        P1_SCORE = 0
        P2_SCORE = 0
        WINNER = ""
        start = False
        prev_winner = 0
        if keys[pygame.K_RETURN]:
            state = "ready"

    # Prepare to launch ball
    if state == "ready":
        ballVel = [0, 0]
        paddle1 = Paddle(0, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        paddle2 = Paddle(WIDTH - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        ball = Ball(WIDTH // 2 - RADIUS // 2, HEIGHT // 2 - RADIUS // 2, RADIUS)
        redrawGameWindow()
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if start:
                # prev winner determines direction
                ballVel[0] = -prev_winner * ball_start_vel
                ballVel[1] = uniform(-2, 2)
            else:
                direction = choice([-1, 1])
                ballVel[0] = direction * ball_start_vel
                if ballVel[0] > max_speed:
                    ballVel[0] = max_speed
                elif ballVel[0] < -max_speed:
                    ballVel[0] = -max_speed
                ballVel[1] = uniform(-2, 2)
            state = "play"

    if state == "play":
        start = True
        if keys[pygame.K_w]:
            paddle1.y -= velocity
            if paddle1.y < 0:
                paddle1.y = 0
        if keys[pygame.K_s]:
            paddle1.y += velocity
            if paddle1.y + paddle1.height > HEIGHT:
                paddle1.y = HEIGHT - paddle1.height

        # Arrow keys not working well :(
        if keys[pygame.K_UP]:
            paddle2.y -= velocity
            if paddle2.y < 0:
                paddle2.y = 0
        if keys[pygame.K_DOWN]:
            paddle2.y += velocity
            if paddle2.y + paddle2.height > HEIGHT:
                paddle2.y = HEIGHT - paddle2.height

        ball.x += ballVel[0]

        if ball.x < 0:
            P2_SCORE += 1
            pygame.mixer.Sound.play(score_sound)
            prev_winner = 1
            if P2_SCORE == WIN_POINTS:
                state = "win"
                WINNER = "P2"
            else:
                state = "ready"
        if ball.x > WIDTH - ball.width:
            P1_SCORE += 1
            pygame.mixer.Sound.play(score_sound)
            prev_winner = -1
            if P1_SCORE == WIN_POINTS:
                state = "win"
                WINNER = "P1"
            else:
                state = "ready"

        ball.y += ballVel[1]
        if ball.y < 0:
            ball.y = 0
            ballVel[1] = -ballVel[1]
        elif ball.y > HEIGHT - ball.height:
            ball.y = HEIGHT - ball.height
            ballVel[1] = -ballVel[1]

        if collide(paddle1, ball) or collide(paddle2, ball):
            pygame.mixer.Sound.play(hit_sound)
            ballVel[0] = -ballVel[0] * inc_factor
            ballVel[1] += uniform(-1, 1)

    if state == "win":
        redrawGameWindow()
        event = pygame.event.wait()
        if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
            state = "start"

    redrawGameWindow()

pygame.quit()
