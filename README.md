# Impossible Flappy Bird

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Top language](https://img.shields.io/github/languages/top/Genius-Progarmmer/impossible-flappy-bird.svg)](https://github.com/Genius-Progarmmer/impossible-flappy-bird)

A standalone Pygame implementation of a Flappy Bird–style game rendered in pixel art.

flappy_bird.py is a single-file Python game that draws all sprites with filled rectangles and a tiny embedded pixel font. It includes animated wings, rotation, procedurally spawned pipes, clouds, a countdown, scoring, and a game-over / restart flow.

## Features
- Pixel-art bird with 3 wing frames and rotation based on velocity
- Randomized top/bottom pipes with configurable gap
- Score counter and "GAME OVER" screen with restart
- Moving clouds background and simple ground tiles
- Tiny built-in pixel font renderer for on-screen text
- Single-file: no external assets required

## Requirements
- Python 3.8+ (should work on newer 3.x)
- Pygame

Install Pygame:
```bash
pip install pygame
