import random
import math
import pygame
from cogworks import GameObject
from cogworks.components.background import Background
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.transform import Transform
from cogworks.components.ui.ui_button import UIButton
from cogworks.components.ui.ui_label import UILabel
from cogworks.components.ui.ui_transform import UITransform
from cogworks.pygame_wrappers.event_manager import EventManager
from cogworks.pygame_wrappers.input_manager import InputManager
from cogworks.pygame_wrappers.window import Window

# --- Constants ---
BALL_SPEED = 200
BALL_ACCELERATION = 20
PADDLE_SPEED = 400
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BALL_SIZE = 20

window_width, window_height = (800, 800)

# --- Dynamic Padding Functions ---
def get_top_padding():
    return window_height * 0.25  # 25% of current window height

def get_bottom_padding():
    return window_height * -0.25  # same as top


# --- Event Handler for Window Resize ---
def handle_window_resize(event):
    global window_width, window_height
    if event.type == pygame.VIDEORESIZE:
        window_width, window_height = Window.get_instance().get_size()


# --- Player Paddle ---
class PlayerPaddleScript(ScriptComponent):
    def __init__(self, speed=PADDLE_SPEED):
        super().__init__()
        self.speed = speed
        self.input_manager = InputManager.get_instance()

    def start(self):
        global window_width, window_height
        window_width, window_height = Window.get_instance().get_size()
        EventManager.get_instance().subscribe(handle_window_resize)

    def update(self, dt):
        transform = self.game_object.get_component(Transform)
        x, y = transform.get_local_position()

        if self.input_manager.is_key_down(pygame.K_w):
            y -= self.speed * dt
        if self.input_manager.is_key_down(pygame.K_s):
            y += self.speed * dt

        # Keep paddle in window with dynamic padding
        half_height = PADDLE_HEIGHT / 2
        y = max(half_height + get_top_padding(), min(window_height - half_height - get_bottom_padding(), y))
        transform.set_local_position(x, y)

    def on_remove(self):
        EventManager.get_instance().unsubscribe(handle_window_resize)


# --- AI Paddle ---
class AIPaddleScript(ScriptComponent):
    def __init__(self, ball=None, speed=PADDLE_SPEED, reaction=0.2):
        super().__init__()
        self.ball = ball
        self.speed = speed
        self.reaction = reaction

    def update(self, dt):
        if not self.ball:
            return

        transform = self.game_object.get_component(Transform)
        paddle_x, paddle_y = transform.get_local_position()
        ball_x, ball_y = self.ball.get_component(Transform).get_local_position()

        if abs(paddle_y - ball_y) > 10:
            direction = 1 if ball_y > paddle_y else -1
            paddle_y += direction * self.speed * dt * self.reaction

        half_height = PADDLE_HEIGHT / 2
        paddle_y = max(half_height + get_top_padding(), min(window_height - half_height - get_bottom_padding(), paddle_y))
        transform.set_local_position(paddle_x, paddle_y)


# --- Ball ---
class BallScript(ScriptComponent):
    def __init__(self, player_paddle, ai_paddle, player_score_obj, ai_score_obj, speed=BALL_SPEED):
        super().__init__()
        self.player_paddle = player_paddle
        self.ai_paddle = ai_paddle
        self.player_score_obj = player_score_obj
        self.ai_score_obj = ai_score_obj
        self.speed = speed
        self.velocity = [0, 0]

    def start(self):
        self.reset_ball()

    def reset_ball(self):
        transform = self.game_object.get_component(Transform)
        transform.set_local_position(window_width // 2, window_height // 2)

        angle = random.uniform(-math.pi / 4, math.pi / 4)
        direction = random.choice([-1, 1])
        self.velocity = [math.cos(angle) * self.speed * direction,
                         math.sin(angle) * self.speed * direction]

    def update(self, dt):
        transform = self.game_object.get_component(Transform)
        x, y = transform.get_local_position()
        x += self.velocity[0] * dt
        y += self.velocity[1] * dt

        # Bounce off top/bottom with dynamic padding
        if y <= BALL_SIZE / 2 + get_top_padding() and self.velocity[1] < 0:
            self.velocity[1] *= -1
        elif y >= window_height - BALL_SIZE / 2 - get_bottom_padding() and self.velocity[1] > 0:
            self.velocity[1] *= -1

        # Paddle collisions
        for paddle in [self.player_paddle, self.ai_paddle]:
            px, py = paddle.get_component(Transform).get_local_position()
            if (abs(x - px) < PADDLE_WIDTH / 2 + BALL_SIZE / 2 and
                    abs(y - py) < PADDLE_HEIGHT / 2 + BALL_SIZE / 2):

                # Flip horizontal velocity
                self.velocity[0] *= -1

                # Move ball outside paddle to prevent sticking
                if x < px:  # ball is on left side of paddle
                    x = px - (PADDLE_WIDTH / 2 + BALL_SIZE / 2)
                else:  # ball is on right side of paddle
                    x = px + (PADDLE_WIDTH / 2 + BALL_SIZE / 2)

                # Add vertical offset based on collision point
                offset = (y - py) / (PADDLE_HEIGHT / 2)
                self.velocity[1] += offset * BALL_ACCELERATION
                break

        # Scoring
        if x <= 0:
            self._increment_score(self.ai_score_obj)
            self.reset_ball()
        elif x >= window_width:
            self._increment_score(self.player_score_obj)
            self.reset_ball()

        transform.set_local_position(x, y)

    def _increment_score(self, score_obj):
        label = score_obj.get_component(UILabel)
        score = int(label.text) + 1
        label.set_text(str(score))


# --- Scene Setup ---
def setup_pong_scene(engine):
    scene = engine.create_scene("Pong", (0, 0))

    # Background
    background = GameObject("Background")
    background.add_component(Sprite("images/sky_background.png"))
    background.add_component(Background())
    scene.add_game_object(background)

    # Player Paddle
    player_paddle = GameObject("PlayerPaddle")
    player_paddle.add_component(Sprite("images/paddle.png"))
    player_paddle.get_component(Transform).set_local_position(50, window_height // 2)
    player_paddle.add_component(PlayerPaddleScript())
    scene.add_game_object(player_paddle)

    # AI Paddle
    ai_paddle = GameObject("AIPaddle")
    ai_paddle.add_component(Sprite("images/paddle.png"))
    ai_paddle.get_component(Transform).set_local_position(window_width - 50, window_height // 2)
    ai_paddle_script = AIPaddleScript()
    ai_paddle.add_component(ai_paddle_script)
    scene.add_game_object(ai_paddle)

    # Scores
    player_score = GameObject("PlayerScore")
    player_score.add_component(UILabel(text="0", font_size=48, color=(255, 255, 255)))
    player_score.add_component(UITransform(x=0.25, y=0.05, anchor="center", relative=True))
    scene.add_game_object(player_score)

    ai_score = GameObject("AIScore")
    ai_score.add_component(UILabel(text="0", font_size=48, color=(255, 255, 255)))
    ai_score.add_component(UITransform(x=0.75, y=0.05, anchor="center", relative=True))
    scene.add_game_object(ai_score)

    # Ball
    ball = GameObject("Ball")
    ball.add_component(Sprite("images/ball.png"))
    ball.get_component(Transform).set_local_position(window_width // 2, window_height // 2)
    ball_script = BallScript(player_paddle, ai_paddle, player_score, ai_score)
    ball.add_component(ball_script)
    scene.add_game_object(ball)

    # Exit button
    def exit_scene(go):
        engine.change_active_scene("Menu")

    exit_btn = GameObject("ExitButton")
    exit_btn.add_component(UITransform(width=0.1, height=0.05, x=1, anchor="topright"))
    exit_btn.add_component(UIButton("Exit", on_click=exit_scene, border_radius=20))
    scene.add_game_object(exit_btn)

    # Assign ball to AI script
    ai_paddle_script.ball = ball

    return scene
