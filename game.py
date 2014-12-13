'''THE GAME'''

import argparse
import logging
import pygame
import sys

from three_d import viewport


def main():
    parser = argparse.ArgumentParser(description='Snake game!')
    parser.add_argument('--show-fps', nargs=None, type=bool, default=False,
                        help='whether to display an fps counter')
    parser.add_argument('--fps', type=int, default=60,
                        help='the framerate of the game')
    parser.add_argument('--fov', type=int, default=70,
                        help='the (vertical) field of field of view angle \
                        in degrees')
    args = parser.parse_args()

    # TODO: parse FPS
    fps = args.fps
    show_fps = args.show_fps

    # TODO: parse log level
    logging.basicConfig(level=logging.INFO)

    pygame.init()

    pygame.display.set_mode((800, 600))

    main_display = pygame.display.get_surface()
    gameview = viewport.Viewport(main_display, vertical_fov_deg=args.fov)

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
            if show_fps:
                fps_text = fps_font.render(fps_clock.get_fps(), False,
                                           (255, 0, 0))
                main_display.blit(fps_text, (0, 0))

    sys.exit()


if __name__ == "__main__":
    main()
