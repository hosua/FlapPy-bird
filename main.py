#!flappy-venv/bin/python3

import pygame
import os
import sys
import time

from global_vars import *
from flappy_bird import Bird, Pipe, Game
from input_handler import handle_input
from graphics import Graphics

if __name__ == "__main__":
    pygame.init()
    pygame.key.set_repeat(INPUT_REPEAT_DELAY, INPUT_REPEAT_INTERVAL)
    screen = pygame.Surface((SCREEN_W, SCREEN_H))
    actual_screen = pygame.display.set_mode([WINDOW_W, WINDOW_H])

    game = Game(BirdColor.BLUE, BgType.DAY)
    # game = Game(BirdColor.RED, BgType.DAY)
    # game.state = GameState.PLAYING
    clock = pygame.time.Clock()

    gfx = Graphics(screen, actual_screen)
    gfx.update_screen()

    frame: int = 0
    curr_time: int = 0

    while game.is_running:
        event = pygame.event.get()
        handle_input(event, game, gfx)
        curr_time = round(time.time() * 1000)

        match game.state:
            case GameState.PREGAME:
                delta_flap_time = curr_time - game.bird.last_flap_time
                if delta_flap_time >= BIRD_SPR_FLAP_INTERVAL:
                    game.bird.last_flap_time = curr_time
                    game.bird.inc_sprite_index()

                gfx.interpolate_bird(game)

                gfx.draw_bg(game)
                gfx.draw_ground(game)
                gfx.draw_bird(game)

            case GameState.PLAYING:
                gfx.clear_screen()

                delta_flap_time = curr_time - game.bird.last_flap_time
                if delta_flap_time >= BIRD_SPR_FLAP_INTERVAL:
                    game.bird.last_flap_time = curr_time
                    game.bird.inc_sprite_index()

                delta_phys_time = curr_time - game.bird.last_phys_calc_time
                game.bird.last_phys_calc_time = curr_time
                game.run_bird_calcs()
                game.check_collision()

                game.scroll_pipes_left()

                gfx.draw_bg(game)
                gfx.draw_pipe(game)
                gfx.draw_ground(game)
                gfx.draw_bird(game)
                gfx.draw_ui_score(game, game.score)

            case GameState.GAMEOVER:
                game.run_bird_calcs(dead=True)
                gfx.draw_bg(game)
                gfx.draw_pipe(game)
                gfx.draw_ground(game, False)
                gfx.draw_ui_gameover(game)
                gfx.draw_bird_dead(game)

            case _:
                raise Exception(f"Fatal Error: Unknown game state {game.state}")
        gfx.draw_to_actual_screen()
        gfx.update_screen()
        clock.tick(FPS)
        frame += 1

