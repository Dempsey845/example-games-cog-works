import pygame
from cogworks.components.rigidbody2d import Rigidbody2D
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.pygame_wrappers.input_manager import InputManager


class PlatformerMovement(ScriptComponent):
    """
    Simple 2D platformer movement using the Rigidbody2D system.
    Requires Rigidbody2D for physics and collision handling.
    """
    def __init__(self, speed=200, jump_force=500):
        super().__init__()
        self.speed = speed
        self.jump_force = jump_force
        self.input = InputManager.get_instance()
        self.rigidbody: Rigidbody2D = None
        self.sprite: Sprite = None
        self.is_grounded = False
        self.jump_pressed_last_frame = False
        self.can_move = True
        self.can_flip_sprite = True
        self.move_speed_multiplier = 1.0

    def start(self):
        self.move_speed_multiplier = 1.0
        self.rigidbody = self.game_object.get_component(Rigidbody2D)
        if not self.rigidbody:
            raise Exception("PlatformerMovement requires a Rigidbody2D")
        self.sprite = self.game_object.get_component(Sprite)
        self.rigidbody.velocity_controlled = True


    def update(self, dt):
        rb = self.rigidbody
        if not rb or not self.can_move:
            return

        jump_pressed = self.input.is_key_down(pygame.K_SPACE)
        self.is_grounded = rb.body.velocity[1] == 0
        if jump_pressed and not self.jump_pressed_last_frame and self.is_grounded:
            rb.body.apply_impulse_at_world_point(
                (0, -self.jump_force * rb.body.mass),
                rb.body.position
            )
        self.jump_pressed_last_frame = jump_pressed

    def fixed_update(self, dt):
        rb = self.rigidbody
        if not rb:
            return

        if not self.can_move:
            rb.desired_velocity = 0, rb.body.velocity.y
            return

        vx = 0
        if self.input.is_key_down(pygame.K_a) or self.input.is_key_down(pygame.K_LEFT):
            vx -= self.speed * self.move_speed_multiplier
            if self.sprite and self.can_flip_sprite:
                self.sprite.flip_x = True
        if self.input.is_key_down(pygame.K_d) or self.input.is_key_down(pygame.K_RIGHT):
            vx += self.speed * self.move_speed_multiplier
            if self.sprite and self.can_flip_sprite:
                self.sprite.flip_x = False

        rb.desired_velocity = vx, rb.body.velocity.y
