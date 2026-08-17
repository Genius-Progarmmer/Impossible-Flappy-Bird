import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)
GREEN = (34, 139, 34)
YELLOW = (255, 200, 0)
ORANGE = (255, 140, 0)
RED = (255, 0, 0)
DARK_GREEN = (20, 100, 20)
LIGHT_BLUE = (200, 230, 255)

BIRD_WIDTH = 56
BIRD_HEIGHT = 32
BIRD_X = 100
GRAVITY = 0.5
FLAP_STRENGTH = -10

PIPE_WIDTH = 70
PIPE_GAP = 250
PIPE_SPEED = 3
PIPE_SPAWN_INTERVAL = 1500

PIXEL_FONT = {
    "0": [(1, 0), (2, 0), (3, 0), (0, 1), (4, 1), (0, 2), (4, 2), (0, 3), (4, 3), (0, 4), (4, 4), (0, 5), (4, 5), (1, 6), (2, 6), (3, 6)],
    "1": [(2, 0), (1, 1), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (1, 6), (2, 6), (3, 6)],
    "2": [(1, 0), (2, 0), (3, 0), (0, 1), (4, 1), (4, 2), (3, 3), (2, 4), (1, 5), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6)],
    "3": [(1, 0), (2, 0), (3, 0), (0, 1), (4, 1), (4, 2), (2, 3), (3, 3), (4, 4), (0, 5), (4, 5), (1, 6), (2, 6), (3, 6)],
    "4": [(0, 0), (4, 0), (0, 1), (4, 1), (0, 2), (4, 2), (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (4, 4), (4, 5), (4, 6)],
    "5": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 3), (4, 4), (4, 5), (0, 6), (1, 6), (2, 6), (3, 6)],
    "6": [(1, 0), (2, 0), (3, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 3), (0, 4), (4, 4), (0, 5), (4, 5), (1, 6), (2, 6), (3, 6)],
    "7": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (3, 2), (3, 3), (2, 4), (2, 5), (2, 6)],
    "8": [(1, 0), (2, 0), (3, 0), (0, 1), (4, 1), (0, 2), (4, 2), (1, 3), (2, 3), (3, 3), (0, 4), (4, 4), (0, 5), (4, 5), (1, 6), (2, 6), (3, 6)],
    "9": [(1, 0), (2, 0), (3, 0), (0, 1), (4, 1), (0, 2), (4, 2), (1, 3), (2, 3), (3, 3), (4, 3), (4, 4), (4, 5), (1, 6), (2, 6), (3, 6)],
    "G": [(1, 0), (2, 0), (3, 0), (0, 1), (4, 1), (0, 2), (0, 3), (2, 3), (3, 3), (4, 3), (0, 4), (4, 4), (0, 5), (4, 5), (1, 6), (2, 6), (3, 6)],
    "A": [(2, 0), (1, 1), (3, 1), (0, 2), (4, 2), (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (0, 4), (4, 4), (0, 5), (4, 5), (0, 6), (4, 6)],
    "M": [(0, 0), (4, 0), (0, 1), (1, 1), (3, 1), (4, 1), (0, 2), (2, 2), (4, 2), (0, 3), (4, 3), (0, 4), (4, 4), (0, 5), (4, 5), (0, 6), (4, 6)],
    "E": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 3), (0, 4), (0, 5), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6)],
    "O": [(1, 0), (2, 0), (3, 0), (0, 1), (4, 1), (0, 2), (4, 2), (0, 3), (4, 3), (0, 4), (4, 4), (0, 5), (4, 5), (1, 6), (2, 6), (3, 6)],
    "V": [(0, 0), (4, 0), (0, 1), (4, 1), (0, 2), (4, 2), (0, 3), (4, 3), (1, 4), (3, 4), (1, 5), (3, 5), (2, 6)],
    "R": [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (4, 1), (0, 2), (4, 2), (0, 3), (1, 3), (2, 3), (3, 3), (0, 4), (3, 4), (0, 5), (4, 5), (0, 6), (4, 6)],
    "P": [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (4, 1), (0, 2), (4, 2), (0, 3), (1, 3), (2, 3), (3, 3), (0, 4), (0, 5), (0, 6)],
    "S": [(1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (0, 2), (1, 3), (2, 3), (3, 3), (4, 4), (4, 5), (0, 6), (1, 6), (2, 6), (3, 6)],
    "C": [(1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 6), (2, 6), (3, 6), (4, 6)],
    "T": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)],
    " ": [],
}


def draw_pixel_text(screen, text, x, y, pixel_size, color, shadow_color=None):
    """Draw text using pixel font"""
    offset_x = 0
    for char in text.upper():
        if char in PIXEL_FONT:
            pixels = PIXEL_FONT[char]
            if shadow_color:
                for px, py in pixels:
                    pygame.draw.rect(screen, shadow_color,
                                     (x + offset_x + px * pixel_size + pixel_size,
                                      y + py * pixel_size + pixel_size,
                                      pixel_size, pixel_size))
            for px, py in pixels:
                pygame.draw.rect(screen, color,
                                 (x + offset_x + px * pixel_size,
                                  y + py * pixel_size,
                                  pixel_size, pixel_size))
            offset_x += 6 * pixel_size
    return offset_x


def get_pixel_text_width(text, pixel_size):
    """Calculate the width of pixel text"""
    return len(text) * 6 * pixel_size


class Cloud:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.pixel_size = 4

    def update(self):
        self.x -= self.speed
        if self.x < -60:
            self.x = SCREEN_WIDTH + 20

    def draw(self, screen):
        ps = self.pixel_size
        cloud_pixels = [
            (2, 0), (3, 0), (4, 0),
            (1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
            (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2),
            (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3),
            (1, 4), (2, 4), (3, 4), (4, 4), (5, 4),
        ]
        for px, py in cloud_pixels:
            pygame.draw.rect(screen, WHITE, (self.x + px *
                             ps, self.y + py * ps, ps, ps))


class Bird:
    def __init__(self):
        self.x = BIRD_X
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.width = BIRD_WIDTH
        self.height = BIRD_HEIGHT
        self.pixel_size = 4
        self.wing_frame = 0
        self.wing_timer = 0
        self.rotation = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH
        self.wing_frame = 0

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

        self.wing_timer += 1
        if self.wing_timer > 5:
            self.wing_timer = 0
            self.wing_frame = (self.wing_frame + 1) % 3

        self.rotation = min(max(self.velocity * 3, -30), 60)

    def draw(self, screen):
        ps = self.pixel_size

        body_pixels = [
            (4, 0), (5, 0), (6, 0), (7, 0), (8, 0),
            (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1),
            (2, 2), (3, 2), (4, 2), (5, 2), (6,
                                             2), (7, 2), (8, 2), (9, 2), (10, 2),
            (2, 3), (3, 3), (4, 3), (5, 3), (6,
                                             3), (7, 3), (8, 3), (9, 3), (10, 3),
            (2, 4), (3, 4), (4, 4), (5, 4), (6,
                                             4), (7, 4), (8, 4), (9, 4), (10, 4),
            (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
            (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6),
            (4, 7), (5, 7), (6, 7),
        ]

        eye_pixels = [(8, 2), (9, 2), (8, 3), (9, 3)]

        eye_white = [(9, 2)]

        beak_pixels = [
            (11, 3), (12, 3), (13, 3),
            (11, 4), (12, 4),
        ]

        if self.wing_frame == 0:
            wing_pixels = [
                (1, 4), (2, 4), (3, 4),
                (1, 5), (2, 5), (3, 5), (4, 5),
                (2, 6), (3, 6), (4, 6), (5, 6),
            ]
        elif self.wing_frame == 1:
            wing_pixels = [
                (1, 3), (2, 3), (3, 3),
                (1, 4), (2, 4), (3, 4), (4, 4),
                (2, 5), (3, 5), (4, 5),
            ]
        else:
            wing_pixels = [
                (1, 5), (2, 5), (3, 5),
                (1, 6), (2, 6), (3, 6), (4, 6),
                (2, 7), (3, 7), (4, 7), (5, 7),
            ]

        for px, py in wing_pixels:
            pygame.draw.rect(screen, ORANGE, (self.x + px *
                             ps, self.y + py * ps, ps, ps))

        for px, py in body_pixels:
            pygame.draw.rect(screen, YELLOW, (self.x + px *
                             ps, self.y + py * ps, ps, ps))

        for px, py in eye_pixels:
            pygame.draw.rect(screen, BLACK, (self.x + px *
                             ps, self.y + py * ps, ps, ps))

        for px, py in eye_white:
            pygame.draw.rect(screen, WHITE, (self.x + px *
                             ps, self.y + py * ps, ps, ps))

        for px, py in beak_pixels:
            pygame.draw.rect(screen, ORANGE, (self.x + px *
                             ps, self.y + py * ps, ps, ps))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.width = PIPE_WIDTH
        self.gap_y = random.randint(150, SCREEN_HEIGHT - 250)
        self.scored = False

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.gap_y))
        pygame.draw.rect(screen, BLACK, (self.x, 0, self.width, self.gap_y), 2)
        pygame.draw.rect(screen, GREEN, (self.x - 5,
                         self.gap_y - 30, self.width + 10, 30))
        pygame.draw.rect(screen, BLACK, (self.x - 5,
                         self.gap_y - 30, self.width + 10, 30), 2)

        bottom_y = self.gap_y + PIPE_GAP
        pygame.draw.rect(screen, GREEN, (self.x, bottom_y,
                         self.width, SCREEN_HEIGHT - bottom_y))
        pygame.draw.rect(screen, BLACK, (self.x, bottom_y,
                         self.width, SCREEN_HEIGHT - bottom_y), 2)
        pygame.draw.rect(screen, GREEN, (self.x - 5,
                         bottom_y, self.width + 10, 30))
        pygame.draw.rect(screen, BLACK, (self.x - 5,
                         bottom_y, self.width + 10, 30), 2)

    def collides_with(self, bird):
        bird_rect = bird.get_rect()
        top_pipe = pygame.Rect(self.x, 0, self.width, self.gap_y)
        bottom_pipe = pygame.Rect(
            self.x, self.gap_y + PIPE_GAP, self.width, SCREEN_HEIGHT)
        return bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe)

    def is_off_screen(self):
        return self.x + self.width < 0


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.clouds = [
            Cloud(100, 80, 0.5),
            Cloud(250, 120, 0.3),
            Cloud(380, 60, 0.4),
        ]
        self.reset_game()

    def reset_game(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.game_started = False
        self.countdown = 3
        self.countdown_timer = pygame.time.get_ticks()
        self.last_pipe_time = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset_game()
                    elif self.game_started:
                        self.bird.flap()
                if event.key == pygame.K_ESCAPE:
                    return False
        return True

    def update(self):
        for cloud in self.clouds:
            cloud.update()

        if self.game_over:
            return

        if not self.game_started:
            current_time = pygame.time.get_ticks()
            if current_time - self.countdown_timer > 1000:
                self.countdown_timer = current_time
                self.countdown -= 1
                if self.countdown <= 0:
                    self.game_started = True
                    self.last_pipe_time = current_time
            return

        self.bird.update()

        if self.bird.y > SCREEN_HEIGHT - 50 - self.bird.height or self.bird.y < 0:
            self.game_over = True

        current_time = pygame.time.get_ticks()
        if current_time - self.last_pipe_time > PIPE_SPAWN_INTERVAL:
            self.pipes.append(Pipe())
            self.last_pipe_time = current_time

        for pipe in self.pipes[:]:
            pipe.update()

            if pipe.collides_with(self.bird):
                self.game_over = True

            if not pipe.scored and pipe.x + pipe.width < self.bird.x:
                pipe.scored = True
                self.score += 1
            if pipe.is_off_screen():
                self.pipes.remove(pipe)

    def draw(self):
        self.screen.fill(BLUE)

        for cloud in self.clouds:
            cloud.draw(self.screen)

        for pipe in self.pipes:
            pipe.draw(self.screen)

        pygame.draw.rect(self.screen, GREEN,
                         (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        pygame.draw.rect(self.screen, DARK_GREEN,
                         (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50), 3)

        for i in range(0, SCREEN_WIDTH, 20):
            pygame.draw.rect(self.screen, DARK_GREEN,
                             (i, SCREEN_HEIGHT - 48, 8, 8))
            pygame.draw.rect(self.screen, DARK_GREEN,
                             (i + 10, SCREEN_HEIGHT - 42, 6, 6))

        self.bird.draw(self.screen)

        if not self.game_started and self.countdown > 0:
            countdown_str = str(self.countdown)
            text_width = get_pixel_text_width(countdown_str, 8)
            draw_pixel_text(self.screen, countdown_str,
                            SCREEN_WIDTH // 2 - text_width // 2,
                            SCREEN_HEIGHT // 2 - 28,
                            8, WHITE, BLACK)

        if self.game_started:
            score_str = str(self.score)
            text_width = get_pixel_text_width(score_str, 6)
            draw_pixel_text(self.screen, score_str,
                            SCREEN_WIDTH // 2 - text_width // 2,
                            40,
                            6, WHITE, BLACK)

        if self.game_over:
            game_over_text = "GAME OVER"
            text_width = get_pixel_text_width(game_over_text, 4)
            draw_pixel_text(self.screen, game_over_text,
                            SCREEN_WIDTH // 2 - text_width // 2,
                            SCREEN_HEIGHT // 2 - 40,
                            4, RED, BLACK)

            press_text = "PRESS SPACE"
            text_width = get_pixel_text_width(press_text, 2)
            draw_pixel_text(self.screen, press_text,
                            SCREEN_WIDTH // 2 - text_width // 2,
                            SCREEN_HEIGHT // 2 + 10,
                            2, WHITE, BLACK)

            restart_text = "TO RESTART"
            text_width = get_pixel_text_width(restart_text, 2)
            draw_pixel_text(self.screen, restart_text,
                            SCREEN_WIDTH // 2 - text_width // 2,
                            SCREEN_HEIGHT // 2 + 30,
                            2, WHITE, BLACK)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
