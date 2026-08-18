import pygame
import random
import sys

pygame.init()

# Game settings
WIDTH = 400
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY = (135, 206, 235)
GREEN = (34, 139, 34)
DARK_GREEN = (20, 100, 20)
YELLOW = (255, 200, 0)
ORANGE = (255, 140, 0)
RED = (255, 0, 0)

# Player settings
bird_x = 100
bird_width = 56
bird_height = 32
gravity = 0.5
jump_power = -10

# Pipe settings
pipe_width = 70
pipe_gap = 250
pipe_speed = 3
pipe_time = 1500


PIXEL_FONT = {
    "0": [(1,0),(2,0),(3,0),(0,1),(4,1),(0,2),(4,2),(0,3),(4,3),
          (0,4),(4,4),(0,5),(4,5),(1,6),(2,6),(3,6)],
    "1": [(2,0),(1,1),(2,1),(2,2),(2,3),(2,4),(2,5),(1,6),(2,6),(3,6)],
    "2": [(1,0),(2,0),(3,0),(0,1),(4,1),(4,2),(3,3),(2,4),(1,5),
          (0,6),(1,6),(2,6),(3,6),(4,6)],
    "3": [(1,0),(2,0),(3,0),(0,1),(4,1),(4,2),(2,3),(3,3),(4,4),
          (0,5),(4,5),(1,6),(2,6),(3,6)],
    "4": [(0,0),(4,0),(0,1),(4,1),(0,2),(4,2),(0,3),(1,3),(2,3),
          (3,3),(4,3),(4,4),(4,5),(4,6)],
    "5": [(0,0),(1,0),(2,0),(3,0),(4,0),(0,1),(0,2),(0,3),(1,3),
          (2,3),(3,3),(4,4),(4,5),(0,6),(1,6),(2,6),(3,6)],
    "6": [(1,0),(2,0),(3,0),(0,1),(0,2),(0,3),(1,3),(2,3),(3,3),
          (0,4),(4,4),(0,5),(4,5),(1,6),(2,6),(3,6)],
    "7": [(0,0),(1,0),(2,0),(3,0),(4,0),(4,1),(3,2),(3,3),(2,4),
          (2,5),(2,6)],
    "8": [(1,0),(2,0),(3,0),(0,1),(4,1),(0,2),(4,2),(1,3),(2,3),
          (3,3),(0,4),(4,4),(0,5),(4,5),(1,6),(2,6),(3,6)],
    "9": [(1,0),(2,0),(3,0),(0,1),(4,1),(0,2),(4,2),(1,3),(2,3),
          (3,3),(4,3),(4,4),(4,5),(1,6),(2,6),(3,6)],
    "G": [(1,0),(2,0),(3,0),(0,1),(4,1),(0,2),(0,3),(2,3),(3,3),
          (4,3),(0,4),(4,4),(0,5),(4,5),(1,6),(2,6),(3,6)],
    "A": [(2,0),(1,1),(3,1),(0,2),(4,2),(0,3),(1,3),(2,3),(3,3),
          (4,3),(0,4),(4,4),(0,5),(4,5),(0,6),(4,6)],
    "M": [(0,0),(4,0),(0,1),(1,1),(3,1),(4,1),(0,2),(2,2),(4,2),
          (0,3),(4,3),(0,4),(4,4),(0,5),(4,5),(0,6),(4,6)],
    "E": [(0,0),(1,0),(2,0),(3,0),(4,0),(0,1),(0,2),(0,3),(1,3),
          (2,3),(3,3),(0,4),(0,5),(0,6),(1,6),(2,6),(3,6),(4,6)],
    "O": [(1,0),(2,0),(3,0),(0,1),(4,1),(0,2),(4,2),(0,3),(4,3),
          (0,4),(4,4),(0,5),(4,5),(1,6),(2,6),(3,6)],
    "V": [(0,0),(4,0),(0,1),(4,1),(0,2),(4,2),(0,3),(4,3),(1,4),
          (3,4),(1,5),(3,5),(2,6)],
    "R": [(0,0),(1,0),(2,0),(3,0),(0,1),(4,1),(0,2),(4,2),(0,3),
          (1,3),(2,3),(3,3),(0,4),(3,4),(0,5),(4,5),(0,6),(4,6)],
    "P": [(0,0),(1,0),(2,0),(3,0),(0,1),(4,1),(0,2),(4,2),(0,3),
          (1,3),(2,3),(3,3),(0,4),(0,5),(0,6)],
    "S": [(1,0),(2,0),(3,0),(4,0),(0,1),(0,2),(1,3),(2,3),(3,3),
          (4,4),(4,5),(0,6),(1,6),(2,6),(3,6)],
    "C": [(1,0),(2,0),(3,0),(4,0),(0,1),(0,2),(0,3),(0,4),(0,5),
          (1,6),(2,6),(3,6),(4,6)],
    "T": [(0,0),(1,0),(2,0),(3,0),(4,0),(2,1),(2,2),(2,3),(2,4),
          (2,5),(2,6)],
    " ": []
}


def pixel_text(text, x, y, size, color, shadow=None):
    pos = 0

    for letter in text.upper():
        if letter not in PIXEL_FONT:
            continue

        for px, py in PIXEL_FONT[letter]:
            if shadow:
                pygame.draw.rect(
                    screen,
                    shadow,
                    (x + pos + px * size + size,
                     y + py * size + size,
                     size,
                     size)
                )

        for px, py in PIXEL_FONT[letter]:
            pygame.draw.rect(
                screen,
                color,
                (x + pos + px * size,
                 y + py * size,
                 size,
                 size)
            )

        pos += size * 6


def text_size(text, size):
    return len(text) * size * 6


class Player:

    def __init__(self):
        self.x = bird_x
        self.y = HEIGHT // 2
        self.speed = 0

        self.width = bird_width
        self.height = bird_height

        self.wing = 0
        self.wing_count = 0

    def jump(self):
        self.speed = jump_power
        self.wing = 0

    def update(self):
        self.speed += gravity
        self.y += self.speed

        self.wing_count += 1

        if self.wing_count >= 6:
            self.wing_count = 0
            self.wing += 1

            if self.wing > 2:
                self.wing = 0

    def draw(self):

        size = 4

        body = [
            (4,0),(5,0),(6,0),(7,0),(8,0),
            (3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),
            (2,2),(3,2),(4,2),(5,2),(6,2),(7,2),(8,2),(9,2),(10,2),
            (2,3),(3,3),(4,3),(5,3),(6,3),(7,3),(8,3),(9,3),(10,3),
            (2,4),(3,4),(4,4),(5,4),(6,4),(7,4),(8,4),(9,4),(10,4),
            (2,5),(3,5),(4,5),(5,5),(6,5),(7,5),(8,5),(9,5),
            (3,6),(4,6),(5,6),(6,6),(7,6),(8,6),
            (4,7),(5,7),(6,7)
        ]

        if self.wing == 0:
            wing = [
                (1,4),(2,4),(3,4),
                (1,5),(2,5),(3,5),(4,5),
                (2,6),(3,6),(4,6),(5,6)
            ]

        elif self.wing == 1:
            wing = [
                (1,3),(2,3),(3,3),
                (1,4),(2,4),(3,4),(4,4),
                (2,5),(3,5),(4,5)
            ]

        else:
            wing = [
                (1,5),(2,5),(3,5),
                (1,6),(2,6),(3,6),(4,6),
                (2,7),(3,7),(4,7),(5,7)
            ]

        for x, y in wing:
            pygame.draw.rect(
                screen,
                ORANGE,
                (self.x + x * size, self.y + y * size, size, size)
            )

        for x, y in body:
            pygame.draw.rect(
                screen,
                YELLOW,
                (self.x + x * size, self.y + y * size, size, size)
            )

        pygame.draw.rect(
            screen,
            BLACK,
            (self.x + 8 * size, self.y + 2 * size, size, size)
        )

        pygame.draw.rect(
            screen,
            WHITE,
            (self.x + 9 * size, self.y + 2 * size, size, size)
        )

        beak = [
            (11,3),(12,3),(13,3),
            (11,4),(12,4)
        ]

        for x, y in beak:
            pygame.draw.rect(
                screen,
                ORANGE,
                (self.x + x * size, self.y + y * size, size, size)
            )

    def rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )


class Cloud:

    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def update(self):
        self.x -= self.speed

        if self.x < -60:
            self.x = WIDTH + 20

    def draw(self):

        size = 4

        shape = [
            (2,0),(3,0),(4,0),
            (1,1),(2,1),(3,1),(4,1),(5,1),
            (0,2),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),
            (0,3),(1,3),(2,3),(3,3),(4,3),(5,3),(6,3),
            (1,4),(2,4),(3,4),(4,4),(5,4)
        ]

        for x, y in shape:
            pygame.draw.rect(
                screen,
                WHITE,
                (self.x + x * size,
                 self.y + y * size,
                 size,
                 size)
            )


class Pipe:

    def __init__(self):
        self.x = WIDTH
        self.gap_y = random.randint(150, HEIGHT - 250)
        self.passed = False

    def update(self):
        self.x -= pipe_speed

    def draw(self):

        bottom = self.gap_y + pipe_gap

        pygame.draw.rect(
            screen,
            GREEN,
            (self.x, 0, pipe_width, self.gap_y)
        )

        pygame.draw.rect(
            screen,
            BLACK,
            (self.x, 0, pipe_width, self.gap_y),
            2
        )

        pygame.draw.rect(
            screen,
            GREEN,
            (self.x - 5, self.gap_y - 30, pipe_width + 10, 30)
        )

        pygame.draw.rect(
            screen,
            BLACK,
            (self.x - 5, self.gap_y - 30, pipe_width + 10, 30),
            2
        )

        pygame.draw.rect(
            screen,
            GREEN,
            (self.x, bottom, pipe_width, HEIGHT - bottom)
        )

        pygame.draw.rect(
            screen,
            BLACK,
            (self.x, bottom, pipe_width, HEIGHT - bottom),
            2
        )

        pygame.draw.rect(
            screen,
            GREEN,
            (self.x - 5, bottom, pipe_width + 10, 30)
        )

        pygame.draw.rect(
            screen,
            BLACK,
            (self.x - 5, bottom, pipe_width + 10, 30),
            2
        )

    def hit_player(self, player):

        top = pygame.Rect(
            self.x,
            0,
            pipe_width,
            self.gap_y
        )

        bottom = pygame.Rect(
            self.x,
            self.gap_y + pipe_gap,
            pipe_width,
            HEIGHT
        )

        return player.rect().colliderect(top) or player.rect().colliderect(bottom)


clouds = [
    Cloud(100, 80, 0.5),
    Cloud(250, 120, 0.3),
    Cloud(380, 60, 0.4)
]

player = Player()
pipes = []

score = 0
game_over = False
started = False

countdown = 3
countdown_start = pygame.time.get_ticks()
last_pipe = pygame.time.get_ticks()


running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_SPACE:

                if game_over:
                    player = Player()
                    pipes = []
                    score = 0
                    game_over = False
                    started = False
                    countdown = 3
                    countdown_start = pygame.time.get_ticks()
                    last_pipe = pygame.time.get_ticks()

                elif started:
                    player.jump()

    for cloud in clouds:
        cloud.update()

    if not game_over:

        if not started:

            now = pygame.time.get_ticks()

            if now - countdown_start >= 1000:
                countdown_start = now
                countdown -= 1

                if countdown <= 0:
                    started = True
                    last_pipe = now

        else:

            player.update()

            if player.y < 0:
                game_over = True

            if player.y + player.height > HEIGHT - 50:
                game_over = True

            now = pygame.time.get_ticks()

            if now - last_pipe >= pipe_time:
                pipes.append(Pipe())
                last_pipe = now

            for pipe in pipes[:]:

                pipe.update()

                if pipe.hit_player(player):
                    game_over = True

                if pipe.passed == False:
                    if pipe.x + pipe_width < player.x:
                        pipe.passed = True
                        score += 1

                if pipe.x + pipe_width < 0:
                    pipes.remove(pipe)

    screen.fill(SKY)

    for cloud in clouds:
        cloud.draw()

    for pipe in pipes:
        pipe.draw()

    pygame.draw.rect(
        screen,
        GREEN,
        (0, HEIGHT - 50, WIDTH, 50)
    )

    pygame.draw.rect(
        screen,
        DARK_GREEN,
        (0, HEIGHT - 50, WIDTH, 50),
        3
    )

    for x in range(0, WIDTH, 20):
        pygame.draw.rect(
            screen,
            DARK_GREEN,
            (x, HEIGHT - 48, 8, 8)
        )

        pygame.draw.rect(
            screen,
            DARK_GREEN,
            (x + 10, HEIGHT - 42, 6, 6)
        )

    player.draw()

    if started:
        score_text = str(score)
        width = text_size(score_text, 6)

        pixel_text(
            score_text,
            WIDTH // 2 - width // 2,
            40,
            6,
            WHITE,
            BLACK
        )

    elif countdown > 0:

        number = str(countdown)
        width = text_size(number, 8)

        pixel_text(
            number,
            WIDTH // 2 - width // 2,
            HEIGHT // 2 - 28,
            8,
            WHITE,
            BLACK
        )

    if game_over:

        title = "GAME OVER"
        width = text_size(title, 4)

        pixel_text(
            title,
            WIDTH // 2 - width // 2,
            HEIGHT // 2 - 40,
            4,
            RED,
            BLACK
        )

        text = "PRESS SPACE"
        width = text_size(text, 2)

        pixel_text(
            text,
            WIDTH // 2 - width // 2,
            HEIGHT // 2 + 10,
            2,
            WHITE,
            BLACK
        )

        text = "TO RESTART"
        width = text_size(text, 2)

        pixel_text(
            text,
            WIDTH // 2 - width // 2,
            HEIGHT // 2 + 30,
            2,
            WHITE,
            BLACK
        )

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
