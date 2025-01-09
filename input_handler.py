import pygame

from global_vars import *
from flappy_bird import Game
from sound_handler import sounds

def handle_input(event: pygame.event, game, gfx):

    for e in event:
        if e.type == pygame.QUIT:
            game.is_running = False

        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if game.state == GameState.GAMEOVER:
                game.reset()
                continue
            if game.state == GameState.PREGAME:
                game.state = GameState.PLAYING
            game.bird.flap()

        elif e.type == pygame.KEYDOWN:
            match e.key:
                case InputKey.QUIT.value:
                    game.is_running = False
                case InputKey.FLAP_KB.value:
                    if game.state == GameState.GAMEOVER:
                        game.reset()
                        continue
                    if game.state == GameState.PREGAME:
                        game.state = GameState.PLAYING
                    game.bird.flap()
                case InputKey.PAUSE.value:
                    pass
