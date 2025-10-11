from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite_animation import SpriteAnimation
from assets.scripts.platformer.platformer_movement import PlatformerMovement


class PlayerState:
    IDLE = "Idle"
    RUN = "Run"
    JUMP = "Jump"
    FALL = "Fall"


class PlayerAnimationController(ScriptComponent):
    def __init__(self):
        super().__init__()
        self.sprite_animation = None
        self.platformer_movement = None
        self.state = PlayerState.IDLE

    def start(self):
        self.sprite_animation = SpriteAnimation()
        self.sprite_animation.add_animation(PlayerState.IDLE, "images/player/idle.png", 0, 0, 0.1)
        self.sprite_animation.add_animation(PlayerState.JUMP, "images/player/jump.png", 0, 0, 0.1)
        self.sprite_animation.add_animation(PlayerState.FALL, "images/player/fall.png", 0, 0, 0.1)
        self.sprite_animation.add_animation(PlayerState.RUN, "images/player/run/run.png", 0, 7, 0.1)
        self.game_object.add_component(self.sprite_animation)

        self.platformer_movement = self.game_object.get_component(PlatformerMovement)
        self.change_state(PlayerState.IDLE)

    def update(self, dt):
        x_vel, y_vel = self.platformer_movement.rigidbody.body.velocity
        grounded = self.platformer_movement.is_grounded

        # State transitions
        if not grounded:
            # Airborne states
            if y_vel < -50 and self.state != PlayerState.JUMP:
                self.change_state(PlayerState.JUMP)
            elif y_vel > 50 and self.state != PlayerState.FALL:
                self.change_state(PlayerState.FALL)
        else:
            # Grounded states
            if self.state in (PlayerState.JUMP, PlayerState.FALL):
                # Transition to appropriate grounded state after landing
                if abs(x_vel) > 0:
                    self.change_state(PlayerState.RUN)
                else:
                    self.change_state(PlayerState.IDLE)
            else:
                # Only allow Idle/Run when grounded
                if abs(x_vel) > 0 and self.state != PlayerState.RUN:
                    self.change_state(PlayerState.RUN)
                elif abs(x_vel) == 0 and self.state != PlayerState.IDLE:
                    self.change_state(PlayerState.IDLE)

    def change_state(self, new_state):
        """Handles all animation state changes safely."""
        if new_state != self.state:
            self.state = new_state
            self.sprite_animation.set_animation(new_state)
