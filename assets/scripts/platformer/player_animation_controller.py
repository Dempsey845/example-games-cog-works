from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite_animation import SpriteAnimation

from assets.scripts.platformer.platformer_movement import PlatformerMovement


class PlayerAnimationController(ScriptComponent):
    def __init__(self):
        super().__init__()
        self.sprite_animation = None
        self.platformer_movement = None
        self.animations = ["Idle", "Run", "Jump", "Fall"]
        self.current_animation = self.animations[0]

    def start(self):
        self.sprite_animation = SpriteAnimation()
        self.sprite_animation.add_animation("Idle", "images/player/idle.png", 0, 0, 0.1)
        self.sprite_animation.add_animation("Jump", "images/player/jump.png", 0, 0, 0.1)
        self.sprite_animation.add_animation("Fall", "images/player/fall.png", 0, 0, 0.1)
        self.sprite_animation.add_animation("Run", "images/player/run/run.png", 0, 7, 0.1)
        self.game_object.add_component(self.sprite_animation)

        self.platformer_movement = self.game_object.get_component(PlatformerMovement)

    def update(self, dt):
        x_vel, y_vel = self.platformer_movement.rigidbody.body.velocity

        # Prioritise vertical movement first
        if y_vel < -50:  # Jumping
            if self.current_animation != "Jump":
                self.sprite_animation.set_animation("Jump")
                self.current_animation = "Jump"
        elif y_vel > 50:  # Falling
            if self.current_animation != "Fall":
                self.sprite_animation.set_animation("Fall")
                self.current_animation = "Fall"
        else:  # On ground
            if abs(x_vel) > 0:  # Running
                if self.current_animation != "Run":
                    self.sprite_animation.set_animation("Run")
                    self.current_animation = "Run"
            else:  # Idle
                if self.current_animation != "Idle":
                    self.sprite_animation.set_animation("Idle")
                    self.current_animation = "Idle"

    def play_run_animation(self):
        self.sprite_animation.set_animation("Run")

    def play_idle_animation(self):
        self.sprite_animation.set_animation("Idle")