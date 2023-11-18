import pygame
from global_vars import *

# Game graphics
class Graphics:
    def __init__(self, screen: pygame.Surface, actual_screen: pygame.display):
        self.screen = screen
        self.actual_screen = actual_screen
        self.font = {
            FontSize.SMALL: pygame.font.Font(f"{DIR_FONT}/8bitOperatorPlus-Regular.ttf", 20),
            FontSize.MED: pygame.font.Font(f"{DIR_FONT}/8bitOperatorPlus-Regular.ttf", 25),
            FontSize.LARGE: pygame.font.Font(f"{DIR_FONT}/8bitOperatorPlus-Regular.ttf", 30),
        }

        self.spr_bird = {
            BirdColor.BLUE: [
                pygame.image.load(f"{DIR_SPR_BIRD}/bird-blue-downflap.png"),
                pygame.image.load(f"{DIR_SPR_BIRD}/bird-blue-midflap.png"),
                pygame.image.load(f"{DIR_SPR_BIRD}/bird-blue-upflap.png"),
                pygame.image.load(f"{DIR_SPR_BIRD}/bird-blue-midflap.png"),
            ],
            BirdColor.RED: [
                pygame.image.load(f"{DIR_SPR_BIRD}/bird-red-downflap.png"),
                pygame.image.load(f"{DIR_SPR_BIRD}/bird-red-midflap.png"),
                pygame.image.load(f"{DIR_SPR_BIRD}/bird-red-upflap.png"),
                pygame.image.load(f"{DIR_SPR_BIRD}/bird-red-midflap.png"),
            ],
            BirdColor.YELLOW: [
                pygame.image.load(f"{DIR_SPR_BIRD}/bird-yellow-downflap.png"),
                pygame.image.load(f"{DIR_SPR_BIRD}/bird-yellow-midflap.png"),
                pygame.image.load(f"{DIR_SPR_BIRD}/bird-yellow-upflap.png"),
                pygame.image.load(f"{DIR_SPR_BIRD}/bird-yellow-midflap.png"),
            ],
        }

        self.width = self.spr_bird[BirdColor.BLUE][0].get_width()
        self.height = self.spr_bird[BirdColor.BLUE][0].get_height()

        self.spr_bg = {
            BgType.DAY: pygame.image.load(f"{DIR_SPR_BG}/background-day.png"),
            BgType.NIGHT: pygame.image.load(f"{DIR_SPR_BG}/background-night.png"),
        }

        self.spr_ground = pygame.image.load(f"{DIR_SPR_BG}/ground.png")

        self.spr_pipe = {
            PipeColor.RED: pygame.image.load(f"{DIR_SPR_PIPE}/pipe-red.png"),
            PipeColor.GREEN: pygame.image.load(f"{DIR_SPR_PIPE}/pipe-green.png"),
        }

        self.spr_text = {
            "gameover": pygame.image.load(f"{DIR_SPR_TEXT}/gameover.png"),
        }
        for i in range(10):
            self.spr_text[str(i)] = pygame.image.load(f"{DIR_SPR_TEXT}/{i}.png")

        self.ground_pos:(int,int) = GROUND_POS

        self.bird_y_interpolation:int = 0
        self.bird_interpolation_dir:int = +1
        self.last_interpolate_time:int = 0


    def clear_screen(self):
        self.screen.fill(COLOR_BACKGROUND)

    def update_screen(self):
        pygame.display.flip()

    def draw_ui_text(self, text, pos: (int,int), font_size: FontSize=FontSize.MED, color=COLOR_FONT_FG):
        text_obj = self.font[font_size].render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = pos
        self.screen.blit(text_obj, text_rect)

    def draw_ui_signature(self):
        x, y = UI_SIGNATURE_POS
        self.draw_ui_text("Made by Hoswoo", (x+35, y+20), FontSize.SMALL, COLOR_FONT_FG)

    def draw_ui_gameover(self, game):
        x, y = UI_GAMEOVER_POS
        spr_gameover = self.spr_text["gameover"]
        self.screen.blit(spr_gameover, (x,y))

        pos = (x+10,y+50)
        rect_size = (175, 175)
        rw, rh = rect_size
        pygame.draw.rect(self.screen, COLOR_UI_BG, (pos[0],pos[1],rw,rh), 0, 10)
        pygame.draw.rect(self.screen, COLOR_FONT_FG, (pos[0],pos[1],rw,rh), 2, 10)

        pos = (x+85,y+75)
        self.draw_ui_text("SCORE", pos, FontSize.SMALL, color=COLOR_FONT_FG)
        pos = (x+10,y+90)
        self.draw_ui_score(game, game.score, pos)

        pos = (x+85,y+150)
        self.draw_ui_text("BEST", pos, FontSize.SMALL, color=COLOR_FONT_FG)
        pos = (x+10,y+165)
        self.draw_ui_score(game, game.hiscore, pos)

    def draw_ui_score(self, game, score: int, pos:(int,int)=UI_SCORE_POS):
        x, y = pos
        blank_inc = 10
        for digit in str(score).rjust(9):
            pos = (x,y)
            if not digit == ' ':
                spr = self.spr_text[digit]
                self.screen.blit(spr, pos)
                x += spr.get_width()
            else:
                x += blank_inc

    def draw_bg(self, game):
        x, y = (0,0)
        spr_bg = self.spr_bg[game.bg_type]
        self.screen.blit(spr_bg, (x, y))

    def draw_ground(self, game, moving: bool=True):
        x, y = self.ground_pos
        if moving:
            self.ground_pos = ((x-SCROLL_SPEED), y)
            if x <= -SCREEN_W:
                self.ground_pos = (SCREEN_W+x, y)
        self.screen.blit(self.spr_ground, (x,y))
        self.screen.blit(self.spr_ground, (x+SCREEN_W,y))

    def interpolate_bird(self, game):
        pos_bird = game.bird.pos
        self.bird_y_interpolation += self.bird_interpolation_dir * 0.1
        if self.bird_y_interpolation >= BIRD_INTERPOLATE_Y_MAX or \
            self.bird_y_interpolation <= BIRD_INTERPOLATE_Y_MIN:
            self.bird_interpolation_dir *= -1
        game.bird.pos = (pos_bird[0], pos_bird[1] + self.bird_y_interpolation)

    def draw_bird_dead(self, game):
        bird_color = game.bird.color
        sprites = self.spr_bird[bird_color]
        spr_index = 1
        spr_bird = self.spr_bird[bird_color][spr_index]
        spr_angle = game.bird.angle

        spr_bird_rot = pygame.transform.rotate(spr_bird, spr_angle)
        pos_bird = game.bird.pos
        self.screen.blit(spr_bird_rot, pos_bird)


    def draw_bird_with_interpolation(self, game):
        bird_color = game.bird.color
        sprites = self.spr_bird[bird_color]
        spr_index = game.bird.sprite_index
        spr_bird = self.spr_bird[bird_color][spr_index]

        pos_bird = game.bird.pos
        pos_bird = (pos_bird[0], pos_bird[1] + self.bird_y_interpolation)

        self.screen.blit(spr_bird, pos_bird)

    def draw_bird(self, game):
        bird_color = game.bird.color
        sprites = self.spr_bird[bird_color]
        spr_index = game.bird.sprite_index
        spr_bird = self.spr_bird[bird_color][spr_index]
        spr_angle = game.bird.angle

        spr_bird_rot = pygame.transform.rotate(spr_bird, spr_angle)

        pos_bird = game.bird.pos

        self.screen.blit(spr_bird_rot, pos_bird)

    def draw_pipe(self, game):
        pipe_spr = self.spr_pipe[game.pipe_color]

        for pipe in game.pipes:
            x = pipe.x
            y_top = pipe.y_top
            y_bottom = pipe.y_bottom

            pipe_spr_flipped = pygame.transform.rotate(pipe_spr, 180)
            self.screen.blit(pipe_spr_flipped, (x, y_top))

            self.screen.blit(pipe_spr, (x, y_bottom))


    def draw_to_actual_screen(self):
        transformed_screen = pygame.transform.scale(self.screen, (WINDOW_W, WINDOW_H))
        self.actual_screen.blit(transformed_screen, (0,0))
