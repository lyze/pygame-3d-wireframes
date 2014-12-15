'''THE GAME'''

import argparse
import logging
import pygame
import sys

from game import Game
from three_d.viewport import Viewport

def main():
    parser = argparse.ArgumentParser(description='Snake game!')
    parser.add_argument('--show-fps', nargs=None, type=bool, default=False,
                        help='whether to display an fps counter')
    parser.add_argument('--fps', type=int, default=60,
                        help='the framerate of the game')
    parser.add_argument('--fov', type=int, default=70,
                        help='the (vertical) field of field of view angle \
                        in degrees')
    parser.add_argument('--log-level', type=int, default=logging.INFO,
                        help='a value in [0, 50] in increments of 10, where 0 \
                        is for all messages, and 50 for only critical errors')
    args = parser.parse_args()

    fps = args.fps
    show_fps = args.show_fps

    logging.basicConfig(level=args.log_level)

    pygame.init()

    pygame.display.set_mode((800, 600))

    main_surface = pygame.display.get_surface()
    gameview = Viewport(main_surface, vertical_fov_deg=args.fov)
    game = Game(gameview)

    pygame.display.flip()

    logging.info('Initializing clock...')
    fps_clock = pygame.time.Clock()

    logging.info('Initializing fonts...')
    if show_fps:
        fps_font = pygame.font.SysFont(None, 10)

    logging.info('Entering main game loop...')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info('Received QUIT event.')
                sys.exit()
            else:
                pass
        fps_clock.tick(fps)
        game.tick()
        pygame.display.update()
        if show_fps:
            fps_text = fps_font.render(fps_clock.get_fps(), False,
                                       (255, 0, 0))
            main_surface.blit(fps_text, (0, 0))

    sys.exit()


if __name__ == "__main__":
    main()
