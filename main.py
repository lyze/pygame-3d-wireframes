'''THE GAME'''

import argparse
import logging
import numpy as np
import pygame
import random
import sys

from game import Game
from three_d.viewport import Viewport
from shapes import Cube
from shape_reader import ShapeReader

def get_random_color():
    def random_intensity():
        return int(np.clip(random.normalvariate(0xFF * 4 / 7, 0xFF / 3),
                           0, 0xFF))
    color = random_intensity()
    color <<= 8
    color |= random_intensity()
    color <<= 8
    color |= random_intensity()
    return color

default_playground = [Cube(np.array([-100, -100, 100]), side=50,
                           color=get_random_color()),
                      Cube(np.array([-50, -50, 300]), side=60,
                           color=get_random_color()),
                      Cube(np.array([0, 10, 200]), side=100,
                           color=get_random_color()),
                      Cube(np.array([40, 0, 1000]), side=200,
                           color=get_random_color()),
                      Cube(np.array([100, -50, 220]), side=50,
                           color=get_random_color()),
                      Cube(np.array([0, 0, 550]), side=500,
                           color=get_random_color()),
                      Cube(np.array([120, -30, 200]), side=100,
                           color=get_random_color())]
def main():
    parser = argparse.ArgumentParser(description='Wireframe visualizer')
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
    parser.add_argument('--input-file', '--input', type=str, default=None,
                        help='the name of the file containing a description of \
                        the meshes to draw')
    args = parser.parse_args()

    if args.input_file is None:
        playground = default_playground
    else:
        playground = [ShapeReader(args.input_file).process_file()]

    fps = args.fps
    show_fps = args.show_fps

    logging.basicConfig(level=args.log_level)

    pygame.init()

    pygame.display.set_mode((800, 600))

    main_surface = pygame.display.get_surface()
    gameview = Viewport(main_surface, vertical_fov_deg=args.fov)

    game = Game(gameview, objects=playground)

    pygame.display.flip()

    logging.info('Initializing clock...')
    fps_clock = pygame.time.Clock()

    logging.info('Initializing fonts...')
    if show_fps:
        fps_font = pygame.font.SysFont(None, 10)

    is_mouse_focused = False

    logging.info('Entering main game loop...')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info('Received QUIT event.')
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                game.move_camera(*pygame.mouse.get_rel())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    game.begin_move_forward()
                elif event.key == pygame.K_a:
                    game.begin_move_left()
                elif event.key == pygame.K_d:
                    game.begin_move_right()
                elif event.key == pygame.K_s:
                    game.begin_move_backward()
                else:
                    pass
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.set_grab(not is_mouse_focused)
                    pygame.mouse.set_visible(is_mouse_focused)
                    is_mouse_focused = not is_mouse_focused
                elif event.key == pygame.K_w:
                    game.end_move_forward()
                elif event.key == pygame.K_a:
                    game.end_move_left()
                elif event.key == pygame.K_d:
                    game.end_move_right()
                elif event.key == pygame.K_s:
                    game.end_move_backward()
                else:
                    pass
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
