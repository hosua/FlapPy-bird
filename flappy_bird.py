from global_vars import *
from sound_handler import sounds

def check_hitbox(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2

    if x1 < x2 + w2 and \
        x1 + w1 > x2 and \
        y1 < y2 + h2 and \
        y1 + h1 > y2:
        # collision detected
        return True
    return False

class Bird:
    def __init__(self, color: BirdColor=BirdColor.BLUE):
        self.color: BirdColor=color
        self.reset()

    def reset(self):
        self.pos: (int,int)=BIRD_POS_START
        self.angle: int = 0

        # physics
        self.y_vel: float = 0.0

        self.y_vel_prev: float = 0.0
        self.last_phys_calc_time: int = 0

        # for animation
        self.last_flap_time: int = 0
        self.sprite_index: int = 0

    def inc_sprite_index(self):
        self.sprite_index = (self.sprite_index + 1) % BIRD_SPR_COUNT

    def print_phys_info(self):
        print(f"\
pos: {self.pos}\n\
angle: {self.angle}\n\
y_vel: {self.y_vel}\n\
              ")

    def calc_gravity(self):
        self.y_vel -= GRAVITY_ACCEL
        self.y_vel = min(VEL_Y_MAX, max(VEL_Y_MIN, self.y_vel))

    def calc_pos(self):
        gy = GROUND_POS[1]
        x = self.pos[0]
        y = min(self.pos[1]+self.y_vel, gy-BIRD_H)
        self.pos = (x, y)

    def calc_angle(self):
        self.angle = -(self.y_vel * 4) + 20

    def calc_angle_dead(self):
        self.angle = -(self.y_vel * 15) + 35

    def flap(self):
        self.y_vel -= FLAP_STRENGTH
        self.calc_pos()
        sounds["flap"].play()

class Pipe:
    def __init__(self, y_top: int, y_bottom: int, x: int=PIPE_X_START):
        self.x: int=x
        self.y_top: int=y_top
        self.y_bottom: int=y_bottom
        self.counted = False


class Game:
    def __init__(self, bird_color: BirdColor=BirdColor.BLUE,
                 bg_type: BgType=BgType.DAY,
                 pipe_color: PipeColor=PipeColor.GREEN):
        self.is_running: bool = True
        self.bird = Bird(bird_color)
        self.reset()
        self.bg_type: BgType = bg_type
        self.pipe_color = pipe_color

    def reset(self):
        self.state = GameState.PREGAME
        self.score: int = 0
        self.hiscore: int = 0
        self.load_hiscore()
        self.bird.reset()
        self.pipes: list[Pipe] = []
        self.prev_pipe = {
            "y_top": PIPE_Y_TOP_START,
            "y_bottom": PIPE_Y_BOTTOM_START,
        }
        self.populate_pipes()

    def kill_bird(self):
        self.state = GameState.GAMEOVER
        self.bird.y_vel = 10
        self.save_hiscore()
        sounds["die"].play()

    def check_collision(self):
        bx, by = self.bird.pos
        bird_rect = (bx, by, BIRD_W, BIRD_H)

        bw, bh = BIRD_SPR_DIM
        gx, gy = GROUND_POS
        # check collision against ground & roof
        if by >= (gy - bh) or by <= 0:
            self.kill_bird()

        # check collision against pipes
        for pipe in self.pipes:
            pipe_rect_top = (pipe.x, pipe.y_top, PIPE_W, PIPE_H)
            pipe_rect_bottom = (pipe.x, pipe.y_bottom, PIPE_W, PIPE_H)

            if check_hitbox(bird_rect, pipe_rect_top) or \
                    check_hitbox(bird_rect, pipe_rect_bottom):
                self.kill_bird()

    def generate_rand_pipe(self, x:int=PIPE_X_START) -> Pipe:
        import random
        next_pipe_y_top: int = random.randint(PIPE_Y_MIN, PIPE_Y_MAX)

        next_pipe_y_delta: int = random.randint(PIPE_Y_GAP_MIN,
                                                PIPE_Y_GAP_MAX)
        next_pipe_y_bottom: int = next_pipe_y_top + next_pipe_y_delta
        new_pipe = Pipe(next_pipe_y_top, next_pipe_y_bottom, x)

        return new_pipe

    def populate_pipes(self):
        x:int = PIPE_X_START
        x_gap:int = PIPE_X_GAP
        for i in range(2):
            x += x_gap
            new_pipe = self.generate_rand_pipe(x)
            self.pipes.append(new_pipe)

    def scroll_pipes_left(self):
        for pipe in self.pipes:
            pipe.x -= SCROLL_SPEED
            if not pipe.counted and pipe.x <= self.bird.pos[0]:
                pipe.counted = True
                self.score += 1
            if pipe.x+PIPE_W+2 < 0:
                self.pipes.pop(0)
                new_pipe = self.generate_rand_pipe()
                self.pipes.append(new_pipe)

    def run_bird_calcs(self, dead: bool=False):
        self.bird.calc_gravity()
        self.bird.calc_pos()
        if not dead:
            self.bird.calc_angle()
        else:
            self.bird.calc_angle_dead()

    def save_hiscore(self):
        print("saving hiscore")
        import os
        import pickle
        self.load_hiscore()
        self.hiscore = max(self.hiscore, self.score)
        data = { 'hiscore': self.hiscore }
        with open(FILE_HISCORE, 'wb') as f:
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

    def load_hiscore(self):
        import os
        import pickle
        if os.path.exists(FILE_HISCORE):
            with open(FILE_HISCORE, 'rb') as f:
                self.hiscore = pickle.load(f)['hiscore']
        else:
            self.hiscore = 0
        print(f"loaded hiscore {self.hiscore}")
