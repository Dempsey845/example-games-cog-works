import math
import weakref
from assets.scripts.platformer.bullet import Bullet
from cogworks import GameObject
from cogworks.components.audio_source import AudioSource
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.sprite_animation import SpriteAnimation
from cogworks.pygame_wrappers.input_manager import InputManager

from assets.scripts.platformer.muzzle_flash_particle_effect import MuzzleFlashParticleEffect
from assets.scripts.platformer.platformer_movement import PlatformerMovement


class PlayerState:
    IDLE = "Idle"
    RUN = "Run"
    JUMP = "Jump"
    FALL = "Fall"
    SHOOT = "Shoot"
    SHOOT_IN_AIR = "ShootInAir"


class PlayerAnimationController(ScriptComponent):
    def __init__(self):
        super().__init__()
        self.sprite_animation = None
        self.platformer_movement = None

        self.attack_pressed_last_frame = False

        self.state = PlayerState.IDLE
        self.input = InputManager.get_instance()

        self.camera_ref = None
        self.sprite = None

    def start(self):
        self.camera_ref = weakref.ref(self.game_object.scene.camera_component)
        self.sprite = self.game_object.get_component(Sprite)

        self.sprite_animation = SpriteAnimation()
        self.sprite_animation.add_animation(PlayerState.IDLE, "images/player/idle.png", 0, 0, 0.1, loop=False)
        self.sprite_animation.add_animation(PlayerState.JUMP, "images/player/jump.png", 0, 0, 0.1, loop=False)
        self.sprite_animation.add_animation(PlayerState.FALL, "images/player/fall.png", 0, 0, 0.1, loop=False)
        self.sprite_animation.add_animation(PlayerState.RUN, "images/player/run/run.png", 0, 7, 0.1)
        shoot_anim = self.sprite_animation.add_animation(PlayerState.SHOOT, "images/player/shoot/shoot.png", 0, 2, 0.15, loop=False)
        shoot_anim.add_event(1, self.on_attack)
        shoot_in_air_anim = self.sprite_animation.add_animation(PlayerState.SHOOT_IN_AIR, "images/player/shoot_in_air/shoot_in_air.png", 0, 2, 0.2, loop=False)
        shoot_in_air_anim.add_event(1, self.on_attack)
        self.game_object.add_component(self.sprite_animation)

        self.platformer_movement = self.game_object.get_component(PlatformerMovement)
        self.change_state(PlayerState.IDLE)

    def is_mouse_on_left(self):
        camera = self.camera_ref()
        if camera is None:
            return False

        mx, my = self.input.get_mouse_position()
        mwx, mwy = camera.screen_to_world(mx, my)

        pwx, pwy = self.game_object.transform.get_world_position()

        return mwx < pwx


    def on_attack(self):
        camera = self.camera_ref()
        if camera is None:
            return

        pwx, pwy = self.game_object.transform.get_world_position()
        mx, my = self.input.get_mouse_position()
        mouse_x, mouse_y = camera.screen_to_world(mx, my)

        # Spawn point and angle
        mouse_on_left = self.is_mouse_on_left()
        spawn_x = pwx - 200 if mouse_on_left else pwx + 200
        spawn_y = pwy - 100

        angle = 180 if mouse_on_left else 0

        # Muzzle flash
        muzzle = GameObject("MuzzleFX", x=spawn_x, y=spawn_y)
        muzzle.add_component(MuzzleFlashParticleEffect())

        # Bullet pointing toward clamped angle
        bullet = GameObject(
            "Bullet", x=spawn_x, y=spawn_y, scale_x=0.8, scale_y=0.8, rotation=angle, z_index=5
        )
        bullet.add_component(Bullet())

        self.game_object.scene.instantiate_game_object(muzzle)
        self.game_object.scene.instantiate_game_object(bullet)

        self.game_object.get_component(AudioSource).play_one_shot("sounds/shoot.mp3")

    def update(self, dt):
        x_vel, y_vel = self.platformer_movement.rigidbody.body.velocity
        grounded = self.platformer_movement.is_grounded

        # Check if left mouse button is pressed this frame
        attack_pressed = self.input.is_mouse_button_down(1)

        # --- Attack Handling ---
        if attack_pressed and not self.attack_pressed_last_frame:
            if grounded:
                if self.platformer_movement.rigidbody.body.velocity.x == 0:
                    self.change_state(PlayerState.SHOOT)
                    self.sprite.flip_x = self.is_mouse_on_left()
            else:
                self.change_state(PlayerState.SHOOT_IN_AIR)
                self.sprite.flip_x = self.is_mouse_on_left()

        self.attack_pressed_last_frame = attack_pressed
        self.platformer_movement.can_move = not self.state == PlayerState.SHOOT
        self.platformer_movement.can_flip_sprite = not self.state == PlayerState.SHOOT_IN_AIR

        # --- Prevent movement state overrides while shooting ---
        if self.state in (PlayerState.SHOOT, PlayerState.SHOOT_IN_AIR):
            if self.sprite_animation.is_playing:
                return  # wait until animation finishes
            else:
                # once done, transition back to correct state
                if grounded:
                    if abs(x_vel) > 0:
                        self.change_state(PlayerState.RUN)
                    else:
                        self.change_state(PlayerState.IDLE)
                else:
                    if y_vel < 0:
                        self.change_state(PlayerState.JUMP)
                    else:
                        self.change_state(PlayerState.FALL)
                return

        # --- Movement/State Handling ---
        if not grounded:
            # Airborne states
            if y_vel < -50 and self.state != PlayerState.JUMP:
                self.change_state(PlayerState.JUMP)
            elif y_vel > 50 and self.state != PlayerState.FALL:
                self.change_state(PlayerState.FALL)
        else:
            # Grounded states
            if self.state in (PlayerState.JUMP, PlayerState.FALL):
                if abs(x_vel) > 0:
                    self.change_state(PlayerState.RUN)
                else:
                    self.change_state(PlayerState.IDLE)
            else:
                if abs(x_vel) > 0 and self.state != PlayerState.RUN:
                    self.change_state(PlayerState.RUN)
                elif abs(x_vel) == 0 and self.state != PlayerState.IDLE:
                    self.change_state(PlayerState.IDLE)

    def change_state(self, new_state):
        """Handles all animation state changes safely."""
        if new_state != self.state:
            self.state = new_state
            self.sprite_animation.set_animation(new_state)
