import random
import math
import pygame
from cogworks import GameObject
from cogworks.components.background import Background
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.transform import Transform
from cogworks.components.trigger_collider import TriggerCollider
from cogworks.components.ui.ui_button import UIButton
from cogworks.components.ui.ui_label import UILabel
from cogworks.components.ui.ui_transform import UITransform
from cogworks.pygame_wrappers.input_manager import InputManager

# --- Constants ---
BALL_SPEED = 250
BALL_ACCELERATION = 200
PADDLE_SPEED = 400
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_X_OFFSET = 50
BALL_SIZE = 20

# --- Helper Functions ---
def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))


# --- Player Paddle Script ---
class PlayerPaddleScript(ScriptComponent):
    def __init__(self, speed=PADDLE_SPEED):
        super().__init__()
        self.speed = speed
        self.input_manager = InputManager.get_instance()
        self.transform = None
        self.camera= None

    def start(self):
        self.transform = self.game_object.transform
        self.camera = self.game_object.scene.camera_component
        start_x, start_y = self.camera.get_world_position_of_point("leftcenter")
        self.transform.set_local_position(start_x + PADDLE_X_OFFSET, start_y)

    def update(self, dt):
        x, y = self.transform.get_local_position()

        if self.input_manager.is_key_down(pygame.K_w):
            y -= self.speed * dt
        if self.input_manager.is_key_down(pygame.K_s):
            y += self.speed * dt

        top, bottom, _, _ = self.camera.get_bounds()
        self.transform.set_local_position(x, clamp(y, top + PADDLE_HEIGHT/2, bottom - PADDLE_HEIGHT/2))


# --- AI Paddle Script ---
class AIPaddleScript(ScriptComponent):
    def __init__(self, ball=None, speed=PADDLE_SPEED, reaction=0.15):
        super().__init__()
        self.ball = ball
        self.speed = speed
        self.reaction = reaction
        self.transform = None
        self.camera = None

    def start(self):
        self.transform = self.game_object.transform
        self.camera = self.game_object.scene.camera_component
        start_x, start_y = self.camera.get_world_position_of_point("rightcenter",)
        self.transform.set_local_position(start_x - PADDLE_X_OFFSET, start_y)

    def update(self, dt):
        if not self.ball:
            return

        px, py = self.transform.get_local_position()
        _, ball_y = self.ball.get_component(Transform).get_local_position()

        if abs(py - ball_y) > 5:
            direction = 1 if ball_y > py else -1
            py += direction * self.speed * dt * self.reaction

        top, bottom, _, _ = self.camera.get_bounds()
        self.transform.set_local_position(px, clamp(py, top + PADDLE_HEIGHT/2, bottom - PADDLE_HEIGHT/2))


# --- Ball Script ---
class BallScript(ScriptComponent):
    def __init__(self, player_paddle, ai_paddle, player_score_obj, ai_score_obj, speed=BALL_SPEED):
        super().__init__()
        self.player_paddle = player_paddle
        self.ai_paddle = ai_paddle
        self.player_score_obj = player_score_obj
        self.ai_score_obj = ai_score_obj
        self.speed = speed
        self.velocity = [0, 0]
        self.transform = None
        self.camera = None

    def start(self):
        self.transform = self.game_object.transform
        self.camera = self.game_object.scene.camera_component
        start_x, start_y = self.camera.get_world_position_of_point("center")
        self.transform.set_local_position(start_x, start_y)
        self.reset_ball()

    def reset_ball(self):
        x, y = self.camera.get_world_position_of_point("center")
        self.transform.set_local_position(x, y)
        angle = random.uniform(-math.pi/4, math.pi/4)
        direction = random.choice([-1, 1])
        self.velocity = [math.cos(angle) * self.speed * direction, math.sin(angle) * self.speed]

    def update(self, dt):
        x, y = self.transform.get_local_position()
        x += self.velocity[0] * dt
        y += self.velocity[1] * dt

        top, bottom, left, right = self.camera.get_bounds()

        # Bounce off top/bottom
        if y - BALL_SIZE / 2 < top and self.velocity[1] < 0:
            self.velocity[1] *= -1
            y = top + BALL_SIZE / 2
        elif y + BALL_SIZE / 2 > bottom and self.velocity[1] > 0:
            self.velocity[1] *= -1
            y = bottom - BALL_SIZE / 2

        # Bounce off left/right walls
        if x - BALL_SIZE / 2 < left and self.velocity[0] < 0:
            self.velocity[0] *= -1
            x = left + BALL_SIZE / 2
            self._increment_score(self.ai_score_obj)
        elif x + BALL_SIZE / 2 > right and self.velocity[0] > 0:
            self.velocity[0] *= -1
            x = right - BALL_SIZE / 2
            self._increment_score(self.player_score_obj)

        self.transform.set_local_position(x, y)

    def on_trigger_enter(self, other_collider):
        if other_collider.game_object in [self.player_paddle, self.ai_paddle]:
            paddle = other_collider.game_object
            px, py = paddle.get_component(Transform).get_local_position()
            transform = self.game_object.get_component(Transform)
            x, y = transform.get_local_position()

            # Reflect horizontally
            self.velocity[0] *= -1
            x = px - (PADDLE_WIDTH/2 + BALL_SIZE/2) if x < px else px + (PADDLE_WIDTH/2 + BALL_SIZE/2)

            # Add vertical offset
            offset = (y - py) / (PADDLE_HEIGHT/2)
            self.velocity[1] += offset * BALL_ACCELERATION

            transform.set_local_position(x, y)

    def _increment_score(self, score_obj):
        label = score_obj.get_component(UILabel)
        label.set_text(str(int(label.text) + 1))


# --- Scene Setup ---
def setup_pong_scene(engine):
    scene = engine.create_scene("Pong", (0, 0))
    scene.camera_component.zoom = 1.2

    # --- Background ---
    background = GameObject("Background")
    background.add_component(Sprite("images/sky_background.png"))
    background.add_component(Background())
    scene.add_game_object(background)

    # --- Player Paddle ---
    player_paddle = GameObject("PlayerPaddle")
    player_paddle.add_component(Sprite("images/paddle.png"))
    player_paddle.add_component(PlayerPaddleScript())
    player_collider = TriggerCollider(shape="rect")
    player_paddle.add_component(player_collider)
    scene.add_game_object(player_paddle)

    # --- AI Paddle ---
    ai_paddle = GameObject("AIPaddle")
    ai_paddle.add_component(Sprite("images/paddle.png"))
    ai_script = AIPaddleScript()
    ai_paddle.add_component(ai_script)
    ai_collider = TriggerCollider(shape="rect")
    ai_paddle.add_component(ai_collider)
    scene.add_game_object(ai_paddle)

    # --- Score Labels (UI, relative, no zoom) ---
    player_score = GameObject("PlayerScore")
    player_score.add_component(UILabel(text="0", font_size=48, color=(255, 255, 255)))
    player_score.add_component(UITransform(x=0.25, y=0.05, anchor="center", relative=True))
    scene.add_game_object(player_score)

    ai_score = GameObject("AIScore")
    ai_score.add_component(UILabel(text="0", font_size=48, color=(255, 255, 255)))
    ai_score.add_component(UITransform(x=0.75, y=0.05, anchor="center", relative=True))
    scene.add_game_object(ai_score)

    # --- Ball ---
    ball = GameObject("Ball")
    ball.add_component(Sprite("images/ball.png"))
    ball_script = BallScript(player_paddle, ai_paddle, player_score, ai_score)
    ball.add_component(ball_script)
    ball_collider = TriggerCollider(shape="circle")
    ball.add_component(ball_collider)
    scene.add_game_object(ball)

    # AI references the ball
    ai_script.ball = ball


    # --- Exit Button ---
    def exit_scene(go):
        engine.set_active_scene("Menu")

    exit_btn = GameObject("ExitButton")
    exit_btn.add_component(UITransform(width=0.1, height=0.05, x=1, anchor="topright"))
    exit_btn.add_component(UIButton("Exit", on_click=exit_scene, border_radius=20))
    scene.add_game_object(exit_btn)

    return scene
