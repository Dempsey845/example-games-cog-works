import pygame
from cogworks.components.rigidbody2d import Rigidbody2D
from cogworks.components.script_component import ScriptComponent
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
        self.is_grounded = False
        self.jump_pressed_last_frame = False

    def start(self):
        self.rigidbody = self.game_object.get_component(Rigidbody2D)
        if not self.rigidbody:
            raise Exception("PlatformerMovement requires a Rigidbody2D")
        self.rigidbody.velocity_controlled = True

    def update(self, dt):
        jump_pressed = self.input.is_key_down(pygame.K_SPACE)
        if jump_pressed and not self.jump_pressed_last_frame and self.is_grounded:
            self.rigidbody.body.apply_impulse_at_world_point(
                (0, -self.jump_force * self.rigidbody.body.mass),
                self.rigidbody.body.position
            )
        self.jump_pressed_last_frame = jump_pressed

    def fixed_update(self, dt):
        # Desired horizontal velocity from input
        vx = 0
        if self.input.is_key_down(pygame.K_a) or self.input.is_key_down(pygame.K_LEFT):
            vx -= self.speed
        if self.input.is_key_down(pygame.K_d) or self.input.is_key_down(pygame.K_RIGHT):
            vx += self.speed

        self.rigidbody.desired_velocity = vx, self.rigidbody.body.velocity.y

        # Update grounded state
        self.is_grounded = self.rigidbody.check_grounded()
