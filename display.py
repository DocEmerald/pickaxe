import numpy as np

import sys

import pygame
import pygame.gfxdraw
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from board import Space
from game import Game
from random_bot import RandomPlayer
from pickaxe_bot import Pickaxer
from pacifist_pickaxe_bot import Pacifist_Pickaxer
bg_image = pygame.image.load('Space.jpg')
bg_image_red = pygame.image.load('Space_red.jpg')
bg_image_blue = pygame.image.load('Space_blue.jpg')
def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def hexagon(
    screen: pygame.Surface, x: float, y: float, size: float, color: tuple[int, int, int]
):
    corners = [
        (
            x + 0.9 * size * np.cos(theta),
            y + 0.9 * size * np.sin(theta),
        )
        for theta in np.linspace(0, 2 * np.pi, 6, endpoint=False) + np.pi / 6
    ]
    pygame.gfxdraw.aapolygon(screen, corners, color)
    pygame.gfxdraw.filled_polygon(screen, corners, color)


def draw(screen: pygame.Surface, game: Game):
    if game.winner == None:
        screen.fill((0, 0, 0))
        screen.blit(bg_image, (0,0))
    elif game.winner == Space.RED:
        screen.fill((100, 0, 0))
        screen.blit(bg_image_red, (0,0))
    elif game.winner == Space.BLUE:
        screen.fill((0, 0, 100))
        screen.blit(bg_image_blue, (0,0))
    cell_size = screen.get_width() / (3.5 * game.board.size)
    for coord in game.board.cells:
        q, r = coord[:2]
        x = screen.get_width() / 2 + cell_size * (np.sqrt(3) * q + np.sqrt(3) / 2 * r)
        y = screen.get_height() / 2 + cell_size * 1.5 * r
        contents = game.board.cells[coord]
        if contents == Space.WALL:
            color = (48, 213, 200)
            
        else:
            color = (225, 255, 254)
        hexagon(screen, x, y, cell_size, color)
        if contents == Space.RED:
            pygame.gfxdraw.aacircle(screen, int(x), int(y), int(0.6 * cell_size), (255, 0, 0))
            pygame.gfxdraw.filled_circle(screen, int(x), int(y), int(0.6 * cell_size), (255, 0, 0))
        elif contents == Space.BLUE:
            pygame.gfxdraw.aacircle(screen, int(x), int(y), int(0.6 * cell_size), (0, 0, 255))
            pygame.gfxdraw.filled_circle(screen, int(x), int(y), int(0.6 * cell_size), (0, 0, 255))

    pygame.display.flip()


def runPyGame(game: Game):
    pygame.init()
    pygame.mixer.music.load("Iris.mp3")
    ##pygame.mixer.music.play(-1)

    # Set up the window.
    width, height = 800, 800
    screen = pygame.display.set_mode((width, height))

    while True:
        update()
        draw(screen, game)
        if game.winner is None:
            game.step()


def main():
    player_a, player_b = Pickaxer(), Pacifist_Pickaxer()
    game = Game(player_a, player_b, time_per_move=3, small=True, min_sleep_time=0)
    runPyGame(game)


if __name__ == "__main__":
    main()
