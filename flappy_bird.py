import pygame
import random
import sys
import math
from array import array

pygame.init()
pygame.mixer.init()

w = 400
h = 600
fps = 60

screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)
sky = (135, 206, 235)
green = (34, 139, 34)
dark_green = (20, 100, 20)
yellow = (255, 200, 0)
orange = (255, 140, 0)
red = (255, 0, 0)

bird_x = 100
bird_w = 56
bird_h = 32

gravity = .5
jump_power = -10

pipe_w = 70
pipe_gap = 250
pipe_speed = 3
pipe_delay = 1500

sound_on = True
sound_btn = pygame.Rect(10, 10, 90, 30)


def make_sound(start, end, length, vol):
    rate = 44100
    data = array("h")
    count = int(rate * length)

    for i in range(count):
        t = i / count
        freq = start + (end - start) * t

        fade = 1

        if t < .1:
            fade = t / .1
        elif t > .8:
            fade = (1 - t) / .2

        v = int(
            32767
            * vol
            * fade
            * math.sin(2 * math.pi * freq * i / rate)
        )

        data.append(v)

    return pygame.mixer.Sound(buffer=data)


s3 = make_sound(420, 520, .14, .16)
s2 = make_sound(500, 600, .14, .16)
s1 = make_sound(580, 700, .16, .16)

jump_s = make_sound(500, 900, .09, .13)
pipe_s = make_sound(260, 180, .12, .10)
lose_s = make_sound(420, 100, .35, .16)


def play(s):
    if sound_on:
        s.play()


font = {
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


def text(txt, x, y, size, color, shadow=None):
    pos = 0

    for ch in txt.upper():
        if ch not in font:
            continue

        for px, py in font[ch]:
            if shadow:
                pygame.draw.rect(
                    screen,
                    shadow,
                    (
                        x + pos + px * size + size,
                        y + py * size + size,
                        size,
                        size
                    )
                )

        for px, py in font[ch]:
            pygame.draw.rect(
                screen,
                color,
                (
                    x + pos + px * size,
                    y + py * size,
                    size,
                    size
                )
            )

        pos += size * 6


def txt_w(txt, size):
    return len(txt) * size * 6


class Bird:

    def __init__(self):
        self.x = bird_x
        self.y = h // 2
        self.v = 0
        self.w = bird_w
        self.h = bird_h
        self.wing = 0
        self.wing_t = 0

    def jump(self):
        self.v = jump_power
        self.wing = 0

    def update(self):
        self.v += gravity
        self.y += self.v

        self.wing_t += 1

        if self.wing_t >= 6:
            self.wing_t = 0
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

        for px, py in wing:
            pygame.draw.rect(
                screen,
                orange,
                (
                    self.x + px * size,
                    self.y + py * size,
                    size,
                    size
                )
            )

        for px, py in body:
            pygame.draw.rect(
                screen,
                yellow,
                (
                    self.x + px * size,
                    self.y + py * size,
                    size,
                    size
                )
            )

        pygame.draw.rect(
            screen,
            black,
            (self.x + 8 * size, self.y + 2 * size, size, size)
        )

        pygame.draw.rect(
            screen,
            white,
            (self.x + 9 * size, self.y + 2 * size, size, size)
        )

        beak = [
            (11,3),(12,3),(13,3),
            (11,4),(12,4)
        ]

        for px, py in beak:
            pygame.draw.rect(
                screen,
                orange,
                (
                    self.x + px * size,
                    self.y + py * size,
                    size,
                    size
                )
            )

    def rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.w,
            self.h
        )


class Cloud:

    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def update(self):
        self.x -= self.speed

        if self.x < -60:
            self.x = w + 20

    def draw(self):
        size = 4

        shape = [
            (2,0),(3,0),(4,0),
            (1,1),(2,1),(3,1),(4,1),(5,1),
            (0,2),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),
            (0,3),(1,3),(2,3),(3,3),(4,3),(5,3),(6,3),
            (1,4),(2,4),(3,4),(4,4),(5,4)
        ]

        for px, py in shape:
            pygame.draw.rect(
                screen,
                white,
                (
                    self.x + px * size,
                    self.y + py * size,
                    size,
                    size
                )
            )


class Pipe:

    def __init__(self):
        self.x = w
        self.gap_y = random.randint(150, h - 250)
        self.passed = False

    def update(self):
        self.x -= pipe_speed

    def draw(self):
        bottom = self.gap_y + pipe_gap

        pygame.draw.rect(
            screen,
            green,
            (self.x, 0, pipe_w, self.gap_y)
        )

        pygame.draw.rect(
            screen,
            black,
            (self.x, 0, pipe_w, self.gap_y),
            2
        )

        pygame.draw.rect(
            screen,
            green,
            (self.x - 5, self.gap_y - 30, pipe_w + 10, 30)
        )

        pygame.draw.rect(
            screen,
            black,
            (self.x - 5, self.gap_y - 30, pipe_w + 10, 30),
            2
        )

        pygame.draw.rect(
            screen,
            green,
            (self.x, bottom, pipe_w, h - bottom)
        )

        pygame.draw.rect(
            screen,
            black,
            (self.x, bottom, pipe_w, h - bottom),
            2
        )

        pygame.draw.rect(
            screen,
            green,
            (self.x - 5, bottom, pipe_w + 10, 30)
        )

        pygame.draw.rect(
            screen,
            black,
            (self.x - 5, bottom, pipe_w + 10, 30),
            2
        )

    def hit(self, bird):
        top = pygame.Rect(
            self.x,
            0,
            pipe_w,
            self.gap_y
        )

        bottom = pygame.Rect(
            self.x,
            self.gap_y + pipe_gap,
            pipe_w,
            h
        )

        r = bird.rect()

        return r.colliderect(top) or r.colliderect(bottom)


clouds = [
    Cloud(100, 80, .5),
    Cloud(250, 120, .3),
    Cloud(380, 60, .4)
]

bird = Bird()
pipes = []

score = 0
over = False
started = False
lost = False

count = 3
count_t = pygame.time.get_ticks()
pipe_t = pygame.time.get_ticks()

play(s3)

run = True

while run:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                run = False

            if event.key == pygame.K_SPACE:

                if over:
                    bird = Bird()
                    pipes = []
                    score = 0
                    over = False
                    started = False
                    lost = False
                    count = 3

                    count_t = pygame.time.get_ticks()
                    pipe_t = pygame.time.get_ticks()

                    play(s3)

                elif started:
                    bird.jump()
                    play(jump_s)

        if event.type == pygame.MOUSEBUTTONDOWN:

            if sound_btn.collidepoint(event.pos):
                sound_on = not sound_on

    for cloud in clouds:
        cloud.update()

    if not over:

        if not started:

            now = pygame.time.get_ticks()

            if now - count_t >= 1000:
                count_t = now

                if count == 3:
                    play(s3)
                elif count == 2:
                    play(s2)
                elif count == 1:
                    play(s1)

                count -= 1

                if count <= 0:
                    started = True
                    pipe_t = now

        else:

            bird.update()

            if bird.y < 0 or bird.y + bird.h > h - 50:
                over = True

            now = pygame.time.get_ticks()

            if now - pipe_t >= pipe_delay:
                pipes.append(Pipe())
                play(pipe_s)
                pipe_t = now

            for p in pipes[:]:

                p.update()

                if p.hit(bird):
                    over = True

                if not p.passed and p.x + pipe_w < bird.x:
                    p.passed = True
                    score += 1

                if p.x + pipe_w < 0:
                    pipes.remove(p)

    if over and not lost:
        play(lose_s)
        lost = True

    screen.fill(sky)

    for cloud in clouds:
        cloud.draw()

    for p in pipes:
        p.draw()

    pygame.draw.rect(
        screen,
        green,
        (0, h - 50, w, 50)
    )

    pygame.draw.rect(
        screen,
        dark_green,
        (0, h - 50, w, 50),
        3
    )

    for x in range(0, w, 20):

        pygame.draw.rect(
            screen,
            dark_green,
            (x, h - 48, 8, 8)
        )

        pygame.draw.rect(
            screen,
            dark_green,
            (x + 10, h - 42, 6, 6)
        )

    bird.draw()

    pygame.draw.rect(
        screen,
        white,
        sound_btn
    )

    pygame.draw.rect(
        screen,
        black,
        sound_btn,
        2
    )

    if sound_on:
        text(
            "SOUND",
            20,
            18,
            2,
            black
        )
    else:
        text(
            "MUTED",
            20,
            18,
            2,
            red
        )

    if started:

        s = str(score)
        sw = txt_w(s, 6)

        text(
            s,
            w // 2 - sw // 2,
            40,
            6,
            white,
            black
        )

    elif count > 0:

        s = str(count)
        sw = txt_w(s, 8)

        text(
            s,
            w // 2 - sw // 2,
            h // 2 - 28,
            8,
            white,
            black
        )

    if over:

        s = "GAME OVER"
        sw = txt_w(s, 4)

        text(
            s,
            w // 2 - sw // 2,
            h // 2 - 40,
            4,
            red,
            black
        )

        s = "PRESS SPACE"
        sw = txt_w(s, 2)

        text(
            s,
            w // 2 - sw // 2,
            h // 2 + 10,
            2,
            white,
            black
        )

        s = "TO RESTART"
        sw = txt_w(s, 2)

        text(
            s,
            w // 2 - sw // 2,
            h // 2 + 30,
            2,
            white,
            black
        )

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
sys.exit()
